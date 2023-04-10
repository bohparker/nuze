import os
from urllib.parse import urlparse
from flask import render_template, url_for, request, flash, redirect, g, abort
from app import db, login_manager
from . import auth
from ..models import User, Article, Permission
from ..email import send_email
from .forms import RegistrationForm, LoginForm
from flask_login import current_user, login_user, logout_user, login_required
from functools import wraps
from .internal_routes import INTERNAL_ROUTES

# git list of safe urls to redirect to after logging in
SAFE_URLS = os.environ.get('SAFE_URLS') or INTERNAL_ROUTES

def is_safe_url(target):
    ref_urls = SAFE_URLS
    matches = 0
    for url in ref_urls:
        test_url = urlparse(target)
        safe_url = urlparse(url)

        if (test_url.netloc != '' and test_url.netloc == safe_url.netloc) or \
        (test_url.path != '' and test_url.path == safe_url.path):
            matches += 1
        else:
            continue
    return matches >= 1


# Permission decorator
def has_permission(permission):
    def decorator(f):
        @wraps(f)
        def decorated_view(*args, **kwargs):
            # find permission from Permissions table using parameter
            perm = Permission.query.filter_by(name=permission).first()
            if not perm in current_user.role.permissions.all():
                abort(403)
            return f(*args, **kwargs)
        return decorated_view
    return decorator

@login_manager.user_loader
def load_user(id):
    return User.query.get(int(id))

# overwrite unauthorized handler to get next endpoint
@login_manager.unauthorized_handler
def redirect_to_login_with_next():
    flash('You must be logged in to view this page.', 'info')
    return redirect(url_for('auth.login', next=request.endpoint))

@auth.before_request
def get_current_user():
    g.user = current_user

@auth.route('/')
def index():
    articles = Article.query.all()
    return render_template('index.html', articles=articles)

@auth.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        flash('You are already logged in.', 'info')
        return redirect(url_for('.index'))
    
    form = RegistrationForm()
    if request.method == 'POST' and form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        email = form.email.data.lower()

        existing_username = User.query.filter_by(username=username).first()
        if existing_username:
            flash('Sorry, that username has already been taken.', 'warning')
            return render_template('register.html', form=form)
        existing_email = User.query.filter_by(email=email).first()
        if existing_email:
            flash('Sorry, that email is already in use.', 'warning')
            return render_template('register.html', form=form)
        
        new_user = User(username, password, email, role_id=1, confirmed=False)
        db.session.add(new_user)
        db.session.commit()

        login_user(new_user)

        token = new_user.generate_confirm_token()
        send_email(new_user.email, 'Confirm Your Account',
                   'email/confirm', user=new_user, token=token)

        flash('You are registered! You have been sent a confirmation email.', 'success')
        return redirect(url_for('articles.get_profile', username=new_user.username))
    
    if form.errors:
        for error, message in form.errors.items():
            flash(message[0], 'danger')
            return render_template('register.html', form=form)

    return render_template('register.html', form=form)

@auth.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        flash('You are already logged in.', 'warning')
        return redirect(url_for('.index'))

    form = LoginForm()
    if request.method == 'POST' and form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        existing_user = User.query.filter_by(username=username).first()
        
        if existing_user and existing_user.check_password(password):
            login_user(existing_user)
            next = form.next.data

            if next and is_safe_url(next):
                return redirect(url_for(next))
            else:
                flash(f'Welcome, {existing_user.username}! You have logged in.', 'info')
                return redirect(url_for('.index'))
        else:
            flash('Invalid username or password.', 'danger')
            render_template('login.html', form=form)
    
    if form.errors:
        for error, message in form.errors.items():
            flash(message[0], 'danger')
            return render_template('login.html', form=form)

    return render_template('login.html', form=form)

@auth.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have logged out.', 'info')
    return redirect(url_for('.index'))

@auth.route('/confirm/<token>')
def confirm(token):
    username = request.args.get('username')
    user = User.query.filter_by(username=username).first()
    if user.confirmed:
        return redirect(url_for('.index'))
    elif user.confirm(token):
        flash('You have successfully confirmed your account!', 'success')
    else:
        flash('The confirmation link is invalid or has expired.', 'warning')
    return redirect(url_for('.index'))

@auth.route('/confirm')
@login_required
def resend_confirmation():
    token = current_user.generate_confirm_token()
    send_email(current_user.email, 'Confirm your account',
               'email/confirm', user=current_user, token=token)
    flash('A new confirmation email has been sent.', 'info')
    return redirect(url_for('.index'))