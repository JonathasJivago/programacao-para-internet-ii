from http import HTTPStatus

from fastapi.testclient import TestClient

from app.main import app

def test_home():
    client = TestClient(app) # A - Arrange
    response = client.get('/') # A - Act
    assert response.status_code == HTTPStatus.OK # A - Assert
    assert response.json() == {'mensagem': 'Hello, World!!!!'}

def test_criar_um_usuario():
    client = TestClient(app)
    response = client.post('/usuarios', 
        json={
        "nome": "Ana Souza",
        "email": "anaser@example.com",
        "senha": "12345",
        "avaliacao": ["Muito Bom", 5 ],
        "notas": [  {
          "nota1": 5,
          "nota2": 10,
          "nota3": 8
       }]}
        )
    assert response.status_code == HTTPStatus.CREATED
    assert response.json() == {
        "id": 1,
        "nome": "Ana Souza",
        "email": "anaser@example.com",
        }

def test_buscar_usuario():
    client = TestClient(app)
    response = client.get('/usuarios/1')
    assert response.status_code == HTTPStatus.OK
    assert response.json() == {
        "id": 1,
        "nome": "Ana Souza",
        "email": "anaser@example.com",
        }

def test_buscar_usuario_invalido():
    client = TestClient(app)
    response = client.get('/usuarios/999')

    assert response.status_code == HTTPStatus.NOT_FOUND

    

