from mothra import db,login_manager
from datetime import datetime
from werkzeug.security import generate_password_hash,check_password_hash
from flask_login import UserMixin, current_user

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)

class User(db.Model, UserMixin):

    id = db.Column(db.Integer, primary_key = True)
    roll = db.Column(db.String(64), unique=True, index=True)
    username = db.Column(db.String(64), unique=True, index=True)
    password_hash = db.Column(db.String(128))
    user_type=db.Column(db.String(128), default='Mothra')
    level=db.Column(db.Integer, default=0)

    def __init__(self, roll, username, password,user_type,level):
        self.roll = roll
        self.username = username
        self.password_hash = generate_password_hash(password)
        self.user_type = user_type
        self.level=level

    def check_password(self,password):
        return check_password_hash(self.password_hash,password)

    def __repr__(self):
        return f"{self.roll},{self.username},{self.user_type}"


class Submission(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    by = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
