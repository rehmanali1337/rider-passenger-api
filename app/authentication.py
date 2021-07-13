from app.models import TokenData
from jose.exceptions import JWTError
from passlib.context import CryptContext
from app.db import MongoDB
from app.vars import UKeys
from jose import JOSEError, jwt
from datetime import datetime as dt, timedelta
from fastapi.security import OAuth2PasswordBearer
from fastapi import Depends, status, HTTPException

db = MongoDB()
password_context = CryptContext(schemes=['bcrypt'])
oauth2_scheme = OAuth2PasswordBearer(tokenUrl='token')

SECRET_KEY = 'efb943548bc640c3b02a6d3c68400d26037872a340dd0cfba62afb1122fbb076'
ALGORITHM = 'HS256'
ACCESS_TOKEN_EXPIRES_IN = 90


def verify_password(plain_password: str, hashed_password):
    return password_context.verify(plain_password, hashed_password)


def create_hashed_password(plain_password):
    return password_context.hash(plain_password)


def authenticate_user(user_email, password):
    user = db.get_user_with_email(user_email)
    if not user:
        return False
    if not verify_password(password, user.get(UKeys.password)):
        return False
    return user


def get_current_user(token: str = Depends(oauth2_scheme)):
    creds_exception = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                                    detail="Invalid credentials")
    try:
        payload = decode_access_token(token)
        email = payload.get("sub")
        if email is None:
            raise creds_exception
        token_data = TokenData(email=email)
    except JWTError:
        # JWTError is raised in case the token is expired ...
        raise creds_exception
    user = db.get_user_with_email(token_data.email)
    if user is None:
        raise creds_exception
    return user


def create_access_token(data: dict):
    to_encode = data.copy()
    expire = dt.now() + timedelta(days=ACCESS_TOKEN_EXPIRES_IN)
    to_encode.update({
        'exp': expire
    })
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def decode_access_token(token):
    decoded = jwt.decode(token, SECRET_KEY, algorithms=ALGORITHM)
    return decoded
