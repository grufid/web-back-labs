from flask import Blueprint, render_template, request, make_response, redirect

lab3 = Blueprint('lab3', __name__)

@lab3.route('/lab3/')
def lab():
    name = request.cookies.get('name')
    name_color = request.cookies.get('name_color')
    age = request.cookies.get('age')
    return render_template('lab3/lab3.html', name=name, name_color= name_color, age=age)

@lab3.route('/lab3/cookie')
def cookie():
    resp = make_response(redirect('/lab3/'))
    resp.set_cookie('name', 'Dayana', max_age=5)
    resp.set_cookie('age', '19')
    resp.set_cookie('name_color', '#2c3e50')
    return resp

@lab3.route('/lab3/del_cookie')
def del_cookie():
    resp = make_response(redirect('/lab3/'))
    resp.delete_cookie('name')
    resp.delete_cookie('age')
    resp.delete_cookie('name_color')
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
    return render_template('lab3/form1.html', user=user, age=age, sex=sex, errors=errors)


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

@lab3.route('/lab3/paid')
def success():
    price = request.args.get('price', 0)
    return render_template('lab3/paid.html', price=price)

@lab3.route('/lab3/settings')
def settings():
    color = request.args.get('color')
    bg_color = request.args.get('bg_color')
    font_size = request.args.get('font_size')
    text_transform = request.args.get('text_transform')

    if any([color, bg_color, font_size, text_transform]):
        resp = make_response(redirect('/lab3/settings'))
        if color:
            resp.set_cookie('color', color)
        if bg_color:
            resp.set_cookie('bg_color', bg_color)
        if font_size:
            resp.set_cookie('font_size', font_size)
        if text_transform:
            resp.set_cookie('text_transform', text_transform)
        return resp
    
    color = request.cookies.get('color', '#000000')
    bg_color = request.cookies.get('bg_color', '#ffffff')
    font_size = request.cookies.get('font_size', '16')
    text_transform = request.cookies.get('text_transform', 'none')
    
    resp = make_response(render_template('lab3/settings.html', color=color, bg_color=bg_color, font_size=font_size, text_transform=text_transform))
    return resp

@lab3.route('/lab3/ticket')
def ticket():
    if request.args:

        fio = request.args.get('fio', '').strip()
        shelf = request.args.get('shelf', '')
        bedding = request.args.get('bedding') == 'on'
        baggage = request.args.get('baggage') == 'on'
        age_str = request.args.get('age', '').strip()
        departure = request.args.get('departure', '').strip()
        destination = request.args.get('destination', '').strip()
        date = request.args.get('date', '')
        insurance = request.args.get('insurance') == 'on'

        errors = []
        if not fio:
            errors.append("ФИО пассажира обязательно")
        if not shelf:
            errors.append("Выберите полку")
        if not age_str:
            errors.append("Возраст обязателен")
        if not departure:
            errors.append("Пункт выезда обязателен")
        if not destination:
            errors.append("Пункт назначения обязателен")
        if not date:
            errors.append("Дата поездки обязательна")

        try:
            age = int(age_str)
            if age < 1 or age > 120:
                errors.append("Возраст должен быть от 1 до 120 лет")
        except ValueError:
            errors.append("Возраст должен быть числом")

        if errors:
            return render_template('lab3/ticket_form.html', 
                                 errors=errors,
                                 fio=fio, shelf=shelf, bedding=bedding, 
                                 baggage=baggage, age=age_str, 
                                 departure=departure, destination=destination, 
                                 date=date, insurance=insurance)

        base_price = 700 if age < 18 else 1000  
        shelf_price = 100 if shelf in ['нижняя', 'нижняя боковая'] else 0
        bedding_price = 75 if bedding else 0
        baggage_price = 250 if baggage else 0
        insurance_price = 150 if insurance else 0

        total_price = base_price + shelf_price + bedding_price + baggage_price + insurance_price

        ticket_data = {
            'fio': fio,
            'shelf': shelf,
            'bedding': 'Да' if bedding else 'Нет',
            'baggage': 'Да' if baggage else 'Нет',
            'age': age,
            'ticket_type': 'Детский билет' if age < 18 else 'Взрослый билет',
            'departure': departure,
            'destination': destination,
            'date': date,
            'insurance': 'Да' if insurance else 'Нет',
            'base_price': base_price,
            'shelf_price': shelf_price,
            'bedding_price': bedding_price,
            'baggage_price': baggage_price,
            'insurance_price': insurance_price,
            'total_price': total_price
        }

        return render_template('lab3/ticket_result.html', ticket=ticket_data)
    
    return render_template('lab3/ticket_form.html')


@lab3.route('/lab3/settings/clear')
def clear_settings():
    response = make_response(redirect('/lab3/settings'))
    
    cookies_to_clear = ['color', 'bg_color', 'font_size', 'text_transform']
    
    for cookie_name in cookies_to_clear:
        response.set_cookie(cookie_name, '', expires=0)
    
    return response
