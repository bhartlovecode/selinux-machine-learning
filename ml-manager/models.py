from pydantic import BaseModel
from typing import Union

class Token(BaseModel):
    ''' Represents a JWT token used for Authorization '''
    access_token: str
    token_type: str


class TokenData(BaseModel):
    ''' Represents the data stored inside our JWT '''
    username: Union[str, None] = None

class User(BaseModel):
    ''' Represents a user '''
    username: str
    sensitivity: str
    category: str

class UserInDB(User):
    ''' Represents a user in the database (with a hashed password) '''
    hashed_password: str