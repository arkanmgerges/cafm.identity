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
            realmName = realm['name']
            createRealm(token, realmName, realm['type'])
            for role in realm['roles']:
                roleId = createRole(token, role['name'], realmName)
                for user in role['users']:
                    userId = createUser(token, user['email'])
                    setPassword(token, userId, user['password'])
                    assignUserToRole(token, roleId, userId)
    except Exception as e:
        click.echo(click.style(f'{e}', fg='red'))


def getAccessToken():
    click.echo(click.style(f'Get Access Token', fg='green'))
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


def createRole(token, name, realmName):
    click.echo(click.style(f'Creating Role name: {name}', fg='green'))
    resp = requests.post(baseURL + 'v1/identity/roles/create', headers=dict(Authorization='Bearer ' + token),
                         json=dict(name=f'{realmName}_{name}', title=name))
    resp.raise_for_status()
    return checkForResult(token, resp.json()['request_id'], checkForID=True)


def createUser(token, email):
    click.echo(click.style(f'Creating User email: {email}', fg='green'))
    resp = requests.post(baseURL + 'v1/identity/users/create', headers=dict(Authorization='Bearer ' + token),
                         json=dict(email=email))
    resp.raise_for_status()
    return checkForResult(token, resp.json()['request_id'], checkForID=True)


def setPassword(token, user_id, password):
    click.echo(click.style(f'Set password for User: {user_id}', fg='green'))
    resp = requests.put(baseURL + 'v1/identity/users/' + user_id + '/set_password',
                        headers=dict(Authorization='Bearer ' + token),
                        json=dict(password=password))
    resp.raise_for_status()
    checkForResult(token, resp.json()['request_id'])


def assignUserToRole(token, roleID, userID):
    click.echo(click.style(f'Assign user To role', fg='green'))
    resp = requests.post(baseURL + 'v1/identity/assignments/role_to_user',
                         headers=dict(Authorization='Bearer ' + token),
                         json=dict(role_id=roleID, user_id=userID))
    resp.raise_for_status()
    checkForResult(token, resp.json()['request_id'])


def checkForResult(token, requestId, checkForID=False):
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
                if checkForID:
                    return result['items'][0]['id']
                else:
                    return
            else:
                for item in result['items']:
                    if 'reason' in item:
                        raise Exception(item['reason']['message'])
                raise Exception('Unknown error!')

    raise Exception('Response time out!')


if __name__ == '__main__':
    cli()
