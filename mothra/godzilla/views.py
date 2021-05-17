from flask import render_template, request, Blueprint, redirect, url_for, flash, abort
from flask_login import current_user, login_required
from mothra import db
from mothra.models import User, Submission, Answer, Notification, Announcement, Stats, Feedback
from mothra.forms import AnswerFillingForm, ReviewForm, AnnounceForm, NotifForm
from mothra.views import classify
from datetime import datetime

godzilla = Blueprint('godzilla', __name__)

def godzilla_check():
    if current_user.user_type!='Godzilla':
        abort(403)

@godzilla.route('/admin_dash')
@login_required
def admin_dash():
    godzilla_check()
    return render_template('godzilla/admin_dash.html')


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

    return render_template('godzilla/ans_filling.html', form=form, stages=stages)


@godzilla.route('/review', methods=['GET','POST'])
@login_required
def review():
    godzilla_check()
    form=ReviewForm()
    submissions = Submission.query.filter_by(correct=1).all()
    users=User.query.all()

    return render_template('godzilla/review.html', submissions=submissions, form=form, users=users)

@godzilla.route('/checking_<submission_id>', methods=['GET','POST'])
@login_required
def checking(submission_id):
    now=datetime.now()
    godzilla_check()
    form=ReviewForm()
    if form.validate_on_submit():
        submission=Submission.query.filter_by(id=submission_id).first()
        user=User.query.filter_by(id=submission.by).first()
        if form.review.data=='Accept':
            submission.correct=2
            if user.level==submission.stage:
                message="Your Submission for the "+classify[user.level] +" upgrade on "+now.strftime("%d %b %Y at %I:%M %p")+" has been rejected because one of your previous submissions for this upgrade have been accepted."
            else:
                message = "Congratulations! Your Submission for the "+classify[user.level+1] +" upgrade on "+now.strftime("%d %b %Y at %I:%M %p")+" has been accepted. You are now promoted to " +classify[user.level+1]
                user.level=submission.stage
                user.upgrade_time=submission.time
                stat=Stats(uid=user.id, level=user.level, uptime=submission.time)
                db.session.add(stat)
        else:
            submission.correct=0
            message = "Oops! Your Submission for the "+classify[user.level+1] + " upgrade on "+now.strftime("%d %b %Y at %I:%M %p")+" did not meet the requirements for the upgrade."

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
    return render_template('godzilla/announce.html', form=form)


@godzilla.route('/all_users')
@login_required
def all_users():
    godzilla_check()
    users=User.query.order_by(User.id.asc()).all()
    return render_template('godzilla/users.html', users=users)


@godzilla.route('/dnotif', methods=['GET','POST'])
@login_required
def dnotif():
    godzilla_check()
    form=NotifForm()
    if form.validate_on_submit():
        notif=Notification(uid=form.uid.data, message=form.message.data)
        db.session.add(notif)
        db.session.commit()
        return redirect(url_for('godzilla.dnotif'))
    return render_template('godzilla/dnotif.html', form=form)



@godzilla.route('/all_subs')
@login_required
def all_subs():
    godzilla_check()
    submissions = Submission.query.order_by(Submission.time.desc()).all()
    users=User.query.all()
    return render_template('godzilla/all_subs.html', submissions=submissions, users=users)


@godzilla.route('/all_feeds')
@login_required
def all_feeds():
    godzilla_check()
    feedbacks = Feedback.query.order_by(Feedback.id.desc()).all()
    users=User.query.all()
    return render_template('godzilla/all_feeds.html', feedbacks=feedbacks, users=users)
