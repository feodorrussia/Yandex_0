from constants import *


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(120), unique=False, nullable=False)


    def __repr__(self):
        return '<YandexLyceumStudent {} {} {}>'.format(self.id, self.username, self.password)


class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, unique=False, nullable=False)
    title = db.Column(db.String(50), unique=False, nullable=False)
    description = db.Column(db.String(1000), unique=False, nullable=False)
    deadline = db.Column(db.String(50), unique=False, nullable=False)

    performer_id = db.Column(db.Integer, unique=False, nullable=True)
    category_id = db.Column(db.Integer, unique=True, nullable=True)
    priority = db.Column(db.String(10), unique=False, nullable=True)
    step = db.Column(db.String(100), unique=False, nullable=True)
    done = db.Column(db.Boolean, unique=False, nullable=True)


class Admins(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, unique=False, nullable=False)


class Category(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    category = db.Column(db.String(50), unique=True, nullable=False)