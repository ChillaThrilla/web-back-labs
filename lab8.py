from flask import Blueprint, render_template, request, session, redirect, current_app
from db import db
from db.models import users, articles
from werkzeug.security import check_password_hash, generate_password_hash
from flask_login import login_user, logout_user, current_user, login_required


lab8 = Blueprint('lab8', __name__)

@lab8.route('/lab8/')
def lab():
    return render_template('lab8/lab8.html')



@lab8.route('/lab8/register/', methods=['GET', 'POST'])
def register():
    if request.method == 'GET':
        return render_template('lab8/register.html')

    login_form = request.form.get('login')
    password_form = request.form.get('password')

    if not login_form:
        return render_template('lab8/register.html',
                               error='Логин не должен быть пустым')

    if not password_form:
        return render_template('lab8/register.html',
                               error='Пароль не должен быть пустым')

    login_exists = users.query.filter_by(login=login_form).first()
    if login_exists:
        return render_template(
            'lab8/register.html',
            error='Такой пользователь уже существует'
        )

    password_hash = generate_password_hash(password_form)
    new_user = users(login=login_form, password=password_hash)

    db.session.add(new_user)
    db.session.commit()

    login_user(new_user)    
    return redirect('/lab8/')



@lab8.route('/lab8/login/', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('lab8/login.html')

    login_form = request.form.get('login')
    password_form = request.form.get('password')

    if not login_form or not password_form:
        return render_template(
            'lab8/login.html',
            error='Логин и пароль не должны быть пустыми'
        )

    user = users.query.filter_by(login=login_form).first()

    remember_me = True if request.form.get('remember') else False

    if user:
        if check_password_hash(user.password, password_form):
            login_user(user, remember=remember_me)  
            return redirect('/lab8/')
    
    return render_template(
        'lab8/login.html',
        error='Ошибка входа: логин и/или пароль неверны'
    )




@lab8.route('/lab8/articles/')
@login_required
def article_list():
    user_articles = articles.query.filter_by(login_id=current_user.id).all()
    return render_template('lab8/articles.html', articles=user_articles)




@lab8.route('/lab8/logout')
@login_required
def logout():
    logout_user()
    return redirect('/lab8/')



@lab8.route('/lab8/create/', methods=['GET', 'POST'])
@login_required
def create_article():
    if request.method == 'GET':
        return render_template('lab8/create.html')

    title = request.form.get('title')
    text = request.form.get('text')

    if not title or not text:
        return render_template(
            'lab8/create.html',
            error="Название и текст статьи не должны быть пустыми"
        )

    new_article = articles(
        login_id=current_user.id,
        title=title,
        article_text=text,
        likes=0
    )

    db.session.add(new_article)
    db.session.commit()

    return redirect('/lab8/articles/')



@lab8.route('/lab8/edit/<int:id>/', methods=['GET', 'POST'])
@login_required
def edit_article(id):
    article = articles.query.get(id)

    # Проверяем, что статья существует
    if not article:
        return "Статья не найдена", 404

    # Проверяем, что пользователь — автор
    if article.login_id != current_user.id:
        return "Доступ запрещён", 403

    if request.method == 'GET':
        return render_template('lab8/edit.html', article=article)

    # POST — сохраняем изменения
    new_title = request.form.get('title')
    new_text = request.form.get('text')

    if not new_title or not new_text:
        return render_template(
            'lab8/edit.html',
            article=article,
            error="Поля не должны быть пустыми"
        )

    article.title = new_title
    article.article_text = new_text

    db.session.commit()

    return redirect('/lab8/articles/')



@lab8.route('/lab8/delete/<int:id>/')
@login_required
def delete_article(id):
    article = articles.query.get(id)

    if not article:
        return "Статья не найдена", 404

    # Проверяем, что это статья текущего пользователя
    if article.login_id != current_user.id:
        return redirect('/lab8/articles/')

    db.session.delete(article)
    db.session.commit()

    return redirect('/lab8/articles/')
