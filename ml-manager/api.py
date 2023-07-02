# Application imports
from models import Token, User
from app import create_app
from auth import authenticate_user, get_user_from_token, create_access_token
from utils import stop_and_clean, start_container, stop_container

# Pip Imports
import requests
from fastapi import Depends, HTTPException, status, File, UploadFile
from fastapi.security import OAuth2PasswordRequestForm

# Standard Library Imports
import subprocess
import time
from typing import Annotated
from datetime import timedelta

# Constants
FILE_DIR = "/var/run/ml-containers/"

# Intialize port reservations list
if not stop_and_clean():
    print("Something went wrong trying to clean up the environment...")
    exit(1)
port_directories = { k:True for k in range(20000, 20020) }

# Helper functions
def get_available_port():
    for port, avail in port_directories.items():
        if avail:
            port_directories[port] = False
            return port
    return None

def release_port(port):
    port_directories[port] = True
    cmd = ["systemctl", "stop", f"ml-container@{port}"]
    p = subprocess.run(cmd)
    if p.returncode != 0:
        print(f"Unable to stop ml-container@{port} service: {p.stderr}")
        return False
    return True

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

@app.post("/train")
def upload(current_user: Annotated[User, Depends(get_user_from_token)], file: UploadFile = File()):
    port = get_available_port()
    try:
        if not port:
            return {"message": "Error reserving port"}

        port = str(port)
        started = start_container(port)
        if not started:
            return {"message": "Error starting container"}

        file_path = f"{FILE_DIR}/{port}/{file.filename}"
        with open(file_path, 'wb') as f:
            while contents := file.file.read(1024 * 1024):
                f.write(contents)
    except Exception:
        return {"message": f"There was an error uploading the file: {file.filename}"}
    finally:
        file.file.close()

    return {"message": "Started container"}
    #sensitivity = current_user.sensitivity
    #category = current_user.category

    #url = "http://localhost:20000/train"
    #response = requests.get(url=url)
    
    #return response.json()
