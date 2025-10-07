from flask import Flask, url_for, request, redirect, abort, render_template
import datetime
app = Flask(__name__)

visit_log = []

@app.errorhandler(404)
def not_found(err):
    
    client_ip = request.remote_addr
    access_time = datetime.datetime.today()
    requested_url = request.url

    visit_log.append(f'[<i>{access_time}</i>, пользователь <i>{client_ip}</i>] зашёл на адрес: <i>{requested_url}</i>')
    img_path = url_for("static", filename="kotic.jpg")

    log_html = "<ul style='list-style:none; padding:0;'>"
    for entry in visit_log:
        log_html += f"<li style='margin:5px 0; padding:10px; background:#eee; border-radius:6px;'>{entry}</li>"
    log_html += "</ul>"


    return '''
<!doctype html>
<html>
    <head>
        <title> WARNING <br> 404 <br> NO PAGE FOUND</title>
        <style>
            body {
                background-color: black;
                font-family: desdemona;
                padding: 30px;
                color: #D3D3D3;
                text-align: center;
                position: relative;
                
                display:flex;
                min-height: 100vh;
            }
            h1 {
            position: absolute;
            font-size: 50px;
            top: -220%;
            


            }
            h1:hover {
            color: red;
            }
            a {
            color: gray;
            }
            .book {
            color: gray;
            width: 800px;
            }
            .place {
            color: white;
            position: absolute;
            left: 50%;
            top: 40%;
            h2 {
            color: white;}

        
        </style>
    </head>
    <body>
        <div class='place'>
            <h1> WARNING <br> 404 <br> NO PAGE FOUND </h1>
            <a href="/">Вернуться в безопасное место</a>
            <p>Твой IP: ''' + client_ip + '''</p>
            <p>Дата и время: ''' + str(access_time) + '''</p>
            <p>Запрошенный адрес: ''' + requested_url + '''</p>
        </div>
        <div>
        <img src="''' + img_path + '''">
        <div>
        <div class='book'>
        <h2>Журнал ошибок 404</h2>
        ''' + log_html + '''
        </div>
 
        
    </div>
    </body>
</html>
''', 404

@app.route("/bad_request")
def bad_request():
    return '''
<!doctype html>
<html>
    <body style="font-family:monospace; font-weight: bold; background-color:#7B68EE; font-size: 2em; color: white">
        <h1>Error 400 <br> (Недопустимый запрос)!!</h1>
    </body>
</html>
''', 400


@app.route("/unauthorized")
def unauthorized():
    return '''
<!doctype html>
<html>
    <body style="text-align:center; background-color:red; color: black; font-size: 2em">
        <h1>401 — Unauthorized</h1>
        <p><i>Эта страница только для избранных</i></p>
    </body>
</html>
''', 401


@app.route("/payment_required")
def payment_required():
    return '''
<!doctype html>
<html>
    <body style="margin:40px; font-family: franklin gothic medium; background-color:black; color: red">
        <h1 style="padding:20px;">402 — Payment Required</h1>
        <p>Пожалуйста заплатите деньгами или отправьте на номер 5Rywgdv%sugdhbcs</p>
    </body>
</html>
''', 402


@app.route("/forbidden")
def forbidden():
    return '''
<!doctype html>
<html>
    <body style="text-align: center; margin-top:300px; font-family: century schoolbook; background-color:#191970; color: #FFE4E1">
        <h1>403 — Forbidden</h1>
        <p>Недостаточный уровень доступа</p>
    </body>
</html>
''', 403


@app.route("/method_not_allowed")
def method_not_allowed():
    return '''
<!doctype html>
<html>
    <body style="text-align: center; margin: 40px; margin-top:150px; font-family: matura mt script capitals; background-color: #8FBC8F; color: #800000">
        <h1>405 — Method Not Allowed</h1>
        <p>Метод запроса не разрешён для данного ресурса</p>
    </body>
</html>
''', 405

@app.route("/teapot")
def teapot():
    return '''
<!doctype html>
<html>
    <body style="text-align: center; font-family: mv boli; background-color: #556B2F; font-size: 2em; color: #F0FFF0">
        <h1>418 <br> I'm a teapot</h1>
    </body>
</html>
''', 418

