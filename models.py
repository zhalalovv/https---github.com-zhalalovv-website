# -*- coding: UTF-8 -*-
from sqlalchemy import Column,  Integer,Float,Date,  DateTime, Text, Boolean, String, ForeignKey, or_, not_
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import relationship, query_expression
from sqlalchemy.sql import func
from database import Base, db_session, engine as db_engine
import datetime
from flask_login import UserMixin
from app import manager

# Таблица "Ресторан"
class Restaurant(Base):
    __tablename__ = 'restaurants'
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(25))
    photo = Column(String(500))
    hours_of_operation = Column(String(25))
    rating = Column(Integer)
    href = Column(String(100))
    # Отношение между рестораном и блюдами
    dishes = relationship('Dish', back_populates='restaurant')
    orders = relationship('Order', back_populates='restaurant')

# Таблица "Блюдо"
class Dish(Base):
    __tablename__ = 'dishes'
    id = Column(Integer, primary_key=True, autoincrement=True)
    rest_id = Column(Integer, ForeignKey('restaurants.id'))
    name = Column(String(100))
    photo = Column(String(100))
    price = Column(Integer)
    weight = Column(Integer)
    category = Column(String(50))
    # Отношение между блюдом и рестораном
    restaurant = relationship('Restaurant', back_populates='dishes')
    orders = relationship('OrderDish', back_populates='dish')

# Таблица "Заказ"
class Order(Base):
    __tablename__ = 'orders'
    id = Column(Integer, primary_key=True, autoincrement=True)
    restaurant_id = Column(Integer, ForeignKey('restaurants.id'))
    order_date = Column(DateTime, default=func.utcnow)
    address = Column(String(255))
    total = Column(Integer)
    recipient_name = Column(String(50))
    recipient_phone = Column(String(15))
    # Отношение между заказом и рестораном
    restaurant = relationship('Restaurant', back_populates='orders')
    # Отношение между заказом и блюдами
    dishes = relationship('OrderDish', back_populates='order')

# Таблица "Заказ - Блюдо"
class OrderDish(Base):
    __tablename__ = 'order_dishes'
    order_id = Column(Integer, ForeignKey('orders.id'), primary_key=True)
    dish_id = Column(Integer, ForeignKey('dishes.id'), primary_key=True)
    price = Column(Integer)
    # Отношение между блюдом и заказом
    dish = relationship('Dish', back_populates='orders')
    # Отношение между заказом и блюдами
    order = relationship('Order', back_populates='dishes')

class User(Base, UserMixin):
    __tablename__ = 'user'
    id = Column(Integer, primary_key=True)
    login = Column(String(32), unique=True)
    password = Column(String(64))


def init_db():
    # import all modules here that might define models so that
    # they will be registered properly on the metadAata.  Otherwise
    # you will have to import them first before calling init_db()
    from database import engine
    Base.metadata.create_all(bind=engine)
    db_session.commit()

@manager.user_loader
def load_user(user_id):
    from models import User
    return User.query.get(user_id)

if __name__ == "__main__":
    init_db()

