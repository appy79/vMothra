from flask import render_template, request, Blueprint, redirect, url_for, flash, abort
from flask_login import current_user, login_required
from mothra import db
from mothra.models import User, Submission, Attempts, Answer
from mothra.forms import SubmissionForm


challenges = Blueprint('challenges', __name__)

# SUBMISSION HANDLING

def sub(form):
    att=Attempts.query.filter_by(of=current_user.id, stage= current_user.level+1).first()
    if att:
        if att.atmpts==3:
            abort(403)
        else:
            att.atmpts+=1
    else:
        atmpt=Attempts()
        db.session.add(atmpt)
    ans=form.ans.data
    corans=Answer.query.filter_by(stage=current_user.level+1).first()
    if ans!=corans.ans:
        correct=0
    else:
        correct=1
    sub=form.sub.data
    submission=Submission(ans=ans, sub=sub, correct=correct)
    db.session.add(submission)
    db.session.commit()


#CHALLENGE ROUTES

@challenges.route('/noob', methods=['GET', 'POST'])
@login_required
def noob():
    form=SubmissionForm()
    if form.validate_on_submit():
        sub(form)
        return redirect(url_for('challenges.noob', form=form))

    return render_template('chal_1.html', form=form)

@challenges.route('/unknown', methods=['GET', 'POST'])
@login_required
def unknown():
    if current_user.level<1:
        abort(403)

    form=SubmissionForm()
    if form.validate_on_submit():
        sub(form)
        return redirect(url_for('challenges.noob', form=form))

    return render_template('chal_2.html', form=form)

@challenges.route('/amateur', methods=['GET', 'POST'])
@login_required
def amateur():
    if current_user.level<2:
        abort(403)

    form=SubmissionForm()
    if form.validate_on_submit():
        sub(form)
        return redirect(url_for('challenges.noob', form=form))

    return render_template('chal_3.html', form=form)

@challenges.route('/average', methods=['GET', 'POST'])
@login_required
def average():
    if current_user.level<3:
        abort(403)

    form=SubmissionForm()
    if form.validate_on_submit():
        sub(form)
        return redirect(url_for('challenges.noob', form=form))

    return render_template('chal_4.html', form=form)

@challenges.route('/working', methods=['GET', 'POST'])
@login_required
def working():
    if current_user.level<4:
        abort(403)

    return render_template('wip.html')

@challenges.route('/famous', methods=['GET', 'POST'])
@login_required
def famous():
    if current_user.level<5:
        abort(403)

    return render_template('wip.html')

@challenges.route('/creator', methods=['GET', 'POST'])
@login_required
def creator():
    if current_user.level<6:
        abort(403)
        
    return render_template('wip.html')

@challenges.route('/wip', methods=['GET', 'POST'])
@login_required
def wip():
    return render_template('wip.html')
