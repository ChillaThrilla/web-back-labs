from flask import Blueprint, render_template, request, session, redirect, current_app
import psycopg2
from psycopg2.extras import RealDictCursor
from werkzeug.security import check_password_hash, generate_password_hash
import sqlite3
from os import path


lab5 = Blueprint('lab5', __name__)



def db_connect():
    # Выбор между PostgreSQL и SQLite
    if current_app.config['DB_TYPE'] == 'postgres':
        conn = psycopg2.connect(
            host='127.0.0.1',
            database='kirill_chinkevich_knowledge_base',
            user='kirill_chinkevich_knowledge_base',
            password='1'
        )
        cur = conn.cursor(cursor_factory=RealDictCursor)
    else:
        # Подключение SQLite
        dir_path = path.dirname(path.realpath(__file__))
        db_path = path.join(dir_path, "database.db")
        conn = sqlite3.connect(db_path)
        conn.row_factory = sqlite3.Row
        cur = conn.cursor()

    return conn, cur


def db_close(conn, cur):
    conn.commit()
    cur.close()
    conn.close()



# Главная страница ЛР5
@lab5.route('/lab5/')
def lab():
    return render_template('lab5/lab5.html', login=session.get('login'))



@lab5.route('/lab5/register', methods=['GET', 'POST'])
def register():
    # GET — просто показать форму
    if request.method == 'GET':
        return render_template('lab5/register.html')

    # POST — обработка данных
    login = request.form.get('login')
    password = request.form.get('password')

    # Проверка заполненности
    if not login or not password:
        return render_template('lab5/register.html',
                               error='Заполните все поля')

    conn, cur = db_connect()    

    # Проверяем существование логина
    if current_app.config['DB_TYPE'] == 'postgres':
        cur.execute("SELECT login FROM users WHERE login=%s;", (login,))
    else:
        cur.execute("SELECT login FROM users WHERE login=?;", (login,))

    if cur.fetchone():
        db_close(conn, cur)
        return render_template('lab5/register.html',
                               error='Такой пользователь уже существует')

    real_name = request.form.get('real_name')

    if not real_name:
        return render_template('lab5/register.html', error="Введите имя")

    password_hash = generate_password_hash(password)

    if current_app.config['DB_TYPE'] == 'postgres':
        cur.execute(
            "INSERT INTO users (login, password, real_name) VALUES (%s, %s, %s);",
            (login, password_hash, real_name)
        )
    else:
        cur.execute(
            "INSERT INTO users (login, password, real_name) VALUES (?, ?, ?);",
            (login, password_hash, real_name)
        )

    db_close(conn, cur)

    # Показываем успех
    return render_template('lab5/success.html', login=login)



@lab5.route('/lab5/login', methods=['GET', 'POST'])
def login():
    # Показать форму
    if request.method == 'GET':
        return render_template('lab5/login.html')

    # Получаем данные формы
    login = request.form.get('login')
    password = request.form.get('password')

    # Проверка заполнения
    if not (login or password):
        return render_template('lab5/login.html',
                               error="Заполните поля")

    conn, cur = db_connect()

    # Ищем пользователя
    if current_app.config['DB_TYPE'] == 'postgres':
        cur.execute("SELECT * FROM users WHERE login=%s;", (login,))
    else:
        cur.execute("SELECT * FROM users WHERE login=?;", (login,))
    user = cur.fetchone()

    # Логин не найден
    if not user:
        db_close(conn, cur)
        return render_template('lab5/login.html',
                               error="Логин и/или пароль неверны")

    # Проверка пароля
    if not check_password_hash(user['password'], password):  
        db_close(conn, cur)
        return render_template('lab5/login.html',
                               error="Логин и/или пароль неверны")

    # Авторизация прошла
    session['login'] = login

    db_close(conn, cur)
    return render_template('lab5/success_login.html', login=login)



