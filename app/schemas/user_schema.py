from pydantic import BaseModel, EmailStr

class UsuarioRegistro(BaseModel):
    nome: str
    email: EmailStr
    senha: str

class UsuarioLogin(BaseModel):
    email: EmailStr
    senha: str