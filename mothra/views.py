from flask import render_template, request, Blueprint
from mothra import app

my_view = Blueprint('my_view', __name__)

@app.route('/')
def index():
    return render_template('home.html')
