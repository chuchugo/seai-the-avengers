import sys
import os
from flask import jsonify
from flask import Flask
import pickle
import json
from flask import request, make_response
import requests
import numpy as np
import random

app = Flask('load-balancer-server')

def checkHealth(ip_addr):
    return os.system('nc -vz ' + ip_addr) == 0

@app.route('/')
def basic_route():
    return {"message": "Welcome to The Avengers!"}

@app.route('/recommend/<int:userid>', methods=['GET'])
def welcome(userid):
    # add health check
    A_server_up = checkHealth('0.0.0.0 7004')
    B_server_up = checkHealth('0.0.0.0 7005')

    # if not B_server_up and A_server_up:
    #     response = requests.get(F'http://0.0.0.0:7004/recommend/{userid}')
    # elif B_server_up and not A_server_up:
    #     response = requests.get(F'http://0.0.0.0:7005/recommend/{userid}')
    if A_server_up and B_server_up: 
        if userid%2!=0:
            response = requests.get(F'http://0.0.0.0:7004/recommend/{userid}')
        else:
            response = requests.get(F'http://0.0.0.0:7005/recommend/{userid}')
    else:
        response = ''
    return str(response.text)

if __name__ == '__main__':
    app.run(host='17645-team17.isri.cmu.edu', port=8082, debug=False)
