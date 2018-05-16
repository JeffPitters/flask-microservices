#!/usr/bin/python
from flask import Flask, render_template, request, jsonify, flash, url_for, redirect
from app import app, db
import requests
import json
from jwcrypto import jwt, jwk
from .form import LoginForm, RegForm
from .models import Staff
token = None
key = jwk.JWK(generate='oct', size=256)

@app.route('/', methods = ['GET', 'POST'])
def index():
    logForm = LoginForm()
    if logForm.validate_on_submit():
        ok = check(logForm.uname.data, str(logForm.psw.data), None, None, None)
        if ok == 1:
            return redirect("http://localhost:6003", code=302)
    return render_template("index.html",
        form = logForm, t=token)

@app.route('/reg', methods = ['GET', 'POST'])
def reg():
    regForm = RegForm()
    if regForm.validate_on_submit():
        ok = check(regForm.uname.data, 
                str(regForm.psw.data), 
                regForm.rights.data, 
                regForm.adder_name.data, 
                str(regForm.adder_psw.data))
        if ok == 1:
            return redirect("http://localhost:6003", code=302)
        else:
            return redirect('/index')
    return render_template("reg.html",
        form = regForm)

def check(uname, psw, right, adder, adder_psw):
    global key
    global token
    if adder is None:
        staff = Staff.query.filter_by(name = uname).first()
        if staff is None:
            flash('This staff doesnt exist')
            return 0
        else:
            if psw == staff.pswd:
                #add JWT, start JWT session
                Token = jwt.JWT(header={"alg": "HS256"},
                    claims={"name": uname})
                Token.make_signed_token(key)
                Etoken = jwt.JWT(header={"alg": "A256KW", "enc": "A256CBC-HS512"},
                     claims=Token.serialize())
                Etoken.make_encrypted_token(key)
                token = Etoken.serialize()
                requests.post('http://transfer-server/token', headers={'Content-Type': 'application/json'},
                    data=json.dumps({"token": token}))
                requests.post('http://goods-server/token', headers={'Content-Type': 'application/json'},
                    data=json.dumps({"token": token}))
                flash( token )
                flash('Login success')
                return 1
            else:
                flash('Wrong password')
                return 0
    else:
        staff = Staff.query.filter_by(name = uname).first()
        if staff is not None:
            flash('This staff already exist')
            return 0
        else:
            staff = Staff.query.filter_by(name = adder).first()
            if staff is None:
                flash('Adder doesnt exist')
                return 0
            else:
                if staff.rights > 2:
                    new = Staff(name = uname, pswd = psw, rights = right)
                    db.session.add(new)
                    db.session.commit()
                    #add JWT, start JWT session
                    Token = jwt.JWT(header={"alg": "HS256"},
                        claims={"name": uname})
                    Token.make_signed_token(key)
                    Etoken = jwt.JWT(header={"alg": "A256KW", "enc": "A256CBC-HS512"},
                        claims=Token.serialize())
                    Etoken.make_encrypted_token(key)
                    token = Etoken.serialize()
                    requests.post('http://transfer-server/token', headers={'Content-Type': 'application/json'},
                        data=json.dumps({"token": token}))
                    requests.post('http://goods-server/token', headers={'Content-Type': 'application/json'},
                        data=json.dumps({"token": token}))
                    flash('Staff add successfuly')
                    return 1
                else:
                    flash('Adder`s rights are low')
                    return 0

@app.route('/check_rights', methods = ['POST'])
def check_rights():
    global key
    n = request.json['name']
    staff = Staff.query.filter_by(name = n).first()
    if staff == None:
        return jsonify({'module':'staff', 'type':'check_rights', 'status':'name_error'})
    else:
        return jsonify({'module':'staff', 'type':'check_rights','status':'ok', 'rights': str(staff.rights)})