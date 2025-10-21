from flask import Blueprint, url_for, redirect, request
import datetime
lab1 = Blueprint('lab1', __name__)

@lab1.route("/lab1")
def lab():
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
            <li><a href="/">Главная страница (/)</a></li>
            <li><a href="/index">Главная страница (/index)</a></li>    
            <li><a href="/lab1/web">Web</a></li>
            <li><a href="/lab1/author">Author</a></li>
            <li><a href="/lab1/image">Image</a></li>
            <li><a href="/lab1/counter">Counter</a></li>
            <li><a href="/lab1/info">Info</a></li>
            <li><a href="/created">Created</a></li>
            <li><a href="/400">Ошибка 400</a></li>
            <li><a href="/401">Ошибка 401</a></li>
            <li><a href="/402">Ошибка 402</a></li>
            <li><a href="/403">Ошибка 403</a></li>
            <li><a href="/405">Ошибка 405</a></li>
            <li><a href="/418">Ошибка 418</a></li>
            <li><a href="/500">Ошибка 500</a></li>
        </ul>
    </body>
</html>
'''


@lab1.route("/lab1/web")
def web():
    return """<!doctype html>
        <html>
           <body>
               <h1>web-сервер на flask</h1>
                <a href="/lab1/author">author</a><br>
                <a href="/lab1">Назад к лабораторной</a>   
            </body>
        </html>""", 200, {
            'X-Server': 'sample',
            'Content-Type': 'text/plain; charset=utf-8'
        }


@lab1.route("/lab1/author")
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


@lab1.route("/lab1/image")
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

@lab1.route('/lab1/counter/clear')
def clear_counter():
    global count
    count = 0
    return redirect('/lab1/counter')


@lab1.route('/lab1/counter')
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


@lab1.route('/lab1/info')
def info():
    return redirect("/lab1/author")

@lab1.route('/created')
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


@lab1.route('/400')
def bad_request():
    return "Неверный запрос - сервер не может обработать запрос из-за клиентской ошибки", 400


@lab1.route('/401')
def unauthorized():
    return "Неавторизован - требуется аутентификация", 401


@lab1.route('/402')
def payment_required():
    return "Требуется оплата", 402


@lab1.route('/403')
def forbidden():
    return "Доступ запрещен", 403


@lab1.route('/405')
def method_not_allowed():
    return "Метод не разрешен", 405


@lab1.route('/418')
def teapot():
    return "Я чайник", 418


@lab1.route('/500')
def server_error():
    result = 1 / 0
    return "Эта строка никогда не выполнится"