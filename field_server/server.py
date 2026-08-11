import asyncio, json, math, time, sqlite3, threading
from fastapi import FastAPI, WebSocket
from fastapi.middleware.cors import CORSMiddleware
from collections import defaultdict
import uvicorn

app = FastAPI()
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_credentials=True, allow_methods=["*"], allow_headers=["*"])

# ============ DATABASE ============
DB_PATH = "/mnt/agents/output/paintball-field/matches.db"

def init_db():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS matches (
        id INTEGER PRIMARY KEY,
        mode TEXT,
        start_time REAL,
        end_time REAL,
        winner TEXT,
        data TEXT
    )''')
    c.execute('''CREATE TABLE IF NOT EXISTS events (
        id INTEGER PRIMARY KEY,
        match_id INTEGER,
        timestamp REAL,
        type TEXT,
        player_id TEXT,
        data TEXT
    )''')
    conn.commit()
    conn.close()

init_db()

# ============ GAME STATE ============
players = {}      # band_id -> {x, y, team, health, last_seen, spectre, vip, overwatch}
nodes = {}        # node_id -> {type, state, owner, x, y, progress}
aps = {}          # ap_id -> {x, y, tx_power, path_loss}
game_mode = "spectre"
match_id = None
field_w, field_h = 50, 30
match_start = 0

# ============ WEBSOCKET ============
@app.websocket("/ws")
async def websocket_endpoint(ws: WebSocket):
    await ws.accept()
    band_id = None
    try:
        while True:
            msg = await ws.receive_json()
            band_id = msg.get("band_id", band_id)
            
            if msg["type"] == "register":
                players[band_id] = {
                    "x": msg.get("x", field_w/2),
                    "y": msg.get("y", field_h/2),
                    "team": msg["team"],
                    "health": 100,
                    "last_seen": time.time(),
                    "spectre": False,
                    "vip": False,
                    "overwatch": False,
                    "ws": ws
                }
                await ws.send_json({"type": "registered", "band_id": band_id})
                
            elif msg["type"] == "rssi_batch" and band_id:
                pos = trilaterate(msg["readings"])
                players[band_id].update({"x": pos["x"], "y": pos["y"], "last_seen": time.time()})
                visible = get_visible_players(band_id, game_mode)
                await ws.send_json({
                    "type": "state",
                    "you": {k: v for k, v in players[band_id].items() if k != "ws"},
                    "visible": visible,
                    "mode": game_mode,
                    "pulse": should_pulse(band_id)
                })
                
            elif msg["type"] == "hit" and band_id:
                target = msg["target_id"]
                if target in players:
                    players[target]["health"] -= msg.get("damage", 10)
                    log_event("hit", band_id, {"target": target, "damage": msg.get("damage", 10)})
                    if players[target]["health"] <= 0:
                        players[target]["health"] = 0
                        await broadcast({"type": "elimination", "player": target, "by": band_id})
                        log_event("elimination", band_id, {"target": target})
                        
            elif msg["type"] == "ping" and band_id:
                # Forward ping to team
                team = players[band_id]["team"]
                for pid, p in players.items():
                    if p["team"] == team and pid != band_id and "ws" in p:
                        await p["ws"].send_json({"type": "ping", "from": band_id, "x": players[band_id]["x"], "y": players[band_id]["y"]})
                        
    except Exception as e:
        print(f"WS error: {e}")
        if band_id and band_id in players:
            del players[band_id]

# ============ TRILATERATION ============
def trilaterate(readings):
    weights, wx, wy = 0, 0, 0
    for r in readings:
        if r["ap_id"] not in aps:
            continue
        ap = aps[r["ap_id"]]
        d = 10 ** ((ap["tx_power"] - r["rssi"]) / (10 * ap["path_loss"]))
        w = 1.0 / max(d, 0.1)
        weights += w
        wx += ap["x"] * w
        wy += ap["y"] * w
    if weights == 0:
        return {"x": field_w/2, "y": field_h/2}
    return {"x": wx/weights, "y": wy/weights}

# ============ VISION LOGIC ============
def get_visible_players(band_id, mode):
    me = players.get(band_id)
    if not me:
        return []
    visible = []
    
    for pid, p in players.items():
        if pid == band_id or p["health"] <= 0:
            continue
        dist = math.hypot(p["x"] - me["x"], p["y"] - me["y"])
        
        if mode == "spectre":
            if me.get("spectre", False):
                visible.append({"id": pid, "x": p["x"], "y": p["y"], "team": p["team"], "dist": dist, "type": "enemy"})
            elif p["team"] == me["team"]:
                visible.append({"id": pid, "x": p["x"], "y": p["y"], "team": p["team"], "dist": dist, "type": "team"})
                
        elif mode == "hunter":
            if p["team"] == me["team"]:
                visible.append({"id": pid, "x": p["x"], "y": p["y"], "team": p["team"], "dist": dist, "type": "team"})
            # Enemies visible during pulse (handled by should_pulse)
            
        elif mode == "ghost":
            if me["health"] <= 0:  # I'm a ghost
                visible.append({"id": pid, "x": p["x"], "y": p["y"], "team": p["team"], "dist": dist, "type": "all"})
            elif p["team"] == me["team"] or p["health"] <= 0:
                visible.append({"id": pid, "x": p["x"], "y": p["y"], "team": p["team"], "dist": dist, "type": "team"})
                
        elif mode == "infection":
            if me.get("infected", False):
                if not p.get("infected", False):
                    visible.append({"id": pid, "x": p["x"], "y": p["y"], "team": "survivor", "dist": dist, "type": "survivor"})
            else:
                if p.get("infected", False):
                    visible.append({"id": pid, "x": p["x"], "y": p["y"], "team": "infected", "dist": dist, "type": "infected"})
                    
        elif mode == "vip_escort":
            if p["team"] == me["team"] or p.get("vip", False):
                visible.append({"id": pid, "x": p["x"], "y": p["y"], "team": p["team"], "dist": dist, "type": "vip" if p.get("vip") else "team"})
            elif p.get("vip", False) and vip_visible_to_enemy():
                visible.append({"id": pid, "x": p["x"], "y": p["y"], "team": p["team"], "dist": dist, "type": "vip"})
                
        elif mode == "battle_royale":
            # All visible inside zone
            visible.append({"id": pid, "x": p["x"], "y": p["y"], "team": p["team"], "dist": dist, "type": "all"})
            
        elif mode == "overwatch":
            # Overwatch sees all; others see standard
            if me.get("overwatch", False):
                visible.append({"id": pid, "x": p["x"], "y": p["y"], "team": p["team"], "dist": dist, "type": "all"})
            elif p["team"] == me["team"]:
                visible.append({"id": pid, "x": p["x"], "y": p["y"], "team": p["team"], "dist": dist, "type": "team"})
    
    return visible

def should_pulse(band_id):
    # Hunter-Prey: pulse every 60s for 3s
    if game_mode == "hunter":
        elapsed = time.time() - match_start
        return (int(elapsed) % 60) < 3
    return False

def vip_visible_to_enemy():
    # VIP visible to enemy every 30s for 5s
    elapsed = time.time() - match_start
    return (int(elapsed) % 30) < 5

# ============ BROADCAST ============
async def broadcast(msg):
    for pid, p in players.items():
        if "ws" in p:
            try:
                await p["ws"].send_json(msg)
            except:
                pass

# ============ LOGGING ============
def log_event(event_type, player_id, data):
    if match_id is None:
        return
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("INSERT INTO events (match_id, timestamp, type, player_id, data) VALUES (?, ?, ?, ?, ?)",
              (match_id, time.time(), event_type, player_id, json.dumps(data)))
    conn.commit()
    conn.close()

# ============ API ============
@app.get("/api/state")
def get_state():
    return {
        "mode": game_mode,
        "players": {k: {kk: vv for kk, vv in v.items() if kk != "ws"} for k, v in players.items()},
        "nodes": nodes,
        "match_time": time.time() - match_start if match_start else 0
    }

@app.post("/api/mode/{mode}")
def set_mode(mode: str):
    global game_mode, match_id, match_start
    game_mode = mode
    match_start = time.time()
    
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("INSERT INTO matches (mode, start_time, data) VALUES (?, ?, ?)",
              (mode, match_start, json.dumps({"field_w": field_w, "field_h": field_h})))
    match_id = c.lastrowid
    conn.commit()
    conn.close()
    
    # Assign special roles
    if mode == "spectre":
        assign_spectres()
    elif mode == "vip_escort":
        assign_vips()
    elif mode == "overwatch":
        assign_overwatch()
    elif mode == "infection":
        assign_infected()
        
    return {"mode": mode, "match_id": match_id}

def assign_spectres():
    teams = defaultdict(list)
    for pid, p in players.items():
        teams[p["team"]].append(pid)
    for team, members in teams.items():
        if members:
            import random
            spectre = random.choice(members)
            players[spectre]["spectre"] = True

def assign_vips():
    teams = defaultdict(list)
    for pid, p in players.items():
        teams[p["team"]].append(pid)
    for team, members in teams.items():
        if members:
            import random
            vip = random.choice(members)
            players[vip]["vip"] = True

def assign_overwatch():
    teams = defaultdict(list)
    for pid, p in players.items():
        teams[p["team"]].append(pid)
    for team, members in teams.items():
        if members:
            import random
            ow = random.choice(members)
            players[ow]["overwatch"] = True

def assign_infected():
    import random
    all_players = list(players.keys())
    if all_players:
        infected = random.choice(all_players)
        players[infected]["infected"] = True

# ============ MAIN ============
if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8765)
