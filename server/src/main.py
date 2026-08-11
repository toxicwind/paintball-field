import asyncio, json, math, time, sqlite3, threading, random
from fastapi import FastAPI, WebSocket
from fastapi.middleware.cors import CORSMiddleware
from collections import defaultdict, deque
import numpy as np
from scipy.optimize import minimize
import uvicorn

app = FastAPI()
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_credentials=True, allow_methods=["*"], allow_headers=["*"])

DB_PATH = "server/matches.db"
CALIBRATION_PATH = "server/configs/blitz_outdoor_50x30.json"

# ============ KALMAN FILTER ============
class KalmanFilter:
    def __init__(self, dt=0.2):
        self.dt = dt
        self.x = np.array([25.0, 15.0, 0.0, 0.0])
        self.P = np.eye(4) * 10.0
        self.Q = np.eye(4)
        self.Q[0,0] = self.Q[1,1] = 0.1
        self.Q[2,2] = self.Q[3,3] = 1.0
        self.R = np.eye(2) * 4.0

    def predict(self, ax=0, ay=0):
        F = np.array([[1,0,self.dt,0],[0,1,0,self.dt],[0,0,1,0],[0,0,0,1]])
        B = np.array([[0.5*self.dt**2,0],[0,0.5*self.dt**2],[self.dt,0],[0,self.dt]])
        u = np.array([ax, ay])
        self.x = F @ self.x + B @ u
        self.P = F @ self.P @ F.T + self.Q

    def update(self, z):
        H = np.array([[1,0,0,0],[0,1,0,0]])
        y = z - H @ self.x
        S = H @ self.P @ H.T + self.R
        K = self.P @ H.T @ np.linalg.inv(S)
        self.x = self.x + K @ y
        self.P = (np.eye(4) - K @ H) @ self.P
        return self.x[:2]

# ============ PARTICLE FILTER ============
class ParticleFilter:
    def __init__(self, n_particles=500, field_w=50, field_h=30):
        self.n = n_particles
        self.particles = np.random.rand(n_particles, 2)
        self.particles[:,0] *= field_w
        self.particles[:,1] *= field_h
        self.weights = np.ones(n_particles) / n_particles
        self.field_w = field_w
        self.field_h = field_h

    def predict(self, noise=1.0):
        self.particles += np.random.randn(self.n, 2) * noise
        self.particles[:,0] = np.clip(self.particles[:,0], 0, self.field_w)
        self.particles[:,1] = np.clip(self.particles[:,1], 0, self.field_h)

    def update(self, readings, aps):
        for r in readings:
            if r["ap_id"] not in aps:
                continue
            ap = aps[r["ap_id"]]
            d_est = 10 ** ((ap["tx_power"] - r["rssi"]) / (10 * ap["path_loss"]))
            dx = self.particles[:,0] - ap["x"]
            dy = self.particles[:,1] - ap["y"]
            d_actual = np.sqrt(dx**2 + dy**2)
            self.weights *= np.exp(-0.5 * ((d_actual - d_est) / 2.0) ** 2)
        self.weights += 1e-300
        self.weights /= np.sum(self.weights)

    def resample(self):
        indices = np.random.choice(self.n, self.n, p=self.weights)
        self.particles = self.particles[indices]
        self.weights = np.ones(self.n) / self.n

    def estimate(self):
        return np.average(self.particles, weights=self.weights, axis=0)

# ============ DATABASE ============
def init_db():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("""CREATE TABLE IF NOT EXISTS matches (
        id INTEGER PRIMARY KEY, mode TEXT, start_time REAL, end_time REAL,
        winner TEXT, field TEXT, data TEXT)""")
    c.execute("""CREATE TABLE IF NOT EXISTS events (
        id INTEGER PRIMARY KEY, match_id INTEGER, timestamp REAL,
        type TEXT, player_id TEXT, data TEXT)""")
    c.execute("""CREATE TABLE IF NOT EXISTS rssi_log (
        id INTEGER PRIMARY KEY, match_id INTEGER, timestamp REAL,
        band_id TEXT, ap_id TEXT, rssi INTEGER, raw_rssi INTEGER)""")
    conn.commit()
    conn.close()

