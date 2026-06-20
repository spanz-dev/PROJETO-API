from fastapi import FastAPI, HTTPException
from config.database import SessionLocal
from models.item_model import Usuarios
from services.auth import gerar_hash
from services.auth import verificar_senha
from schemas.user_schema import UsuarioRegistro, UsuarioLogin

app = FastAPI()

@app.post("/registro")
def registrar(usuario: UsuarioRegistro):

    db = SessionLocal()

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
def login(usuario: UsuarioLogin):

    db = SessionLocal()

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