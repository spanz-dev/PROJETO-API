from fastapi import FastAPI, HTTPException, Depends
from sqlalchemy.orm import Session
from app.config.database import engine, SessionLocal 
from app.models.item_model import Usuarios, Base  # <-- IMPORTANTE: Importe o Base diretamente daqui!
from app.services.auth import gerar_hash, verificar_senha
from app.schemas.user_schema import UsuarioRegistro, UsuarioLogin

# Garante que o SQLAlchemy conhece os modelos atrelados a este Base específico antes de criar
Base.metadata.create_all(bind=engine)

app = FastAPI()

# 2. FUNÇÃO AUXILIAR PARA GERENCIAR A SESSÃO DO BANCO (Fecha a conexão automaticamente)
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.post("/registro")
def registrar(usuario: UsuarioRegistro, db: Session = Depends(get_db)): # Usando o Depends aqui

    existe = db.query(Usuarios)\
        .filter(Usuarios.email == usuario.email)\
        .first()

    if existe:
        raise HTTPException(
            status_code=400,
            detail="Email já cadastrado"
        )

    novo_usuario = Usuarios(
        nome=usuario.nome,
        email=usuario.email,
        senha=gerar_hash(usuario.senha)
    )

    db.add(novo_usuario)
    db.commit()

    return {"mensagem": "Usuário criado"}

@app.post("/login")
def login(usuario: UsuarioLogin, db: Session = Depends(get_db)): # Usando o Depends aqui

    usuario_db = db.query(Usuarios)\
        .filter(Usuarios.email == usuario.email)\
        .first()

    if not usuario_db:
        raise HTTPException(
            status_code=401,
            detail="Credenciais inválidas"
        )

    if not verificar_senha(
        usuario.senha,
        usuario_db.senha
    ):
        raise HTTPException(
            status_code=401,
            detail="Credenciais inválidas"
        )

    return {
        "mensagem": "Login realizado",
        "usuario": usuario_db.nome
    }