init_db()

# ============ GAME STATE ============
players = {}
nodes = {}
aps = {}
game_mode = "hunter_prey"
match_id = None
field_w, field_h = 50, 30
match_start = 0
kalman_filters = {}
particle_filters = {}

# ============ LOAD FIELD CONFIG ============
def load_field_config(path):
    global aps, field_w, field_h
    try:
        with open(path) as f:
            cfg = json.load(f)
        aps = {ap["id"]: ap for ap in cfg.get("aps", [])}
        field_w = cfg.get("field", {}).get("width", 50)
        field_h = cfg.get("field", {}).get("height", 30)
        print(f"Loaded field: {cfg.get('field_name', 'unknown')} {field_w}x{field_h}")
    except Exception as e:
        print(f"Failed to load field config: {e}")
        aps = {
            "AP-01": {"x":0,"y":0,"tx_power":-30,"path_loss":2.5},
            "AP-02": {"x":25,"y":0,"tx_power":-30,"path_loss":2.5},
            "AP-03": {"x":50,"y":0,"tx_power":-30,"path_loss":2.5},
            "AP-04": {"x":0,"y":15,"tx_power":-30,"path_loss":2.5},
            "AP-05": {"x":50,"y":15,"tx_power":-30,"path_loss":2.5},
            "AP-06": {"x":25,"y":30,"tx_power":-30,"path_loss":2.5},
        }

load_field_config(CALIBRATION_PATH)

# ============ TRILATERATION WITH FUSION ============
def trilaterate(readings, band_id):
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

    wls_pos = np.array([wx/weights, wy/weights]) if weights > 0 else np.array([field_w/2, field_h/2])

    if band_id not in particle_filters:
        particle_filters[band_id] = ParticleFilter(field_w=field_w, field_h=field_h)
    pf = particle_filters[band_id]
    pf.predict(noise=0.5)
    pf.update(readings, aps)
    pf.resample()
    pf_pos = pf.estimate()

    if band_id not in kalman_filters:
        kalman_filters[band_id] = KalmanFilter()
    kf = kalman_filters[band_id]

    fused_z = 0.6 * wls_pos + 0.4 * pf_pos
    kf.predict()
    kf_pos = kf.update(fused_z)

    return {"x": float(kf_pos[0]), "y": float(kf_pos[1]), "confidence": float(1.0/(1.0+np.linalg.norm(wls_pos-pf_pos)))}

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
                    "x": msg.get("x", field_w/2), "y": msg.get("y", field_h/2),
                    "team": msg["team"], "health": 100, "last_seen": time.time(),
                    "spectre": False, "vip": False, "overwatch": False,
                    "infected": False, "ws": ws
                }
                await ws.send_json({"type": "registered", "band_id": band_id})

            elif msg["type"] == "rssi_batch" and band_id:
                pos = trilaterate(msg["readings"], band_id)

                if match_id:
                    conn = sqlite3.connect(DB_PATH)
                    c = conn.cursor()
                    for r in msg["readings"]:
                        c.execute("INSERT INTO rssi_log (match_id, timestamp, band_id, ap_id, rssi, raw_rssi) VALUES (?,?,?,?,?,?)",
                                  (match_id, time.time(), band_id, r["ap_id"], r.get("median_rssi", r["rssi"]), r["rssi"]))
                    conn.commit()
                    conn.close()

                players[band_id].update({"x": pos["x"], "y": pos["y"], "last_seen": time.time()})
                visible = get_visible_players(band_id, game_mode)
                await ws.send_json({
                    "type": "state",
                    "you": {k: v for k, v in players[band_id].items() if k != "ws"},
                    "visible": visible, "mode": game_mode,
                    "pulse": should_pulse(band_id)
                })

            elif msg["type"] == "shock_hit" and band_id:
                log_event("shock_hit", band_id, {"shock": msg.get("shock", 0)})
                await broadcast({"type": "hit_confirmed", "target": band_id, "direction": "unknown"})

            elif msg["type"] == "mark_hit" and band_id:
                players[band_id]["health"] = 0
                log_event("mark_hit", band_id, {})
                await broadcast({"type": "eliminated", "player": band_id})

    except Exception as e:
        print(f"WS error: {e}")
        if band_id and band_id in players:
            del players[band_id]

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

        elif mode == "hunter_prey":
            if p["team"] == me["team"]:
                visible.append({"id": pid, "x": p["x"], "y": p["y"], "team": p["team"], "dist": dist, "type": "team"})

        elif mode == "ghost":
            if me["health"] <= 0:
                visible.append({"id": pid, "x": p["x"], "y": p["y"], "team": p["team"], "dist": dist, "type": "all"})
            elif p["team"] == me["team"] or p["health"] <= 0:
                visible.append({"id": pid, "x": p["x"], "y": p["y"], "team": p["team"], "dist": dist, "type": "team"})

        elif mode in ["capture_flag", "domination", "frontline"]:
            if p["team"] == me["team"]:
                visible.append({"id": pid, "x": p["x"], "y": p["y"], "team": p["team"], "dist": dist, "type": "team"})
            else:
                visible.append({"id": pid, "x": p["x"], "y": p["y"], "team": p["team"], "dist": dist, "type": "enemy"})

    return visible

