from flask import Blueprint, render_template, request, session, redirect, current_app
import psycopg2
from psycopg2.extras import RealDictCursor
from werkzeug.security import check_password_hash, generate_password_hash
import sqlite3
from os import path
import os
from dotenv import load_dotenv
load_dotenv()

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

    # Добавляем нового пользователя
    password_hash = generate_password_hash(password)
    if current_app.config['DB_TYPE'] == 'postgres':
        cur.execute(
            "INSERT INTO users (login, password) VALUES (%s, %s);",
            (login, password_hash)
        )
    else:
        cur.execute(
            "INSERT INTO users (login, password) VALUES (?, ?);",
            (login, password_hash)
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
        return render_template('lab5/create_article.html')

    title = request.form.get('title')
    article_text = request.form.get('article_text')

    conn, cur = db_connect()

    if current_app.config['DB_TYPE'] == 'postgres':
        cur.execute("SELECT * FROM users WHERE login=%s;", (login,))
    else:
        cur.execute("SELECT * FROM users WHERE login=?;", (login,))

    login_id = cur.fetchone()["id"]

    if current_app.config['DB_TYPE'] == 'postgres':
        cur.execute(
            "INSERT INTO articles (login_id, title, article_text) VALUES (%s, %s, %s);",
            (login_id, title, article_text)
        )
    else:
        cur.execute(
            "INSERT INTO articles (login_id, title, article_text) VALUES (?, ?, ?);",
            (login_id, title, article_text)
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
        cur.execute("SELECT * FROM articles WHERE login_id=%s;", (login_id,))
    else:
        cur.execute("SELECT * FROM articles WHERE login_id=?;", (login_id,))

    articles = cur.fetchall()

    db_close(conn, cur)

    return render_template('lab5/articles.html', articles=articles)

