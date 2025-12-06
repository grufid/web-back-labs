from flask import Flask, url_for, request, redirect, abort, render_template
from lab1 import lab1
from lab2 import lab2
from lab3 import lab3
from lab4 import lab4
from lab5 import lab5
from lab6 import lab6
from lab6 import lab7

import datetime
import os

app = Flask(__name__)

app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'секретно-секретный секрет')
app.config['DB_TYPE'] = os.getenv('DB_TYPE', 'postgres')

app.register_blueprint(lab1)
app.register_blueprint(lab2)
app.register_blueprint(lab3)
app.register_blueprint(lab4)
app.register_blueprint(lab5)
app.register_blueprint(lab6)
app.register_blueprint(lab7)

visit_log = []

@app.errorhandler(404)
def not_found(err):
    
    client_ip = request.remote_addr
    access_time = datetime.datetime.today()
    requested_url = request.url

    visit_log.append(f'[<i>{access_time}</i>, пользователь <i>{client_ip}</i>] зашёл на адрес: <i>{requested_url}</i>')
    img_path = url_for("static", filename="lab1/kotic.jpg")

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
            position: fixed;
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
        <ol>
            <li>
                <a href="/lab1">Лабораторная I</a>
            </li>
            <li>
                <a href="/lab2">Лабораторная II</a>
            </li>
            <li>
                <a href="/lab3">Лабораторная III</a>
            </li>
            <li>
                <a href="/lab4">Лабораторная IV</a>
            </li>
            <li>
                <a href="/lab5">Лабораторная V</a>
            </li>
            <li>
                <a href="/lab6">Лабораторная VI</a>
            </li>
            <li>
                <a href="/lab7">Лабораторная VII</a>
            </li>
        </main>
        <footer>
            Шамшиева Даяна Артуровна, ФБИ-32, 3 курс, 2025
        </footer>
    <body>
<html>
'''

