from flask import Flask, url_for, request, redirect
import datetime
app = Flask(__name__)

@app.errorhandler(404)
def not_found(err):
    return "нет такой страницы", 404

@app.route("/")
@app.route("/web")
def web():
    return """<!doctype html>
        <html>
           <body>
               <h1>web-сервер на flask</h1>
                <a href= "/author">author</a>   
            </body>
        </html>""", 200, {
            'X-Server': 'sample',
            'Content-Type': 'text/plain; charset=utf-8'
            }

@app.route("/author")
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
               <a href= "/web">web</a>
            </body>
        </html>"""

@app.route("/image")
def image():
    path = url_for("static", filename="oak.jpg")
    css = url_for("static", filename="lab1.css")
    return f'''
<!doctype html>
<html>
    <head>
        <link rel="stylesheet" href="{css}">
    </head>
    <body>
        <h1>Дуб</h1>
        <img src="''' + path + '''">   
    </body>
</html>
'''

count = 0

@app.route('/counter/clear')
def clear_counter():
    global count
    count = 0
    return redirect('/counter')

@app.route('/counter')
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
        <p><a href="/counter/clear">Сбросить счётчик</a></p>
        <hr>
        <p>Дата и Время: {time}</p>
        <p>Запрошенный адрес: {url}</p>
        <p>Ваш IP-адрес: {client_ip}</p>
    </body>
</html>
'''

@app.route('/info')
def info():
    return redirect("/author")

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