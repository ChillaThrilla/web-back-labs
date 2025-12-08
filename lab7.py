from flask import Blueprint, render_template, request, jsonify
import sqlite3
from datetime import datetime
import os

lab7 = Blueprint('lab7', __name__)

DB_PATH = "lab7.db"


# =====================================================
# 1. Автоматическое создание БД при запуске
# =====================================================
def init_db():
    if not os.path.exists(DB_PATH):

        conn = sqlite3.connect(DB_PATH)

        conn.execute("""
            CREATE TABLE films (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                title_ru TEXT NOT NULL,
                year INTEGER NOT NULL,
                description TEXT NOT NULL
            );
        """)

        # Начальные фильмы (как были в списке)
        initial_films = [
            ("Inception", "Начало", 2010,
             "Кобб — профессиональный вор, извлекающий секреты из подсознания во сне..."),

            ("Spirited Away", "Унесённые призраками", 2001,
             "Девочка Тихиро попадает в мир духов..."),

            ("The Dark Knight", "Тёмный рыцарь", 2008,
             "Бэтмен сталкивается с Джокером..."),

            ("Your Name", "Твоё имя", 2016,
             "Двое подростков начинают загадочно меняться телами..."),

            ("Whiplash", "Одержимость", 2014,
             "Молодой барабанщик мечтает стать великим музыкантом...")
        ]

        conn.executemany("""
            INSERT INTO films (title, title_ru, year, description)
            VALUES (?, ?, ?, ?)
        """, initial_films)

        conn.commit()
        conn.close()

        print("База данных создана и заполнена.")


# вызываем создание БД при запуске
init_db()


def get_db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn



# =====================================================
# 2. Валидация
# =====================================================
def validate_film(film):
    errors = {}

    title = (film.get('title') or '').strip()
    title_ru = (film.get('title_ru') or '').strip()
    description = (film.get('description') or '').strip()

    # Русское название — обязательно
    if not title_ru:
        errors['title_ru'] = 'Русское название не может быть пустым'

    # Оригинальное название — обязательно только если русское пустое
    if not title and not title_ru:
        errors['title'] = 'Оригинальное название должно быть заполнено, если русское пустое'

    # Проверка года
    current_year = datetime.now().year
    try:
        year = int(film.get('year', 0))
    except ValueError:
        year = 0

    if year < 1895 or year > current_year:
        errors['year'] = f'Год должен быть от 1895 до {current_year}'

    # Описание
    if not description:
        errors['description'] = 'Описание не может быть пустым'
    elif len(description) > 2000:
        errors['description'] = 'Описание не должно превышать 2000 символов'

    return errors



# =====================================================
# 3. Маршруты
# =====================================================

@lab7.route('/lab7/')
def lab():
    return render_template('lab7/lab7.html')


# ---- GET ALL ----
@lab7.route('/lab7/rest-api/films/', methods=['GET'])
def get_films():
    db = get_db()
    rows = db.execute("SELECT * FROM films").fetchall()
    films = [dict(row) for row in rows]
    return jsonify(films)


# ---- GET ONE ----
@lab7.route('/lab7/rest-api/films/<int:id>/', methods=['GET'])
def get_film(id):
    db = get_db()
    row = db.execute("SELECT * FROM films WHERE id = ?", (id,)).fetchone()

    if row is None:
        return '', 404

    return dict(row)


# ---- DELETE ----
@lab7.route('/lab7/rest-api/films/<int:id>/', methods=['DELETE'])
def delete_film(id):
    db = get_db()
    cur = db.execute("DELETE FROM films WHERE id = ?", (id,))
    db.commit()

    if cur.rowcount == 0:
        return '', 404

    return '', 204


# ---- PUT ----
@lab7.route('/lab7/rest-api/films/<int:id>/', methods=['PUT'])
def put_film(id):
    film = request.get_json()

    # автозаполнение оригинального названия
    if (film.get('title') or '') == '' and film.get('title_ru'):
        film['title'] = film['title_ru']

    errors = validate_film(film)
    if errors:
        return errors, 400

    db = get_db()
    cur = db.execute("""
        UPDATE films
        SET title = ?, title_ru = ?, year = ?, description = ?
        WHERE id = ?
    """, (film['title'], film['title_ru'], film['year'], film['description'], id))

    db.commit()

    if cur.rowcount == 0:
        return '', 404

    return film


# ---- POST ----
@lab7.route('/lab7/rest-api/films/', methods=['POST'])
def add_film():
    film = request.get_json()

    # автозаполнение оригинального названия
    if (film.get('title') or '') == '' and film.get('title_ru'):
        film['title'] = film['title_ru']

    errors = validate_film(film)
    if errors:
        return errors, 400

    db = get_db()
    cur = db.execute("""
        INSERT INTO films (title, title_ru, year, description)
        VALUES (?, ?, ?, ?)
    """, (film['title'], film['title_ru'], film['year'], film['description']))

    db.commit()

    return str(cur.lastrowid)