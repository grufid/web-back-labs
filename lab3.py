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

cosmetics = [
    {'name': 'Тональный крем Perfect Match', 'price': 1200, 'brand': "L'Oreal", 'type': 'Лицо', 'volume': '30мл'},
    {'name': 'Тушь для ресниц Volume Boost', 'price': 890, 'brand': 'Maybelline', 'type': 'Глаза', 'volume': '10мл'},
    {'name': 'Помада Matte Revolution', 'price': 1500, 'brand': 'MAC', 'type': 'Губы', 'volume': '3г'},
    {'name': 'Увлажняющий крем Hydra Genius', 'price': 2300, 'brand': 'La Roche-Posay', 'type': 'Уход', 'volume': '50мл'},
    {'name': 'Тени для век Ultimate Palette', 'price': 750, 'brand': 'NYX', 'type': 'Глаза', 'volume': '5г'},
    {'name': 'Румяна Blush Paradise', 'price': 1100, 'brand': 'NARS', 'type': 'Лицо', 'volume': '4г'},
    {'name': 'Лак для ногтей Gel Couture', 'price': 450, 'brand': 'Essie', 'type': 'Ногти', 'volume': '13мл'},
    {'name': 'Пудра Lumiere Velvet', 'price': 1800, 'brand': 'Chanel', 'type': 'Лицо', 'volume': '15г'},
    {'name': 'Консилер High Coverage', 'price': 950, 'brand': 'Catrice', 'type': 'Лицо', 'volume': '5мл'},
    {'name': 'Хайлайтер Diamond Bomb', 'price': 1300, 'brand': 'Fenty Beauty', 'type': 'Лицо', 'volume': '8г'},
    {'name': 'BB крем All-in-One', 'price': 850, 'brand': 'Garnier', 'type': 'Лицо', 'volume': '40мл'},
    {'name': 'Подводка для глаз Liquid Liner', 'price': 680, 'brand': 'Maybelline', 'type': 'Глаза', 'volume': '2мл'},
    {'name': 'Бальзам для губ Lip Therapy', 'price': 350, 'brand': 'Nivea', 'type': 'Губы', 'volume': '4г'},
    {'name': 'Сыворотка Vitamin C', 'price': 3200, 'brand': 'The Ordinary', 'type': 'Уход', 'volume': '30мл'},
    {'name': 'Крем для рук Repair', 'price': 280, 'brand': 'Neutrogena', 'type': 'Уход', 'volume': '75мл'},
    {'name': 'Гель для бровей Brow Fix', 'price': 520, 'brand': 'Anastasia', 'type': 'Брови', 'volume': '8мл'},
    {'name': 'Спрей для лица Thermal', 'price': 950, 'brand': 'Avene', 'type': 'Уход', 'volume': '150мл'},
    {'name': 'Палетка контуринга', 'price': 1400, 'brand': 'Kylie Cosmetics', 'type': 'Лицо', 'volume': '12г'},
    {'name': 'Масло для снятия макияжа', 'price': 1100, 'brand': 'DHC', 'type': 'Уход', 'volume': '120мл'},
    {'name': 'Кисть для пудры', 'price': 1800, 'brand': 'Sigma', 'type': 'Аксессуар', 'volume': '-'},
    {'name': 'Праймер для век', 'price': 620, 'brand': 'Urban Decay', 'type': 'Глаза', 'volume': '10мл'},
    {'name': 'Блеск для губ Shine Loud', 'price': 780, 'brand': 'NYX', 'type': 'Губы', 'volume': '4мл'},
    {'name': 'Крем-хайлайтер', 'price': 1250, 'brand': 'Rare Beauty', 'type': 'Лицо', 'volume': '15мл'},
    {'name': 'Салфетки для снятия макияжа', 'price': 320, 'brand': 'Garnier', 'type': 'Уход', 'volume': '25шт'},
    {'name': 'Пудровые тени Mono', 'price': 480, 'brand': 'MAC', 'type': 'Глаза', 'volume': '1.5г'}
]

@lab3.route('/lab3/cosmetics')
def cosmetics_search():

    min_price = request.args.get('min_price', '')
    max_price = request.args.get('max_price', '')
    
    if not min_price:
        min_price = request.cookies.get('min_price', '')
    if not max_price:
        max_price = request.cookies.get('max_price', '')
    
    # Рассчитываем минимальную и максимальную цены из всех товаров
    all_prices = [product['price'] for product in cosmetics]
    global_min_price = min(all_prices)
    global_max_price = max(all_prices)
    
    # Фильтрация товаров
    filtered_products = cosmetics.copy()
    
    if min_price:
        try:
            min_price_int = int(min_price)
    
            if max_price and min_price_int > int(max_price):
                min_price, max_price = max_price, min_price
                min_price_int = int(min_price)
            filtered_products = [p for p in filtered_products if p['price'] >= min_price_int]
        except ValueError:
            min_price = ''
    
    if max_price:
        try:
            max_price_int = int(max_price)
            filtered_products = [p for p in filtered_products if p['price'] <= max_price_int]
        except ValueError:
            max_price = ''
    
    response = make_response(render_template('lab3/cosmetics.html',
        products=filtered_products,
        min_price=min_price,
        max_price=max_price,
        global_min_price=global_min_price,
        global_max_price=global_max_price,
        products_count=len(filtered_products),
        total_count=len(cosmetics)
    ))
    
    if min_price or max_price:
        if min_price:
            response.set_cookie('min_price', min_price, max_age=60*60*24*7)
        if max_price:
            response.set_cookie('max_price', max_price, max_age=60*60*24*7)
    
    return response

@lab3.route('/lab3/cosmetics/reset')
def reset_cosmetics():
    response = make_response(redirect('/lab3/cosmetics'))
    response.set_cookie('min_price', '', expires=0)
    response.set_cookie('max_price', '', expires=0)
    return response