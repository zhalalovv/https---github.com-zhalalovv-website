# -*- coding: UTF-8 -*-
from sqlalchemy import Column,  Integer,Float,Date,  DateTime, Text, Boolean, String, ForeignKey, or_, not_
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import relationship, query_expression
from sqlalchemy.sql import func
from database import Base, db_session, engine as db_engine
import datetime

# "Ресторан"
class Restaurant(Base):
    __tablename__ = 'restaurants'
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(25))
    photo = Column(String(500))
    hours_of_operation = Column(String(10))
    rating = Column(Integer)
    dishes = relationship('RestaurantDish', back_populates='restaurant')
    orders = relationship('RestaurantOrder', back_populates='restaurant')

# "Блюдо"
class Dish(Base):
    __tablename__ = 'dishes'
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(50))
    photo = Column(String(100))
    price = Column(Integer)
    weight = Column(Integer)
    category = Column(String(50))
    restaurants = relationship('RestaurantDish', back_populates='dish')
    orders = relationship('OrderDish', back_populates='dish')

# "Ресторан - Блюдо"
class RestaurantDish(Base):
    __tablename__ = 'restaurant_dishes'
    id = Column(Integer, primary_key=True, autoincrement=True)
    restaurant_id = Column(Integer, ForeignKey('restaurants.id'))
    dish_id = Column(Integer, ForeignKey('dishes.id'))
    restaurant = relationship('Restaurant', back_populates='dishes')
    dish = relationship('Dish', back_populates='restaurants')

# "Заказ"
class Order(Base):
    __tablename__ = 'orders'
    id = Column(Integer, primary_key=True, autoincrement=True)
    restaurant_id = Column(Integer, ForeignKey('restaurants.id'))
    restaurant_name = Column(String(25))
    order_date = Column(DateTime, default=func.utcnow)
    order_time = Column(String(10))
    order_amount = Column(Float)
    address = Column(String(255))
    recipient_name = Column(String(50))
    recipient_phone = Column(String(15))
    dishes = relationship('OrderDish', back_populates='order')
    restaurant = relationship('RestaurantOrder', back_populates='orders')

# "Заказ - Блюдо"
class OrderDish(Base):
    __tablename__ = 'order_dishes'
    id = Column(Integer, primary_key=True, autoincrement=True)
    order_id = Column(Integer, ForeignKey('orders.id'))
    dish_id = Column(Integer, ForeignKey('dishes.id'))
    quantity = Column(Integer)
    dish = relationship('Dish', back_populates='orders')
    order = relationship('OrderDish', back_populates='dishes')
    


def init_db():
    # import all modules here that might define models so that
    # they will be registered properly on the metadata.  Otherwise
    # you will have to import them first before calling init_db()
    from database import engine
    Base.metadata.create_all(bind=engine)
    db_session.commit()


if __name__ == "__main__":
    init_db()

    #print_columns(Payment, "created")
    #print_schema(SoltButton)
