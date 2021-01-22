"""
@author: Mohammad M. Mohammad<mmdii@develoop.run>
"""
import sys

sys.path.append("../../../")

import os
from dotenv import load_dotenv

import yaml
import click
import requests
from time import sleep

load_dotenv()

baseURL = os.getenv('API_URL')


@click.group()
def cli():
    pass


@cli.command(
    help='Create user from file')
@click.argument('file_name')
def build_resource_tree_from_file(file_name):
    try:
        token = getAccessToken()
        with open(f'{file_name}', 'r') as f:
            fileData = yaml.safe_load(f)

        # Parse access tree
        for realm in fileData['realms']:
            createRealm(token, realm['name'], realm['type'])
            # for role in realm['roles']:
            #     roleReqId = createRole(token, role['name'])
            #     for user in role['users']:
            #         userReqId = createUser(token, user['email'])
            #         passReqId = setPassword(token, userId, user['password'])
            #         assignReqId = assignUserToRole(token, roleId, userId)
    except Exception as e:
        click.echo(click.style(f'{e}', fg='red'))


def getAccessToken():
    resp = requests.post(baseURL + 'v1/identity/auth/authenticate',
                         json=dict(email=os.getenv('ADMIN_EMAIL', None),
                                   password=os.getenv('ADMIN_PASSWORD', None)))
    resp.raise_for_status()
    return resp.text.replace('\"', '')


def createRealm(token, name, type):
    click.echo(click.style(f'Creating realm name: {name} type: {type}', fg='green'))
    resp = requests.post(baseURL + 'v1/identity/realms/create', headers=dict(Authorization='Bearer ' + token),
                         json=dict(name=name, realm_type=type))
    resp.raise_for_status()
    checkForResult(token, resp.json()['request_id'])


def createRole(token, name):
    click.echo(click.style(f'Creating realm name: {name} type: {type}', fg='green'))
    resp = requests.post(baseURL + 'v1/identity/roles/create', headers=dict(Authorization='Bearer ' + token),
                         json=dict(name=name))
    resp.raise_for_status()
    return resp.json()['request_id']


def createUser(token, email):
    resp = requests.post(baseURL + 'v1/identity/users/create', headers=dict(Authorization='Bearer ' + token),
                         json=dict(email=email))
    resp.raise_for_status()
    return resp.json()['request_id']


def setPassword(token, user_id, password):
    resp = requests.post(baseURL + 'v1/identity/users/' + user_id + '/set_password',
                         headers=dict(Authorization='Bearer ' + token),
                         json=dict(password=password))
    resp.raise_for_status()
    return resp.json()['request_id']


def assignUserToRole(token, roleID, userID):
    resp = requests.post(baseURL + 'v1/identity/assignments/role_to_user',
                         headers=dict(Authorization='Bearer ' + token),
                         json=dict(role_id=roleID, user_id=userID))
    resp.raise_for_status()
    return resp.json()['request_id']


def checkForResult(token, requestId):
    for i in range(5):
        sleep(1)
        isSuccessful = requests.get(baseURL + 'v1/common/request/is_successful',
                                    headers=dict(Authorization='Bearer ' + token),
                                    params=dict(request_id=str(requestId)))
        if isSuccessful.status_code == 200:
            resp = requests.get(baseURL + 'v1/common/request/result', headers=dict(Authorization='Bearer ' + token),
                                params=dict(request_id=str(requestId)))
            resp.raise_for_status()
            result = resp.json()['result']
            if isSuccessful.json()['success']:
                return result['items'][0]['id']
            else:
                for item in result['items']:
                    if 'reason' in item:
                        raise Exception(item['reason']['message'])
                raise Exception('Unknown error!')

    raise Exception('Response time out!')


if __name__ == '__main__':
    cli()
