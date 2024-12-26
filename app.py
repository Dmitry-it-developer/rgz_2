from flask import Flask, url_for, redirect, render_template, jsonify, request, make_response, session, current_app
from werkzeug.security import check_password_hash, generate_password_hash
from flask_sqlalchemy import SQLAlchemy
import os
from os import path
from db import db
from db.models import db, furniture, users

app = Flask(__name__)

app.config['SECRET_KEY'] = 'секретныйкод'
app.config['DB_TYPE'] = 'sqlite'


dir_path = path.dirname(path.realpath(__file__))
db_path = path.join(dir_path, 'furniture.db')
app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{db_path}'

db.init_app(app)

def seed_data():
    if furniture.query.first():
        return
    items = [
    furniture(name="Деревянный стул Classic", description="Удобный деревянный стул", price=1500.00),
    furniture(name="Офисный стул Comfort", description="Современный офисный стул", price=2500.00),
    furniture(name="Мягкий стул Lounge", description="Стул с мягким сиденьем", price=1800.00),
    furniture(name="Стул Retro High", description="Деревянный стул с высокой спинкой", price=2200.00),
    furniture(name="Садовый стул GreenLine", description="Пластиковый стул для сада", price=900.00),
    furniture(name="Кухонный стол Harmony", description="Кухонный стол на 4 персоны", price=3500.00),
    furniture(name="Обеденный стол Oakwood", description="Обеденный стол из дуба", price=8000.00),
    furniture(name="Складной стол Picnic", description="Складной стол для пикника", price=2000.00),
    furniture(name="Компьютерный стол SmartDesk", description="Компьютерный стол с полками", price=5000.00),
    furniture(name="Журнальный столик Glassy", description="Стеклянный журнальный столик", price=4000.00),
    furniture(name="Диван Family Corner", description="Угловой диван с обивкой из ткани", price=15000.00),
    furniture(name="Диван-кровать SleepWell", description="Диван-кровать с механизмом трансформации", price=20000.00),
    furniture(name="Кожаный диван Premium", description="Кожаный двухместный диван", price=25000.00),
    furniture(name="Диван с ящиком StorageSofa", description="Диван с ящиком для хранения", price=18000.00),
    furniture(name="Классический диван Elegance", description="Классический диван с подлокотниками", price=17000.00),
    furniture(name="Кресло Relax Soft", description="Кресло с мягкими подлокотниками", price=7000.00),
    furniture(name="Офисное кресло LeatherPro", description="Кожаное офисное кресло", price=12000.00),
    furniture(name="Кресло для отдыха ComfortPlus", description="Кресло для отдыха с подставкой для ног", price=9500.00),
    furniture(name="Плетёное кресло Terrace", description="Плетёное кресло для террасы", price=6000.00),
    furniture(name="Ретро-кресло Vintage", description="Ретро-кресло в стиле 60-х", price=11000.00),
    furniture(name="Шкаф-купе MirrorLine", description="Шкаф-купе с зеркальными дверцами", price=25000.00),
    furniture(name="Классический шкаф Heritage", description="Классический деревянный шкаф", price=20000.00),
    furniture(name="Шкаф для одежды Glow", description="Шкаф для одежды с подсветкой", price=27000.00),
    furniture(name="Шкаф для обуви ShoeKeeper", description="Шкаф с отделениями для обуви", price=22000.00),
    furniture(name="Модульный шкаф LivingSpace", description="Модульный шкаф для гостиной", price=30000.00),
    furniture(name="Комод FiveDrawers", description="Комод с пятью ящиками", price=12000.00),
    furniture(name="Белый комод WhiteWood", description="Белый комод с деревянной отделкой", price=13000.00),
    furniture(name="Узкий комод SlimFit", description="Высокий узкий комод для спальни", price=11000.00),
    furniture(name="Комод с зеркалом Shine", description="Комод с зеркалом для прихожей", price=15000.00),
    furniture(name="Маленький комод MiniStore", description="Маленький комод для хранения аксессуаров", price=8000.00)
]

    db.session.bulk_save_objects(items)
    db.session.commit()


def initialize_database():
    db.create_all()  
    seed_data()

with app.app_context():
    db.create_all()  
    seed_data() 

@app.route("/")
@app.route('/index')
def index():
    if not 'login' in dict(session).keys():
        return  render_template('index.html')
    return render_template('index.html', login=session['login'])

@app.route('/json-rpc-api/', methods=['POST'])
def json_rpc_api():
    data = request.json
    method = data.get('method')
    request_id = data.get('id', None)

    if method == 'list':
        furniture_list = furniture.query.order_by(furniture.id).all()
        result = [
            {
                'id': item.id,
                'name': item.name,
                'description': item.description,
                'price': item.price
            }
                for item in furniture_list
            ]
        return jsonify({
                'jsonrpc': '2.0',
                'result': result,
                'id': request_id
        })

       
    return jsonify({
        'jsonrpc': '2.0',
        'error': {
                'code': -32601,
                'message': 'Method not found'
            },
        'id': request_id
    })

@app.route('/register', methods=['POST'])
def register():
    data = request.json
    username = data.get('username')
    password = data.get('password')

    if not username or not password:
        return jsonify({'error': {'message': 'Логин и пароль обязательны'}}), 400

    existing_user = users.query.filter_by(login=username).first()
    if existing_user:
        return jsonify({'error': {'message': 'Логин уже используется'}}), 400

    hashed_password = generate_password_hash(password)
    new_user = users(login=username, password=hashed_password)
    db.session.add(new_user)
    db.session.commit()

    session['login'] = username
    return jsonify({'message': 'Регистрация успешна'})


@app.route('/login', methods=['POST'])
def login():
    data = request.json
    username = data.get('username')
    password = data.get('password')

    if not username or not password:
        return jsonify({'error': {'message': 'Логин и пароль обязательны'}}), 400

    user = users.query.filter_by(login=username).first()
    if not user or not check_password_hash(user.password, password):
        return jsonify({'error': {'message': 'Неверный логин или пароль'}}), 400

    session['login'] = username
    return jsonify({'message': 'Вход выполнен успешно'})


@app.route('/logout', methods=['POST'])
def logout():
    session.pop('login', None)
    return jsonify({'message': 'Выход выполнен успешно'})

@app.errorhandler(404)
def not_found(err):
    path = url_for('static', filename='404-error.jpg')
    return '''<!doctype html> 
        <html>
            <head>
            <style>
            body {
                background-color: black;
                font-weight: bold;
                color: red
            }
            h1 {
                margin-left: 45%
            }
            </style>
            </head>
           <body>
               <h1>Ошибка 404</h1>
               <img src='''f"""{path}>
            </body>
        </html>""", 400

@app.errorhandler(500)
def server_err(err):
    return 'Ошибка сервера! Сервер временно не отвечает'