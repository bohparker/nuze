from flask import render_template, request, redirect, url_for, flash
from app import db
from . import articles
from ..models import User, Article
from .forms import ArticleForm
from flask_login import current_user, login_required
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
    articles = Article.query.filter_by(author_id=user.id).all()
    return render_template('profile.html', user=user, articles=articles)