@app.route("/break-server")
def break_server(): 
    my_list = [1, 2, 3] # Выход за границы списка
    return my_list[10]  

@app.errorhandler(500)
def internal_error(err):
    return '''
<!doctype html>
<html>
<body>
    <h1>500</h1>
    <h2>Внутрення ошибка сервера</h2>
    <p>Кажется, наш сервер захотел немного отдохнуть</p>
    <div>
        <strong>Что случилось:</strong><br>
            • Сервер столкнулся с непредвиденной ошибкой<br>
            • Наши инженеры-котики уже работают над решением<br>
            • Попробуйте обновить страницу через несколько минут
    </div>
</body>
<html>
''', 500
@app.route("/")
@app.route("/index")
def index():
    return '''
<!doctype html>
<html>
    <body>
        <header>
            НГТУ, ФБ, WEB-программирование, часть 2. Список лабораторных
        </header>
        <main>
        <a href="/lab1">Первая лабораторная</a>
        </main>
        <footer>
            Шамшиева Даяна Артуровна, ФБИ-32, 3 курс, 2025
        </footer>
    <body>
<html>
'''


@app.route("/lab1/web")
def web():
    return """<!doctype html>
        <html>
           <body>
               <h1>web-сервер на flask</h1>
               <a href="/lab1/author">author</a>
           </body>
        </html>""", 200, {"X-Server": "sample", "Content-Type": "text/plain; charset=utf-8"
                          }

@app.route("/lab1/author")
def author():
    name = "Шамшиева Даяна Артуровна"
    group = "ФБИ-32"
    faculty = "ФБ"

    return """<!doctype html>
        <html>
            <body>
                <p>Студент: """ + name + """</p>
                <p>Группа: """ + group + """</p>
                <p>Факультет: """ + faculty + """</p>
                <a href="/lab1/web">web</a>
            </body>
        </html>"""

@app.route('/lab1/image')
def image ():
    path = url_for("static", filename="mili.jpg")
    css_path = url_for("static", filename="lab1.css")
    return '''
<!doctype html>
<html>
    <head>
        <link rel="stylesheet" href="''' + css_path + '''">
    </head>
    <body>
        <h1> (=^‥^=) котик (=^‥^=)'</h1>
        <img src="''' + path + '''" class="cat-image">
    </body>
</html>
''', 200, {
    'Content-Language': 'en',
    'Cat-Breed': 'bengal',
    'Cat-Age': '2 years'
}

count = 0

@app.route('/lab1/counter')
def counter():
    global count
    count += 1
    time = datetime.datetime.today()
    url = request.url
    client_ip = request.remote_addr

    return '''
<!doctype html>
<html>
    <body style="font-family: fantasy; font-size: 16pt">
        Сколько раз вы сюда заходили: ''' + str(count) + '''
        <hr>
        Дата и время : ''' + str(time) + '''<br>
        Запрошенный адрес: ''' + url + '''<br>
        Ваш IP-адресс: ''' + client_ip + '''<br>
        <hr>
        <a href="/lab1/counter/reset">Очистка счётчика</a>
    </body>
</html>
'''

visit_count = 0

@app.route('/lab1/counter/reset')
def reset_counter():
    global count
    count = 0
    return redirect("/lab1/counter")

@app.route("/lab1/info")
def info():
    return redirect("/lab1/author")
@app.route("/lab1/created")
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

