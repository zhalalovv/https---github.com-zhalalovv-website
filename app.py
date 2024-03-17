# -*- coding: UTF-8 -*-
import os

from flask import Flask, g, render_template, request, jsonify, url_for, send_file
from models import db_session, Restaurant, Dish, Order, OrderDish

import settings

app = Flask(__name__, template_folder="templates")

app.config['SECRET_KEY'] = settings.SECRET_KEY

#restourantsDataBase = [
#{'id': 1, 'restourant': 'Zotman pizza', 'rating': 4.9, 'feedback': 'Отлично', 'image': 'images/zotman/zotman.jpg', 'href': '/zotmanpizza'},
#{'id': 2, 'restourant': 'Burger King', 'rating' : 4.5, 'feedback': 'Хорошо', 'image': 'images/burgerking/burgerking.jpg', 'href': '/burgerking'},
#{'id': 3, 'restourant': 'Vanvok', 'rating': 4.7, 'feedback': 'Отлично', 'image': 'images/vanvok/vanvok.jpg', 'href': '/vanvok'},
#{'id': 4, 'restourant': 'Вкусно и точка', 'rating': 4.8, 'feedback': 'Отлично','image': 'images/mac/mac.jpg', 'href': '/mac'},
#{'id': 5, 'restourant': 'KFC', 'rating': 5, 'feedback': 'Отлично', 'image': 'images/kfc/kfc.jpg', 'href': '/kfc'},
#{'id': 6, 'restourant': 'Кебабник', 'rating': 4.8, 'feedback': 'Хорошо', 'image': 'images/kebabnik/kebabnik.jpg', 'href': '/kebabnik'},
#]

@app.errorhandler(404)
def page_not_found(error):
    return render_template('404.htm'), 404

@app.route("/")
def index():
    restaurants = db_session.query(Restaurant).all()
    return render_template("index.html", rest = restaurants)

@app.route("/login")
def login():
    return render_template("login.html")

@app.route("/registration")
def registration():
    return render_template("registration.html")

@app.route("/search")
def search():
    return render_template("search_res.html")

@app.route("/zotmanpizza")
def zotman():
    return render_template("zotmanpizza.html")

@app.route("/burgerking")
def burgerking():
    return render_template("burgerking.html")

@app.route("/vanvok")
def vanvok():
    return render_template("vanvok.html")

@app.route("/mac")
def mac():
    return render_template("mac.html")

@app.route("/kfc")
def kfc():
    return render_template("kfc.html")

@app.route("/kebabnik")
def kebabnik():
    return render_template("kebabnik.html")

@app.route("/oplata")
def optala():
    return render_template("oplata.html")

if __name__ == "__main__":
##    #Еще один способ добавления статической дирректории
    from werkzeug.middleware.shared_data import SharedDataMiddleware
    app.wsgi_app = SharedDataMiddleware(app.wsgi_app, {
      '/': os.path.join(os.path.dirname(__file__), 'static')
    })
    app.run(host='0.0.0.0', port=5000, debug=True)
    