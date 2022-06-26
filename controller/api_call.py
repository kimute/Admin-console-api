import os
import requests
from dotenv import load_dotenv
import logging


load_dotenv()


data = {}

'''
path: cM API url
method: GET/POST
jwt: credentials.jwt_token
'''


async def api_req(path, method: str, jwt, data={}):
    url = path
    headers = {'Accept': 'application/json; version=1.3',
               'Authorization': 'Bearer %s' % jwt,
               'Content-Type': 'application/json'}
    try:
        if method == 'GET':
            return requests.get(url, headers=headers)
        elif method == 'POST':
            result = requests.post(path, headers=headers, json=data)
            return result
        elif method == 'PUT':
            result = requests.put(path, headers=headers, json=data)
            return result
        elif method == 'DELETE':
            result = requests.delete(path, headers=headers)
            return result

    except Exception as e:
        logging.error('SP console API | CM api request:{}'.format(e))
        return False
