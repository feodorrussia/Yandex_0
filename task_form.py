from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField, DateTimeField, IntegerField, BooleanField, SelectField
from wtforms.validators import DataRequired
from database import *


class TaskModel(FlaskForm):
    title = StringField('Название', validators=[DataRequired()])
    description = TextAreaField('Описание', validators=[DataRequired()])
    deadline = DateTimeField('Дата выполнения (в формате год-месяц-день час:мин:сек)', validators=[DataRequired()])
    users = db.session.query(User).all()
    users = [(str(i.username), str(i.username)) for i in users]
    performer_name = SelectField('Имя исполнителя', choices=users)
    cats = db.session.query(Category).all()
    cats = [(str(i.category), str(i.category)) for i in cats]
    category_name = SelectField('Название категории', choices=cats)
    priority = SelectField('Приоритет', choices=[('низкий', 'низкий'), ('средний', 'средний'), ('высокий', 'высокий')])
    step = TextAreaField('Этап исполнения')
    done = BooleanField('Выполнено')
    submit = SubmitField('Добавить')
