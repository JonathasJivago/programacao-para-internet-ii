from http import HTTPStatus
from typing import Annotated

from fastapi import FastAPI, HTTPException, Query, Depends

from schemas import Mensagem, UsuarioBD, UsuarioPublic, UsuarioSchema

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models import Usuario

from database import get_session

app = FastAPI()

banco = [
    # UsuarioBD('id': 1, 'nome': 'Alice', 'email': 'alice@example.com'),
    # {'id': 2, 'nome': 'Bob', 'email': 'bob@example.com'},
    # {'id': 3, 'nome': 'Charlie', 'email': 'charlie@example.com'},
]


@app.get('/', response_model=Mensagem)
def home():
    return {'mensagem': 'Hello, World!!!!'}


@app.get('/usuarios', response_model=list[UsuarioPublic])
def listar_usuarios(session=Depends(get_session)):
    usuarios = session.scalars(select(Usuario)).all()
    return usuarios


@app.get(
    '/teste/',
    summary='Endpoint de teste',
    description='Endpoint para testar a rota com parâmetro',
)
def teste(
    numero: Annotated[
        int,
        Query(title='Número', description='Um número inteiro', ge=1, le=10),
    ],
):
    return {'msg': str(type(numero))}


@app.get('/usuarios/{id}', status_code=HTTPStatus.OK, response_model=UsuarioPublic)
def buscar_usuario_pelo_id(id: int, session=Depends(get_session)):
    usuario = session.scalar(select(Usuario).where(Usuario.id == id))
    if usuario:
        return usuario

    raise HTTPException(
        status_code=HTTPStatus.NOT_FOUND, detail='Usuário não encontrado'
    )


@app.put('/usuarios/{id}', response_model=UsuarioPublic)
def atualizar_usuario(id: int, usuario: UsuarioSchema, session: Session = Depends(get_session)):
    usuario_bd = session.scalar(select(Usuario).where(Usuario.id == id))
    if usuario_bd:
        if session.scalar(select(Usuario).where(Usuario.email == usuario.email)):
            raise HTTPException(
                    status_code=HTTPStatus.CONFLICT, detail='Email já cadastrado!'
                )
        else:
            usuario_bd.nome = usuario.nome
            usuario_bd.email = usuario.email
            usuario_bd.senha = usuario.senha

            session.add(usuario_bd)
            session.commit()
            session.refresh(usuario_bd)
            return usuario_bd
    else:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND, detail='Usuário não encontrado'
        )


@app.post('/usuarios', status_code=HTTPStatus.CREATED, response_model=UsuarioPublic)
def criar_usuario(usuario: UsuarioSchema, session=Depends(get_session)):

    usuario_bd = session.scalar(select(Usuario).where(Usuario.email == usuario.email))

    if usuario_bd:
        raise HTTPException(status_code=HTTPStatus.CONFLICT, detail="Email já existe!!!")
    else:
        usuario_bd = Usuario(
            nome=usuario.nome,
            email=usuario.email,
            senha=usuario.senha
        )

        session.add(usuario_bd)
        session.commit()
        session.refresh(usuario_bd)

        return usuario_bd

    # usuario_com_id = UsuarioBD(id=len(banco) + 1, **usuario.model_dump())
    # banco.append(usuario_com_id)

    # return usuario_com_id


@app.delete('/usuarios/{id}', response_model=Mensagem)
def deletar_usuario(id: int, session: Session = Depends(get_session)):
    usuario_bd = session.get(Usuario, id)

    if not usuario_bd:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND, detail='Usuário não encontrado!'
        )
    else:
        session.delete(usuario_bd)
        session.commit()
        
        return Mensagem(mensagem="Usuário Excluido!")

