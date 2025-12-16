from flask import Blueprint, render_template, request, jsonify, session, redirect
import sqlite3
import os
from werkzeug.security import generate_password_hash, check_password_hash
import re

RGZ = Blueprint('RGZ', __name__)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, 'rgz.db')

ADMIN_LOGIN = 'pharmacist'
ADMIN_PASSWORD = 'pharma123'  

LOGIN_PASSWORD_RE = re.compile(r'^[A-Za-z0-9!"#$%&\'()*+,\-./:;<=>?@[\\\]^_`{|}~]+$')

def get_db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    conn = get_db()
    cur = conn.cursor()

    cur.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            login TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL,
            is_admin INTEGER NOT NULL
        )
    """)

    cur.execute("""
        CREATE TABLE IF NOT EXISTS medicines (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            generic_name TEXT NOT NULL,
            prescription_only INTEGER NOT NULL,
            price REAL NOT NULL,
            quantity INTEGER NOT NULL
        )
    """)

    cur.execute("""
        CREATE TABLE IF NOT EXISTS favorites (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            medicine_id INTEGER NOT NULL,
            UNIQUE(user_id, medicine_id)
        )
    """)

    # администратор 
    cur.execute("SELECT * FROM users WHERE login = ?", (ADMIN_LOGIN,))
    if cur.fetchone() is None:
        cur.execute(
            "INSERT INTO users (login, password, is_admin) VALUES (?, ?, 1)",
            (ADMIN_LOGIN, generate_password_hash(ADMIN_PASSWORD))
        )


    conn.commit()
    conn.close()


init_db()



@RGZ.route('/RGZ/')
def main():
    return render_template('RGZ/RGZ.html')



@RGZ.route('/RGZ/register/', methods=['GET', 'POST'])
def register():
    if request.method == 'GET':
        return render_template('RGZ/RGZ_register.html')

    login = request.form.get('login')
    password = request.form.get('password')

    ok, msg = validate_login_password(login)
    if not ok:
        return render_template(
            'RGZ/RGZ_register.html',
            error=msg
        )

    ok, msg = validate_login_password(password)
    if not ok:
        return render_template(
            'RGZ/RGZ_register.html',
            error=msg
        )

    conn = get_db()
    cur = conn.cursor()

    try:
        cur.execute(
            "INSERT INTO users (login, password, is_admin) VALUES (?, ?, 0)",
            (login, generate_password_hash(password))
        )
        conn.commit()
    except sqlite3.IntegrityError:
        conn.close()
        return render_template(
            'RGZ/RGZ_register.html',
            error='Пользователь с таким логином уже существует'
        )

    conn.close()
    return redirect('/RGZ/login/')



@RGZ.route('/RGZ/login/', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('RGZ/RGZ_login.html')

    login_form = request.form.get('login')
    password_form = request.form.get('password')

    ok, msg = validate_login_password(login_form)
    if not ok:
        return render_template(
            'RGZ/RGZ_login.html',
            error=msg
        )

    ok, msg = validate_login_password(password_form)
    if not ok:
        return render_template(
            'RGZ/RGZ_login.html',
            error=msg
        )

    conn = get_db()
    cur = conn.cursor()
    cur.execute("SELECT * FROM users WHERE login = ?", (login_form,))
    user = cur.fetchone()
    conn.close()

    if user and check_password_hash(user['password'], password_form):
        session['login'] = user['login']
        session['is_admin'] = user['is_admin']
        return redirect('/RGZ/')

    return render_template(
        'RGZ/RGZ_login.html',
        error='Неверный логин или пароль'
    )



@RGZ.route('/RGZ/api/delete_account', methods=['POST'])
def delete_account():
    if not session.get('login'):
        return '', 401

    conn = get_db()
    cur = conn.cursor()

    cur.execute(
        "SELECT id FROM users WHERE login = ?",
        (session['login'],)
    )
    user_id = cur.fetchone()['id']

    cur.execute("DELETE FROM favorites WHERE user_id = ?", (user_id,))
    cur.execute("DELETE FROM users WHERE id = ?", (user_id,))

    conn.commit()
    conn.close()

    session.clear()
    return '', 204



@RGZ.route('/RGZ/logout/')
def logout():
    session.clear()
    return redirect('/RGZ/')



@RGZ.route('/RGZ/admin/')
def admin():
    if not session.get('is_admin'):
        return redirect('/RGZ/login/')
    return render_template('RGZ/RGZ_admin.html')



@RGZ.route('/RGZ/api/medicines')
def get_medicines():
    name = request.args.get('name', '')
    prescription = request.args.get('prescription_only')
    offset = int(request.args.get('offset', 0))

    conn = get_db()
    cur = conn.cursor()

    query = "SELECT * FROM medicines WHERE 1=1"
    params = []

    if name:
        query += " AND name LIKE ?"
        params.append(f'%{name}%')

    if prescription in ['0', '1']:
        query += " AND prescription_only = ?"
        params.append(int(prescription))

    query += " LIMIT 10 OFFSET ?"
    params.append(offset)

    cur.execute(query, params)
    rows = cur.fetchall()
    conn.close()

    result = []
    for r in rows:
        result.append({
            'id': r['id'],
            'name': r['name'],
            'generic_name': r['generic_name'],
            'prescription_only': bool(r['prescription_only']),
            'price': r['price'],
            'quantity': 'отсутствует' if r['quantity'] == 0 else r['quantity']
        })

    return jsonify(result)



@RGZ.route('/RGZ/api/medicines/<int:id>', methods=['GET'])
def get_medicine_by_id(id):
    conn = get_db()
    cur = conn.cursor()
    cur.execute("SELECT * FROM medicines WHERE id = ?", (id,))
    r = cur.fetchone()
    conn.close()

    if r is None:
        return jsonify({'error': 'Препарат не найден'}), 404

    return jsonify({
        'id': r['id'],
        'name': r['name'],
        'generic_name': r['generic_name'],
        'prescription_only': bool(r['prescription_only']),
        'price': r['price'],
        'quantity': r['quantity']
    })



@RGZ.route('/RGZ/api/medicines', methods=['POST'])
def add_medicine():
    if not session.get('is_admin'):
        return '', 403

    data = request.get_json()

    ok, msg = validate_medicine(data)
    if not ok:
        return jsonify({'error': msg}), 400

    conn = get_db()
    cur = conn.cursor()
    cur.execute("""
        INSERT INTO medicines (name, generic_name, prescription_only, price, quantity)
        VALUES (?, ?, ?, ?, ?)
    """, (
        data['name'],
        data['generic_name'],
        int(data['prescription_only']),
        float(data['price']),
        int(data['quantity'])
    ))
    conn.commit()
    conn.close()

    return '', 201



@RGZ.route('/RGZ/api/medicines/<int:id>', methods=['PUT'])
def update_medicine(id):
    if not session.get('is_admin'):
        return '', 403

    data = request.get_json()

    ok, msg = validate_medicine(data)
    if not ok:
        return jsonify({'error': msg}), 400

    conn = get_db()
    cur = conn.cursor()

    cur.execute("""
        UPDATE medicines
        SET name = ?,
            generic_name = ?,
            prescription_only = ?,
            price = ?,
            quantity = ?
        WHERE id = ?
    """, (
        data['name'],
        data['generic_name'],
        int(data['prescription_only']),
        float(data['price']),
        int(data['quantity']),
        id
    ))

    conn.commit()
    conn.close()

    return '', 204



@RGZ.route('/RGZ/api/medicines/<int:id>', methods=['DELETE'])
def delete_medicine(id):
    if not session.get('is_admin'):
        return '', 403

    conn = get_db()
    cur = conn.cursor()
    cur.execute("DELETE FROM medicines WHERE id = ?", (id,))
    conn.commit()
    conn.close()

    return '', 204



@RGZ.route('/RGZ/api/favorites/<int:medicine_id>', methods=['POST'])
def toggle_favorite(medicine_id):
    if not session.get('login'):
        return '', 401

    conn = get_db()
    cur = conn.cursor()

    cur.execute(
        "SELECT id FROM users WHERE login = ?",
        (session['login'],)
    )
    user_id = cur.fetchone()['id']

    cur.execute("""
        SELECT id FROM favorites
        WHERE user_id = ? AND medicine_id = ?
    """, (user_id, medicine_id))

    exists = cur.fetchone()

    if exists:
        cur.execute(
            "DELETE FROM favorites WHERE user_id = ? AND medicine_id = ?",
            (user_id, medicine_id)
        )
        action = 'removed'
    else:
        cur.execute(
            "INSERT INTO favorites (user_id, medicine_id) VALUES (?, ?)",
            (user_id, medicine_id)
        )
        action = 'added'

    conn.commit()
    conn.close()

    return jsonify({'status': action})



@RGZ.route('/RGZ/api/favorites')
def get_favorites():
    if not session.get('login'):
        return '', 401

    conn = get_db()
    cur = conn.cursor()

    cur.execute(
        "SELECT id FROM users WHERE login = ?",
        (session['login'],)
    )
    user_id = cur.fetchone()['id']

    cur.execute("""
        SELECT m.*
        FROM medicines m
        JOIN favorites f ON m.id = f.medicine_id
        WHERE f.user_id = ?
    """, (user_id,))

    rows = cur.fetchall()
    conn.close()

    return jsonify([dict(r) for r in rows])



def validate_login_password(value):
    if not value:
        return False, "Поле не должно быть пустым"
    if not LOGIN_PASSWORD_RE.match(value):
        return False, "Допустимы только латинские буквы, цифры и знаки препинания"
    return True, ""



def validate_medicine(data):
    if not data.get('name'):
        return False, "Название не должно быть пустым"

    if not data.get('generic_name'):
        return False, "Непатентованное название не должно быть пустым"

    if str(data.get('prescription_only')) not in ['0', '1']:
        return False, "Некорректное значение поля 'по рецепту'"

    try:
        price = float(data.get('price'))
        if price <= 0:
            return False, "Цена должна быть больше нуля"
    except:
        return False, "Цена должна быть числом"

    try:
        quantity = int(data.get('quantity'))
        if quantity < 0:
            return False, "Количество не может быть отрицательным"
    except:
        return False, "Количество должно быть целым числом"

    return True, ""
