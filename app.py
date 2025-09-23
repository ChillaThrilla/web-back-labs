from flask import Flask, url_for, request, redirect
import datetime
app = Flask(__name__)

@app.errorhandler(404)
def not_found(err):
    return '''
<!doctype html>
<html>
    <head>
        <title>Страница не найдена</title>
        <style>
            body {
                font-family: Arial, sans-serif;
                text-align: center;
                padding: 50px;
                background-color: #f8f9fa;
            }
            h1 {
                color: #dc3545;
            }
            .container {
                max-width: 600px;
                margin: 0 auto;
                background: white;
                padding: 30px;
                border-radius: 10px;
                box-shadow: 0 2px 10px rgba(0,0,0,0.1);
            }
        </style>
    </head>
    <body>
        <div class="container">
            <h1>Ошибка 404 - Страница не найдена</h1>
            <p>Запрашиваемая страница не существует на сервере.</p>
            <p><a href="/">Вернуться на главную</a></p>
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
                <li><a href="/lab1">Первая лабораторная</a></li>
            </ul>
        </div>
        <footer>
            <p>Чинкевич Кирилл Алексеевич, ФБИ-32, Курс: 3, 2025 год</p>
        </footer>
    </body>
</html>
'''
@app.route("/lab1")
def lab1():
    return '''
<!doctype html>
<html>
    <head>
        <title>Лабораторная 1</title>
    </head>
    <body>
        <h1>Лабораторная работа 1</h1>
        <p>Flask — фреймворк для создания веб-приложений на языке программирования Python, использующий набор инструментов Werkzeug, а также шаблонизатор Jinja2. Относится к категории так называемых микрофреймворков — минималистичных каркасов веб-приложений, сознательно предоставляющих лишь самые базовые возможности.</p>
        <a href="/">На главную</a>
        
        <h2>Список роутов</h2>
        <ul>
            <li><a href="/lab1/web">Web</a></li>
            <li><a href="/lab1/author">Author</a></li>
            <li><a href="/lab1/image">Image</a></li>
            <li><a href="/lab1/counter">Counter</a></li>
            <li><a href="/lab1/info">Info</a></li>
        </ul>
    </body>
</html>
'''
@app.route("/lab1/web")
def web():
    return """<!doctype html>
        <html>
           <body>
               <h1>web-сервер на flask</h1>
                <a href="/lab1/author">author</a><br>
                <a href="/lab1">Назад к лабораторной</a>   
            </body>
        </html>"""

@app.route("/lab1/author")
def author():
    name = "Чинкевич Кирилл Алексеевич"
    group = "ФБИ-32"
    faculty = "ФБ"

    return """<!doctype html>
        <html>
           <body>
               <p>Студент: """ + name + """</p>
               <p>Группа: """ + group + """</p>
               <p>Факультет: """ + faculty + """</p>
               <a href= "/lab1/web">web</a><br>
               <a href="/lab1">Назад к лабораторной</a>
            </body>
        </html>"""

@app.route("/lab1/image")
def image():
    path = url_for("static", filename="oak.jpg")
    css = url_for("static", filename="lab1.css")
    
    html_content = f'''
<!doctype html>
<html>
    <head>
        <link rel="stylesheet" href="{css}">
    </head>
    <body>
        <div class="container">
            <h1>Дуб</h1>
            <img src="{path}">
            <p><a href="/lab1">Назад к лабораторной</a></p>
        </div>
    </body>
</html>
'''
    return html_content, 200, {
        'Content-Language': 'ru',
        'X-Custom-Header': 'MyValue',
        'X-Student-Name': 'Chinkevich-Kirill'
    }

count = 0

@app.route('/lab1/counter/clear')
def clear_counter():
    global count
    count = 0
    return redirect('/lab1/counter')

@app.route('/lab1/counter')
def counter():
    global count
    count += 1
    time = datetime.datetime.today()
    url = request.url
    client_ip = request.remote_addr

    return f'''
<!doctype html>
<html>
    <body>
        <h1>Счётчик посещений</h1>
        <p>Сколько раз вы сюда заходили: {count}</p>
        <p><a href="/lab1/counter/clear">Сбросить счётчик</a></p>
        <hr>
        <p>Дата и Время: {time}</p>
        <p>Запрошенный адрес: {url}</p>
        <p>Ваш IP-адрес: {client_ip}</p>
        <a href="/lab1">Назад к лабораторной</a>
    </body>
</html>
'''

@app.route('/lab1/info')
def info():
    return redirect("/lab1/author")

@app.route('/created')
def created():
    return '''
<!doctype html>
<html>
    <body>
            <h1>Создано успешно</h1>
            <div><i>что-то создано...</i></div>
    </body>
</html>
''', 201

@app.route('/bad_request')
def bad_request():
    return "Неверный запрос - сервер не может обработать запрос из-за клиентской ошибки", 400

@app.route('/unauthorized')
def unauthorized():
    return "Неавторизован - требуется аутентификация", 401

@app.route('/payment_required')
def payment_required():
    return "Требуется оплата", 402

@app.route('/forbidden')
def forbidden():
    return "Доступ запрещен", 403

@app.route('/method_not_allowed')
def method_not_allowed():
    return "Метод не разрешен", 405

@app.route('/teapot')
def teapot():
    return "Я чайник", 418

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

@app.route('/server_error')
def server_error():
    result = 1 / 0
    return "Эта строка никогда не выполнится"