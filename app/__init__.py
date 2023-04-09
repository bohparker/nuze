from dotenv import load_dotenv
from flask import Flask, render_template
from flask_mail import Mail
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import CSRFProtect
from config import config
from flask_login import LoginManager
from flask_ckeditor import CKEditor


mail = Mail()
db = SQLAlchemy()
csrf = CSRFProtect()
login_manager = LoginManager()
ckeditor = CKEditor()

# set environment variables from .env file
load_dotenv()

def create_app(config_name):
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    config[config_name].init_app(app)
    
    mail.init_app(app)
    db.init_app(app)
    csrf.init_app(app)
    login_manager.init_app(app)
    login_manager.login_view = 'auth.login'
    login_manager.login_message_category = 'info'
    ckeditor.init_app(app)

    from .auth import auth as auth_blueprint
    app.register_blueprint(auth_blueprint)

    from .articles import articles as articles_blueprint
    app.register_blueprint(articles_blueprint)

    from .admin import admin as admin_blueprint
    app.register_blueprint(admin_blueprint)

    # error handling
    @app.errorhandler(404)
    def page_not_found(e):
        return render_template('404.html'), 404
    
    @app.errorhandler(403)
    def permission_denied(e):
        return render_template('403.html'), 403

    return app