@app.route('/lab1')
def lab1():
    return '''
<!doctype html>
<html>
    <head>
        <title>Лабораторная работа I</title>
    </head>
    <body>
        <p>
            <b>Flask</b> — фреймворк для создания веб-приложений на языке
        программирования Python, использующий набор инструментов
        Werkzeug, а также шаблонизатор Jinja2. Относится к категории так
        называемых микрофреймворков — минималистичных каркасов

        веб-приложений, сознательно предоставляющих лишь самые ба-
        зовые возможности.
        </p>
        <a href='/'>Вернуться на главную страницу</a>
        <h2>Список роутов</h2>
        <ul>
            <li>
                <a href="/lab1/web">Web-сервер на Flask</a>
            </li>
            <li>
                <a href="/lab1/image">Картинка</a>
            </li>
            <li>
                <a href="/lab1/author">Автор</a>
            </li>
            <li>
                <a href="/lab1/counter">Счётчик</a>
            </li>
            <li>
                <a href="/lab1/counter/reset">Обнуление</a>
            </li>
            <li>
                <a href='/lab1/info'>Перенаправление</a>
            </li>
            <li>
                <a href='/lab1/created'>Код ответа 201</a>
            </li>
            <li>
                <a href='/bad_request'>Ошибка 400</a>
            </li>
            <li>
                <a href='/unauthorized'>Ошибка 401</a>
            </li>
            <li>
                <a href='/payment_required'>Ошибка 402</a>
            </li>
            <li>
                <a href='/forbidden'>Ошибка 403</a>
            </li>
            <li>
                <a href='/lab1/not_found'>Ошибка 404</a>
            </li>
            <li>
                <a href='/method_not_allowed'>Ошибка 405</a>
            </li>
            <li>
                <a href='/teapot'>Ошибка 418</a>
            </li>
            <li>
                <a href='/break-server'>Ошибка 500</a>
            </li>
    </body>
<html>
'''

@app.route('/lab2/a')
def a ():
    return 'без слэша'

@app.route('/lab2/a/')
def a2 ():
    return 'со слэшем'

flower_list = ['роза', 'тюльпан', 'незабудка', 'ромашка']

@app.route('/lab2/flowers/<int:flower_id>')
def flowers(flower_id):
    if flower_id >= len(flower_list):
        abort(404)
    else:
        flower = flower_list[flower_id] 
        all_flowers_url = url_for('all_flowers')
        return render_template('flowers.html', flower_id=flower_id, flower=flower,
        all_flowers_url=all_flowers_url)

@app.route('/lab2/add_flower/<name>')
def add_flower(name):
        flower_list.append(name)
        return f'''
        <h1>Добавлен новый цветок</h1>
        <p>Название нового цветка: {name}</p>
        <p>Всего цветов: {len(flower_list)}</p>
        <a href="/lab2/flowers/all">Полный список</a>
    </body>
</html>
'''

@app.route('/lab2/add_flower/')
def add_flower_error():
    return '''
<!doctype html>
<html>
    <body>
        <h1>Вы не задали имя цветка<h1>
    </body>
</html>
''', 400

@app.route('/lab2/flowers/all')
def all_flowers():
    return f'''
<!doctype html>
<html>
    <body>
        <p>Количество цветов: {len(flower_list)}</p>
        <p>Список цветов:</p>
        <ul>
            {''.join(f'<li>{flower}</li>' for flower in flower_list)}
        </ul>
        <a href="/lab2/clean_flower">Очистить список цветов</a>
    </body>
</html>
'''

@app.route('/lab2/clean_flower')
def f_cleaner():
        global flower_list
        flower_list = []
        return '''
<!doctype html>
<html>
    <body>
        <p>Список цветов очищен</p>
        <a href="/lab2/flowers/all">К списку цветов</a>
    </body>
</html>
'''




@app.route('/lab2/example/')
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
@app.route('/lab2/')
def lab2():
    return render_template('lab2.html')

@app.route('/lab2/filters')
def filters():
    phrase = "О <b>сколько</b> <u>нам</U> <i>открытий</i> чудных... "
    return render_template('filter.html', phrase = phrase)


@app.route('/lab2/calc/')
def calc_1_1():
    return redirect('/lab2/calc/1/1')

@app.route('/lab2/calc/<int:a>')
def calc_a_1(a):
    return redirect(url_for('calc', a=a, b=1))

@app.route('/lab2/calc/<int:a>/<int:b>')
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
@app.route('/lab2/books/')
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

@app.route('/lab2/dogs')
def dogs_list():
    f'''Обработчик для вывода списка собак'''
    return render_template('dogs.html', dogs=dogs)