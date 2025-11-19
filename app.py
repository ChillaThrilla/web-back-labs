from flask import Flask, url_for, request, redirect, abort, render_template
import os

from lab1 import lab1
from lab2 import lab2
from lab3 import lab3
from lab4 import lab4
from lab5 import lab5


import datetime
app = Flask(__name__)
app.register_blueprint(lab1)
app.register_blueprint(lab2)
app.register_blueprint(lab3)
app.register_blueprint(lab5)


app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'секретно-секретный секрет')
app.config['DB_TYPE'] = os.getenv('DB_TYPE', 'postgres')


# Добавляем глобальную переменную для хранения лога в начало файла (после импортов)
error_log_404 = []

@app.errorhandler(404)
def not_found(err):

    timestamp = datetime.datetime.now()
    ip_address = request.remote_addr
    requested_url = request.url
    
    log_entry = f"{timestamp}, пользователь {ip_address} зашёл на адрес: {requested_url}"
    error_log_404.append(log_entry)
    
    journal_html = "<h3>Полный журнал обращений к несуществующим страницам:</h3>"
    journal_html += "<div style='background: #f5f5f5; padding: 15px; border-radius: 5px; margin-top: 20px; font-family: monospace; font-size: 12px; max-height: 300px; overflow-y: auto;'>"
    
    if error_log_404:
        for entry in reversed(error_log_404):  
            journal_html += f"<div style='margin-bottom: 8px; padding: 5px; background: white; border-left: 3px solid #dc3545;'>"
            journal_html += f"<strong>{entry}</strong>"
            journal_html += "</div>"
    else:
        journal_html += "<p>Журнал пока пуст</p>"
    
    journal_html += "</div>"
    
    return f'''
<!doctype html>
<html>
    <head>
        <title>Страница не найдена</title>
        <style>
            body {{
                font-family: Arial, sans-serif;
                text-align: center;
                padding: 50px;
                background-color: #f8f9fa;
            }}
            h1 {{
                color: #dc3545;
            }}
            .container {{
                max-width: 800px;
                margin: 0 auto;
                background: white;
                padding: 30px;
                border-radius: 10px;
                box-shadow: 0 2px 10px rgba(0,0,0,0.1);
                text-align: left;
            }}
            .info-block {{
                background: #e9ecef;
                padding: 15px;
                border-radius: 5px;
                margin: 20px 0;
            }}
            .journal {{
                text-align: left;
                margin-top: 30px;
            }}
            .back-link {{
                display: inline-block;
                background: #007bff;
                color: white;
                padding: 10px 20px;
                text-decoration: none;
                border-radius: 5px;
                margin: 15px 0;
            }}
            .back-link:hover {{
                background: #0056b3;
            }}
        </style>
    </head>
    <body>
        <div class="container">
            <h1>Ошибка 404 - Страница не найдена</h1>
            
            <div class="info-block">
                <p><strong>Ваш IP-адрес:</strong> {ip_address}</p>
                <p><strong>Дата и время обращения:</strong> {timestamp}</p>
                <p><strong>Запрошенный адрес:</strong> {requested_url}</p>
            </div>
            
            <p>Запрашиваемая страница не существует на сервере.</p>
            
            <a href="/" class="back-link">Вернуться на главную</a>
            
            <div class="journal">
                {journal_html}
            </div>
        </div>
    </body>
</html>
''', 404

@app.route("/")
@app.route("/index")
def index():
    return '''
<!doctype html>
<html>
    <head>
        <title>HTTP, ФБ, Лабораторные работы</title>
    </head>
    <body>
        <h1>HTTP, ФБ, WEB-программирование, часть 2. Список лабораторных</h1>
        <div>
            <ul>
                <li><a href="/lab1">Лабораторная работа 1</a></li>
                <li><a href="/lab2">Лабораторная работа 2</a></li>
                <li><a href="/lab3">Лабораторная работа 3</a></li>
                <li><a href="/lab4">Лабораторная работа 4</a></li>
                <li><a href="/lab5">Лабораторная работа 5</a></li>

            </ul>
        </div>
        <footer>
            <p>Чинкевич Кирилл Алексеевич, ФБИ-32, Курс: 3, 2025 год</p>
        </footer>
    </body>
</html>
'''


@app.errorhandler(500)
def internal_error(err):
    return '''
<!doctype html>
<html>
    <head>
        <title>Ошибка сервера</title>
    </head>
    <body>
        <h1>Ошибка 500 - Внутренняя ошибка сервера</h1>
        <p>На сервере произошла непредвиденная ошибка.</p>
        <a href="/">Вернуться на главную</a>
    </body>
</html>
''', 500



