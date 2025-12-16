from flask import Blueprint, render_template, request, jsonify, session
import sqlite3
import random

lab9 = Blueprint('lab9', __name__)
DB_NAME = 'lab9.db'

BOX_SIZE = 140
FIELD_WIDTH = 1000
FIELD_HEIGHT = 500


def get_db():
    return sqlite3.connect(DB_NAME)


def init_db():
    conn = get_db()
    cur = conn.cursor()

    cur.execute("""
        CREATE TABLE IF NOT EXISTS gifts (
            id INTEGER PRIMARY KEY,
            message TEXT NOT NULL,
            opened INTEGER NOT NULL DEFAULT 0
        )
    """)

    cur.execute("SELECT COUNT(*) FROM gifts")
    if cur.fetchone()[0] == 0:
        messages = [
            "🎄 Счастья в новом году!",
            "🎁 Удачи и радости!",
            "❄️ Крепкого здоровья!",
            "✨ Исполнения желаний!",
            "🎉 Весёлых праздников!",
            "🍾 Успехов во всём!",
            "💫 Вдохновения!",
            "🎊 Радости каждый день!",
            "🎅 Отличного настроения!",
            "⭐ Новых побед!"
        ]
        random.shuffle(messages)

        for i in range(1, 11):
            cur.execute(
                "INSERT INTO gifts (id, message) VALUES (?, ?)",
                (i, messages[i - 1])
            )

    conn.commit()
    conn.close()


def intersects(a, b):
    return not (
        a['x'] + BOX_SIZE < b['x'] or
        a['x'] > b['x'] + BOX_SIZE or
        a['y'] + BOX_SIZE < b['y'] or
        a['y'] > b['y'] + BOX_SIZE
    )


def generate_positions(count):
    positions = []

    for _ in range(count):
        for _ in range(100):
            pos = {
                'x': random.randint(0, FIELD_WIDTH - BOX_SIZE),
                'y': random.randint(0, FIELD_HEIGHT - BOX_SIZE)
            }
            if all(not intersects(pos, p) for p in positions):
                positions.append(pos)
                break

    return {
        i + 1: {'left': positions[i]['x'], 'top': positions[i]['y']}
        for i in range(len(positions))
    }


BOX_POSITIONS = generate_positions(10)
init_db()


@lab9.route('/lab9/')
def main():
    session.setdefault('opened_count', 0)

    conn = get_db()
    cur = conn.cursor()

    cur.execute("SELECT id FROM gifts WHERE opened = 1")
    opened_ids = {row[0] for row in cur.fetchall()}

    cur.execute("SELECT COUNT(*) FROM gifts WHERE opened = 0")
    unopened = cur.fetchone()[0]

    conn.close()

    return render_template(
        'lab9/lab9.html',
        positions=BOX_POSITIONS,
        opened_ids=opened_ids,
        unopened=unopened
    )


@lab9.route('/lab9/open', methods=['POST'])
def open_gift():
    if session.get('opened_count', 0) >= 3:
        return jsonify({"error": "Можно открыть не более 3 коробок"})

    box_id = int(request.json['box_id'])

    conn = get_db()
    cur = conn.cursor()
    cur.execute("SELECT opened, message FROM gifts WHERE id = ?", (box_id,))
    row = cur.fetchone()

    if not row or row[0] == 1:
        conn.close()
        return jsonify({"error": "Этот подарок уже открыт"})

    cur.execute("UPDATE gifts SET opened = 1 WHERE id = ?", (box_id,))
    conn.commit()
    conn.close()

    session['opened_count'] += 1
    return jsonify({"message": row[1]})
