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
    if x2 == '0':
        return render_template('lab4/div.html', error='На ноль делить нельзя' )
    x1 = int(x1)
    x2 = int(x2)
    result = x1 / x2
    return render_template('lab4/div.html', x1=x1, x2=x2, result=result)


@lab4.route('/lab4/sum-form')
def sum_form():
    return render_template('lab4/sum-form.html')


@lab4.route('/lab4/sum', methods = ['POST'])
def sum():
    x1 = request.form.get('x1')
    x2 = request.form.get('x2')
    if x1 == '':
        x1 = 0
    else:
        x1 = int(x1) 
    if x2 == '':
        x2 = 0
    else:
        x2 = int(x2)
    result = x1 + x2
    return render_template('lab4/sum.html', x1=x1, x2=x2, result=result)


@lab4.route('/lab4/mul-form')
def mul_form():
    return render_template('lab4/mul-form.html')

@lab4.route('/lab4/mul', methods = ['POST'])
def mul():
    x1 = request.form.get('x1')
    x2 = request.form.get('x2')
    if x1 == '':
        x1 = 1
    else:
        x1 = int(x1) 
    if x2 == '':
        x2 = 1
    else:
        x2 = int(x2)
    result = x1 * x2
    return render_template('lab4/mul.html', x1=x1, x2=x2, result=result)


@lab4.route('/lab4/sub-form')
def sub_form():
    return render_template('lab4/sub-form.html')

@lab4.route('/lab4/sub', methods = ['POST'])
def sub():
    x1 = request.form.get('x1')
    x2 = request.form.get('x2')
    if x1 == '' or x2 == '':
        return render_template('lab4/sub.html', error='Оба поля должны быть заполнены!')
    x1 = int(x1)
    x2 = int(x2)
    result = x1 - x2
    return render_template('lab4/sub.html', x1=x1, x2=x2, result=result)


@lab4.route('/lab4/exp-form')
def exp_form():
    return render_template('lab4/exp-form.html')


@lab4.route('/lab4/exp', methods = ['POST'])
def exp():
    x1 = request.form.get('x1')
    x2 = request.form.get('x2')
    if x1 == '' or x2 == '':
        return render_template('lab4/exp.html', error='Оба поля должны быть заполнены!')
    x1 = int(x1)
    x2 = int(x2)
    if x1 == 0 and x2 == 0 :
        return render_template('lab4/exp.html', error='Оба поля не могут быть равны 0!')
    result = x1 ** x2
    return render_template('lab4/exp.html', x1=x1, x2=x2, result=result)


tree_count=0

@lab4.route('/lab4/tree', methods = ['GET', 'POST'])
def tree():
    global tree_count
    if request.method == 'GET':
        return render_template('/lab4/tree.html', tree_count=tree_count)
    
    operation = request.form.get('operation')

    if operation == 'cut':
        if tree_count > 0:
            tree_count -=1
    elif operation == 'plant':
        if tree_count < 10:
            tree_count += 1

    return redirect('/lab4/tree')

users = [
    {'login': 'alex', 'password': '123', 'name': 'Алексей', 'gender': 'male'},
    {'login': 'bob', 'password': '555', 'name': 'Боб', 'gender': 'male'},
    {'login': 'dayana', 'password': '1312', 'name': 'Даяна', 'gender': 'female'},
    {'login': 'aliya', 'password': '2905', 'name': 'Алия', 'gender': 'female'},
    {'login': 'saliya', 'password': '2411', 'name': 'Салия', 'gender': 'female'}
]

@lab4.route('/lab4/register', methods=['GET', 'POST'])
def register():
    if request.method == 'GET':
        return render_template('lab4/register.html')
    
    login = request.form.get('login')
    password = request.form.get('password')
    password_confirm = request.form.get('password_confirm')
    name = request.form.get('name')
    gender = request.form.get('gender')
    
    errors = []
    
    if not login:
        errors.append('Не введён логин')
    if not password:
        errors.append('Не введён пароль')
    if not password_confirm:
        errors.append('Не введено подтверждение пароля')
    if not name:
        errors.append('Не введено имя')
    if password != password_confirm:
        errors.append('Пароли не совпадают')

    for user in users:
        if user['login'] == login:
            errors.append('Пользователь с таким логином уже существует')
            break
    
    if errors:
        return render_template('lab4/register.html', errors=errors, 
                             login=login, name=name, gender=gender)
    
    # Добавление нового пользователя
    new_user = {
        'login': login,
        'password': password,
        'name': name,
        'gender': gender
    }
    users.append(new_user)
    
    # Автоматический вход после регистрации
    session['login'] = login
    return redirect('/lab4/login')

@lab4.route('/lab4/users')
def users_list():
    if 'login' not in session:
        return redirect('/lab4/login')
    
    current_user_login = session['login']
    return render_template('lab4/users.html', users=users, current_user_login=current_user_login)

@lab4.route('/lab4/users/delete', methods=['POST'])
def delete_user():
    if 'login' not in session:
        return redirect('/lab4/login')
    
    current_user_login = session['login']
    
    # Удаляем пользователя
    global users
    users = [user for user in users if user['login'] != current_user_login]
    
    # Выход из системы
    session.pop('login', None)
    return redirect('/lab4/login')

