from flask import render_template, request, Blueprint, redirect, url_for, flash
from mothra import app,db
from flask_login import login_user, login_required, logout_user, current_user
from mothra.models import User
from mothra.forms import LoginForm, RegistrationForm

my_view = Blueprint('my_view', __name__)

classify=['born','noob','unknown','amateur','average','working','famous','creator','wip']

@app.context_processor
def inject_level():
    def getlev():
        if current_user.is_authenticated:
            lev=classify[current_user.level]
        else:
            lev='Non-Existent'
        return lev
    def clss():
        return classify[1:current_user.level+2]
    return dict(getlev=getlev, clss=clss)

# General Views

@app.route('/')
def index():
    return render_template('home.html')

@app.route('/register', methods=['POST','GET'])
def register():
    form = RegistrationForm()

    if form.validate_on_submit():
        user = User(roll=form.roll.data,
                    username=form.username.data,
                    password=form.password.data,
                    user_type=form.user_type.data,
                    level=form.level.data)

        db.session.add(user)
        db.session.commit()
        return redirect(url_for('login'))
    return render_template('register.html', form=form)

@app.route('/login', methods=['POST','GET'])
def login():
    form=LoginForm()
    if form.validate_on_submit():
        user=User.query.filter_by(roll=form.roll.data).first()
        if user.check_password(form.password.data) and user is not None:
            login_user(user)
            next=request.args.get('next')
            if next==None or not not next[0]=='/':
                next=url_for('index')
            return redirect(next)

        else:
            flash("Username or Password is incorrect!")
    return render_template('login.html', form=form)

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))

@app.route('/leaderboard')
def leaderboard():
    return render_template('leaderboard.html')

@app.route('/instructions')
def instructions():
    return render_template('instructions.html')



# CHALLENGES

@app.route('/locked')
@login_required
def locked():
    return render_template('locked.html')

@app.route('/hunting')
@login_required
def hunting():
    le=current_user.level
    return redirect(url_for(classify[le+1]))

@app.route('/noob')
@login_required
def noob():
    return render_template('chal_1.html')

@app.route('/unknown')
@login_required
def unknown():
    if current_user.level<1:
        return redirect('locked')
    return render_template('chal_2.html')

@app.route('/amateur')
@login_required
def amateur():
    if current_user.level<2:
        return redirect('locked')
    return render_template('chal_3.html')

@app.route('/average')
@login_required
def average():
    if current_user.level<3:
        return redirect('locked')
    return render_template('chal_4.html')

@app.route('/working')
@login_required
def working():
    return render_template('wip.html')

@app.route('/famous')
@login_required
def famous():
    return render_template('wip.html')

@app.route('/creator')
@login_required
def creator():
    return render_template('wip.html')

@app.route('/wip')
@login_required
def wip():
    return render_template('wip.html')
