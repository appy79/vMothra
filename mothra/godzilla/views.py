from flask import render_template, request, Blueprint, redirect, url_for, flash, abort
from flask_login import current_user, login_required
from mothra import db
from mothra.models import User, Submission, Stages
from mothra.forms import AnswerFillingForm

godzilla = Blueprint('godzilla', __name__)

def godzilla_check():
    if current_user.user_type!='Godzilla':
        abort(403)

@godzilla.route('/admin_dash')
@login_required
def admin_dash():
    godzilla_check()
    return render_template('admin_dash.html')


@godzilla.route('/corans')
@login_required
def corans():
    godzilla_check()
    form=AnswerFillingForm()
    if form.validate_on_submit():

        return redirect('ans_filling.html')
    return render_template('ans_filling.html')
