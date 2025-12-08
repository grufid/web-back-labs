from flask import Blueprint, render_template, request, jsonify, session, current_app
import psycopg2
from psycopg2.extras import RealDictCursor
import sqlite3
from os import path
import json
from werkzeug.security import generate_password_hash, check_password_hash

# Создаем Blueprint для РГЗ
rgz = Blueprint('rgz', __name__, url_prefix='/rgz')

def db_connect():
    if current_app.config['DB_TYPE'] == 'postgres':
        conn = psycopg2.connect(
            host='127.0.0.1',
            database='dayana_shamshieva_knowledge_base',
            user='dayana_shamshieva_knowledge_base',
            password='123',
            client_encoding='UTF8'
        )
        cur = conn.cursor(cursor_factory=RealDictCursor)
    else:
        dir_path = path.dirname(path.realpath(__file__))
        db_path = path.join(dir_path, "database.db")
        conn = sqlite3.connect(db_path)
        conn.row_factory = sqlite3.Row
        cur = conn.cursor()
    return conn, cur

def db_close(conn, cur):
    conn.commit()
    cur.close()
    conn.close()

def validate_credentials(username, password):
    """Валидация логина и пароля"""
    import re
    
    if not username or not password:
        return False, 'Логин и пароль не могут быть пустыми'
    
    # Проверка символов
    valid_chars = re.compile(r'^[a-zA-Z0-9!@#$%^&*()_+\-=\[\]{};\':"\\|,.<>\/?]*$')
    if not valid_chars.match(username) or not valid_chars.match(password):
        return False, 'Логин и пароль должны содержать только латинские буквы, цифры и специальные символы'
    
    if len(username) < 3:
        return False, 'Логин должен быть минимум 3 символа'
    
    if len(password) < 6:
        return False, 'Пароль должен быть минимум 6 символов'
    
    return True, ''

@rgz.route('/')
def index():
    return render_template('rgz/index.html')

