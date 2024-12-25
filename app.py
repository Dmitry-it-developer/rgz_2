from flask import Flask, url_for, redirect, render_template
from flask_sqlalchemy import SQLAlchemy
import os
from os import path
from db import db

app = Flask(__name__)

app.config['SECRET_KEY'] = 'секретныйкод'
app.config['DB_TYPE'] = 'sqlite'


dir_path = path.dirname(path.realpath(__file__))
db_path = path.join(dir_path, 'furniture.db')
app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{db_path}'

db.init_app(app)

@app.route("/")
@app.route('/index')
def index():
    return  render_template('index.html')