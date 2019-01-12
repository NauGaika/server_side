# -*- coding: utf-8 -*-
import os
from server import app, db
from flask import Flask, flash, request, redirect, url_for, send_from_directory, render_template
from .common import GetAllRecords, SetNewRecord
from . import app
from .models import Category, Common_props, Menu_points, Glass_type, Glass, Glass_option, Good, Good_option, Treetment, Treetment_option

@app.shell_context_processor
def make_shell_context():
    return {
        'db': db,
        'Category': Category,
        'Common_props': Common_props,
        'Menu_points': Menu_points,
        'Glass_type': Glass_type,
        'Glass': Glass,
        'Glass_option': Glass_option,
        'Good': Good,
        'Good_option': Good_option,
        'Treetment': Treetment,
        'Treetment_option': Treetment_option
    }


@app.route('/robots.txt')
@app.route('/sitemap.xml')
def static_from_root():
    return send_from_directory(app.static_folder, request.path[1:])

#для создания стекла
@app.route('/api/get-all-category-for-glass/', methods=['GET','POST'])
def get_all_category_for_glass():
    if request.method == 'GET':
      return Category.get_all_category_for_glass()

#############################################################
#для создания полей универсально
@app.route('/api/get-category_list/', methods=['GET','POST'])
def get_category_list():
    if request.method == 'GET':
      return Category.get_all_category()


@app.route('/api/get-param/<param_name>', methods=['GET','POST'])
def get_param(param_name):
    return Common_props.get_param(param_name)

@app.route('/api/add/<table_name>', methods=['GET','POST'])
def add_records(table_name):
    if request.method == 'POST':
        return SetNewRecord(table_name, request)()
    if request.method == 'GET':
        return 'Здесь добавляются поля в {}'.format(table_name)

@app.route('/api/get-all/<table_name>', methods=['GET','POST'])
def get_all_records(table_name):
    elem = GetAllRecords(table_name)
    if request.method == 'GET':
        return elem()

########################################################


#для ассортимента
@app.route('/api/get-all-glass-category/', methods=['GET','POST'])
def get_all_glass_category():
    """Возвращает имена и титуалы в виде словаря с ключами 'name', 'title'"""
    elems = Glass_type.get_all_name_and_title()
    return elems
#####################################################################

#для страницы с категорией
@app.route('/api/get-category-data/<cat>', methods=['GET','POST'])
def get_category_data(cat):
    """Возвращает массив со всеми товарами, которые принадлежат категории или подкатегориям'"""
    elems = Category.get_category_data(cat)
    return elems

#общие
@app.route('/api/get-category-name/<cat>', methods=['GET','POST'])
def get_category_name(cat):
    """возвращает титул категории по name'"""
    elems = Category.get_category_name(cat)
    return elems

#для страницы товара
@app.route('/api/get-good-data/<cat>', methods=['GET','POST'])
def get_good_data(cat):
    """возвращает все данные о товаре"""
    elems = Good.get_good_data(cat)
    return elems


@app.route('/api/get-other-good-data/<id>', methods=['GET','POST'])
def get_other_good_data(id):
    """Возвращает необходимые данные для страницы товара
    (другой товар, входящий в исходный) данные дефолтного товара"""
    elem = Good.get_other_good_data(id)
    return elem

@app.route('/api/get-good-by-cat-name/<cat>', methods=['GET','POST'])
def get_goods_by_cat_name(cat):
    """Возвращает все товары данной категории и товары входящих подкатегорий'"""
    elem = Category.get_goods_by_cat_name(cat)
    return elem

@app.route('/api/get-all-glass-by-cat/<cat>', methods=['GET','POST'])
def get_all_glass_by_category(cat):
    """Возвращает имена и титуалы в виде словаря с ключами 'name', 'title'"""
    elems = Glass_type.get_all_glassoption(cat)
    return elems

@app.route('/api/get-menu-point/', methods=['GET','POST'])
def get_all_menu_points():
    """Возвращает все пункты меню 'name', 'title'"""
    elems = Menu_points.get_all_menu_points()
    return elems

@app.route('/api/get-default-option-glass/', methods=['GET','POST'])
def get_default_option_glass():
    """Возвращает стекла для данной категории"""
    elems = Glass_option.get_all_menu_points()
    return elems
