from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from app.main import app
from sqlalchemy import create_engine
from app.models import table_registry
from database import get_session
import pytest
from sqlalchemy.pool import StaticPool

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
                           poolClass=StaticPool)
    
    table_registry.metadata.create_all(engine)

    with Session(engine) as session:
        yield session

    table_registry.metadata.drop_all(engine)
    session.close()
    engine.dispose()

