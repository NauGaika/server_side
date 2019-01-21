# -*- coding: utf-8 -*-
import os
from server import app, db
from flask import Flask, flash, request, redirect, url_for, send_from_directory, render_template, abort
from .common import *
from . import app
from .models import Category, Common_props, Menu_points, Glass_type, Glass, Glass_option, Good, Good_option, Treetment, Treetment_option, Article_pages, Article_container, Article_text, Article_img_containers, Article_img

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
        'Treetment_option': Treetment_option,
        'Article_pages': Article_pages,
        'Article_container': Article_container,
        'Article_text': Article_text,
        'Article_img_containers': Article_img_containers,
        'Article_img': Article_img
    }


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



###############################################################3
### add image
@app.route('/api/article/add-img', methods=['GET','POST'])
def add_article_img():
    """add img to db"""
    if request.method == 'POST':
        return str(Article_class.add_new_img_to_db(request))

### dell image
@app.route('/api/article/del-img', methods=['GET','POST'])
def del_article_img():
    """del img from db"""
    if request.method == 'POST':
        return str(Article_class.del_img_by_id(request.form['id']))

### create article
@app.route('/api/article/create-article', methods=['GET','POST'])
def create_article():
    """create article"""
    if request.method == 'POST':
        Article_class.create_article(request.form['json'])
        return 'ok'

###find article
@app.route('/api/article/get-article/<page_name>', methods=['GET','POST'])
def get_article(page_name):
    """возвращает статью и все данные о ней'"""
    return Article_class.get_article_by_name(page_name)
###find article
@app.route('/api/article/get-all-article-title', methods=['GET','POST'])
def get_all_article_title():
    """возвращает ссылки с путями'"""
    print('test')
    return Article_class.get_all_article_title()
###find article
@app.route('/api/article/is_exist/<name>', methods=['GET','POST'])
def article_is_exist(name):
    """возвращает ссылки с путями'"""
    return Article_class.article_in_base(name)

@app.route('/api/article/check_pass', methods=['GET','POST'])
def check_pass():
    """проверяем пароль администратора'"""
    return Common_props.check_pass(request.form['pass'])
