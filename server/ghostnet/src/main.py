"""
GhostNet Server
FastAPI + WebSocket backend for the LoRaWAN pilot tier.
No player positioning. Only objective tracking, player status, and ref control.

Architecture:
    GhostHub (LoRa) --MQTT/HTTP--> FastAPI Server --WebSocket--> Ref Tablet
    SQLite WAL for match logging.
"""

import asyncio
import json
import sqlite3
from contextlib import asynccontextmanager
from datetime import datetime
from typing import Dict, List, Optional
from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
import uvicorn

# Database setup
DB_PATH = "ghostnet.db"

def init_db():
    conn = sqlite3.connect(DB_PATH)
    conn.execute("PRAGMA journal_mode=WAL")
    conn.executescript("""
        CREATE TABLE IF NOT EXISTS matches (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            mode TEXT NOT NULL,
            field TEXT NOT NULL,
            started_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            ended_at TIMESTAMP,
            winner_team INTEGER,
            duration_seconds INTEGER
        );
        
        CREATE TABLE IF NOT EXISTS players (
            id INTEGER PRIMARY KEY,
            match_id INTEGER,
            player_id INTEGER,
            team_id INTEGER,
            status TEXT DEFAULT 'alive',
            eliminated_at TIMESTAMP,
            respawns_used INTEGER DEFAULT 0,
            FOREIGN KEY (match_id) REFERENCES matches(id)
        );
        
        CREATE TABLE IF NOT EXISTS objectives (
            id INTEGER PRIMARY KEY,
            match_id INTEGER,
            objective_id INTEGER,
            captured_by INTEGER,
            captured_at TIMESTAMP,
            reset_by INTEGER,
            reset_at TIMESTAMP,
            FOREIGN KEY (match_id) REFERENCES matches(id)
        );
        
        CREATE TABLE IF NOT EXISTS events (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            match_id INTEGER,
            timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            event_type TEXT,
            player_id INTEGER,
            team_id INTEGER,
            objective_id INTEGER,
            details TEXT,
            FOREIGN KEY (match_id) REFERENCES matches(id)
        );
        
        CREATE TABLE IF NOT EXISTS game_state (
            match_id INTEGER PRIMARY KEY,
            mode TEXT,
            timer_seconds INTEGER DEFAULT 900,
            team_alpha_score INTEGER DEFAULT 0,
            team_bravo_score INTEGER DEFAULT 0,
            phase TEXT DEFAULT 'setup',
            FOREIGN KEY (match_id) REFERENCES matches(id)
        );
    """)
    conn.commit()
    conn.close()

# Pydantic models
class PlayerStatus(BaseModel):
    player_id: int
    team_id: int
    status: str  # alive, eliminated, wounded, ghost
    respawns_used: int = 0

class ObjectiveState(BaseModel):
    objective_id: int
    captured_by: Optional[int] = None
    captured_at: Optional[str] = None
    reset_by: Optional[int] = None

class GameState(BaseModel):
    match_id: int
    mode: str
    timer_seconds: int
    team_alpha_score: int
    team_bravo_score: int
    phase: str
    players: List[PlayerStatus]
    objectives: List[ObjectiveState]

class RefCommand(BaseModel):
    cmd: str  # eliminate, respawn, wound, reset_objective, pause, resume, end
    target_player: Optional[int] = None
    target_objective: Optional[int] = None
    team_id: Optional[int] = None

# Connection manager for WebSocket ref tablets
class ConnectionManager:
    def __init__(self):
        self.active_connections: List[WebSocket] = []
    
    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)
    
    def disconnect(self, websocket: WebSocket):
        self.active_connections.remove(websocket)
    
    async def broadcast(self, message: dict):
        for connection in self.active_connections:
            await connection.send_json(message)

manager = ConnectionManager()

# Active match state (in-memory, backed by SQLite)
active_matches: Dict[int, dict] = {}

@asynccontextmanager
async def lifespan(app: FastAPI):
    init_db()
    yield
    # Cleanup

app = FastAPI(title="GhostNet Server", lifespan=lifespan)

# Serve ref tablet UI
app.mount("/ref", StaticFiles(directory="static/ref", html=True), name="ref")

@app.get("/api/status")
async def get_status():
    return {
        "status": "online",
        "active_matches": len(active_matches),
        "connected_refs": len(manager.active_connections)
    }

@app.post("/api/match/start")
async def start_match(mode: str, field: str, player_count: int):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    cursor.execute(
        "INSERT INTO matches (mode, field) VALUES (?, ?)",
        (mode, field)
    )
    match_id = cursor.lastrowid
    
    # Initialize game state
    timer = 900 if mode in ["blackhawk_down", "dead_drop"] else 600
    cursor.execute(
        "INSERT INTO game_state (match_id, mode, timer_seconds, phase) VALUES (?, ?, ?, ?)",
        (match_id, mode, timer, "active")
    )
    
    conn.commit()
    conn.close()
    
    active_matches[match_id] = {
        "mode": mode,
        "field": field,
        "players": {},
        "objectives": {},
        "timer": timer,
        "phase": "active"
    }
    
    await manager.broadcast({
        "type": "match_started",
        "match_id": match_id,
        "mode": mode,
        "field": field
    })
    
    return {"match_id": match_id, "mode": mode}

