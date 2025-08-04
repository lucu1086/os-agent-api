from sqlalchemy.orm import Session
from .models import AgentDataDB, ProcessInfoDB, UserSessionDB
from .schemas import AgentData

def create_agent_data(db: Session, agent_data: AgentData, client_ip: str):
    db_agent = AgentDataDB(
        client_ip=client_ip,
        cpu_info=agent_data.cpu_info.dict(),
        os_info=agent_data.os_info.dict()
    )
    db.add(db_agent)
    db.commit()
    db.refresh(db_agent)

    # Procesos
    for proc in agent_data.processes:
        db_proc = ProcessInfoDB(
            pid=proc.pid,
            name=proc.name,
            username=proc.username,
            agent_data_id=db_agent.id
        )
        db.add(db_proc)

    # Usuarios
    for user in agent_data.users:
        db_user = UserSessionDB(
            name=user.name,
            terminal=user.terminal,
            host=user.host,
            started=user.started,
            agent_data_id=db_agent.id
        )
        db.add(db_user)

    db.commit()
    return db_agent

def get_agent_data(db: Session, client_ip: str = None):
    query = db.query(AgentDataDB)
    if client_ip:
        query = query.filter(AgentDataDB.client_ip == client_ip)
    return query.all()