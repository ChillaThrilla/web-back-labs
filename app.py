from flask import Flask, url_for, request, redirect, abort, render_template
from lab1 import lab1
import datetime
app = Flask(__name__)
app.register_blueprint(lab1)

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
            </ul>
        </div>
        <footer>
            <p>Чинкевич Кирилл Алексеевич, ФБИ-32, Курс: 3, 2025 год</p>
        </footer>
    </body>
</html>
'''


@app.route('/400')
def bad_request():
    return "Неверный запрос - сервер не может обработать запрос из-за клиентской ошибки", 400

@app.route('/401')
def unauthorized():
    return "Неавторизован - требуется аутентификация", 401

@app.route('/402')
def payment_required():
    return "Требуется оплата", 402

@app.route('/403')
def forbidden():
    return "Доступ запрещен", 403

@app.route('/405')
def method_not_allowed():
    return "Метод не разрешен", 405

@app.route('/418')
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

@app.route('/500')
def server_error():
    result = 1 / 0
    return "Эта строка никогда не выполнится"

@app.route('/lab2/a')
def a():
    return "без слэша"

@app.route('/lab2/a/')
def a2():
    return "со слэшем"

flower_list = [
    {'name': 'роза', 'price': 150},
    {'name': 'тюльпан', 'price': 80},
    {'name': 'незабудка', 'price': 50},
    {'name': 'ромашка', 'price': 40}
]

flower_list = [
    {'name': 'роза', 'price': 150},
    {'name': 'тюльпан', 'price': 80},
    {'name': 'незабудка', 'price': 50},
    {'name': 'ромашка', 'price': 40}
]

@app.route('/lab2/flowers/')
def show_flowers():
    return render_template('flowers.html', flower_list=flower_list)

@app.route('/lab2/delete_flower/<int:flower_id>')
def delete_flower(flower_id):
    if flower_id < 0 or flower_id >= len(flower_list):
        abort(404)
    
    flower_list.pop(flower_id)
    return redirect(url_for('show_flowers'))

@app.route('/lab2/add_flower/<name>/<int:price>')
def add_flower(name, price):
    flower_list.append({'name': name, 'price': price})
    return redirect(url_for('show_flowers'))

@app.route('/lab2/add_flower/')
def add_flower_err():
    return "вы не задали имя цветка или цену", 400

@app.route('/lab2/clear_flowers/')
def clear_flowers():
    flower_list.clear()
    return redirect(url_for('show_flowers'))

@app.route('/lab2/flowers/<int:flower_id>')
def flowers(flower_id):
    if flower_id >= len(flower_list):
        abort(404)
    else:
        flower = flower_list[flower_id]
        return render_template('flower_detail.html', flower=flower, flower_id=flower_id)

@app.route('/lab2/add_flower_form')
def add_flower_input():
    name = request.args.get('name')
    price = request.args.get('price')
    if name and price:
        flower_list.append({'name': name, 'price': int(price)})
    return redirect('/lab2/flowers')

@app.route('/lab2/example')
def example():
    name = 'Кирилл Чинкевич'
    lab_num = '2'
    group = 'ФБИ-32'
    course = '3'
    fruits = [
        {'name': 'яблоки', 'price': 100},
        {'name': 'груши', 'price': 120},
        {'name': 'апельсины', 'price': 80},
        {'name': 'мандарины', 'price': 95},
        {'name': 'манго', 'price': 321}
    ]
    return render_template('example.html', name=name, lab_num=lab_num, group=group, course=course, fruits=fruits)

@app.route('/lab2/')
def lab():
    return render_template('lab2.html')

@app.route('/lab2/filters')
def filters():
    phrase = "О <b>сколько</b> <u>нам</u> <i>открытий</i> чудных..."
    return render_template('filter.html', phrase=phrase)

@app.route('/lab2/calc/')
def calc_default():
    return redirect(url_for('calc', a=1, b=1))

@app.route('/lab2/calc/<int:a>')
def calc_one(a):
    return redirect(url_for('calc', a=a, b=1))

@app.route('/lab2/calc/<int:a>/<int:b>')
def calc(a, b):
    return render_template('calc.html', a=a, b=b)

books = [
    {'title': 'Мастер и Маргарита', 'author': 'Булгаков', 'genre': 'Роман', 'pages': 480},
    {'title': 'Преступление и наказание', 'author': 'Достоевский', 'genre': 'Роман', 'pages': 672},
    {'title': 'Война и мир', 'author': 'Толстой', 'genre': 'Роман', 'pages': 1225},
    {'title': 'Отцы и дети', 'author': 'Тургенев', 'genre': 'Роман', 'pages': 320},
    {'title': 'Обломов', 'author': 'Гончаров', 'genre': 'Роман', 'pages': 560},
    {'title': 'Шинель', 'author': 'Гоголь', 'genre': 'Повесть', 'pages': 80},
    {'title': 'Белая гвардия', 'author': 'Булгаков', 'genre': 'Роман', 'pages': 450},
    {'title': 'Анна Каренина', 'author': 'Толстой', 'genre': 'Роман', 'pages': 864},
    {'title': 'Пиковая дама', 'author': 'Пушкин', 'genre': 'Повесть', 'pages': 64},
    {'title': 'Доктор Живаго', 'author': 'Пастернак', 'genre': 'Роман', 'pages': 592}
]

@app.route('/lab2/books/')
def show_books():
    return render_template('books.html', books=books)


animals_list = [
    {'name': 'Кошка', 'desc': 'Ласковое и умное домашнее животное', 'img': 'a1.jpg'},
    {'name': 'Собака', 'desc': 'Добрый и верный друг человека', 'img': 'a2.jpg'},
    {'name': 'Лев', 'desc': 'Царь зверей, живёт в саванне', 'img': 'a3.jpg'},
    {'name': 'Тигр', 'desc': 'Сильный и быстрый хищник', 'img': 'a4.jpg'},
    {'name': 'Панда', 'desc': 'Ест бамбук и живёт в Китае', 'img': 'a5.jpg'},
    {'name': 'Слон', 'desc': 'Самое большое сухопутное животное', 'img': 'a6.jpg'},
    {'name': 'Заяц', 'desc': 'Быстро бегает и любит морковку', 'img': 'a7.jpg'},
    {'name': 'Медведь', 'desc': 'Любит мёд и живёт в лесу', 'img': 'a8.jpg'},
    {'name': 'Ёж', 'desc': 'Носит на иголках листья и яблоки', 'img': 'a9.jpg'},
    {'name': 'Попугай', 'desc': 'Яркая птица, умеет говорить', 'img': 'a10.jpg'},
    {'name': 'Жираф', 'desc': 'Высокое животное с длинной шеей', 'img': 'a11.jpg'},
    {'name': 'Пингвин', 'desc': 'Птица, которая не летает, но плавает', 'img': 'a12.jpg'},
    {'name': 'Кенгуру', 'desc': 'Прыгает и носит детёныша в сумке', 'img': 'a13.jpg'},
    {'name': 'Лиса', 'desc': 'Хитрая и красивая хищница', 'img': 'a14.jpg'},
    {'name': 'Волк', 'desc': 'Серый хищник, живёт стаями', 'img': 'a15.jpg'},
    {'name': 'Обезьяна', 'desc': 'Очень умное и ловкое животное', 'img': 'a16.jpg'},
    {'name': 'Корова', 'desc': 'Домашнее животное, даёт молоко', 'img': 'a17.jpg'},
    {'name': 'Лошадь', 'desc': 'Сильная и быстрая, помогает человеку', 'img': 'a18.jpg'},
    {'name': 'Крокодил', 'desc': 'Опасный обитатель рек и болот', 'img': 'a19.jpg'},
    {'name': 'Петух', 'desc': 'Поёт по утрам и будит всех', 'img': 'a20.jpg'}
]

@app.route('/lab2/animals')
def animals():
    return render_template('animals.html', animals_list=animals_list)
