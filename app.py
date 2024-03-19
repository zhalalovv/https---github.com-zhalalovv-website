# -*- coding: UTF-8 -*-
import os
import uuid
import settings
from flask_login import LoginManager
from flask import Flask, g, render_template


app = Flask(__name__, template_folder="templates")

app.config['SECRET_KEY'] = str(uuid.uuid4())
manager = LoginManager(app)

@app.errorhandler(404)
def page_not_found(error):
    return render_template('404.htm'), 404

@app.route("/")
def index():
    from models import db_session, Restaurant
    restaurants = db_session.query(Restaurant).all()
    return render_template("index.html", rest = restaurants)

@app.route("/login")
def login():
    return render_template("login.html")

# @app.route("/registration")
# def registration():
#     return render_template("registration.html")

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

@manager.user_loader
def load_user(user_id):
    from models import User
    return User.query.get(user_id)


if __name__ == "__main__":
##    #Еще один способ добавления статической дирректории
    from werkzeug.middleware.shared_data import SharedDataMiddleware
    from controller import *
    app.wsgi_app = SharedDataMiddleware(app.wsgi_app, {
      '/': os.path.join(os.path.dirname(__file__), 'static')
    })
    app.run(host='0.0.0.0', port=5000, debug=True)
