#!/usr/bin/python
from flask import Flask, render_template, request, jsonify, flash, url_for, redirect
from app import app
import requests
import json
from jwcrypto import jwt, jwk
from .form import AddForm, RemoveForm
token = None

@app.route('/', methods = ['GET', 'POST'])
def index():
    return render_template("index.html", t=token)

@app.route('/add', methods = ['GET', 'POST'])
def add():
    global token
    addForm = AddForm()
    if request.method == 'GET':
        return render_template("add.html", form=addForm)
    if addForm.validate_on_submit():
        #flash('Requested for Supplyer="' + addForm.supplyer.data 
        #    + '", Title=' + addForm.title.data
        #    + '", Count=' + str(addForm.count.data)
        #    + '", Staffname=' + addForm.staffname.data)
        #get token from browser
        #if token != t:
        #flash('token error')
        #return render_template("index.html")
        resp = requests.post('http://staff-server/check_rights', headers={'Content-Type': 'application/json'},
            data=json.dumps({"module":"transfer", "type":"check_rights", "name": addForm.staffname.data}))
        buf = json.loads(resp.text)
        if buf['status'] == 'name_error':
            flash('name error')
            return render_template("index.html")
        elif int(buf['rights']) == 2 or int(buf['rights']) == 3:
            flash('rights error')
            return render_template("index.html")
        else:
            resp = requests.post('http://goods-server/add', headers={'Content-Type': 'application/json'}, 
                data=json.dumps({"module": "transfer", "type": "add_goods", "title": addForm.title.data, "count": str(addForm.count.data)}))
            buf = json.loads(resp.text)
            if buf['status'] == 'ok':
                flash('Ok')
                #return render_template("add.html", form = addForm)
                return render_template("index.html")
            else:
                flash('goods error')
                return render_template("index.html")

@app.route('/remove', methods = ['GET', 'POST'])
def remove():
    global token
    removeForm = RemoveForm()
    if request.method == 'GET':
        return render_template('remove.html', form=removeForm)
    if removeForm.validate_on_submit():
        #flash('Requested for Username="' + removeForm.uname.data 
        #	+ '", Title=' + removeForm.title.data
        #    + '", Count=' + str(removeForm.count.data)
        #    + '", Staffname=' + removeForm.staffname.data)
        #get token from browser
        #if token != t:
        #flash('token error')
        #return render_template("index.html")
        resp = requests.post('http://customers-server/usercheck', headers={'Content-Type': 'application/json'},
            data=json.dumps({"module":"transfer", "type":"check_customer", "name": removeForm.uname.data}))
        buf = json.loads(resp.text)
        if buf['is_customer'] == 'no':
            flash('uname error')
            return render_template("index.html")
        resp = requests.post('http://staff-server/check_rights', headers={'Content-Type': 'application/json'},
            data=json.dumps({"module":"transfer", "type":"check_rights", "name": removeForm.staffname.data}))
        buf = json.loads(resp.text)
        if buf['status'] == 'name_error':
            flash('staff error')
            return render_template("index.html")
        elif int(buf['rights']) == 1 or int(buf['rights']) == 3:
            flash('rights error')
            return render_template("index.html")
        else:
            resp = requests.post('http://goods-server/delete', headers={'Content-Type': 'application/json'}, 
                data=json.dumps({"module": "transfer", "type": "delete_goods", 
                    "title": removeForm.title.data, "count": str(removeForm.count.data)}))
            buf = json.loads(resp.text)
            if buf['status'] == 'ok':
                flash('Ok')
                #return render_template("remove.html", form = removeForm)
                return render_template("index.html")
            else:
                flash('goods error')
                return render_template("index.html")

@app.route('/token', methods=['POST'])
def token():
    global token
    token = request.json['token']
    return jsonify({'status': 'ok'})