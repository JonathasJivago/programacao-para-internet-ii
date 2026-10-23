from sqlalchemy import select

from app.models import Usuario

def test_criar_usuario(session):
    usuario = Usuario(nome="Bob", email="bob@email.com", senha="12345")
    session.add(usuario)

    usuario2 = Usuario(nome="Clarice", email="clarice@email.com", senha="54321")
    session.add(usuario2)
    session.commit()

    usuarioBD = session.scalar(select(Usuario).where(Usuario.nome == "Clarice"))

   # breakpoint()

    assert usuarioBD.id == 1