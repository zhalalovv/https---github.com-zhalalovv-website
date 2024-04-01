import os
import uuid
import settings
from flask_login import LoginManager
from flask import Flask, g, render_template, request, redirect, url_for, jsonify


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

@app.route("/search")
def search():
    return render_template("search_res.html")

@app.route("/restaurant/<int:id>/menu")
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
        return render_template("menu.html", restaurant=restaurant, categories=dishes_by_category)
    else:
        return render_template("404.htm"), 404
    
def oplata_tovara_by_post():
    from models import db_session, Order
    if request.method == "GET":
        return render_template("menu.html")
    # Получение данных из запроса
    order_data = request.json

    # Создание нового заказа
    new_order = Order(
        restaurant_id=order_data.get("restaurant_id"),
        order_date=order_data.get("order_date"),
        total=order_data.get("total"),
        address=order_data.get("address"),
        recipient_name=order_data.get("recipient_name"),
        recipient_phone=order_data.get("recipient_phone")
    )

    # Сохранение заказа в базе данных
    db_session.add(new_order)
    db_session.commit()

    return jsonify({"success": True})

# @app.route("/menu", methods=["GET","POST"])
# def oplata_tovara_by_post():
#     from models import db_session, Order
#     if request.method == "GET":
#         return render_template("menu.html")
#     # Получение данных из запроса
#     order_data = request.json

#     # Создание нового заказа
#     new_order = Order(
#         restaurant_id=order_data.get("restaurant_id"),
#         order_date=order_data.get("order_date"),
#         total=order_data.get("total"),
#         address=order_data.get("address"),
#         recipient_name=order_data.get("recipient_name"),
#         recipient_phone=order_data.get("recipient_phone")
#     )

#     # Сохранение заказа в базе данных
#     db_session.add(new_order)
#     db_session.commit()

#     return jsonify({"success": True})


# @app.route("/oplata", methods=["GET","POST"])
# def process_order():
#     if request.method == 'GET':
#         address = request.args.get('address')
#         recipient_name = request.args.get('recipient_name')
#         recipient_phone = request.args.get('recipient_phone', 11, type=int)

#         if address is None or recipient_name is None or recipient_phone is None:
#             return 'Отсутствуют обязательные данные', 400

#         return jsonify({
#             'address': address,
#             'recipient_name': recipient_name,
#             'recipient_phone': recipient_phone,
#         })

#     else:
#         return 'Метод POST не поддерживается для этого маршрута', 405
     
@manager.user_loader
def load_user(user_id):
    from models import User
    return User.query.get(user_id)


if __name__ == "__main__":
    from werkzeug.middleware.shared_data import SharedDataMiddleware
    from controller import *
    app.wsgi_app = SharedDataMiddleware(app.wsgi_app, {
      '/': os.path.join(os.path.dirname(__file__), 'static')
    })
    app.run(host='0.0.0.0', port=5000, debug=True)
