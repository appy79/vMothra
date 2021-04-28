from flask import render_template, request, Blueprint, redirect, url_for, flash, abort
from flask_login import current_user, login_required
from mothra import db
from mothra.models import User, Submission, Attempts, Answer, Notification, Announcement, Stats
from mothra.forms import SubmissionForm
from mothra.views import classify
from datetime import datetime


challenges = Blueprint('challenges', __name__)

# SUBMISSION HANDLING

def sub(form):
    now=datetime.now()
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
        message = "Oops! Your Submission for the "+classify[current_user.level+1] + " upgrade on "+now.strftime("%d %b %Y at %I:%M %p")+" has been auto rejected because your answer was incorrect."
    else:
        correct=1
        message = "Your Submission for the "+classify[current_user.level+1] + " upgrade on "+now.strftime("%d %b %Y at %I:%M %p")+" has been sent for review. Please wait for some time."
    sub=form.sub.data
    submission=Submission(ans=ans, sub=sub, correct=correct)
    notification=Notification(uid=current_user.id, message=message)
    flash(message)
    db.session.add(submission)
    db.session.add(notification)
    db.session.commit()


# MESSAGING

@challenges.route('/notifications')
@login_required
def notifications():
    notifs=Notification.query.filter_by(uid=current_user.id).all()
    notifs.reverse()
    count=Notification.query.filter_by(uid=current_user.id).count()
    current_user.notif_count=count
    db.session.commit()
    return render_template('notifications.html', notifs=notifs)


@challenges.route('/announcements')
@login_required
def announcements():
    ancmts=Announcement.query.all()
    ancmts.reverse()
    return render_template('announcements.html', ancmts=ancmts)




#CHALLENGE ROUTES

@challenges.route('/noob', methods=['GET', 'POST'])
@login_required
def noob():
    if current_user.level>0 and current_user.user_type!="Godzilla":
        stats=Stats.query.filter_by(level=1, uid=current_user.id).first()
        return render_template('challenges/chal_1.html', stats=stats)
    else:
        form=SubmissionForm()
        if form.validate_on_submit():
            sub(form)
            return redirect(url_for('challenges.noob', form=form))

        return render_template('challenges/chal_1.html', form=form)

@challenges.route('/unknown', methods=['GET', 'POST'])
@login_required
def unknown():
    if current_user.level<1:
        abort(403)
    elif current_user.level>1 and current_user.user_type!="Godzilla":
        stats=Stats.query.filter_by(level=2, uid=current_user.id).first()
        return render_template('challenges/chal_2.html', stats=stats)
    else:
        form=SubmissionForm()
        if form.validate_on_submit():
            sub(form)
            return redirect(url_for('challenges.unknown', form=form))

        return render_template('challenges/chal_2.html', form=form)

@challenges.route('/amateur', methods=['GET', 'POST'])
@login_required
def amateur():
    if current_user.level<2:
        abort(403)

    elif current_user.level>2 and current_user.user_type!="Godzilla":
        stats=Stats.query.filter_by(level=3, uid=current_user.id).first()
        return render_template('challenges/chal_3.html', stats=stats)
    else:
        form=SubmissionForm()
        if form.validate_on_submit():
            sub(form)
            return redirect(url_for('challenges.amateur', form=form))

        return render_template('challenges/chal_3.html', form=form)

@challenges.route('/average', methods=['GET', 'POST'])
@login_required
def average():
    if current_user.level<3:
        abort(403)

    elif current_user.level>3 and current_user.user_type!="Godzilla":
        stats=Stats.query.filter_by(level=4, uid=current_user.id).first()
        return render_template('challenges/chal_4.html', stats=stats)
    else:
        form=SubmissionForm()
        if form.validate_on_submit():
            sub(form)
            return redirect(url_for('challenges.average', form=form))

        return render_template('challenges/chal_4.html', form=form)

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
