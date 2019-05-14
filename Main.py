from constant import *
from werkzeug.security import generate_password_hash
from register_form import RegisterModel
from flask import url_for, request, render_template, redirect, session
from flask_sqlalchemy import sqlalchemy
from loginform import *
from add_news import *
from database import *
from task_form import TaskModel
from datetime import datetime


admins = db.session.query(Admins).all()
admins_id = [i.user_id for i in admins]

@app.route('/', methods=['GET', 'POST'])
@app.route('/index')
def index():
    if 'username' not in session:
        return redirect('/login')

    tasks = db.session.query(Task).filter_by(user_id=session['user_id'])

    user_name = session['username']
    user = User.query.filter_by(username=user_name).first()
    task = Task.query.filter_by(user_id=user.id).all()
    bad = [x for x in task if datetime.strptime(x.deadline, '%d.%m.%Y %H:%M') < datetime.now()]
    print(session['user_id'])
    admins = db.session.query(Admins).all()
    admins_id = [i.user_id for i in admins]
    return render_template('index.html', username=session['username'],
                           news=tasks, bad=bad, user_id=session['user_id'], admins_id=admins_id)


@app.route('/register', methods=['POST', 'GET'])
def register():
    form = RegisterModel()
    if request.method == 'GET':
        return render_template('register.html', form=form)
    elif request.method == 'POST':
        if 'username' in session:
            return redirect('/')

        if form.validate_on_submit():
            user_name = form.user_name.data
            password = form.password.data
            password_check = form.password_check.data
            user = db.session.query(User).filter_by(username=user_name).first()
            if not password_check or not password or not user_name:
                return render_template('register.html', form=form, error=2)
            if not user and password == password_check:
                user = User(username=user_name,
                            password=password)
                db.session.add(user)
                db.session.commit()
                return render_template('register.html', form=form, error=0)
            elif password != password_check:
                return render_template('register.html', form=form, error=2)
            else:
                return render_template('register.html', form=form, error=1)
        else:
            return render_template('register.html', form=form, error=2)


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if request.method == 'GET':
        return render_template('login.html', title='Авторизация', form=form)
    elif request.method == 'POST':
        user_name = form.username.data
        password = form.password.data
        user = db.session.query(User).filter_by(username=user_name).first()

        if password and user_name:
            if user and user.password == str(password):
                session.clear()
                session['username'] = user.username
                session['user_id'] = user.id
                return redirect('/index')
            else:
                return redirect('/register')
        else:
            return redirect('/login')
    else:
        return redirect('/login')


@app.route('/logout')
def logout():
    session.pop('username', 0)
    session.pop('user_id', 0)
    return redirect('/login')


@app.route('/admins_console')
def admins_console():
    if 'user_id' not in session:
        return redirect('/index')
    if not db.session.query(Admins).filter_by(user_id=session['user_id']).first():
        return redirect('/index')
    attemp = db.session.query(Task).all()

    return render_template('admins_console.html', title='Админ', attemp=attemp)


# @app.route('/edit_attemp/<int:id>')
# def edit_attemp(id):
#     if not db.session.query(Admins).filter_by(user_id=session['user_id']).first():
#         return redirect('/index')
#
#     a = db.session.query(Task).filter_by(id=id).first()
#     if a.status:
#         a.status = False
#     else:
#         a.status = True
#     db.session.commit()
#     return redirect('/admins_console')


@app.route('/add_task/<int:f>', methods=['GET', 'POST'])
def add_task(f):
    if 'username' not in session:
        return render_template('error.html')
    if f == 0:
        form = TaskModel()
        if form.validate_on_submit():
            title = form.title.data
            description = form.description.data
            deadline = form.deadline.data
            performer_name = form.performer_name.data
            category_name = form.category_name.data
            priority = form.priority.data
            step = form.step.data
            done = form.done.data
            if done == 0:
                done = False
            else:
                done = True
            datetime_string_format = '%d.%m.%Y %H:%M'
            task = Task(user_id=session['user_id'], title=title,
                        description=description,
                        deadline=deadline.strftime(datetime_string_format),
                        performer_name=performer_name)
                        # category_name=category_name,
                        # priority=priority,
                        # step=step,
                        # done=done)
            db.session.add(task)
            db.session.commit()
            return redirect("/index")
        else:
            return render_template('add_news.html', title='Добавление задачи',
                                   form=form, username=session['username'])
    else:
        form = TaskModel()
        if form.validate_on_submit():
            task = db.session.query(Task).filter_by(user_id=session['user_id']).all()[f-1]
            task.title = form.title.data
            task.description = form.description.data
            task.deadline = form.deadline.data.strftime('%d.%m.%Y %H:%M')
            task.performer_name = form.performer_name.data
            task.category_name = form.category_name.data
            task.priority = form.priority.data
            task.step = form.step.data
            done = form.done.data
            if done == 0:
                task.done = False
            else:
                task.done = True
            db.session.add(task)
            db.session.commit()
            return redirect("/index")
        else:
            return render_template('add_news.html', title='Редактирование задачи',
                                   form=form, username=session['username'])


@app.route('/site_users')
def site_users():
    if 'username' not in session:
        return redirect('/login')
    admins = db.session.query(Admins).all()
    admins_id = [i.user_id for i in admins]
    if session['user_id'] not in admins_id:
        return redirect('/')
    all_users = db.session.query(User).all()
    print(admins_id)
    return render_template('site_users.html', users=all_users, admins_id=admins_id, username=session['username'],
                           user_id=session['user_id'])


@app.route('/set_admin/<user_id>')
def set_admin(user_id):
    admin = Admins(user_id=user_id)
    db.session.add(admin)
    db.session.commit()
    all_users = db.session.query(User).all()
    admins = db.session.query(Admins).all()
    admins_id = [i.user_id for i in admins]
    print(admins_id)
    return render_template('site_users.html', users=all_users, admins_id=admins_id, username=session['username'],
                           user_id=session['user_id'])


@app.route('/delete_task/<int:news_id>', methods=['GET'])
def delete_task(news_id):
    if 'username' not in session:
        return redirect('/login')

    nm = db.session.query(Task).filter_by(id=news_id).all()[0]
    nm.title = 'Удалено'

    db.session.commit()
    return redirect("/index")


if __name__ == '__main__':
    app.run(port=8000, host='127.0.0.1')
