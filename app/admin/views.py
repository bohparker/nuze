from flask import render_template, request, redirect, url_for
from app import db
from . import admin
from flask_login import login_required
from ..auth.views import has_permission
from ..models import User
from .forms import UserForm

@admin.route('/users')
@login_required
@has_permission('admin')
def users():
    users = User.query.all()
    return render_template('users.html', users=users)

@admin.route('/delete-user/<int:id>')
@login_required
@has_permission('delete_user')
def delete_user(id):
    user = User.query.filter_by(id=id).first()
    db.session.delete(user)
    db.session.commit()
    users = User.query.all()
    return redirect(url_for('.users'))

@admin.route('/create-user', methods=('GET', 'POST'))
@login_required
@has_permission('create_user')
def create_user():
    form = UserForm()
    if request.method == 'POST' and form.validate_on_submit:
        username = form.username.data
        password = form.password.data
        email = form.email.data
        new_user = User(username, password, email, role_id=1, confirmed=False)
        db.session.add(new_user)
        db.session.commit()
        return redirect(url_for('.create_user'))
    
    return render_template('create-user.html', form=form)