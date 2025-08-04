from sqlalchemy import Column, Integer, String, Float, ForeignKey, JSON
from sqlalchemy.orm import relationship, declarative_base

Base = declarative_base()

class AgentDataDB(Base):
    __tablename__ = "agent_data"
    id = Column(Integer, primary_key=True, autoincrement=True)
    client_ip = Column(String, nullable=False)
    cpu_info = Column(JSON, nullable=False)
    os_info = Column(JSON, nullable=False)

    processes = relationship("ProcessInfoDB", back_populates="agent_data", cascade="all, delete-orphan")
    users = relationship("UserSessionDB", back_populates="agent_data", cascade="all, delete-orphan")

class ProcessInfoDB(Base):
    __tablename__ = "process_info"
    id = Column(Integer, primary_key=True, autoincrement=True)
    pid = Column(Integer, nullable=False)
    name = Column(String, nullable=False)
    username = Column(String)
    agent_data_id = Column(Integer, ForeignKey("agent_data.id"))
    agent_data = relationship("AgentDataDB", back_populates="processes")

class UserSessionDB(Base):
    __tablename__ = "user_session"
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, nullable=False)
    terminal = Column(String)
    host = Column(String)
    started = Column(Float)
    agent_data_id = Column(Integer, ForeignKey("agent_data.id"))
    agent_data = relationship("AgentDataDB", back_populates="users")