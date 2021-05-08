from flask import render_template, request, Blueprint, redirect, url_for, flash, abort
from mothra import app,db
from flask_login import login_user, login_required, logout_user, current_user
from mothra.models import User, Notification, Announcement
from mothra.forms import LoginForm, RegistrationForm, SubmissionForm, AnswerFillingForm
from datetime import datetime

start=datetime(2021, 5, 11, 12, 00, 00 )
end=datetime(2021, 5, 13, 12, 00, 00)

# COMMON FUNCTIONS AND OBJECTS

classify=['born','noob','unknown','amateur','average','working','famous','creator','wip']

# CONTEXT PROCESSOR


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

    def show():
        return classify

    def unread():
        count=Notification.query.filter_by(uid=current_user.id).count()
        if count!=current_user.notif_count:
            notifs=count-current_user.notif_count
        else:
            notifs=0
        return notifs

    return dict(getlev=getlev, clss=clss, show=show, unread=unread)



# GENERAL VIEWS

@app.route('/')
def index():
    announcement=Announcement.query.order_by(Announcement.id.desc()).first()
    return render_template('home.html', announcement=announcement)

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
        flash("Thank you for registering " +form.username.data+ ". Please login.")
        return redirect(url_for('login'))
    return render_template('register.html', form=form)

@app.route('/login', methods=['POST','GET'])
def login():
    form=LoginForm()
    if form.validate_on_submit():
        user=User.query.filter_by(roll=form.roll.data).first_or_404()
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
    if datetime.now()<end and current_user.is_anonymous:
        return render_template("lead_wait.html")
    elif datetime.now()<end and current_user.user_type!="Godzilla":
        return render_template("lead_wait.html")
    users=User.query.filter_by(user_type='Mothra').order_by(User.level.desc(), User.upgrade_time.asc()).all()
    return render_template('leaderboard.html', users=users)

@app.route('/instructions')
def instructions():
    return render_template('instructions.html')

@app.route('/hunting')
@login_required
def hunting():
    le=current_user.level
    return redirect(url_for('challenges.'+classify[le+1]))
