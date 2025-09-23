from flask import Flask, url_for, request, redirect
import datetime
app = Flask(__name__)

@app.errorhandler(404)
def not_found(err):
    img_path = url_for("static", filename="kotic.jpg")
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
                overflow: hidden;
                display:flex;
                min-height: 100vh;
            }
            div {
            z-index: -1;
            position: absolute;
            }
            h1 {
            position: absolute;
            font-size: 70px;
            left: 50%;
            }
            h1:hover {
            color: red;
            }
            a {
            color: gray;

            }

         
        </style>
    </head>
    <body>
        <h1> WARNING <br> 404 <br> NO PAGE FOUND </h1>
        <a href="/">Вернуться в безопасное место</a>
        <div>
        <img src="''' + img_path + '''">
        <div>
        
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