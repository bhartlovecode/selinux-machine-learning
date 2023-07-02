#!/usr/bin/env python3
import argparse
import requests
import os

# Constants
URL = "http://127.0.0.1:8000"
jwt_file_path = os.path.expanduser('~') + '/.mlclient-jwt.txt'

def login_user(username, password):
    request_url = URL + "/token"

    form_data = {
        "username": username,
        "password": password
    }

    response = requests.post(url=request_url, data=form_data)
    return response

def train_model(model, filename):
    print(f"Attemping to train {model} on {filename}")
    return None

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
    if not os.path.exists(jwt_file_path):
        print("No access token found! Please use the 'login' subcommand before making any requests.")
        exit(1)
    train_model(args.model[0], args.filename[0])
else:
    print("No command specified.")
    exit(1)