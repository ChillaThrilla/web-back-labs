from flask import Blueprint, url_for, redirect, request, render_template
import datetime
lab2 = Blueprint('lab2', __name__)


@lab2.route('/lab2/a')
def a():
    return "без слэша"


@lab2.route('/lab2/a/')
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


@lab2.route('/lab2/flowers/')
def show_flowers():
    return render_template('lab2/flowers.html', flower_list=flower_list)


@lab2.route('/lab2/delete_flower/<int:flower_id>')
def delete_flower(flower_id):
    if flower_id < 0 or flower_id >= len(flower_list):
        abort(404)
    
    flower_list.pop(flower_id)
    return redirect(url_for('lab2.show_flowers'))


@lab2.route('/lab2/add_flower/<name>/<int:price>')
def add_flower(name, price):
    flower_list.append({'name': name, 'price': price})
    return redirect(url_for('lab2.show_flowers'))


@lab2.route('/lab2/add_flower/')
def add_flower_err():
    return "вы не задали имя цветка или цену", 400


@lab2.route('/lab2/clear_flowers/')
def clear_flowers():
    flower_list.clear()
    return redirect(url_for('lab2.show_flowers'))


@lab2.route('/lab2/flowers/<int:flower_id>')
def flowers(flower_id):
    if flower_id >= len(flower_list):
        abort(404)
    else:
        flower = flower_list[flower_id]
        return render_template('lab2/flower_detail.html', flower=flower, flower_id=flower_id)


@lab2.route('/lab2/add_flower_form')
def add_flower_input():
    name = request.args.get('name')
    price = request.args.get('price')
    if name and price:
        flower_list.append({'name': name, 'price': int(price)})
    return redirect('/lab2/flowers')


@lab2.route('/lab2/example')
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
    return render_template('lab2/example.html', name=name, lab_num=lab_num, group=group, course=course, fruits=fruits)


@lab2.route('/lab2/')
def lab():
    return render_template('lab2/lab2.html')


@lab2.route('/lab2/filters')
def filters():
    phrase = "О <b>сколько</b> <u>нам</u> <i>открытий</i> чудных..."
    return render_template('lab2/filter.html', phrase=phrase)


@lab2.route('/lab2/calc/')
def calc_default():
    return redirect(url_for('lab2.calc', a=1, b=1))


@lab2.route('/lab2/calc/<int:a>')
def calc_one(a):
    return redirect(url_for('lab2.calc', a=a, b=1))


@lab2.route('/lab2/calc/<int:a>/<int:b>')
def calc(a, b):
    return render_template('lab2/calc.html', a=a, b=b)


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


@lab2.route('/lab2/books/')
def show_books():
    return render_template('lab2/books.html', books=books)


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


@lab2.route('/lab2/animals')
def animals():
    return render_template('lab2/animals.html', animals_list=animals_list)