@app.post("/api/match/{match_id}/command")
async def send_command(match_id: int, command: RefCommand):
    if match_id not in active_matches:
        return {"error": "Match not found"}
    
    match = active_matches[match_id]
    
    if command.cmd == "eliminate" and command.target_player:
        # Update player status
        if command.target_player in match["players"]:
            match["players"][command.target_player]["status"] = "eliminated"
            
            conn = sqlite3.connect(DB_PATH)
            conn.execute(
                "UPDATE players SET status = ?, eliminated_at = ? WHERE match_id = ? AND player_id = ?",
                ("eliminated", datetime.now().isoformat(), match_id, command.target_player)
            )
            conn.execute(
                "INSERT INTO events (match_id, event_type, player_id, team_id, details) VALUES (?, ?, ?, ?, ?)",
                (match_id, "force_eliminate", command.target_player, 
                 match["players"][command.target_player]["team_id"], "Ref forced elimination")
            )
            conn.commit()
            conn.close()
    
    elif command.cmd == "respawn" and command.target_player:
        if command.target_player in match["players"]:
            match["players"][command.target_player]["status"] = "alive"
            match["players"][command.target_player]["respawns_used"] += 1
    
    elif command.cmd == "wound" and command.target_player:
        if command.target_player in match["players"]:
            match["players"][command.target_player]["status"] = "wounded"
    
    elif command.cmd == "end":
        match["phase"] = "ended"
        
        conn = sqlite3.connect(DB_PATH)
        conn.execute(
            "UPDATE matches SET ended_at = ?, duration_seconds = ? WHERE id = ?",
            (datetime.now().isoformat(), 900 - match["timer"], match_id)
        )
        conn.commit()
        conn.close()
    
    await manager.broadcast({
        "type": "command_executed",
        "match_id": match_id,
        "command": command.cmd,
        "target": command.target_player
    })
    
    return {"status": "ok"}

@app.get("/api/match/{match_id}/state")
async def get_match_state(match_id: int):
    if match_id not in active_matches:
        return {"error": "Match not found"}
    
    match = active_matches[match_id]
    return {
        "match_id": match_id,
        "mode": match["mode"],
        "timer": match["timer"],
        "phase": match["phase"],
        "players": list(match["players"].values()),
        "objectives": list(match["objectives"].values())
    }

# WebSocket endpoint for ref tablets
@app.websocket("/ws/ref")
async def websocket_ref(websocket: WebSocket):
    await manager.connect(websocket)
    try:
        while True:
            data = await websocket.receive_json()
            
            if data.get("type") == "join_match":
                match_id = data.get("match_id")
                if match_id in active_matches:
                    await websocket.send_json({
                        "type": "match_state",
                        "data": active_matches[match_id]
                    })
            
            elif data.get("type") == "command":
                # Process ref command
                pass
            
    except WebSocketDisconnect:
        manager.disconnect(websocket)

# LoRa packet receiver endpoint (called by GhostHub)
@app.post("/api/lora/packet")
async def receive_lora_packet(packet: dict):
    """Receive decoded LoRa packets from GhostHub gateway."""
    player_id = packet.get("player_id")
    team_id = packet.get("team_id")
    status = packet.get("status")
    objective_id = packet.get("objective_id")
    match_id = packet.get("match_id")
    
    if match_id not in active_matches:
        return {"error": "Match not active"}
    
    match = active_matches[match_id]
    
    # Update player status
    if player_id not in match["players"]:
        match["players"][player_id] = {
            "player_id": player_id,
            "team_id": team_id,
            "status": "alive",
            "respawns_used": 0
        }
    
    match["players"][player_id]["status"] = status
    
    # Handle objective scan
    if objective_id and objective_id > 0:
        if objective_id not in match["objectives"]:
            match["objectives"][objective_id] = {
                "objective_id": objective_id,
                "captured_by": None,
                "captured_at": None
            }
        
        match["objectives"][objective_id]["captured_by"] = player_id
        match["objectives"][objective_id]["captured_at"] = datetime.now().isoformat()
        
        # Update score
        if team_id == 0:
            match["team_alpha_score"] = match.get("team_alpha_score", 0) + 1
        else:
            match["team_bravo_score"] = match.get("team_bravo_score", 0) + 1
    
    # Log event
    conn = sqlite3.connect(DB_PATH)
    conn.execute(
        "INSERT INTO events (match_id, event_type, player_id, team_id, objective_id) VALUES (?, ?, ?, ?, ?)",
        (match_id, "heartbeat" if not objective_id else "objective_scan", 
         player_id, team_id, objective_id)
    )
    conn.commit()
    conn.close()
    
    # Broadcast to refs
    await manager.broadcast({
        "type": "player_update",
        "match_id": match_id,
        "player_id": player_id,
        "status": status,
        "objective_id": objective_id
    })
    
    return {"received": True}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
