from pwdlib import PasswordHash

pwd_context = PasswordHash.recommended()

def get_password_hash(senha: str):
    return pwd_context.hash(senha)

def verify_password(senha_texto: str, senha_hash: str):
    return pwd_context.verify(senha_texto, senha_hash)

