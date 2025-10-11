from flask import Blueprint, url_for, request, redirect
lab1 = Blueprint('lab1', __name__)
import datetime

@lab1.route("/lab1/web")
def web():
    return """<!doctype html>
        <html>
           <body>
               <h1>web-сервер на flask</h1>
               <a href="/lab1/author">author</a>
           </body>
        </html>""", 200, {"X-Server": "sample", "Content-Type": "text/plain; charset=utf-8"
                          }


@lab1.route("/lab1/author")
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


@lab1.route('/lab1/image')
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


@lab1.route('/lab1/counter')
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


@lab1.route('/lab1/counter/reset')
def reset_counter():
    global count
    count = 0
    return redirect("/lab1/counter")


@lab1.route("/lab1/info")
def info():
    return redirect("/lab1/author")


@lab1.route("/lab1/created")
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


@lab1.route('/lab1')
def lab():
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