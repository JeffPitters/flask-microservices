from flask import Flask, render_template, request, jsonify, flash, url_for, redirect
from app import app, db
import requests
import json
from sqlalchemy import desc
from jwcrypto import jwt, jwk
from .models import Goods
token = None

@app.route('/', methods = ['GET', 'POST'])
def index():
    global token
    #t = request.json['data']
    t = token
    if token != t:
        flash('token error')
        return render_template("index.html")
    rows = db.session.query(Goods).all()
    return render_template("index.html", items=rows)

@app.route('/add', methods = ['POST'])
def add():
    t = request.json['title']
    c = int(request.json['count'])
    item = Goods.query.filter_by(title = t).first()
    if item == None:
        item = Goods(title = t, count = c)
        db.session.add(item)
        db.session.commit()
        return jsonify({'module':'goods', 'type':'add_goods', 'status': 'ok'})
    else:
        newcount = item.count+c
        Goods.query.filter_by(title=t).update(dict(count=newcount))
        db.session.commit()
        return jsonify({'module':'goods', 'type':'add_goods', 'status': 'ok'})

@app.route('/delete', methods = ['POST'])
def delete():
    t = request.json['title']
    c = int(request.json['count'])
    item = Goods.query.filter_by(title = t).first()
    if item == None:
        return jsonify({'module':'goods', 'type':'delete_goods', 'status': 'title_error'})
    elif c > item.count:
        return jsonify({'module':'goods', 'type':'delete_goods', 'status': 'count_error'})
    else:
        newcount = item.count - c
        if newcount == 0:
            Goods.query.filter(Goods.title == t).delete()
            #db.session.delete(item)
            db.session.commit()
            return jsonify({'module':'goods', 'type':'delete_goods', 'status': 'ok'})
        else:
            Goods.query.filter_by(title=t).update(dict(count=newcount))
            db.session.commit()
            return jsonify({'module':'goods', 'type':'delete_goods', 'status': 'ok'})

@app.route('/check', methods = ['POST'])
def check():
    t = request.json['title']
    item = Goods.query.filter_by(title = t).first()
    if item == None:
        return jsonify({'module': 'goods', 'type': 'check_goods', 'title': 'tite_error'})
    else:
        return jsonify({'module': 'goods', 'type': 'check_goods', 'title': t, 'count': str(item.count)})

@app.route('/token', methods=['POST'])
def token():
    global token
    token = request.json['token']
    return jsonify({'status': 'ok'})