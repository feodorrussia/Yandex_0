from register_form import RegisterModel
from flask import Flask, url_for, session, redirect, render_template, request, jsonify, \
    make_response, \
    request
from werkzeug.security import generate_password_hash
from database import *
from constants import *
import os
import datetime
from json import load




@app.route('/')
@app.route('/title')
def title():
    session.pop('username', 0)
    session.pop('user_id', 0)
    if 'username' not in session:
        return render_template('title_out.html')
    if session['user_id'] == 1:
        return redirect("/title_admin")
    return render_template('title_in.html', text1=open('text_init.txt').read(),
                           username=session['username'])


@app.route('/login', methods=['POST', 'GET'])
def login():
    if request.method == 'GET':
        if 'username' not in session:
            if "username" in session:
                return redirect("/logout")
            return redirect('/login')
        return render_template('login.html')


@app.route('/register', methods=['POST', 'GET'])
def register():
    # if 'username' in session:
    #     return redirect('/')
    form = RegisterModel()
    if form.validate_on_submit():
        user_name = form.user_name.data
        password = form.password.data
        password_check = form.password_check.data
        user = User()
        flag = user.is_username_busy(user_name)
        if flag and password == password_check:
            user.insert(user_name, password)
            session['username'] = user_name
            hash = generate_password_hash(password)
            exists = user.exists(user_name, password)
            session['user_id'] = exists[1]
            return render_template('register.html', form=form, error=0)
        elif password != password_check:
            return render_template('register.html', form=form, error=2)
        else:
            return render_template('register.html', form=form, error=1)
    return render_template('register.html', form=form)


if __name__ == '__main__':
    app.run(port=8080, host='127.0.0.1')
