from flask import Blueprint, render_template, request, make_response, redirect
lab3 = Blueprint('lab3', __name__)


@lab3.route('/lab3/')
def lab():
    name = request.cookies.get('name')
    name_color = request.cookies.get('name_color')
    age = request.cookies.get('age')
    return render_template('lab3/lab3.html', name=name, name_color=name_color, age=age)

    return render_template(
        'lab3/lab3.html',
        name=name,
        age=age,
        name_color=name_color
    )

@lab3.route('/lab3/cookie')
def cookie():
    resp = make_response(redirect('/lab3/'))
    resp.set_cookie('name', 'Alex', max_age=5)
    resp.set_cookie('age', '20')
    resp.set_cookie('name_color', 'magenta')
    return resp



@lab3.route('/lab3/del_cookie')
def del_cookie():
    resp = make_response(redirect('/lab3/'))
    resp.set_cookie('name',)
    resp.set_cookie('age',)
    resp.set_cookie('name_color',)
    return resp


@lab3.route('/lab3/form1')
def form1():
    errors = {}
    user = request.args.get('user')
    if user == '':
        errors['user'] = 'Заполните поле!'

    age = request.args.get('age')
    if age == '':
        errors['age'] = 'Заполните поле!'
    sex = request.args.get('sex')
    return render_template('lab3/form1.html', user = user, age = age, sex = sex, errors = errors)


@lab3.route('/lab3/order')
def order():
    return render_template('lab3/order.html')

@lab3.route('/lab3/pay')
def pay():
    price = 0
    drink = request.args.get('drink')

    if drink == 'coffee':
        price = 120
    elif drink == 'black-tea':
        price = 80
    else:
        price = 70

    if request.args.get('milk') == 'on':
        price += 30
    if request.args.get('sugar') == 'on':
        price += 10

    return render_template('lab3/pay.html', price=price)


@lab3.route('/lab3/success')
def success():
    return render_template('lab3/success.html')


@lab3.route('/lab3/settings')
def settings():
    color = request.args.get('color')
    bg_color = request.args.get('bg_color')
    font_size = request.args.get('font_size')
    font_weight = request.args.get('font_weight')  

    if color or bg_color or font_size or font_weight:
        resp = make_response(redirect('/lab3/settings'))
        if color:
            resp.set_cookie('color', color)
        if bg_color:
            resp.set_cookie('bg_color', bg_color)
        if font_size:
            resp.set_cookie('font_size', font_size)
        if font_weight:
            resp.set_cookie('font_weight', font_weight)
        return resp

    color = request.cookies.get('color', '#000000')
    bg_color = request.cookies.get('bg_color', '#ffffff')
    font_size = request.cookies.get('font_size', '16')
    font_weight = request.cookies.get('font_weight', 'normal')

    resp = make_response(
        render_template(
            'lab3/settings.html',
            color=color,
            bg_color=bg_color,
            font_size=font_size,
            font_weight=font_weight
        )
    )
    return resp


@lab3.route('/lab3/ticket')
def ticket():
    return render_template('lab3/ticket.html')


@lab3.route('/lab3/ticket_result')
def ticket_result():
    fio = request.args.get('fio')
    berth = request.args.get('berth')
    linen = request.args.get('linen')
    baggage = request.args.get('baggage')
    age = request.args.get('age')
    from_city = request.args.get('from_city')
    to_city = request.args.get('to_city')
    date = request.args.get('date')
    insurance = request.args.get('insurance')

    errors = {}

    # --- Проверка полей ---
    if not fio:
        errors['fio'] = 'Введите ФИО пассажира!'
    if not berth:
        errors['berth'] = 'Выберите полку!'
    if not age:
        errors['age'] = 'Введите возраст!'
    elif not age.isdigit() or int(age) < 1 or int(age) > 120:
        errors['age'] = 'Возраст должен быть от 1 до 120 лет!'
    if not from_city:
        errors['from_city'] = 'Введите пункт выезда!'
    if not to_city:
        errors['to_city'] = 'Введите пункт назначения!'
    if not date:
        errors['date'] = 'Выберите дату поездки!'

    # Если ошибки есть — возвращаем обратно на форму
    if errors:
        return render_template(
            'lab3/ticket.html',
            errors=errors,
            fio=fio, berth=berth, linen=linen, baggage=baggage,
            age=age, from_city=from_city, to_city=to_city,
            date=date, insurance=insurance
        )

    # --- Расчёт цены ---
    age_int = int(age)
    if age_int < 18:
        ticket_type = 'Детский билет'
        price = 700
    else:
        ticket_type = 'Взрослый билет'
        price = 1000

    if berth in ['нижняя', 'нижняя боковая']:
        price += 100
    if linen == 'on':
        price += 75
    if baggage == 'on':
        price += 250
    if insurance == 'on':
        price += 150

    return render_template(
        'lab3/ticket_result.html',
        fio=fio, berth=berth, linen=linen, baggage=baggage,
        age=age, from_city=from_city, to_city=to_city,
        date=date, insurance=insurance, ticket_type=ticket_type,
        price=price
    )