@lab5.route('/lab5/create', methods=['GET', 'POST'])
def create():
    login = session.get('login')
    if not login:
        return redirect('/lab5/login')

    if request.method == 'GET':
        return render_template('lab5/create.html')

    title = request.form.get('title')
    article_text = request.form.get('article_text')

    # Валидация — не принимаем пустые статьи
    if not title or not article_text:
        return render_template(
            'lab5/create_article.html',
            error='Заполните заголовок и текст статьи',
            title=title,
            article_text=article_text
        )

    conn, cur = db_connect()

    if current_app.config['DB_TYPE'] == 'postgres':
        cur.execute("SELECT * FROM users WHERE login=%s;", (login,))
    else:
        cur.execute("SELECT * FROM users WHERE login=?;", (login,))

    login_id = cur.fetchone()["id"]

    is_public = True if request.form.get("is_public") else False

    if current_app.config['DB_TYPE'] == 'postgres':
        cur.execute(
            "INSERT INTO articles (login_id, title, article_text, is_public) VALUES (%s, %s, %s, %s);",
            (login_id, title, article_text, is_public)
        )
    else:
        cur.execute(
            "INSERT INTO articles (login_id, title, article_text, is_public) VALUES (?, ?, ?, ?);",
            (login_id, title, article_text, is_public)
        )


    db_close(conn, cur)

    return redirect('/lab5')

@lab5.route('/lab5/list')
def list():
    login = session.get('login')
    if not login:
        return redirect('/lab5/login')

    conn, cur = db_connect()

    if current_app.config['DB_TYPE'] == 'postgres':
        cur.execute("SELECT id FROM users WHERE login=%s;", (login,))
    else:
        cur.execute("SELECT id FROM users WHERE login=?;", (login,))

    login_id = cur.fetchone()["id"]

    if current_app.config['DB_TYPE'] == 'postgres':
        cur.execute(
            "SELECT * FROM articles WHERE login_id=%s ORDER BY is_favorite DESC, id DESC;",
            (login_id,)
        )
    else:
        cur.execute(
            "SELECT * FROM articles WHERE login_id=? ORDER BY is_favorite DESC, id DESC;",
            (login_id,)
        )

    articles = cur.fetchall()

    db_close(conn, cur)

    return render_template('lab5/list.html', articles=articles)



@lab5.route('/lab5/logout')
def logout():
    session.pop('login', None)
    return redirect('/lab5/login')



@lab5.route('/lab5/edit/<int:article_id>', methods=['GET', 'POST'])
def edit_article(article_id):
    login = session.get('login')
    if not login:
        return redirect('/lab5/login')

    conn, cur = db_connect()

    # id пользователя
    if current_app.config['DB_TYPE'] == 'postgres':
        cur.execute("SELECT id FROM users WHERE login=%s;", (login,))
    else:
        cur.execute("SELECT id FROM users WHERE login=?;", (login,))
    row = cur.fetchone()

    if not row:
        db_close(conn, cur)
        return redirect('/lab5/login')

    login_id = row["id"]

    # сначала вытаскиваем статью пользователя
    if current_app.config['DB_TYPE'] == 'postgres':
        cur.execute(
            "SELECT * FROM articles WHERE id=%s AND login_id=%s;",
            (article_id, login_id)
        )
    else:
        cur.execute(
            "SELECT * FROM articles WHERE id=? AND login_id=?;",
            (article_id, login_id)
        )
    article = cur.fetchone()

    if not article:
        db_close(conn, cur)
        abort(404)

    if request.method == 'GET':
        db_close(conn, cur)
        return render_template('lab5/edit_list.html', article=article)

    # POST — сохраняем изменения
    title = request.form.get('title')
    article_text = request.form.get('article_text')

    is_public = True if request.form.get('is_public') else False

    if not title or not article_text:
        db_close(conn, cur)
        # снова отрисуем форму с ошибкой
        return render_template(
            'lab5/edit_list.html',
            article=article,
            error='Заполните заголовок и текст статьи'
        )

    if current_app.config['DB_TYPE'] == 'postgres':
        cur.execute(
            "UPDATE articles "
            "SET title=%s, article_text=%s, is_public=%s "
            "WHERE id=%s AND login_id=%s;",
            (title, article_text, is_public, article_id, login_id)
        )
    else:
        cur.execute(
            "UPDATE articles "
            "SET title=?, article_text=?, is_public=? "
            "WHERE id=? AND login_id=?;",
            (title, article_text, is_public, article_id, login_id)
        )

    db_close(conn, cur)

    return redirect('/lab5/list')