def should_pulse(band_id):
    if game_mode == "hunter_prey":
        elapsed = time.time() - match_start
        return (int(elapsed) % 60) < 3
    return False

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

    if mode == "spectre":
        assign_spectres()
    elif mode == "frontline":
        assign_reinforcements()

    return {"mode": mode, "match_id": match_id}

@app.post("/api/force_eliminate/{band_id}")
def force_eliminate(band_id: str):
    if band_id in players:
        players[band_id]["health"] = 0
        log_event("force_eliminate", band_id, {})
        return {"status": "eliminated", "band_id": band_id}
    return {"status": "not_found"}

@app.post("/api/force_revive/{band_id}")
def force_revive(band_id: str):
    if band_id in players:
        players[band_id]["health"] = 100
        log_event("force_revive", band_id, {})
        return {"status": "revived", "band_id": band_id}
    return {"status": "not_found"}

def assign_spectres():
    teams = defaultdict(list)
    for pid, p in players.items():
        teams[p["team"]].append(pid)
    for team, members in teams.items():
        if members:
            spectre = random.choice(members)
            players[spectre]["spectre"] = True

def assign_reinforcements():
    for pid, p in players.items():
        p["reinforcements"] = 50

# ============ SIMULATION MODE ============
@app.post("/api/simulate/start")
def start_simulation(n_players: int = 16, field: str = "blitz_outdoor_50x30"):
    global game_mode, match_id, match_start
    load_field_config(f"server/configs/{field}.json")

    for i in range(n_players):
        band_id = f"SIM-{i:03d}"
        team = "red" if i < n_players // 2 else "blue"
        players[band_id] = {
            "x": random.uniform(5, field_w-5),
            "y": random.uniform(5, field_h-5),
            "team": team, "health": 100, "last_seen": time.time(),
            "spectre": False, "vip": False, "overwatch": False,
            "infected": False, "ws": None
        }

    game_mode = "hunter_prey"
    match_start = time.time()

    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("INSERT INTO matches (mode, start_time, data) VALUES (?, ?, ?)",
              (game_mode, match_start, json.dumps({"simulated": True, "n_players": n_players, "field": field})))
    match_id = c.lastrowid
    conn.commit()
    conn.close()

    return {"status": "simulation_started", "players": n_players, "field": field, "match_id": match_id}

@app.get("/api/simulate/state")
def get_sim_state():
    return {
        "mode": game_mode,
        "players": {k: {kk: vv for kk, vv in v.items() if kk != "ws"} for k, v in players.items()},
        "match_time": time.time() - match_start if match_start else 0
    }

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8765)
