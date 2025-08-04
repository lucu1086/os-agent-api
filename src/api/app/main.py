from fastapi import FastAPI, Request, Query, Depends
from fastapi.responses import JSONResponse
from .schemas import AgentData
from .database import SessionLocal
from .crud import create_agent_data, get_agent_data
from sqlalchemy.orm import Session
from .models import AgentDataDB  # Import the AgentDataDB model

app = FastAPI()

# Dependencia para obtener la sesión de la base de datos
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.post("/api/agent_data")
async def receive_data(agent_data: AgentData, request: Request, db=Depends(get_db)):
    client_ip = request.client.host
    db_agent = create_agent_data(db, agent_data, client_ip)
    return JSONResponse(content={"message": "Data received", "client_ip": client_ip, "id": db_agent.id}, status_code=201)

@app.get("/api/agent_data")
def read_agent_data(client_ip: str = Query(None, description="Filter by client IP"), db=Depends(get_db)):
    results = get_agent_data(db, client_ip)
    # Serializar los resultados a dict para la respuesta
    data = []
    for agent in results:
        item = {
            "id": agent.id,
            "client_ip": agent.client_ip,
            "cpu_info": agent.cpu_info,
            "os_info": agent.os_info,
            "processes": [
                {"pid": p.pid, "name": p.name, "username": p.username}
                for p in agent.processes
            ],
            "users": [
                {"name": u.name, "terminal": u.terminal, "host": u.host, "started": u.started}
                for u in agent.users
            ]
        }
        data.append(item)
    return JSONResponse(content=data, status_code=200)

def get_agent_data(db: Session, client_ip: str = None):
    query = db.query(AgentDataDB)
    if client_ip:
        query = query.filter(AgentDataDB.client_ip == client_ip)