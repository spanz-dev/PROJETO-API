from sqlalchemy import Column , Integer , String , Float
from app.config.database import Base

class Usuarios(Base):
    __tablename__ = "contas"

    id = Column(Integer , primary_key=True , index=True)
    nome = Column(String , index=True , nullable=False)
    email = Column(String , nullable=False)
    senha = Column(String , nullable=True)
