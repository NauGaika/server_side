# -*- coding: utf-8 -*-
import sys

from .. import db
from datetime import datetime
from .Category_mixin import *
from .User_mixin import *
from .Common_props_mixin import *
from .Goods_mixin import *
from .Glass_mixin import *
from .Treet_mixin import *
from .Order_mixin import *
from .Menu_points_mixin import *

glass_cat = db.Table('glass_cat',
    db.Column('cat_id', db.Integer, db.ForeignKey('category.id')),
    db.Column('glass_option_id', db.Integer, db.ForeignKey('glass_option.id'))
)
#Категории товаров
class Category(db.Model, Category_mixin):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), nullable=False)
    title = db.Column(db.String(120), nullable=False)
    description = db.Column(db.Text)
    img_src = db.Column(db.String(240), nullable=False)

    general_category_id = db.Column(db.Integer, db.ForeignKey('category.id'))

    general_category = db.relationship('Category', backref="sub_category", remote_side="Category.id")
    goods = db.relationship('Good', backref="category")

    glasses = db.relationship('Glass_option', secondary=glass_cat, backref=db.backref('categories', lazy = 'dynamic'))


    def __repr__(self):
        return '<Категория {}>'.format(self.name)



#Общие параметры
class Common_props(db.Model, Common_props_mixin):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True, nullable=False)
    value = db.Column(db.Text)

    def __repr__(self):
        return '<{} Равен {}>'.format(str(self.name), self.value)


class Good(db.Model, Good_mixin):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(240), nullable=False)
    description = db.Column(db.Text)
    article = db.Column(db.String(60))
    img_src = db.Column(db.String(240))
    default = db.Column(db.Text)
    formula_name = db.Column(db.String(240))
    price = db.Column(db.Float)

    category_id = db.Column(db.Integer, db.ForeignKey('category.id'))
    good_options = db.relationship('Good_option', backref="good")

    def __repr__(self):
        return '<Товар {}>'.format(self.name)
#
#
#Опции товаров
class Good_option(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), nullable=False)
    value = db.Column(db.Text)

    good_id = db.Column(db.Integer, db.ForeignKey('good.id'))

    def __repr__(self):
        return '<Опция товара {}>'.format(self.good.name)


#Типы стекла
class Glass_type(db.Model, Glass_type_mixin):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), nullable=False)
    title = db.Column(db.String(240), nullable=False)
    description = db.Column(db.Text)

    glass = db.relationship('Glass', backref="glass_type", lazy=False)
#
#
#
# #Стекла
class Glass(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), nullable=False)
    title = db.Column(db.String(240), nullable=False)
    description = db.Column(db.Text)

    glass_type_id = db.Column(db.Integer, db.ForeignKey('glass_type.id'), nullable=False)
    glass_option = db.relationship('Glass_option', backref="glass", lazy=False)
#
#Опции стекла
class Glass_option(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    price = db.Column(db.Float, nullable=False)
    thick = db.Column(db.Integer, nullable=False)
    color = db.Column(db.String(64), nullable=False)
    img_src = db.Column(db.String(240))
    glass_count = db.Column(db.Float)
    article = db.Column(db.String(60))
    glass_id = db.Column(db.Integer, db.ForeignKey('glass.id'))


    def __repr__(self):
        return '<Опции стекла {}>'.format(self.glass.name)


#Обработка стекла
class Treetment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), nullable=False)
    title = db.Column(db.String(240), nullable=False)
    description = db.Column(db.Text)
    treetment_option = db.relationship('Treetment_option', backref="treetment")


    def __repr__(self):
        return '<Обработка стекла {}>'.format(self.name)


#Опции обработки стекла
class Treetment_option(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    options = db.Column(db.Text, nullable=False)
    price = db.Column(db.Integer, nullable=False)
    article = db.Column(db.String(60))
    treetment_id = db.Column(db.Integer, db.ForeignKey('treetment.id'))

    def __repr__(self):
        return '<Обработка стекла {}>'.format(self.name)


#Пользователи
# class User(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     name = db.Column(db.String(64), nullable=False)
#     telephone = db.Column(db.String(120), unique=True, nullable=False)
#     is_activated = db.Column(db.Boolean)
#     code_activate = db.Column(db.Integer)
#
#     orders = db.relationship('Order', backref="user")
#
#     def __repr__(self):
#         return '<ID {} User {}>'.format(str(self.id), self.name)

#Статус заказа
# class Order_state(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     name = db.Column(db.String(240), nullable=False)
#     title = db.Column(db.String(240), nullable=False)
#
#     order = db.relationship('Order', backref="order_state")
#
#     def __repr__(self):
#         return '<Статус заказа {}>'.format(self.name)

#Заказ
# class Order(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     is_confim = db.Column(db.Boolean)
#     is_paid = db.Column(db.Boolean)
#     number_of_order = db.Column(db.String(240), nullable=False)
#     date_order = db.Column(db.DateTime, index=True, default=datetime.utcnow)
#
#     user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
#     order_state_id = db.Column(db.Integer, db.ForeignKey('order_state.id'))
#
#     order_goods = db.relationship('Order_goods', backref="order")
#
#     def __repr__(self):
#         return '<Номер заказа {}>'.format(self.number_of_order)

#Товары заказа
# class Order_goods(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     price = db.Column(db.Float, nullable=False)
#
#     order_id = db.Column(db.Integer, db.ForeignKey('order.id'))
#     good_option = db.Column(db.Integer, db.ForeignKey('good_option.id'))
#
#     def __repr__(self):
#         return '<Номер товар заказа с id  {}>'.format(self.order_id)

class Menu_points(db.Model, Menu_points_mixin):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(240), nullable=False)
    src = db.Column(db.String(240), nullable=False)
    position = db.Column(db.Integer)
    general_point_id = db.Column(db.Integer, db.ForeignKey('menu_points.id'))
    general_point = db.relationship('Menu_points', backref="sub_point", remote_side="Menu_points.id")

########################3
class Article_pages(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    page_name = db.Column(db.Text, nullable=False)
    page_description = db.Column(db.Text, nullable=False)
    page_transcription = db.Column(db.Text, nullable=False)
    article_containers = db.relationship('Article_container', backref="article")
    date = db.Column(db.DateTime, nullable = False, default=datetime.utcnow)

class Article_container(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    page_id = db.Column(db.Integer, db.ForeignKey('article_pages.id'))
    title = db.Column(db.Text)
    position =  db.Column(db.Integer)
    container_type = db.String(240)
    article_text = db.relationship('Article_text', backref="article_container")
    article_img = db.relationship('Article_img_containers', backref="article_container")
    def __repr__(self):
        return '<контейнер id {} name {}>'.format(str(self.id), self.title)

class Article_text(db.Model):
    id= db.Column(db.Integer, primary_key=True)
    cont_id = db.Column(db.Integer, db.ForeignKey('article_container.id'))
    text = db.Column(db.Text)

class Article_img_containers(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    cont_id = db.Column(db.Integer, db.ForeignKey('article_container.id'))
    imges = db.relationship('Article_img', backref="article_img_container")

class Article_img(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    alt = db.Column(db.Text)
    src = db.Column(db.Text, nullable=False)
    article_img_container_id = db.Column(db.Integer, db.ForeignKey('article_img_containers.id'))
