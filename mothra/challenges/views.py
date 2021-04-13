from flask import render_template, request, Blueprint, redirect, url_for, flash, abort
from flask_login import current_user, login_required
from mothra import db
from mothra.models import User, Submission
from mothra.forms import SubmissionForm


challenges = Blueprint('challenges', __name__)


@challenges.route('/noob')
@login_required
def noob():
    form=SubmissionForm()
    if form.validate_on_submit():
        ans=form.ans.data
        sub=form.sub.data

    return render_template('chal_1.html', form=form)

@challenges.route('/unknown')
@login_required
def unknown():
    if current_user.level<1:
        abort(403)
    form=SubmissionForm()
    return render_template('chal_2.html', form=form)

@challenges.route('/amateur')
@login_required
def amateur():
    if current_user.level<2:
        abort(403)
    form=SubmissionForm()
    return render_template('chal_3.html', form=form)

@challenges.route('/average')
@login_required
def average():
    if current_user.level<3:
        abort(403)
    form=SubmissionForm()
    return render_template('chal_4.html', form=form)

@challenges.route('/working')
@login_required
def working():
    if current_user.level<4:
        abort(403)
    return render_template('wip.html')

@challenges.route('/famous')
@login_required
def famous():
    if current_user.level<5:
        abort(403)
    return render_template('wip.html')

@challenges.route('/creator')
@login_required
def creator():
    if current_user.level<6:
        abort(403)
    return render_template('wip.html')

@challenges.route('/wip')
@login_required
def wip():
    return render_template('wip.html')
