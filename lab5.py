from flask import Blueprint, render_template, request
import psycopg2

lab5 = Blueprint('lab5', __name__)



# Главная страница ЛР5
@lab5.route('/lab5/')
def lab():
    return render_template('lab5/lab5.html')



# Регистрация пользователя
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
