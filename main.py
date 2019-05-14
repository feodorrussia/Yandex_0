from register_form import RegisterModel
from login_form import LoginForm
from db import DB
from flask import Flask, redirect, render_template, session, request
from users_model import UsersModel
from werkzeug.security import generate_password_hash

app = Flask(__name__)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'
db = DB()


@app.route('/')
@app.route('/index/', methods=['POST', 'GET'])
def index():
    if request.method == 'GET':
        if 'username' not in session:
            if "username" in session:
                return redirect("/logout")
            return redirect('/login')
    return render_template('base.html')


@app.route('/register', methods=['POST', 'GET'])
def register():
    if request.method == 'GET':

        # if 'username' in session:
        #     return redirect('/')
        form = RegisterModel()
        if form.validate_on_submit():
            user_name = form.user_name.data
            password = form.password.data
            password_check = form.password_check.data
            user = UsersModel(db.get_connection())
            flag = user.is_username_busy(user_name)
            if flag and password == password_check:
                user.insert(user_name, password)
                session['username'] = user_name
                hash = generate_password_hash(password)
                exists = user.exists(user_name, password)
                session['user_id'] = exists[1]
                print(hash)
                return render_template('register.html', form=form, error=0)
            elif password != password_check:
                return render_template('register.html', form=form, error=2)
            else:
                return render_template('register.html', form=form, error=1)
        return render_template('register.html', form=form)


@app.route('/login', methods=['GET', 'POST'])
def login():
    global flag_perm
    form = LoginForm()
    if form.validate_on_submit():
        user_name = form.username.data
        password = form.password.data
        perm = form.remember_me.data
        user_model = UsersModel(db.get_connection())
        exists = user_model.exists(user_name, password)
        if exists[0]:
            session['username'] = user_name
            session['user_id'] = exists[1]
            if perm:
                session.permanent = True
                flag_perm = True
            else:
                session.permanent = False
                flag_perm = True
            return redirect("/index")
        else:
            return render_template('login.html', form=form, error=1)
    return render_template('login.html', title='Авторизация', form=form)


@app.route('/logout')
def logout():
    session.pop('username', 0)
    session.pop('user_id', 0)
    return redirect('/login')


UsersModel(db.get_connection()).init_table()

if __name__ == '__main__':
    app.run(port=8080, host='127.0.0.1', debug=True)
