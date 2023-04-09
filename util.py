import os
import secrets
from app.models import User

def get_users():
    users = User.query.all()

    for user in users:
        user_string = f"""
        username: {user.username}
        role: {user.role}
        permissions:
        """
        print(user_string)
        for role in user.role.permissions:
            print(role)
        print('-----------')


def get_env():
    print('Environment Variables')
    print('----------------------')
    for k,v in os.environ.items():
        print(f'{k}:{v}')


def get_urls(app):
    routes = []
    print('URL Map')
    print('==============')
    for rule in app.url_map.iter_rules():
        routes.append(rule.endpoint)
    print(routes)


def make_key():
    print(secrets.token_hex(16))
