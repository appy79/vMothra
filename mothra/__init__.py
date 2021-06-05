import os, time
from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from datetime import datetime

os.environ['TZ'] = 'Asia/Kolkata'
time.tzset()

start=datetime(2021, 5, 11, 18, 00, 00 )
end=datetime(2021, 5, 14, 12, 00, 00)
inno_end=datetime(2021, 5, 16, 21, 00, 00)

app = Flask(__name__)

app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY)

app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False


db = SQLAlchemy(app)
migrate = Migrate(app,db)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

from mothra import views

from mothra.error_pages.handlers import error_pages
app.register_blueprint(error_pages)

from mothra.challenges.views import challenges
app.register_blueprint(challenges)

from mothra.godzilla.views import godzilla
app.register_blueprint(godzilla)
