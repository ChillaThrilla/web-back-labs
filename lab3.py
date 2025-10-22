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


@lab3.route('/lab3/clear_settings')
def clear_settings():
    resp = make_response(redirect('/lab3/settings'))
    resp.delete_cookie('color')
    resp.delete_cookie('bg_color')
    resp.delete_cookie('font_size')
    resp.delete_cookie('text_align')
    return resp


@lab3.route('/lab3/cars')
def cars():
    cars_list = [
        {'name': 'Toyota Camry', 'price': 2800000, 'brand': 'Toyota', 'year': 2023, 'color': 'черный'},
        {'name': 'Hyundai Solaris', 'price': 1600000, 'brand': 'Hyundai', 'year': 2022, 'color': 'белый'},
        {'name': 'Kia Rio', 'price': 1500000, 'brand': 'Kia', 'year': 2021, 'color': 'серебристый'},
        {'name': 'Lada Vesta', 'price': 1400000, 'brand': 'Lada', 'year': 2023, 'color': 'синий'},
        {'name': 'Volkswagen Polo', 'price': 1800000, 'brand': 'Volkswagen', 'year': 2021, 'color': 'серый'},
        {'name': 'Skoda Octavia', 'price': 2600000, 'brand': 'Skoda', 'year': 2022, 'color': 'белый'},
        {'name': 'Mazda 6', 'price': 3200000, 'brand': 'Mazda', 'year': 2023, 'color': 'красный'},
        {'name': 'Nissan Qashqai', 'price': 3500000, 'brand': 'Nissan', 'year': 2023, 'color': 'синий'},
        {'name': 'Renault Duster', 'price': 2100000, 'brand': 'Renault', 'year': 2022, 'color': 'оранжевый'},
        {'name': 'Geely Coolray', 'price': 2200000, 'brand': 'Geely', 'year': 2023, 'color': 'красный'},
        {'name': 'Chery Tiggo 7 Pro', 'price': 2300000, 'brand': 'Chery', 'year': 2023, 'color': 'белый'},
        {'name': 'BMW 3 Series', 'price': 5200000, 'brand': 'BMW', 'year': 2022, 'color': 'черный'},
        {'name': 'Mercedes-Benz C-Class', 'price': 5600000, 'brand': 'Mercedes-Benz', 'year': 2023, 'color': 'серый'},
        {'name': 'Audi A4', 'price': 5000000, 'brand': 'Audi', 'year': 2022, 'color': 'белый'},
        {'name': 'Honda CR-V', 'price': 4100000, 'brand': 'Honda', 'year': 2023, 'color': 'черный'},
        {'name': 'Lexus RX', 'price': 7500000, 'brand': 'Lexus', 'year': 2023, 'color': 'серебристый'},
        {'name': 'Tesla Model 3', 'price': 6500000, 'brand': 'Tesla', 'year': 2023, 'color': 'белый'},
        {'name': 'Volvo XC60', 'price': 6300000, 'brand': 'Volvo', 'year': 2023, 'color': 'серый'},
        {'name': 'Haval Jolion', 'price': 2400000, 'brand': 'Haval', 'year': 2023, 'color': 'синий'},
        {'name': 'UAZ Patriot', 'price': 1900000, 'brand': 'UAZ', 'year': 2023, 'color': 'зеленый'}
    ]

    min_price = request.args.get('min_price')
    max_price = request.args.get('max_price')
    reset = request.args.get('reset')

    # Очистка фильтра
    if reset:
        resp = make_response(redirect('/lab3/cars'))
        resp.delete_cookie('min_price')
        resp.delete_cookie('max_price')
        return resp

    # Сохраняем фильтр в куки — только если пользователь нажал "Поиск"
    if ('search' in request.args) and (min_price or max_price):
        # если min и max перепутаны — меняем местами
        if min_price and max_price and int(min_price) > int(max_price):
            min_price, max_price = max_price, min_price

        resp = make_response(redirect('/lab3/cars'))
        if min_price:
            resp.set_cookie('min_price', min_price)
        if max_price:
            resp.set_cookie('max_price', max_price)
        return resp

    # Берём значения из кук, если не переданы в запросе
    if not min_price:
        min_price = request.cookies.get('min_price')
    if not max_price:
        max_price = request.cookies.get('max_price')

    # Проверяем и корректируем диапазон
    if min_price and max_price and int(min_price) > int(max_price):
        min_price, max_price = max_price, min_price

    # Фильтрация списка
    filtered = cars_list
    if min_price:
        filtered = [c for c in filtered if c['price'] >= int(min_price)]
    if max_price:
        filtered = [c for c in filtered if c['price'] <= int(max_price)]

    # Сообщение если пусто
    message = ''
    if not filtered:
        message = 'Автомобилей в этом диапазоне цен не найдено.'

    # Подсказки по ценам
    prices = [c['price'] for c in cars_list]
    min_all, max_all = min(prices), max(prices)

    return render_template(
        'lab3/cars.html',
        cars=filtered,
        count=len(filtered),
        min_price=min_price or '',
        max_price=max_price or '',
        message=message,
        min_all=min_all,
        max_all=max_all
    )

