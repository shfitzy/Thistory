import bcrypt

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verify a password against a hash"""
    if not plain_password or not hashed_password:
        return False
    
    # Ensure password is bytes for bcrypt
    if isinstance(plain_password, str):
        plain_password = plain_password.encode('utf-8')
    
    # Ensure hashed_password is bytes
    if isinstance(hashed_password, str):
        hashed_password = hashed_password.encode('utf-8')
    
    try:
        return bcrypt.checkpw(plain_password, hashed_password)
    except (ValueError, TypeError):
        return False


def get_password_hash(password: str) -> str:
    """Hash a password"""
    if password is None:
        raise ValueError("Password cannot be None")
    
    # Ensure password is bytes for bcrypt
    if isinstance(password, str):
        password_bytes = password.encode('utf-8')
    else:
        password_bytes = password
    
    # Handle bcrypt's 72-byte limit by pre-hashing with SHA-256 if needed
    # if len(password_bytes) > 72:
    #     import hashlib
    #     password_bytes = hashlib.sha256(password_bytes).digest()
    
    # Generate salt and hash the password
    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(password_bytes, salt)
    
    # Return as string for database storage
    return hashed.decode('utf-8')