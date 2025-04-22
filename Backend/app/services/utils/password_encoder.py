import bcrypt 

def hash_password(password: str) -> str:
    """Hash de contraseña usando bcrypt"""
    bytes_pass = password.encode('utf-8') 
    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(bytes_pass, salt) 
    return hashed.decode('utf-8')

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verificar contraseña contra hash"""
    hashed_password_bytes = hashed_password.encode('utf-8')
    userBytes = plain_password.encode('utf-8') 
    # return bcrypt.verify(plain_password, hashed_password)
    return bcrypt.checkpw(userBytes, hashed_password_bytes)