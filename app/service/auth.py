from datetime import UTC , datetime, timedelta

import jwt
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from pwdlib import PasswordHash

from ..config.authConfig import settings

password_hash = PasswordHash.recommended()

oauth2_schema = HTTPBearer()

def hash_password(input_password : str) -> str:
    return password_hash.hash(input_password)

def verify_password(plain_password: str , hashed_password : str) -> bool:
    return password_hash.verify(plain_password, hashed_password);

def create_access_token(data : dict) -> str : 
    claims = data.copy()

    expire = datetime.now(UTC) + timedelta(minutes= settings.access_token_expire_minutes)

    claims.update({"exp" : expire})

    encoded_jwt = jwt.encode(
        claims,
        settings.secret_key.get_secret_value(),
        settings.algorithm
    )

    return encoded_jwt

def verify_token(token : str) -> str | None:
    try:
        payload = jwt.decode(
            token,
            settings.secret_key.get_secret_value(),
            algorithms=[settings.algorithm],
            options={"require" : ["exp" , "sub"]},
        )

    except jwt.InvalidTokenError:
        return None
    else:
        return payload.get("sub")