import os
import uuid
from datetime import datetime
from flask_login import LoginManager
from flask import Flask, g, render_template, request, redirect, url_for, jsonify
from sqlalchemy.exc import SQLAlchemyError


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
    from models import db_session, Restaurant
    query = request.args.get('query', '').strip()
    if not query:
        return render_template("search_res.html", query=query, results=None)

    results = db_session.query(Restaurant).filter(
        Restaurant.name.ilike(f'%{query}%')
    ).all()

    return render_template("search_res.html", query=query, results=results)



@app.route('/admin_panel')
def admin_panel():
    from models import db_session, OrderDish, Order
    # Создаем сессию базы данных
    session = db_session()
    # Получаем данные из таблицы OrderDish
    order_dishes = session.query(OrderDish).all()
    # Получаем данные из таблицы Dish
    orders = session.query(Order).all()
    # Закрываем сессию базы данных
    session.close()
    # Объединяем данные в список кортежей
    data = zip(order_dishes, orders)
    # Рендерим HTML-шаблон и передаем данные на страницу
    return render_template('admin_panel.html', data=data)

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
    
@app.route('/restaurant/<int:id>/menu', methods=['POST'])
def create_order(id):
    from models import db_session, Order, OrderDish, Dish
    from datetime import datetime
    order_data = request.json
    # Создание нового заказа
    new_order = Order(
        restaurant_id=id,
        order_date=datetime.now(),
        total=order_data.get('total'),
        address=order_data.get('address'),
        recipient_name=order_data.get('recipient_name'),
        recipient_phone=order_data.get('recipient_phone')
    )

    # Добавление заказа в базу данных и сохранение изменений
    db_session.add(new_order)
    db_session.flush()
    
    # Добавление блюд в заказ
    for dish_data in order_data.get('dishes', []):
        dish_id = dish_data['dish_id']
        quantity = dish_data['quantity']
        
        # Получение цены блюда из базы данных
        dish = db_session.query(Dish).filter(Dish.id == dish_id).first()
        price = dish.price
        
        # Создание записи о блюде в заказе
        order_dish = OrderDish(
            order_id=new_order.id,
            dish_id=dish_id,
            quantity=quantity,
            price=price
        )
        db_session.add(order_dish)
    db_session.commit()
    
    return redirect(url_for('index'))




@app.route('/korzina')
def korzina():
    return render_template("korzina.html")

     
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
