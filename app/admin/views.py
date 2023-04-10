from flask import render_template, request, redirect, url_for, flash
from app import db
from . import admin
from flask_login import login_required, current_user
from ..auth.views import has_permission
from ..models import User, Role
from .forms import UserForm, ChangeRoleForm
from sqlalchemy.exc import IntegrityError

@admin.route('/admin-page')
@login_required
@has_permission('admin')
def admin_page():
    return render_template('admin.html', user=current_user)

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
    # the first user (admin) can not be deleted
    # users cannot use this route to delte themselves
    if user.id != 1 and user.id != current_user.id:
        db.session.delete(user)
        db.session.commit()
    users = User.query.all()
    return redirect(url_for('.users'))

@admin.route('/change-role/<int:id>', methods=('GET', 'POST'))
@login_required
@has_permission('change_role')
def change_role(id):
    user = User.query.filter_by(id=id).first()
    form = ChangeRoleForm()
    roles = Role.query.all()
    form.role.choices = [(role.id, role.name) for role in roles]

    if request.method == 'POST' and form.validate_on_submit:
        role_id = form.role.data
        # the first user (admin) cannot have their role changed
        # users cannot change their own role
        if user.id != 1 and user.id != current_user.id:
            if user.confirmed == True:
                user.role_id = role_id
                db.session.commit()
            else:
                flash('That user has not been confirmed.', 'warning')
        return redirect(url_for('.users'))

    return render_template('change-role.html', form=form, user=user)

@admin.route('/create-user', methods=('GET', 'POST'))
@login_required
@has_permission('create_user')
def create_user():
    form = UserForm()
    if request.method == 'POST' and form.validate_on_submit:
        username = form.username.data
        password = form.password.data
        email = form.email.data
    
        try:
            new_user = User(username, password, email, role_id=1, confirmed=False)
            db.session.add(new_user)
            db.session.commit()
        except IntegrityError:
            db.session.rollback()
            flash('Sorry, that username or email has already been taken.', 'warning')
            return render_template('create-user.html', form=form)
        else:
            return redirect(url_for('.create_user'))
    
    return render_template('create-user.html', form=form)