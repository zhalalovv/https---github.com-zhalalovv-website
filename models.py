# -*- coding: UTF-8 -*-
from sqlalchemy import Column,  Integer,Float,Date,  DateTime, Text, Boolean, String, ForeignKey, or_, not_
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import relationship, query_expression
from sqlalchemy.sql import func
from database import Base, db_session, engine as db_engine
import datetime

# Таблица "Ресторан"
class Restaurant(Base):
    __tablename__ = 'restaurants'
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(25))
    photo = Column(String(500))
    hours_of_operation = Column(String(25))
    rating = Column(Integer)

# Таблица "Блюдо"
class Dish(Base):
    __tablename__ = 'dishes'
    rest_id = Column(Integer, ForeignKey('restaurants.id'))
    id = Column(Integer, primary_key=True, autoincrement=True)
    photo = Column(String(100))
    price = Column(Integer)
    weight = Column(Integer)
    category = Column(String(50))
    restaurant = relationship('Restaurant', back_populates='name')

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
    dishes = relationship('OrderDish', back_populates='order')
    restaurant = relationship('RestaurantOrder', back_populates='orders')

# Таблица "Заказ - Блюдо"
class OrderDish(Base):
    __tablename__ = 'order_dishes'

    order_id = Column(Integer, ForeignKey('orders.id'), primary_key=True)
    dish_id = Column(Integer, ForeignKey('dishes.id'))
    price = relationship('Order', back_populates='total')
    dish = relationship('Dish', back_populates='orders')
    order = relationship('Order', back_populates='dishes')


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
