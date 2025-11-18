from flask import Blueprint, render_template, request, session
import psycopg2
from psycopg2.extras import RealDictCursor

lab5 = Blueprint('lab5', __name__)



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

    conn = psycopg2.connect(
        host='127.0.0.1',
        database='kirill_chinkevich_knowledge_base',
        user='kirill_chinkevich_knowledge_base',
        password='1'
    )
    cur = conn.cursor()

    # Проверяем существование логина
    cur.execute(f"SELECT login FROM users WHERE login='{login}';")

    if cur.fetchone():
        cur.close()
        conn.close()
        return render_template('lab5/register.html',
                               error='Такой пользователь уже существует')

    # Добавляем нового пользователя
    cur.execute(
        f"INSERT INTO users (login, password) VALUES ('{login}', '{password}');"
    )
    conn.commit()  
    cur.close()
    conn.close()

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

    # Подключение к базе (как в разделе 5)
    conn = psycopg2.connect(
        host='127.0.0.1',
        database='kirill_chinkevich_knowledge_base',
        user='kirill_chinkevich_knowledge_base',
        password='1'
    )
    cur = conn.cursor(cursor_factory = RealDictCursor)

    # Ищем пользователя
    cur.execute(f"SELECT * FROM users WHERE login='{login}';")
    user = cur.fetchone()

    # Логин не найден
    if not user:
        cur.close()
        conn.close()
        return render_template('lab5/login.html',
                               error="Логин и/или пароль неверны")

    # Проверка пароля
    if user['password'] != password:  
        cur.close()
        conn.close()
        return render_template('lab5/login.html',
                               error="Логин и/или пароль неверны")

    # Авторизация прошла
    session['login'] = login

    cur.close()
    conn.close()
    return render_template('lab5/success_login.html', login=login)
