from flask import render_template, request, Blueprint, redirect, url_for, flash, abort
from flask_login import current_user, login_required
from mothra import db
from mothra.models import User, Submission, Answer
from mothra.forms import AnswerFillingForm, ReviewForm

godzilla = Blueprint('godzilla', __name__)

def godzilla_check():
    if current_user.user_type!='Godzilla':
        abort(403)

@godzilla.route('/admin_dash')
@login_required
def admin_dash():
    godzilla_check()
    return render_template('admin_dash.html')


@godzilla.route('/corans', methods=['GET', 'POST'])
@login_required
def corans():
    godzilla_check()
    form=AnswerFillingForm()
    stages=Answer.query.all()
    if form.validate_on_submit():
        answer = Answer(stage=form.stage.data,
                    ans=form.ans.data)

        db.session.add(answer)
        db.session.commit()
        return redirect(url_for('godzilla.corans', form=form, stages=stages))

    return render_template('ans_filling.html', form=form, stages=stages)


@godzilla.route('/review', methods=['GET','POST'])
@login_required
def review():
    godzilla_check()
    form=ReviewForm()
    submissions = Submission.query.filter_by(correct=1).all()

    return render_template('review.html', submissions=submissions, form=form)

@godzilla.route('/checking_<submission_id>', methods=['GET','POST'])
@login_required
def checking(submission_id):
    form=ReviewForm()
    if form.validate_on_submit():
        submission=Submission.query.filter_by(id=submission_id).first()
        user=User.query.filter_by(id=submission.by).first()
        if form.review.data=='Accept':
            submission.correct=2
            user.level+=1
        else:
            submission.correct=0

        db.session.commit()

    return redirect(url_for('godzilla.review'))
