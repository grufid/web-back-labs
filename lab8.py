from flask import Blueprint, request, render_template, redirect
from werkzeug.security import check_password_hash, generate_password_hash
from db import db
from flask_login import login_user, login_required, current_user, logout_user
from db.models import users, articles
from sqlalchemy import or_
from sqlalchemy import func

lab8 = Blueprint('lab8', __name__)

@lab8.route('/lab8/')
def lab():
    return render_template('lab8/lab8.html')

@lab8.route('/lab8/register', methods=['GET', 'POST'])
def register():
    if request.method == 'GET':
        return render_template('lab8/register.html')

    login_form = request.form.get('login')
    password_form = request.form.get('password')

    
    if not login_form or not login_form.strip():
        return render_template('lab8/register.html', error='Введите логин')
    
    if not password_form or not password_form.strip():
        return render_template('lab8/register.html', error='Введите пароль')
    
    
    if users.query.filter_by(login=login_form).first():
        return render_template('lab8/register.html', error='Логин уже занят')
    
    new_user = users(login=login_form, password=generate_password_hash(password_form))
    db.session.add(new_user)
    db.session.commit()
    
    # Авто-логин после регистрации
    login_user(new_user, remember=False)
    return redirect('/lab8/')

@lab8.route('/lab8/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('lab8/login.html')
    
    login_form = request.form.get('login')
    password_form = request.form.get('password')
    remember = request.form.get('remember') == 'on'

    if not login_form or not password_form:
        return render_template('lab8/login.html', error='Заполните все поля')

    user = users.query.filter_by(login=login_form).first()
    
    if user and check_password_hash(user.password, password_form):
        # Галочка "запомнить меня"
        login_user(user, remember=remember)
        return redirect('/lab8/')
    
    return render_template('lab8/login.html', error='Неверный логин или пароль')

@lab8.route('/lab8/articles/')
def articles_list():
    query = request.args.get('query', '').strip()
    
    if current_user.is_authenticated:
        my_articles = articles.query.filter_by(login_id=current_user.id).all()
        other_public = articles.query.filter(
            articles.is_public == True,
            articles.login_id != current_user.id
        ).all()
        
        if query:
            # Явное приведение к нижнему регистру для гарантированной регистронезависимости
            query_lower = query.lower()
            results = articles.query.filter(
                or_(
                    func.lower(articles.title).contains(query_lower),
                    func.lower(articles.article_text).contains(query_lower)
                ),
                or_(
                    articles.is_public == True,
                    articles.login_id == current_user.id
                )
            ).all()
        else:
            results = []
        
        return render_template('lab8/articles.html',
            my_articles=my_articles,
            public_articles=other_public,
            query=query,
            results=results)
    else:
        public_articles = articles.query.filter_by(is_public=True).all()
        
        if query:
            # То же самое для неавторизованных пользователей
            query_lower = query.lower()
            results = articles.query.filter(
                or_(
                    func.lower(articles.title).contains(query_lower),
                    func.lower(articles.article_text).contains(query_lower)
                ),
                articles.is_public == True
            ).all()
        else:
            results = []
        
        return render_template('lab8/articles.html',
            public_articles=public_articles,
            query=query,
            results=results)

@lab8.route('/lab8/create', methods=['GET', 'POST'])
@login_required
def create_article():
    if request.method == 'GET':
        return render_template('lab8/create.html')
    
    title = request.form.get('title')
    text = request.form.get('article_text')
    is_public = request.form.get('is_public') == 'on'
    is_favorite = request.form.get('is_favorite') == 'on'
    
    if not title or not text:
        return render_template('lab8/create.html', error='Заполните все поля')
    
    article = articles(
        login_id=current_user.id,
        title=title,
        article_text=text,
        is_public=is_public,
        is_favorite=is_favorite,
        likes=0
    )
    
    db.session.add(article)
    db.session.commit()
    return redirect('/lab8/articles/')

@lab8.route('/lab8/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_article(id):
    article = articles.query.filter_by(id=id, login_id=current_user.id).first()
    if not article:
        return "Статья не найдена", 404
    
    if request.method == 'GET':
        return render_template('lab8/edit.html', article=article)
    
    title = request.form.get('title')
    text = request.form.get('article_text')
    is_public = request.form.get('is_public') == 'on'
    is_favorite = request.form.get('is_favorite') == 'on'
    
    if not title or not text:
        return render_template('lab8/edit.html', article=article, error='Заполните все поля')
    
    article.title = title
    article.article_text = text
    article.is_public = is_public
    article.is_favorite = is_favorite
    db.session.commit()
    
    return redirect('/lab8/articles/')

@lab8.route('/lab8/delete/<int:id>')
@login_required
def delete_article(id):
    article = articles.query.filter_by(id=id, login_id=current_user.id).first()
    if article:
        db.session.delete(article)
        db.session.commit()
    return redirect('/lab8/articles/')

@lab8.route('/lab8/logout')
@login_required
def logout():
    logout_user()
    return redirect('/lab8/')