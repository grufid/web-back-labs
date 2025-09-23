from flask import Flask, url_for, request, redirect
import datetime
app = Flask(__name__)

@app.errorhandler(404)
def not_found(err):
    return "нет такой страницы", 404

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
        </html>""", 200, {"X-Server": "sample", 
                          "Content-Type": "text/plain; charset=utf-8"
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
'''

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
    </body>
<html>
'''