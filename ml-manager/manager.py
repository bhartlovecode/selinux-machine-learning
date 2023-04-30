from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import subprocess
import time
import requests

# Constants

app = FastAPI()

origins = [
    "*"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Start container function
@app.get("/train")
async def start_container():
    args = [ "/bin/systemctl", "start", "ml-container@20000" ]
    p = subprocess.run(args)
    print(f"Start output: {p.stdout}, Start Errors: {p.stderr}")

    time.sleep(5) # Give container a moment to spin up

    url = "http://localhost:20000/train"
    response = requests.get(url=url)
    
    args = ["/bin/systemctl", "stop", "ml-container@20000" ]
    p = subprocess.run(args)
    print(f"Stop output: {p.stdout}, Stop Errors: {p.stderr}")

    return response.json()
