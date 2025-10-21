from flask import Blueprint, url_for, request, redirect, abort, render_template

lab2 = Blueprint('lab2', __name__)



@lab2.route('/lab2/a')
def a ():
    return 'без слэша'

@lab2.route('/lab2/a/')
def a2 ():
    return 'со слэшем'

flower_list = [
    {'name': 'роза', 'price': 300},
    {'name': 'тюльпан', 'price': 310},
    {'name': 'незабудка', 'price': 320},
    {'name': 'ромашка', 'price': 330},
    {'name': 'георгин', 'price': 300},
    {'name': 'гладиолус', 'price': 310}
]

@lab2.route('/lab2/all_flowers')
def all_flowers():
     return render_template('all_flowers.html', flowers=flower_list)

@lab2.route('/lab2/flowers/<int:flower_id>')
def flowers(flower_id):
    if flower_id < 0 or flower_id >= len(flower_list):
        abort(404)
    flower = flower_list[flower_id]
    return render_template('flower_detail.html', flower=flower, flower_id=flower_id)

@lab2.route('/lab2/add_flower/<name>')
def add_flower(name):
        flower_list.lab2end({'name': name, 'price': 0})
        return render_template('lab2.all_flowers.html', 
                          name=name, 
                          price=0,
                          count=len(flower_list),
                          flowers=flower_list)

@lab2.route("/lab2/add_flower", methods=['POST'])
def add_flower_post():
    name = request.form.get('name')
    price = request.form.get('price')
    if name and price:
        flower_list.lab2end({'name': name, 'price': int(price)})
        return redirect(url_for('lab2.all_flowers'))
    else:
        return render_template('error.html', message="Не указано имя или цена цветка"), 400

    

@lab2.route('/lab2/add_flower/')
def add_flower_error():
    return '''
<!doctype html>
<html>
    <body>
        <h1>Вы не задали имя цветка<h1>
    </body>
</html>
''', 400

@lab2.route("/lab2/del_flower/<int:flower_id>")
def delete_flower(flower_id):
    if flower_id < 0 or flower_id >= len(flower_list):
        abort(404)
    flower_list.pop(flower_id)
    return redirect(url_for('lab2.all_flowers'))

@lab2.route("/lab2/delete_all")
def delete_all_flowers():
    flower_list.clear()
    return redirect(url_for('lab2.all_flowers'))

@lab2.route('/lab2/clean_flower')
def f_cleaner():
        global flower_list
        flower_list = []
        return '''
<!doctype html>
<html>
    <body>
        <p>Список цветов очищен</p>
        <a href="/lab2/all_flowers">К списку цветов</a>
    </body>
</html>
'''




@lab2.route('/lab2/example/')
def example():
    name, number, group, course = 'Даяна Шамшиева', 2, 32, 3
    fruits = [
        {'name': 'яблоки', 'price': 100},
        {'name': 'груши', 'price': 120},
        {'name': 'апельсины', 'price': 80},
        {'name': 'мандарины', 'price': 95},
        {'name': 'манго', 'price': 321}
    ]
    return render_template('example.html', 
                           name=name, number=number, group=group,
                           course=course, fruits=fruits)
@lab2.route('/lab2/')
def lab():
    return render_template('lab2.html')

@lab2.route('/lab2/filters')
def filters():
    phrase = "О <b>сколько</b> <u>нам</U> <i>открытий</i> чудных... "
    return render_template('filter.html', phrase = phrase)


@lab2.route('/lab2/calc/')
def calc_1_1():
    return redirect('/lab2/calc/1/1')

@lab2.route('/lab2/calc/<int:a>')
def calc_a_1(a):
    return redirect(url_for('calc', a=a, b=1))

@lab2.route('/lab2/calc/<int:a>/<int:b>')
def calc(a, b):
    return f'''
    <!doctype html>
    <html>
    <head>
        <title>Калькулятор</title>
    </head>
    <body>
        <h1>Калькулятор</h1>
        <p>Число A: {a}</p>
        <p>Число B: {b}</p>
        <h2>Результаты операций:</h2>
        <ul>
            <li>{a} + {b} = {a + b}</li>
            <li>{a} - {b} = {a - b}</li>
            <li>{a} * {b} = {a * b}</li>
            <li>{a} / {b} = {a / b if b != 0 else 'деление на ноль!'}</li>
            <li>{a} <sup>{b}</sup> = {a ** b}</li>
        </ul>
    </body>
</html>
'''

