#!/usr/bin/python
from flask import Flask, render_template, request, jsonify, flash, url_for, redirect
from app import app, db
import requests
import json
from .form import LoginForm, RegForm
from .models import Customer

@app.route('/', methods = ['GET', 'POST'])
@app.route('/index', methods = ['GET', 'POST'])
def index():
    logForm = LoginForm()
    if logForm.validate_on_submit():
        check(logForm.uname.data, None, str(logForm.psw.data))
    return render_template("index.html",
        form = logForm)

@app.route('/reg', methods = ['GET', 'POST'])
def reg():
    regForm = RegForm()
    if regForm.validate_on_submit():
        check(regForm.uname.data, regForm.mail.data, str(regForm.psw.data))
        return redirect('/index')
    return render_template("reg.html",
    	form = regForm)

def check(uname, email, psw):
    if email is None:
        user = Customer.query.filter_by(name = uname).first()
        if user is None:
            return flash('User doesnt exist')
        else:
            if psw == user.pswd:
                return flash('User login success')
            else:
                return flash('Wrong Password')
    else:
        user = Customer.query.filter_by(mail = email).first()
        if user is None:
            user = Customer(name = uname, mail = email, pswd = psw)
            db.session.add(user)
            db.session.commit()
            return flash('User create')
        else:
            return flash('User with this email already exist')

@app.route('/usercheck', methods = ['POST'])
def usercheck():
    uname = request.json['name']
    user = Customer.query.filter_by(name = uname).first()
    if user is None:
        return jsonify({"module":'customers', 'type':'check_customer', 'is_customer':'no'})
    else:
        return jsonify({"module":'customers', 'type':'check_customer', 'is_customer':'yes'})