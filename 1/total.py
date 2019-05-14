from flask import Flask, url_for, session, redirect, render_template, request, jsonify, \
    make_response, \
    request
import os
import datetime
from json import load

app = Flask(__name__)
app.secret_key = 'any random string'
UPLOAD_FOLDER = "Загрузки"
delivery = {'Курьером(по г.Пенза)': 1, 'Почта России': 2, 'DPD': 3}


@app.route('/')
@app.route('/title')
def title():
    if 'username' not in session:
        return render_template('title_out.html', text1=open('text_init.txt').read())
    if session['user_id'] == 1:
        return redirect("/title_admin")
    return render_template('title_in.html', text1=open('text_init.txt').read(),
                           username=session['username'])


@app.route('/login')
def login():
    pass


@app.route('/register')
def register():
    pass
