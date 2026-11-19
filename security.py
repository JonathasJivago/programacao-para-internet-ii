from pwdlib import PasswordHash
from fastapi.security import OAuth2PasswordBearer
from fastapi import Depends
from database import get_session
from sqlalchemy.orm import Session

oauth2_schema = OAuth2PasswordBearer(tokenUrl="token")

from http import HTTPStatus
from fastapi import HTTPException
from jwt import decode, DecodeError
from app.models import Usuario
from sqlalchemy import select

from datetime import datetime, timedelta
from zoneinfo import ZoneInfo
from jwt import encode

pwd_context = PasswordHash.recommended()

def get_password_hash(senha: str):
    return pwd_context.hash(senha)

def verify_password(senha_texto: str, senha_hash: str):
    return pwd_context.verify(senha_texto, senha_hash)

TIME_IN_MINUTES=30
SECRET_KEY='senha-muito-segura'
ALGORITHM='HS256'

def create_access_token(data: dict):
    payload = data.copy()
    expire = datetime.now(tz=ZoneInfo('UTC'))+timedelta(minutes=TIME_IN_MINUTES)

    payload.update({'exp': expire})

    encode_jwt = encode(payload, SECRET_KEY, algorithm=ALGORITHM)
    return encode_jwt

def get_current_user(
        session: Session = Depends(get_session),
        token: str = Depends(oauth2_schema)
    ):

    credentials_exception = HTTPException(
        status_code = HTTPStatus.UNAUTHORIZED,
        detail="Não pode validar as credenciais!",
        headers={'WWW-Authenticate': 'Bearer'}
    )

    try:
        payload = decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email = payload.get('sub')

        if not email:
            raise credentials_exception

    except DecodeError:
        raise credentials_exception

    usuario_bd = session.scalar(select(Usuario).where(Usuario.email==email))

    if not usuario_bd:
        raise credentials_exception

    return usuario_bd

