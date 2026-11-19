from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from app.main import app
from sqlalchemy import create_engine
from app.models import table_registry
from database import get_session
from security import get_password_hash
import pytest
from sqlalchemy.pool import StaticPool
from app.models import Usuario

@pytest.fixture
def client(session):
    def get_session_override():
        return session

    with TestClient(app) as client:
        app.dependency_overrides[get_session] = get_session_override
        yield client

    app.dependency_overrides.clear()

@pytest.fixture
def session():
    engine = create_engine('sqlite:///:memory:', 
                           connect_args={"check_same_thread": False},
                           poolclass=StaticPool)
    
    table_registry.metadata.create_all(engine)

    with Session(engine) as session:
        yield session

    table_registry.metadata.drop_all(engine)
    session.close()
    engine.dispose()

@pytest.fixture
def usuario(session):
    senha_em_texto = "12345"
    usuario = Usuario(
        nome="Bob", 
        email="bob@example.com", 
        senha=get_password_hash(senha_em_texto)
    )
    session.add(usuario)
    session.commit()
    session.refresh(usuario)
    usuario.senha_em_texto = senha_em_texto
    return usuario

@pytest.fixture
def lista(session):
    lista = []
    usuario = Usuario(nome="Bob", email="bob@example.com", senha="12345")
    session.add(usuario)
    session.commit()
    session.refresh(usuario)
    lista.append(usuario)
    
    usuario = Usuario(nome="Carol", email="carol@example.com", senha="12345")
    session.add(usuario)
    session.commit()
    session.refresh(usuario)
    lista.append(usuario)

    return lista

@pytest.fixture
def token(client, usuario):
    response = client.post(
        '/token',
        data={
            'username': usuario.email,
            'password': usuario.senha_em_texto
        },
    )

    return response.json()['access_token']