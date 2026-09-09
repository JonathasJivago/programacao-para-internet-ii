from pydantic import BaseModel, EmailStr, ValidationError, Field
from typing import Annotated

class Mensagem(BaseModel):
    mensagem: str

class UsuarioSchema(BaseModel):
    nome: Annotated[str, Field(min_length=3,title="Nome completo",description=("Como aparece no diploma"),examples=["Ana Souza"])]
    email: EmailStr
    senha: str
    avaliacao: tuple[str, int]
    notas: list[dict[str, float]]

class UsuarioBD(UsuarioSchema):
    id: int

class UsuarioPublic(BaseModel):
    id: int
    nome: str
    email: EmailStr

usuario = {
    "nome": "Bob",
    "email": "bob@example.com",
    "senha": "1236",
    "avaliacao": ("Bom", "texto"),
    "notas": [
        {"nota1": 8.5}, 
        {"nota2": 9.0}
    ]   
}

try:
    u = UsuarioSchema(**usuario)
    print("Usuário válido")
except ValidationError as e: 
    print(e.errors())