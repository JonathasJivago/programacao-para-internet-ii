from pwdlib import PasswordHash

pwd_context = PasswordHash.recommended()

def get_password_hash(senha: str):
    return pwd_context.hash(senha)

def verify_password(senha_texto: str, senha_hash: str):
    return pwd_context.verify(senha_texto, senha_hash)


from datetime import datetime, timedelta
from zoneinfo import ZoneInfo
from jwt import encode

TIME_IN_MINUTES=30
SECRET_KEY='senha-muito-segura'
ALGORITHM='HS256'

def create_access_token(data: dict):
    payload = data.copy()
    expire = datetime.now(tz=ZoneInfo('UTC'))+timedelta(minutes=TIME_IN_MINUTES)

    payload.update({'exp': expire})

    encode_jwt = encode(payload, SECRET_KEY, algorithm=ALGORITHM)
    return encode_jwt