@lab5.route('/lab5/delete/<int:article_id>', methods=['POST'])
def delete_article(article_id):
    login = session.get('login')
    if not login:
        return redirect('/lab5/login')

    conn, cur = db_connect()

    # id пользователя
    if current_app.config['DB_TYPE'] == 'postgres':
        cur.execute("SELECT id FROM users WHERE login=%s;", (login,))
    else:
        cur.execute("SELECT id FROM users WHERE login=?;", (login,))
    row = cur.fetchone()

    if not row:
        db_close(conn, cur)
        return redirect('/lab5/login')

    login_id = row["id"]

    # удаляем только свою статью
    if current_app.config['DB_TYPE'] == 'postgres':
        cur.execute(
            "DELETE FROM articles WHERE id=%s AND login_id=%s;",
            (article_id, login_id)
        )
    else:
        cur.execute(
            "DELETE FROM articles WHERE id=? AND login_id=?;",
            (article_id, login_id)
        )

    db_close(conn, cur)

    return redirect('/lab5/list')



@lab5.route('/lab5/users')
def users():
    conn, cur = db_connect()

    if current_app.config['DB_TYPE'] == 'postgres':
        cur.execute("SELECT login, real_name FROM users;")
    else:
        cur.execute("SELECT login, real_name FROM users;")

    users = cur.fetchall()
    db_close(conn, cur)

    return render_template('lab5/users.html', users=users)



@lab5.route('/lab5/profile', methods=['GET', 'POST'])
def profile():
    login = session.get('login')
    if not login:
        return redirect('/lab5/login')

    conn, cur = db_connect()

    if request.method == 'GET':
        if current_app.config['DB_TYPE'] == 'postgres':
            cur.execute("SELECT real_name FROM users WHERE login=%s;", (login,))
        else:
            cur.execute("SELECT real_name FROM users WHERE login=?;", (login,))
        row = cur.fetchone()
        db_close(conn, cur)
        return render_template("lab5/profile.html", real_name=row["real_name"])

    # POST
    new_name = request.form.get("real_name")
    old_pass = request.form.get("old_password")
    new_pass = request.form.get("password")

    if new_name.strip() == "":
        return render_template("lab5/profile.html",
                               error="Введите имя",
                               real_name=new_name)

    # --- старый пароль ОБЯЗАТЕЛЬНЫЙ ---
    if not old_pass:
        return render_template("lab5/profile.html",
                               error="Введите старый пароль",
                               real_name=new_name)

    # достаём текущий хэш
    if current_app.config['DB_TYPE'] == 'postgres':
        cur.execute("SELECT password FROM users WHERE login=%s;", (login,))
    else:
        cur.execute("SELECT password FROM users WHERE login=?;", (login,))
    row = cur.fetchone()
    current_hash = row["password"]

    # проверяем старый пароль
    if not check_password_hash(current_hash, old_pass):
        db_close(conn, cur)
        return render_template("lab5/profile.html",
                               error="Старый пароль неверный",
                               real_name=new_name)

    # --- обновление профиля ---
    if new_pass:
        new_hash = generate_password_hash(new_pass)
        query = "UPDATE users SET real_name=%s, password=%s WHERE login=%s;"
        params = (new_name, new_hash, login)
    else:
        query = "UPDATE users SET real_name=%s WHERE login=%s;"
        params = (new_name, login)

    if current_app.config['DB_TYPE'] == 'postgres':
        cur.execute(query, params)
    else:
        cur.execute(query.replace("%s", "?"), params)

    db_close(conn, cur)

    return render_template("lab5/profile.html",
                           success="Данные обновлены",
                           real_name=new_name)




@lab5.route('/lab5/public')
def public_articles():
    conn, cur = db_connect()

    if current_app.config['DB_TYPE'] == 'postgres':
        cur.execute("SELECT * FROM articles WHERE is_public=true ORDER BY id DESC;")
    else:
        cur.execute("SELECT * FROM articles WHERE is_public=1 ORDER BY id DESC;")

    articles = cur.fetchall()
    db_close(conn, cur)

    return render_template('lab5/public.html', articles=articles)

