from http import HTTPStatus

def test_home(client):
    # A - Arrange
    response = client.get('/') # A - Act
    assert response.status_code == HTTPStatus.OK # A - Assert
    assert response.json() == {'mensagem': 'Hello, World!!!!'}

def test_criar_um_usuario(client, ):
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

def test_buscar_usuario(client, usuario):
    response = client.get(f'/usuarios/{usuario.id}')

    assert response.status_code == HTTPStatus.OK
    
    data = response.json()
    
    assert 'id' in data
    assert data['id'] == 1

    assert 'senha' not in data

    assert response.json() == {
        "id": 1,
        "nome": "Bob",
        "email": "bob@example.com",
        }

def test_buscar_usuario_invalido(client, usuario):
    response = client.get('/usuarios/999')

    assert response.status_code == HTTPStatus.NOT_FOUND

    data = response.json()

    assert data['detail'] == 'Usuário não encontrado'

def test_listar_usuarios(client, usuario):
    response = client.get('/usuarios')

    assert response.status_code == HTTPStatus.OK

    data = response.json()

    assert isinstance(data, list)

    assert len(data) == 1
    assert data[0]['id'] == 1
    assert data[0]['nome'] == 'Bob'
    assert data[0]['email'] == 'bob@example.com'
