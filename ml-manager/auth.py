# Application Imports
from models import UserInDB, TokenData

# Pip Imports
from passlib.context import CryptContext
from jose import JWTError, jwt
from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm

# Standard Library Imports
from datetime import datetime, timedelta
from typing import Annotated, Union

# to get a string like this run:
# openssl rand -hex 32
SECRET_KEY = "f8e6c4bebcae2a25f62f143e46d19ac276393791ebf4581113987d19cdb3b37b"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60

# Store our user database as a dictionary
users_db = {
    "johndoe": {
        "username": "johndoe",
        "hashed_password": "$2b$12$l4AK6Zdsv5CwCN3QJ63vHuyPDjTumB.BJkOl4vntTQRLbjcfash7m",
        "sensitivity": "s0",
        "category": "c1"
    },
    "alicesmith": {
        "username": "alicesmith",
        "hashed_password": "$2b$12$l4AK6Zdsv5CwCN3QJ63vHuyPDjTumB.BJkOl4vntTQRLbjcfash7m",
        "sensitivity": "s0",
        "category": "c2"
    },
    "fredjames": {
        "username": "fredjames",
        "hashed_password": "$2b$12$l4AK6Zdsv5CwCN3QJ63vHuyPDjTumB.BJkOl4vntTQRLbjcfash7m",
        "sensitivity": "s0",
        "category": "c3"
    },
    "bethdavies": {
        "username": "bethdavies",
        "hashed_password": "$2b$12$l4AK6Zdsv5CwCN3QJ63vHuyPDjTumB.BJkOl4vntTQRLbjcfash7m",
        "sensitivity": "s1",
        "category": "c4"
    },
    "samfisher": {
        "username": "samfisher",
        "hashed_password": "$2b$12$l4AK6Zdsv5CwCN3QJ63vHuyPDjTumB.BJkOl4vntTQRLbjcfash7m",
        "sensitivity": "s1",
        "category": "c5"
    },
    "judybass": {
        "username": "judybass",
        "hashed_password": "$2b$12$l4AK6Zdsv5CwCN3QJ63vHuyPDjTumB.BJkOl4vntTQRLbjcfash7m",
        "sensitivity": "s1",
        "category": "c6"
    },
}

# Create our password context with the bcrypt scheme
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

def verify_password(plain_password, hashed_password) -> bool:
    return pwd_context.verify(plain_password, hashed_password)

def get_user(db, username: str) -> Union[UserInDB, None]:
    if username in db:
        user_dict = db[username]
        return UserInDB(**user_dict)


def authenticate_user(username: str, password: str) -> Union[UserInDB, bool, None]:
    user = get_user(users_db, username)
    if not user:
        return False
    if not verify_password(password, user.hashed_password):
        return False
    return user


def create_access_token(data: dict) -> str:
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


async def get_user_from_token(token: Annotated[str, Depends(oauth2_scheme)]) -> Union[UserInDB, HTTPException]:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Unable to validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    token_data = None
    try:
        jwt_payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username = jwt_payload.get("sub")
        if username is None:
            raise credentials_exception
        token_data = TokenData(username=username)
    except JWTError:
        raise credentials_exception
    user = get_user(users_db, username=token_data.username)
    if user is None:
        raise credentials_exception
    return user