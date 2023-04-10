from flask import render_template, request, redirect, url_for, \
flash, abort
from app import db
from . import articles
from ..models import User, Article
from .forms import ArticleForm, BioForm, ChangePasswordForm
from flask_login import current_user, login_required
from werkzeug.security import generate_password_hash
from ..auth.views import has_permission

@articles.route('/<int:id>')
def article(id):
    article = Article.query.get_or_404(id)
    return render_template('article.html', article=article)

@articles.route('/write-article', methods=['GET', 'POST'])
@login_required
@has_permission('write_article')
def write_article():
    form = ArticleForm()
    if request.method == 'POST' and form.validate_on_submit():
        title = form.title.data.title()
        body = form.body.data
        author_id = current_user.id

        new_article = Article(title=title, author_id=author_id, body=body)
        db.session.add(new_article)
        db.session.commit()
        flash('The article has been published!', 'success')
        return redirect(url_for('auth.index'))

    return render_template('write_article.html', form=form)

@articles.route('/user/<username>')
def get_profile(username):
    user = User.query.filter_by(username=username).first()
    if not user:
        abort(404)
    articles = Article.query.filter_by(author_id=user.id).all()
    return render_template('profile.html', user=user, articles=articles)

@articles.route('/bio-form', methods=['GET', 'POST'])
@login_required
def bio_form():
    form = BioForm()
    if request.method == 'POST' and form.validate_on_submit:
        bio = form.bio.data
        current_user.bio = bio
        db.session.commit()
        return render_template('profile.html', user=current_user)

    return render_template('bio-form.html', form=form)

@articles.route('/change-password', methods=['GET', 'POST'])
@login_required
def change_password():
    form = ChangePasswordForm()
    id = request.args.get('id')
    user = User.query.get_or_404(id)
    if user != current_user:
        abort(403)
    if request.method == 'POST' and form.validate_on_submit():
        old_password = form.password.data
        new_password = form.new.data
        if new_password == old_password:
            flash('New Password must be different than Old Password.', 'warning')
            return render_template('change-password.html', form=form, id=current_user.id)
        if current_user.check_password(old_password):
            current_user.pwdhash = generate_password_hash(new_password)
            db.session.commit()
            flash('Password updated.', 'success')
            return redirect(url_for('.get_profile', username=current_user.username))
        flash('Password incorrect', 'danger')
        return render_template('change-password.html', form=form, id=current_user.id)
    
    if form.errors:
        for error, message in form.errors.items():
            flash(message[0], 'danger')
            return render_template('change-password.html', form=form, id=current_user.id)

    return render_template('change-password.html', form=form, id=id)
            