@lab4.route('/lab4/users/edit', methods=['GET', 'POST'])
def edit_user():
    if 'login' not in session:
        return redirect('/lab4/login')
    
    current_user_login = session['login']
    current_user = None
    
    global users

    # Находим текущего пользователя
    for user in users:
        if user['login'] == current_user_login:
            current_user = user
            break
    
    if current_user is None:
        session.pop('login', None)
        return redirect('/lab4/login') 
    
    if request.method == 'GET':
        return render_template('lab4/edit_user.html', user=current_user)
    
    new_login = request.form.get('login')
    new_name = request.form.get('name')
    new_gender = request.form.get('gender')
    new_password = request.form.get('password')
    password_confirm = request.form.get('password_confirm')
    
    errors = []
    
    if not new_login:
        errors.append('Не введён логин')
    if not new_name:
        errors.append('Не введено имя')
    if new_password and new_password != password_confirm:
        errors.append('Пароли не совпадают')
    
    if new_login != current_user_login:
        for user in users:
            if user['login'] == new_login:
                errors.append('Пользователь с таким логином уже существует')
                break
    
    if errors:
        return render_template('lab4/edit_user.html', user=current_user, errors=errors)
    
    # Обновление данных пользователя
    current_user['login'] = new_login
    current_user['name'] = new_name
    current_user['gender'] = new_gender
    
    if new_password:
        current_user['password'] = new_password
    
    # Обновление сессии если изменился логин
    if new_login != current_user_login:
        session['login'] = new_login
    
    return redirect('/lab4/users')



@lab4.route('/lab4/login', methods = ['GET','POST'])
def login():
    if request.method == 'GET':
        if 'login' in session:
            authorized = True
            name = session['login']  
            gender = ''
            for user in users:
                if user['login'] == session['login']:
                    name = user['name']
                    gender = user['gender']
                    break
        else:
            authorized = False
            name = ''
            gender = ''
        return render_template("lab4/login.html", authorized=authorized, name=name, gender=gender)

    login = request.form.get('login')
    password = request.form.get('password')


    if not login:
        error = 'Не введён логин'
        return render_template('/lab4/login.html', error=error, authorized=False, login=login)

    if not password:
        error = 'Не введён пароль'
        return render_template('/lab4/login.html', error=error, authorized=False, login=login)



    for user in users:
        if login == user['login'] and password == user['password']:
            session['login'] = login
            return redirect('/lab4/login')

    error = 'Неверные логин и/или пароль'
    return render_template('/lab4/login.html', error=error, authorized=False, login=login)

@lab4.route('/lab4/logout', methods = ['POST'])
def logout():
    session.pop('login', None)
    session.pop('name', None)
    return redirect('/lab4/login')



@lab4.route('/lab4/fridge')
def fridge_form():
    return render_template('lab4/fridge.html')

@lab4.route('/lab4/fridge', methods=['POST'])
def fridge():
    temperature = request.form.get('temperature')
    
    if not temperature:
        return render_template('lab4/fridge.html', error='Ошибка: не задана температура')
    
    try:
        temp = int(temperature)
    except ValueError:
        return render_template('lab4/fridge.html', error='Ошибка: введите целое число')
    
    if temp < -12:
        return render_template('lab4/fridge.html', error='Не удалось установить температуру — слишком низкое значение')
    elif temp > -1:
        return render_template('lab4/fridge.html', error='Не удалось установить температуру — слишком высокое значение')
    elif -12 <= temp <= -9:
        snowflakes = '❄️❄️❄️'
        message = f'Установлена температура: {temp}°C'
    elif -8 <= temp <= -5:
        snowflakes = '❄️❄️'
        message = f'Установлена температура: {temp}°C'
    elif -4 <= temp <= -1:
        snowflakes = '❄️'
        message = f'Установлена температура: {temp}°C'
    else:
        snowflakes = ''
        message = f'Установлена температура: {temp}°C'
    
    return render_template('lab4/fridge.html', message=message, snowflakes=snowflakes, temperature=temp)

@lab4.route('/lab4/grain')
def grain_form():
    return render_template('lab4/grain.html')

@lab4.route('/lab4/grain', methods=['POST'])
def grain():
    grain_type = request.form.get('grain_type')
    weight = request.form.get('weight')
    
    prices = {
        'barley': 12000,    
        'oats': 8500,      
        'wheat': 9000,     
        'rye': 15000       
    }
    
    grain_names = {
        'barley': 'ячмень',
        'oats': 'овёс', 
        'wheat': 'пшеница',
        'rye': 'рожь'
    }
    
    if not weight:
        return render_template('lab4/grain.html', error='Ошибка: не указан вес')
    
    try:
        weight_float = float(weight)
    except ValueError:
        return render_template('lab4/grain.html', error='Ошибка: введите корректное число для веса')
    
    if weight_float <= 0:
        return render_template('lab4/grain.html', error='Ошибка: вес должен быть больше 0')
    
    if weight_float > 100:
        return render_template('lab4/grain.html', error='Извините, такого объёма сейчас нет в наличии')
    
    if not grain_type or grain_type not in prices:
        return render_template('lab4/grain.html', error='Ошибка: выберите тип зерна')
    
    # Расчет стоимости
    price_per_ton = prices[grain_type]
    total_cost = weight_float * price_per_ton
    
    discount = 0
    if weight_float > 10:
        discount = total_cost * 0.10
        total_cost -= discount
    
    grain_name = grain_names[grain_type]
    
    return render_template('lab4/grain.html', success=True, grain_name=grain_name, weight=weight_float, total_cost=total_cost, discount=discount, has_discount=weight_float > 10)
