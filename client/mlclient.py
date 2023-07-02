#!/usr/bin/env python3
import argparse
import requests
import os

# Constants
URL = "http://127.0.0.1:8000"
jwt_file_path = os.path.expanduser('~') + '/.mlclient-jwt.txt'

def read_jwt_token():
    if os.path.exists(jwt_file_path) and os.path.isfile(jwt_file_path):
        jwt_token = None
        with open(jwt_file_path, 'r') as f:
            jwt_token = f.readline()
            return jwt_token
    print("No access token found! Please use the 'login' subcommand before making any requests.")
    return None

def login_user(username, password):
    request_url = URL + "/token"

    form_data = {
        "username": username,
        "password": password
    }

    response = requests.post(url=request_url, data=form_data)
    return response

def train_model(model, filename):
    jwt_token = read_jwt_token()
    if not jwt_token:
        exit(1)
    header_token = "Bearer " + jwt_token 
    headers = {"Authorization": header_token}
    
    file = {'file': open('test.csv', 'rb')}
    request_url = URL + "/train"
    response = requests.post(url=request_url, files=file, headers=headers)
    return response

# Define our parser
parser = argparse.ArgumentParser(prog='MLClient')
subparsers = parser.add_subparsers(dest='command')
login = subparsers.add_parser('login')
train = subparsers.add_parser('train')

# create the parser for the login command
login_parser = subparsers.add_parser('login')
login_parser.add_argument('--username', required=True, nargs=1)
login_parser.add_argument('--password', required=True, nargs=1)

# Create the parser for the training command
train_parser = subparsers.add_parser('train')
train_parser.add_argument('--filename', nargs=1, required=True)
train_parser.add_argument('--model', nargs=1, required=True, choices=["dtc"])

args = parser.parse_args()

# Parse the command to call
if args.command == 'login':
    response = login_user(args.username[0], args.password[0])
    if response.status_code > 201:
        print(f"Unable to login as user: '{args.username[0]}'. Verify username and password are correct.")
        exit(1)
    json_response = response.json()
    token = json_response.get("access_token")
    
    print(f"Access token saved to path: {jwt_file_path}")
    with open(jwt_file_path, 'w') as f:
        f.write(token)
elif args.command == 'train':
    response = train_model(args.model[0], args.filename[0])
    print(response.json())
else:
    print("No command specified.")
    exit(1)