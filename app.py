from flask import Flask, url_for, request, redirect
import datetime
app = Flask(__name__)


@app.route("/web")
def web():
    return """<!doctype html>
        <html>
           <body>
               <h1>web-сервер на flask</h1>
               <a href="/author">author</a>
           </body>
        </html>"""

@app.route("/author")
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
                <a href="/web">web</a>
            </body>
        </html>"""
@app.route('/lab1/image')
def image ():
    path = url_for("static", filename="mili.jpg")
    return '''
<!doctype html>
<html>
    <body style="text-align: center; background-color: #8B0000">
        <h1 style="color:white">Котик</h1>
        <img src="''' + path + '''" style="-webkit-mask-image: radial-gradient(circle, black 45%, transparent 60%)">
    </body>
</html>
'''

count = 0

@app.route('/counter')
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
    </body>
</html>
'''
@app.route("/info")
def info():
    return redirect("/author")