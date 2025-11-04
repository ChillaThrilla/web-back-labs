from flask import Blueprint, render_template, request, redirect, session
lab4 = Blueprint('lab4', __name__)


@lab4.route('/lab4/')
def lab():
    return render_template('lab4/lab4.html')


@lab4.route('/lab4/div-form')
def div_form():
    return render_template('lab4/div-form.html')


@lab4.route('/lab4/div', methods = ['POST'])
def div():
    x1 = request.form.get('x1')
    x2 = request.form.get('x2')

    if x1 == '' or x2 == '':
        return render_template('lab4/div.html', error='Оба поля должны быть заполнены!')

    x1 = int(x1)
    x2 = int(x2)

    if x2 == 0:
        return render_template('lab4/div.html', error='На ноль делить нельзя!')

    result = x1 / x2
    return render_template('lab4/div.html', x1=x1, x2=x2, result=result)


@lab4.route('/lab4/sum-form')
def sum_form():
    return render_template('lab4/sum-form.html')


@lab4.route('/lab4/sum', methods=['POST'])
def sum():
    x1 = request.form.get('x1')
    x2 = request.form.get('x2')

    # Если пустое поле — считаем, что это 0
    x1 = int(x1) if x1 != '' else 0
    x2 = int(x2) if x2 != '' else 0

    result = x1 + x2
    return render_template('lab4/sum.html', x1=x1, x2=x2, result=result)


@lab4.route('/lab4/mult-form')
def mult_form():
    return render_template('lab4/mult-form.html')


@lab4.route('/lab4/mult', methods=['POST'])
def mult():
    x1 = request.form.get('x1')
    x2 = request.form.get('x2')

    # Если пустое поле — считаем, что это 1
    x1 = int(x1) if x1 != '' else 1
    x2 = int(x2) if x2 != '' else 1

    result = x1 * x2
    return render_template('lab4/mult.html', x1=x1, x2=x2, result=result)


@lab4.route('/lab4/sub-form')
def sub_form():
    return render_template('lab4/sub-form.html')


@lab4.route('/lab4/sub', methods=['POST'])
def sub():
    x1 = request.form.get('x1')
    x2 = request.form.get('x2')

    if x1 == '' or x2 == '':
        return render_template('lab4/sub.html', error='Оба поля должны быть заполнены!')

    x1 = int(x1)
    x2 = int(x2)

    result = x1 - x2
    return render_template('lab4/sub.html', x1=x1, x2=x2, result=result)


@lab4.route('/lab4/pow-form')
def pow_form():
    return render_template('lab4/pow-form.html')


@lab4.route('/lab4/pow', methods=['POST'])
def pow():
    x1 = request.form.get('x1')
    x2 = request.form.get('x2')

    if x1 == '' or x2 == '':
        return render_template('lab4/pow.html', error='Оба поля должны быть заполнены!')

    x1 = int(x1)
    x2 = int(x2)

    if x1 == 0 and x2 == 0:
        return render_template('lab4/pow.html', error='0⁰ не имеет смысла!')

    result = x1 ** x2
    return render_template('lab4/pow.html', x1=x1, x2=x2, result=result)


tree_count = 0

@lab4.route('/lab4/tree', methods=['GET', 'POST'])
def tree():
    global tree_count

    if request.method == 'GET':
        return render_template('lab4/tree.html', tree_count=tree_count)

    operation = request.form.get('operation')

    if operation == 'cut':
        if tree_count > 0:
            tree_count -= 1
            
    elif operation == 'plant':
        if tree_count < 10:
            tree_count += 1

    return redirect('/lab4/tree')


users = [
    {'login': 'alex', 'password': '123', 'name': 'Иван Иванов', 'gender': 'м'},
    {'login': 'bob', 'password': '555', 'name': 'Мария Смирнова', 'gender': 'ж'},
    {'login': 'kate', 'password': '777', 'name': 'Кейт Миллер', 'gender': 'ж'},
    {'login': 'steve', 'password': '999', 'name': 'Стив Джобс', 'gender': 'м'},
]


