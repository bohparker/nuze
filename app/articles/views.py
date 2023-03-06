from flask import render_template, request, redirect, url_for, flash
from app import db
from . import articles
from ..models import User, Article
from .forms import ArticleForm
from flask_login import current_user, login_required

@articles.route('/<int:id>')
def article(id):
    article = Article.query.get_or_404(id)
    return render_template('article.html', article=article)

@articles.route('/write-article', methods=['GET', 'POST'])
@login_required
def write_article():
    form = ArticleForm()
    if request.method == 'POST' and form.validate_on_submit():
        title = form.title.data
        body = form.body.data
        author_id = current_user.id

        new_article = Article(title=title, author_id=author_id, body=body)
        db.session.add(new_article)
        db.session.commit()
        flash('The article has been published!', 'success')
        return redirect(url_for('auth.index')) 

    return render_template('write_article.html', form=form)