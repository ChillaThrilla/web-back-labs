from flask import Blueprint, render_template, request, redirect, session
import sqlite3
import os

lab6 = Blueprint('lab6', __name__)

# === ПУТЬ К БАЗЕ ДАННЫХ ===
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, 'lab6.db')


# === ФУНКЦИЯ ПОДКЛЮЧЕНИЯ К БАЗЕ ===
def get_db():
    return sqlite3.connect(DB_PATH)


# === АВТОСОЗДАНИЕ БАЗЫ И ТАБЛИЦЫ ===
def init_db():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS offices (
        number INTEGER PRIMARY KEY,
        tenant TEXT,
        price INTEGER
    )
    """)

    cursor.execute("SELECT COUNT(*) FROM offices")
    count = cursor.fetchone()[0]

    if count == 0:
        for i in range(1, 11):
            price = 900 + i * 3
            cursor.execute(
                "INSERT INTO offices (number, tenant, price) VALUES (?, ?, ?)",
                (i, "", price)
            )
        print(">>> Таблица offices создана и заполнена начальными данными")

    conn.commit()
    conn.close()


# запускаем при загрузке файла
init_db()



@lab6.route('/lab6/')
def lab():
    return render_template('lab6/lab6.html')



@lab6.route('/lab6/json-rpc-api/', methods = ['POST'])
def api():
    data = request.json
    id = data['id']

    if data['method'] == 'info':
        conn = get_db()
        cursor = conn.cursor()

        cursor.execute("SELECT number, tenant, price FROM offices")
        rows = cursor.fetchall()
        conn.close()

        offices = []
        for r in rows:
            offices.append({
                "number": r[0],
                "tenant": r[1],
                "price": r[2]
            })

        return {
            'jsonrpc': '2.0',
            'result': {
                'offices': offices,
                'login': session.get('login')
            },
            'id': id
        }

    login = session.get('login')
    if not login:
        return {
            'jsonrpc': '2.0',
            'error': {
                'code': 1,
                'message': 'Unauthorized'
            },
            'id': id
        }
    
    if data['method'] == 'booking':
        office_number = data['params']

        conn = get_db()
        cursor = conn.cursor()

        cursor.execute("SELECT tenant FROM offices WHERE number = ?", (office_number,))
        tenant = cursor.fetchone()[0]

        if tenant != "":
            conn.close()
            return {
                'jsonrpc': '2.0',
                'error': {'code': 2, 'message': 'Already booked'},
                'id': id
            }

        cursor.execute("UPDATE offices SET tenant = ? WHERE number = ?", (login, office_number))
        conn.commit()
        conn.close()

        return {
            'jsonrpc': '2.0',
            'result': 'success',
            'id': id
        }

    if data['method'] == 'cancellation':
        office_number = data['params']

        conn = get_db()
        cursor = conn.cursor()

        cursor.execute("SELECT tenant FROM offices WHERE number = ?", (office_number,))
        tenant = cursor.fetchone()[0]

        if tenant == "":
            conn.close()
            return {
                'jsonrpc': '2.0',
                'error': {'code': 3, 'message': 'Not booked'},
                'id': id
            }

        if tenant != login:
            conn.close()
            return {
                'jsonrpc': '2.0',
                'error': {'code': 4, 'message': 'Not your booking'},
                'id': id
            }

        cursor.execute("UPDATE offices SET tenant = '' WHERE number = ?", (office_number,))
        conn.commit()
        conn.close()

        return {
            'jsonrpc': '2.0',
            'result': 'success',
            'id': id
        }


    return {
        'jsonrpc': '2.0',
        'error': {'code': -32601, 'message': 'Method not found'},
        'id': id
    }