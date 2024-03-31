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

@app.route("/search")
def search():
    return render_template("search_res.html")

@app.route("/restaurant/<int:id>/")
def restaurant_by_id(id):
    from models import db_session, Restaurant, Dish
    restaurant = db_session.query(Restaurant).filter(Restaurant.id == id).first()
    if restaurant:
        dishes = db_session.query(Dish).filter(Dish.rest_id == id).all()
        dishes_by_category = {}
        for dish in dishes:
            category = dish.category
            if category not in dishes_by_category:
                dishes_by_category[category] = []
            dishes_by_category[category].append(dish)
        return render_template("mac.html", restaurant=restaurant, categories=dishes_by_category)
    else:
        return render_template("404.htm"), 404

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
