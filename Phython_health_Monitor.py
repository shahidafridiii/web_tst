#!/usr/bin/python
import os
import requests


# IP = '10.229.205.38'
# PORT ='6443'
# URI = '/get-vnmsha-details'
# USERNAME = 'abc'
# PASSWORD = 'vira@123'

USERNAME = os.environ['USERNAME']
PASSWORD = os.environ['PASSWORD']

IP = os.environ['IP']
PORT = os.environ['PORT']
URI = os.environ['URI']


URL = 'http://' + IP +  ':' + PORT + URI

try:
headers = {"Content-Type": "application/json", "Accept": "application/json", 'Connection':'close'}
resp = requests.post(URL, auth=(USERNAME, PASSWORD), headers=headers, verify=False)
# print(resp.headers)
    server_resp = resp.json()
    for e, s in server_resp.items():
        if e is not str:
            if 'output' in e:
                for i, v in s.items():
                    if type(v) is not str:
                        if 'master' in (v['mode']):
                            resp.close()
                            print('up')
except:
    resp.close()