@rgz.route('/api', methods=['POST'])
def api():
    data = request.get_json()
    method = data.get('method')
    params = data.get('params', {})
    request_id = data.get('id', 1)
    
    conn, cur = db_connect()
    
    try:
        # Получить все рецепты
        if method == 'get_recipes':
            cur.execute("SELECT * FROM recipes ORDER BY id")
            recipes = []
            for r in cur.fetchall():
                recipes.append({
                    'id': r['id'],
                    'title': r['title'],
                    'ingredients': json.loads(r['ingredients']),
                    'steps': json.loads(r['steps']),
                    'image_url': r['image_url'] or ''
                })
            db_close(conn, cur)
            return jsonify({'jsonrpc': '2.0', 'result': {'recipes': recipes}, 'id': request_id})
        
        # Поиск рецептов
        elif method == 'search_recipes':
            query = params.get('query', '')
            ingredients = params.get('ingredients', [])
            mode = params.get('mode', 'any')
            
            sql = "SELECT * FROM recipes WHERE 1=1"
            args = []
            
            if query:
                if current_app.config['DB_TYPE'] == 'postgres':
                    sql += " AND title ILIKE %s"
                else:
                    sql += " AND title LIKE ?"
                args.append(f'%{query}%')
            
            if ingredients:
                if mode == 'all':
                    for ing in ingredients:
                        if current_app.config['DB_TYPE'] == 'postgres':
                            sql += " AND ingredients ILIKE %s"
                        else:
                            sql += " AND ingredients LIKE ?"
                        args.append(f'%{ing}%')
                else:
                    sql += " AND ("
                    if current_app.config['DB_TYPE'] == 'postgres':
                        sql += " OR ".join(["ingredients ILIKE %s" for _ in ingredients])
                    else:
                        sql += " OR ".join(["ingredients LIKE ?" for _ in ingredients])
                    sql += ")"
                    args.extend([f'%{ing}%' for ing in ingredients])
            
            cur.execute(sql, args)
            recipes = []
            for r in cur.fetchall():
                recipes.append({
                    'id': r['id'],
                    'title': r['title'],
                    'ingredients': json.loads(r['ingredients']),
                    'steps': json.loads(r['steps']),
                    'image_url': r['image_url'] or ''
                })
            db_close(conn, cur)
            return jsonify({'jsonrpc': '2.0', 'result': {'recipes': recipes}, 'id': request_id})
        
        # Вход администратора
        elif method == 'login':
            username = params.get('username')
            password = params.get('password')
            
            # Валидация
            is_valid, error_msg = validate_credentials(username, password)
            if not is_valid:
                db_close(conn, cur)
                return jsonify({
                    'jsonrpc': '2.0', 
                    'error': {'code': 3, 'message': error_msg}, 
                    'id': request_id
                })
            
            if current_app.config['DB_TYPE'] == 'postgres':
                cur.execute("SELECT * FROM admin_user WHERE username = %s", (username,))
            else:
                cur.execute("SELECT * FROM admin_user WHERE username = ?", (username,))
            
            admin = cur.fetchone()
            db_close(conn, cur)
            
            if admin and check_password_hash(admin['password_hash'], password):
                session['rgz_admin'] = True
                session['rgz_admin_username'] = username
                return jsonify({'jsonrpc': '2.0', 'result': {'success': True}, 'id': request_id})
            
            return jsonify({
                'jsonrpc': '2.0', 
                'error': {'code': 1, 'message': 'Неверный логин или пароль'}, 
                'id': request_id
            })
        
        # Выход
        elif method == 'logout':
            session.pop('rgz_admin', None)
            session.pop('rgz_admin_username', None)
            db_close(conn, cur)
            return jsonify({'jsonrpc': '2.0', 'result': {'success': True}, 'id': request_id})
        
        # Удаление аккаунта администратора
        elif method == 'delete_account':
            if not session.get('rgz_admin'):
                db_close(conn, cur)
                return jsonify({
                    'jsonrpc': '2.0', 
                    'error': {'code': 2, 'message': 'Требуются права администратора'}, 
                    'id': request_id
                })
            
            username = session.get('rgz_admin_username')
            password = params.get('password')
            
            if not username or not password:
                db_close(conn, cur)
                return jsonify({
                    'jsonrpc': '2.0', 
                    'error': {'code': 4, 'message': 'Не указаны данные'}, 
                    'id': request_id
                })
            
            # Проверка пароля
            if current_app.config['DB_TYPE'] == 'postgres':
                cur.execute("SELECT * FROM admin_user WHERE username = %s", (username,))
            else:
                cur.execute("SELECT * FROM admin_user WHERE username = ?", (username,))
            
            admin = cur.fetchone()
            
            if not admin or not check_password_hash(admin['password_hash'], password):
                db_close(conn, cur)
                return jsonify({
                    'jsonrpc': '2.0', 
                    'error': {'code': 1, 'message': 'Неверный пароль'}, 
                    'id': request_id
                })
            
            # Удаление аккаунта
            if current_app.config['DB_TYPE'] == 'postgres':
                cur.execute("DELETE FROM admin_user WHERE username = %s", (username,))
            else:
                cur.execute("DELETE FROM admin_user WHERE username = ?", (username,))
            
            session.pop('rgz_admin', None)
            session.pop('rgz_admin_username', None)
            
            db_close(conn, cur)
            return jsonify({'jsonrpc': '2.0', 'result': {'success': True}, 'id': request_id})
        
        # Добавить рецепт
        elif method == 'add_recipe':
            if not session.get('rgz_admin'):
                db_close(conn, cur)
                return jsonify({
                    'jsonrpc': '2.0', 
                    'error': {'code': 2, 'message': 'Требуются права администратора'}, 
                    'id': request_id
                })
            
            title = params.get('title', '').strip()
            ingredients = params.get('ingredients', [])
            steps = params.get('steps', [])
            image_url = params.get('image_url', '').strip()
            
            if not title or not ingredients or not steps:
                db_close(conn, cur)
                return jsonify({
                    'jsonrpc': '2.0', 
                    'error': {'code': 5, 'message': 'Заполните все обязательные поля'}, 
                    'id': request_id
                })
            
            if current_app.config['DB_TYPE'] == 'postgres':
                cur.execute("INSERT INTO recipes (title, ingredients, steps, image_url) VALUES (%s, %s, %s, %s)", 
                          (title, json.dumps(ingredients), json.dumps(steps), image_url))
            else:
                cur.execute("INSERT INTO recipes (title, ingredients, steps, image_url) VALUES (?, ?, ?, ?)", 
                          (title, json.dumps(ingredients), json.dumps(steps), image_url))
            
            db_close(conn, cur)
            return jsonify({'jsonrpc': '2.0', 'result': {'success': True}, 'id': request_id})
        
        # Обновить рецепт
        elif method == 'update_recipe':
            if not session.get('rgz_admin'):
                db_close(conn, cur)
                return jsonify({
                    'jsonrpc': '2.0', 
                    'error': {'code': 2, 'message': 'Требуются права администратора'}, 
                    'id': request_id
                })
            
            recipe_id = params.get('recipe_id')
            title = params.get('title', '').strip()
            ingredients = params.get('ingredients', [])
            steps = params.get('steps', [])
            image_url = params.get('image_url', '').strip()
            
            if not recipe_id or not title or not ingredients or not steps:
                db_close(conn, cur)
                return jsonify({
                    'jsonrpc': '2.0', 
                    'error': {'code': 5, 'message': 'Заполните все обязательные поля'}, 
                    'id': request_id
                })
            
            if current_app.config['DB_TYPE'] == 'postgres':
                cur.execute("UPDATE recipes SET title=%s, ingredients=%s, steps=%s, image_url=%s WHERE id=%s",
                          (title, json.dumps(ingredients), json.dumps(steps), image_url, recipe_id))
            else:
                cur.execute("UPDATE recipes SET title=?, ingredients=?, steps=?, image_url=? WHERE id=?",
                          (title, json.dumps(ingredients), json.dumps(steps), image_url, recipe_id))
            
            db_close(conn, cur)
            return jsonify({'jsonrpc': '2.0', 'result': {'success': True}, 'id': request_id})
        
        # Удалить рецепт
        elif method == 'delete_recipe':
            if not session.get('rgz_admin'):
                db_close(conn, cur)
                return jsonify({
                    'jsonrpc': '2.0', 
                    'error': {'code': 2, 'message': 'Требуются права администратора'}, 
                    'id': request_id
                })
            
            recipe_id = params.get('recipe_id')
            
            if not recipe_id:
                db_close(conn, cur)
                return jsonify({
                    'jsonrpc': '2.0', 
                    'error': {'code': 6, 'message': 'Не указан ID рецепта'}, 
                    'id': request_id
                })
            
            if current_app.config['DB_TYPE'] == 'postgres':
                cur.execute("DELETE FROM recipes WHERE id=%s", (recipe_id,))
            else:
                cur.execute("DELETE FROM recipes WHERE id=?", (recipe_id,))
            
            db_close(conn, cur)
            return jsonify({'jsonrpc': '2.0', 'result': {'success': True}, 'id': request_id})
        
        db_close(conn, cur)
        return jsonify({
            'jsonrpc': '2.0', 
            'error': {'code': -32601, 'message': 'Метод не найден'}, 
            'id': request_id
        })
    
    except Exception as e:
        db_close(conn, cur)
        return jsonify({
            'jsonrpc': '2.0', 
            'error': {'code': -32603, 'message': f'Ошибка сервера: {str(e)}'}, 
            'id': request_id
        })