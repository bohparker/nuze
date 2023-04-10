from datetime import datetime
from flask import current_app
from werkzeug.security import generate_password_hash, check_password_hash
from app import db
from itsdangerous import TimestampSigner

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True)
    pwdhash = db.Column(db.String())
    email = db.Column(db.String(100), unique=True)
    joined = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    bio = db.Column(db.Text(400))
    # one to many relationship to Role
    role_id = db.Column(db.Integer, db.ForeignKey('role.id'))
    confirmed = db.Column(db.Boolean)
    articles = db.relationship('Article', backref='author', lazy='dynamic')

    def __init__(self, username, password, email, role_id, confirmed):
        self.username = username
        self.pwdhash = generate_password_hash(password)
        self.email = email
        self.role_id = role_id
        self.confirmed = confirmed

    def check_password(self, password):
        return check_password_hash(self.pwdhash, password)
    
    def generate_confirm_token(self):
        s = TimestampSigner(current_app.config['TIMESTAMP_KEY'])
        return s.sign(self.username).decode('utf-8')
    
    def confirm(self, token):
        s = TimestampSigner(current_app.config['TIMESTAMP_KEY'])
        try:
            data = s.unsign(token, max_age=60 * 30).decode('utf-8')
        except:
            return False
        if data != self.username:
            return False
        self.confirmed = True
        db.session.add(self)
        db.session.commit()
        return True
    
    def verify_reset(self, token):
        s = TimestampSigner(current_app.config['TIMESTAMP_KEY'])
        try:
            data = s.unsign(token, max_age=60 * 5).decode('utf-8')
        except:
            return False
        if data != self.username:
            return False
        return True

    
    @property
    def is_authenticated(self):
        return True
    
    @property
    def is_active(self):
        return True
    
    @property
    def is_anonymous(self):
        return False
    
    def get_id(self):
        return str(self.id)
    
    def __repr__(self):
        return f'<User "{self.username}">'
    
# linking table for Permission and Role
role_permission = db.Table('role_permision',
                           db.Column('role_id', db.Integer, db.ForeignKey('role.id')),
                           db.Column('permission_id', db.Integer, db.ForeignKey('permission.id'))
                            )

## ID   Permission
#-----------------
#  1    write_article
#  2    edit_article
#  3    delete_article
#  4    change_role
#  5    delete_user

class Permission(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))

    def __repr__(self):
        return self.name

## ID  Role
#------------
#  1   User
#  2   Author
#  3   Editor
#  4   Admin

class Role(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(10))
    # many to many relationship to Permission
    permissions = db.relationship('Permission', secondary=role_permission, backref='roles', lazy='dynamic')
    # many to one relationship to User
    users = db.relationship('User', backref='role')

    def __repr__(self):
        return f'<Role "{self.name}">'

class Article(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.Text(100))
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    author_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    body = db.Column(db.Text)

    def __init__(self, title, author_id, body):
        self.title = title
        self.author_id = author_id
        self.body = body