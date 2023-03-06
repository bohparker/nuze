import os
from app import create_app, db
from app.models import User, Role, Permission, Article

app = create_app(os.getenv('FLASK_CONFIG') or 'default')


@app.shell_context_processor
def make_shell_context():
    return dict(db=db, User=User, Role=Role, Permission=Permission, Article=Article)


@app.cli.command()
def create_db():
    db.create_all()

@app.cli.command()
def delete_db():
    db.drop_all()

@app.cli.command()
def print_users():
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

@app.cli.command()
def get_environ():
    for k,v in os.environ.items():
        print(f'{k}:{v}')