# Application imports
from models import Token, User
from app import create_app
from auth import authenticate_user, get_user_from_token, create_access_token

# Pip Imports
import requests
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm

# Standard Library Imports
import subprocess
import time
from typing import Annotated
from datetime import timedelta

# Intitialize application
app = create_app()

@app.post("/token", response_model=Token)
async def login_for_access_token(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()]
):
    user = authenticate_user(form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token = create_access_token(
        data={"sub": user.username}
    )
    return {"access_token": access_token, "token_type": "bearer"}

@app.get("/train")
async def start_container(current_user: Annotated[User, Depends(get_user_from_token)]):
    sensitivity = current_user.sensitivity
    category = current_user.category
    return f"Training at context: user_u:user_r:{sensitivity}:{category}"
    # args = [ "/bin/systemctl", "start", "ml-container@20000" ]
    # p = subprocess.run(args)
    # print(f"Start output: {p.stdout}, Start Errors: {p.stderr}")

    # time.sleep(5) # Give container a moment to spin up

    # url = "http://localhost:20000/train"
    # response = requests.get(url=url)
    
    # args = ["/bin/systemctl", "stop", "ml-container@20000" ]
    # p = subprocess.run(args)
    # print(f"Stop output: {p.stdout}, Stop Errors: {p.stderr}")

    # return response.json()
