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

load_dotenv()

baseURL = os.getenv('API_URL')


@click.group()
def cli():
    pass

@cli.command(help='Create a user')
@click.argument('email')
def create_user(email):
    click.echo(click.style(f'Creating a user email: {email}', fg='green'))
    token = getAccessToken()
    createUser(token, email)


@cli.command(help='setting password for user')
@click.argument('user_id')
@click.argument('password')
def set_password(user_id, password):
    click.echo(click.style(f'setting password for user user_id: {user_id}', fg='green'))
    token = getAccessToken()
    setPassword(token, user_id, password)


@cli.command(help='Delete a user')
@click.argument('user_id')
def delete_user(user_id):
    click.echo(click.style(f'Delete a user user_id: {user_id}', fg='green'))
    token = getAccessToken()
    deleteUser(token, user_id)


@cli.command(
    help='Create user from file')
@click.argument('file_name')
def build_resource_tree_from_file(file_name):
    token = getAccessToken()
    fileData = None
    with open(f'{file_name}', 'r') as f:
        fileData = yaml.safe_load(f)

    # Parse access tree
    for user in fileData['users']:
        email = user['email']
        click.echo(click.style(f'Creating user email: {email}', fg='green'))
        createUser(token, email)


def getAccessToken():
    try:
        resp = requests.post(baseURL + 'v1/identity/auth/authenticate',
                             json=dict(email=os.getenv('ADMIN_EMAIL', None),
                                       password=os.getenv('ADMIN_PASSWORD', None)))
        resp.raise_for_status()
        return resp.text.replace('\"', '')
    except Exception as e:
        click.echo(click.style(f'{e}', fg='red'))


def createUser(token, email):
    try:
        resp = requests.post(baseURL + 'v1/identity/users/create', headers=dict(Authorization='Bearer ' + token),
                             json=dict(email=email))
        resp.raise_for_status()
    except Exception as e:
        click.echo(click.style(f'{e}', fg='red'))


def setPassword(token, user_id, password):
    try:
        resp = requests.post(baseURL + 'v1/identity/users/' + user_id + '/set_password',
                             headers=dict(Authorization='Bearer ' + token),
                             json=dict(password=password))
        resp.raise_for_status()
    except Exception as e:
        click.echo(click.style(f'{e}', fg='red'))


def deleteUser(token, user_id):
    try:
        resp = requests.delete(baseURL + 'v1/identity/users/' + user_id,
                               headers=dict(Authorization='Bearer ' + token))
        resp.raise_for_status()
    except Exception as e:
        click.echo(click.style(f'{e}', fg='red'))


if __name__ == '__main__':
    cli()
