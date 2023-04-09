import os
import util
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
def get_users():
    util.get_users()

@app.cli.command()
def get_env():
    util.get_env()

@app.cli.command()
def get_urls():
    util.get_urls(app)

@app.cli.command()
def make_key():
    util.make_key()