books = [
    {'author': 'Чингиз Айтматов', 'title': 'Джамиля', 'genre': 'Повесть', 'pages': 120},
    {'author': 'Фрэнсис Скотт Фицджеральд', 'title': 'Великий Гэтсби', 'genre': 'Роман', 'pages': 218},
    {'author': 'Жюль Верн', 'title': 'Таинственный остров', 'genre': 'Приключения', 'pages': 544},
    {'author': 'Габриэль Гарсиа Маркес', 'title': 'Сто лет одиночества', 'genre': 'Магический реализм', 'pages': 416},
    {'author': 'Рэй Брэдбери', 'title': '451 градус по Фаренгейту', 'genre': 'Антиутопия', 'pages': 256},
    {'author': 'Данте Алигьери', 'title': 'Божественная комедия', 'genre': 'Поэма', 'pages': 672},
    {'author': 'Александр Дюма', 'title': 'Граф Монте-Кристо', 'genre': 'Приключенческий роман', 'pages': 1276},
    {'author': 'Фёдор Достоевский', 'title': 'Братья Карамазовы', 'genre': 'Роман', 'pages': 824},
    {'author': 'Анна Франк', 'title': 'Дневник Анны Франк', 'genre': 'Дневник', 'pages': 352},
    {'author': 'Джоан Роулинг', 'title': 'Гарри Поттер и философский камень', 'genre': 'Фэнтези', 'pages': 432},
    {'author': 'Джеймс Дашнер', 'title': 'Бегущий в лабиринте', 'genre': 'Научная фантастика', 'pages': 374}
]
@lab2.route('/lab2/books/')
def books_list():
    """Обработчик для вывода списка книг"""
    return render_template('books.html', books=books)


dogs = [
    {
        'name': 'Золотистый ретривер',
        'image': 'golden_retriever.jpg',
        'description': 'Дружелюбная, умная и преданная собака с золотистой шерстью'
    },
    {
        'name': 'Корги',
        'image': 'corgi.jpg',
        'description': 'Маленькая собака с короткими лапками и большой улыбкой'
    },
    {
        'name': 'Сибирский хаски',
        'image': 'husky.jpg',
        'description': 'Энергичная собака с голубыми глазами и волчьей внешностью'
    },
    {
        'name': 'Померанский шпиц',
        'image': 'pomeranian.jpg',
        'description': 'Маленький пушистый комочек с весёлым характером'
    },
    {
        'name': 'Самоед',
        'image': 'samoyed.jpg',
        'description': 'Белая пушистая собака с постоянной улыбкой'
    },
    {
        'name': 'Бигль',
        'image': 'beagle.jpg',
        'description': 'Дружелюбная гончая с грустными глазами и висячими ушками'
    },
    {
        'name': 'Французский бульдог',
        'image': 'french_bulldog.jpg',
        'description': 'Компактная собака с большими ушами и забавной мордочкой'
    },
    {
        'name': 'Кавалер кинг чарльз спаниель',
        'image': 'cavalier.jpg',
        'description': 'Элегантная маленькая собака с шелковистой шерстью'
    },
    {
        'name': 'Ши-тцу',
        'image': 'shih_tzu.jpg',
        'description': 'Длинношёрстная собака с милой мордочкой и дружелюбным нравом'
    },
    {
        'name': 'Мопс',
        'image': 'pug.jpg',
        'description': 'Небольшая собака с морщинистой мордочкой и весёлым характером'
    },
    {
        'name': 'Австралийская овчарка',
        'image': 'australian_shepherd.jpg',
        'description': 'Умная и активная собака с разными цветами глаз'
    },
    {
        'name': 'Бернский зенненхунд',
        'image': 'bernese.jpg',
        'description': 'Крупная пушистая собака с трёхцветным окрасом'
    },
    {
        'name': 'Такса',
        'image': 'dachshund.jpg',
        'description': 'Длинная собака с короткими лапками и смелым характером'
    },
    {
        'name': 'Лабрадор ретривер',
        'image': 'labrador.jpg',
        'description': 'Самая популярная порода - добрая, умная и игривая'
    },
    {
        'name': 'Акита-ину',
        'image': 'akita.jpg',
        'description': 'Японская порода с плюшевой шерстью и преданным характером'
    },
    {
        'name': 'Кокер-спаниель',
        'image': 'cocker_spaniel.jpg',
        'description': 'Собака с длинными ушами и шелковистой шерстью'
    },
    {
        'name': 'Бишон фризе',
        'image': 'bichon.jpg',
        'description': 'Белая пушистая собака, похожая на мягкую игрушку'
    },
    {
        'name': 'Далматин',
        'image': 'dalmatian.jpg',
        'description': 'Узнаваемая порода с чёрными пятнами на белой шерсти'
    },
    {
        'name': 'Пудель',
        'image': 'poodle.jpg',
        'description': 'Умная собака с кудрявой шерстью и элегантной внешностью'
    },
    {
        'name': 'Аляскинский маламут',
        'image': 'malamute.jpg',
        'description': 'Крупная ездовая собака с густой шерстью и дружелюбным нравом'
    }
]

@lab2.route('/lab2/dogs')
def dogs_list():
    f'''Обработчик для вывода списка собак'''
    return render_template('dogs.html', dogs=dogs)