@lab4.route('/lab4/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        if 'login' in session:
            return render_template('lab4/login.html',
                                   authorized=True,
                                   name=session.get('name'))
        return render_template('lab4/login.html', authorized=False)

    login = request.form.get('login', '').strip()
    password = request.form.get('password', '').strip()

    if login == '':
        error = 'Не введён логин'
        return render_template('lab4/login.html', error=error, authorized=False, login='')
    if password == '':
        error = 'Не введён пароль'
        return render_template('lab4/login.html', error=error, authorized=False, login=login)

    for user in users:
        if login == user['login'] and password == user['password']:
            # Сохраняем и логин, и имя в сессию
            session['login'] = login
            session['name'] = user['name']
            return redirect('/lab4/login')

    error = 'Неверные логин и/или пароль'
    return render_template('lab4/login.html', error=error, authorized=False, login=login)


@lab4.route('/lab4/logout', methods=['POST'])
def logout():
    session.pop('login', None)
    return redirect('/lab4/login')


# --- Страница регистрации нового пользователя ---
@lab4.route('/lab4/register', methods=['GET', 'POST'])
def register():
    if request.method == 'GET':
        return render_template('lab4/register.html')

    login = request.form.get('login', '').strip()
    password = request.form.get('password', '').strip()
    confirm = request.form.get('confirm', '').strip()
    name = request.form.get('name', '').strip()

    # Проверки
    if login == '' or name == '':
        return render_template('lab4/register.html', error='Не заполнены обязательные поля (логин и имя).')
    if password == '' or confirm == '':
        return render_template('lab4/register.html', error='Введите и подтвердите пароль.')
    if password != confirm:
        return render_template('lab4/register.html', error='Пароли не совпадают.')
    if any(u['login'] == login for u in users):
        return render_template('lab4/register.html', error='Пользователь с таким логином уже существует.')

    # Добавляем нового пользователя
    users.append({'login': login, 'password': password, 'name': name, 'gender': '-'})

    return render_template('lab4/register.html', success=f'Пользователь {name} успешно зарегистрирован!')


# --- Страница со списком пользователей (только для авторизованных) ---
@lab4.route('/lab4/users')
def users_list():
    if 'login' not in session:
        return redirect('/lab4/login')
    return render_template('lab4/users.html', users=users, current=session['login'])


# --- Удаление себя из списка ---
@lab4.route('/lab4/delete', methods=['POST'])
def delete_self():
    if 'login' not in session:
        return redirect('/lab4/login')

    global users
    users = [u for u in users if u['login'] != session['login']]
    session.pop('login', None)
    return redirect('/lab4/login')


# --- Редактирование своих данных ---
@lab4.route('/lab4/edit', methods=['GET', 'POST'])
def edit_user():
    if 'login' not in session:
        return redirect('/lab4/login')

    current_user = next((u for u in users if u['login'] == session['login']), None)
    if not current_user:
        return redirect('/lab4/login')

    if request.method == 'GET':
        return render_template('lab4/edit.html', user=current_user)

    new_login = request.form.get('login', '').strip()
    new_name = request.form.get('name', '').strip()
    new_password = request.form.get('password', '').strip()
    confirm = request.form.get('confirm', '').strip()

    if new_login == '' or new_name == '':
        return render_template('lab4/edit.html', user=current_user, error='Логин и имя не могут быть пустыми.')

    # Проверка, что логин уникален (если изменили)
    if new_login != current_user['login'] and any(u['login'] == new_login for u in users):
        return render_template('lab4/edit.html', user=current_user, error='Такой логин уже существует.')

    # Проверка пароля
    if new_password != '' or confirm != '':
        if new_password != confirm:
            return render_template('lab4/edit.html', user=current_user, error='Пароли не совпадают.')
        current_user['password'] = new_password  # Меняем пароль
    # Если пароль пуст — оставляем старый

    # Обновляем логин и имя
    current_user['login'] = new_login
    current_user['name'] = new_name
    session['login'] = new_login

    return render_template('lab4/edit.html', user=current_user, success='Данные успешно изменены!')



@lab4.route('/lab4/fridge', methods=['GET', 'POST'])
def fridge():
    if request.method == 'GET':
        return render_template('lab4/fridge.html')
    
    temperature = request.form.get('temperature')
    
    if temperature == '':
        return render_template('lab4/fridge.html', error='Ошибка: не задана температура')
    
    temperature = int(temperature)
    
    if temperature < -12:
        return render_template('lab4/fridge.html', error='Не удалось установить температуру — слишком низкое значение')
    
    if temperature > -1:
        return render_template('lab4/fridge.html', error='Не удалось установить температуру — слишком высокое значение')
    
    if -12 <= temperature <= -9:
        snowflakes = 3
    elif -8 <= temperature <= -5:
        snowflakes = 2
    elif -4 <= temperature <= -1:
        snowflakes = 1
    else:
        snowflakes = 0
    
    return render_template('lab4/fridge.html', temperature=temperature, snowflakes=snowflakes, success=True)


@lab4.route('/lab4/grain', methods=['GET', 'POST'])
def grain():
    if request.method == 'GET':
        return render_template('lab4/grain.html')

    grain_type = request.form.get('grain')
    weight = request.form.get('weight', '').strip()

    # Проверка на пустое значение
    if weight == '':
        return render_template('lab4/grain.html', error='Ошибка: не указан вес')

    weight = float(weight)

    # Проверка диапазона веса
    if weight <= 0:
        return render_template('lab4/grain.html', error='Ошибка: вес должен быть больше нуля')
    if weight > 100:
        return render_template('lab4/grain.html', error='Такого объёма сейчас нет в наличии')

    # Цены на зерно (руб/т)
    prices = {
        'ячмень': 12000,
        'овёс': 8500,
        'пшеница': 9000,
        'рожь': 15000
    }

    if grain_type not in prices:
        return render_template('lab4/grain.html', error='Ошибка: не выбран вид зерна')

    price_per_ton = prices[grain_type]
    total = weight * price_per_ton
    discount = 0

    # Скидка 10% при заказе свыше 10 тонн
    if weight > 10:
        discount = total * 0.1
        total -= discount

    return render_template('lab4/grain.html',
                           grain_type=grain_type,
                           weight=weight,
                           total=total,
                           discount=discount,
                           success=True)
