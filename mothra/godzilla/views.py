from flask import render_template, request, Blueprint, redirect, url_for, flash, abort
from flask_login import current_user, login_required
from mothra import db
from mothra.models import User, Submission, Answer, Notification, Announcement
from mothra.forms import AnswerFillingForm, ReviewForm, AnnounceForm
from mothra.views import classify

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
    godzilla_check()
    form=ReviewForm()
    if form.validate_on_submit():
        submission=Submission.query.filter_by(id=submission_id).first()
        user=User.query.filter_by(id=submission.by).first()
        if form.review.data=='Accept':
            submission.correct=2
            message = "Congratulations! Your Submission for the "+classify[user.level+1] +" submitted at "+submission.time+" upgrade has been accepted. You are now promoted to " +classify[user.level+1]
            user.level+=1
        else:
            submission.correct=0
            message = "Oops! Your Submission for the "+classify[user.level+1] + " submitted at "+submission.time+" upgrade did not meet the requirements for the upgrade."

        notification=Notification(uid=user.id, message=message)

        db.session.add(notification)

        db.session.commit()

    return redirect(url_for('godzilla.review'))


@godzilla.route('/announce', methods=['GET','POST'])
@login_required
def announce():
    godzilla_check()
    form=AnnounceForm()
    if form.validate_on_submit():
        announcement=Announcement(message=form.message.data)
        db.session.add(announcement)
        db.session.commit()
        return redirect(url_for('godzilla.announce'))
    return render_template('announce.html', form=form)
