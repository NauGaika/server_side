# -*- coding: utf-8 -*-
from flask import Blueprint
from ..common import Article_class
from ..common.Check_pass import check_pass
from ..models import Common_props
from flask import request

articles_api = Blueprint('articles_api', __name__)
############################################################3
### add image
@articles_api.route('/api/article/add-img', methods=['GET','POST'])
def add_article_img():
    """add img to db"""
    if request.method == 'POST':
        return str(Article_class.add_new_img_to_db(request))

### dell image
@articles_api.route('/api/article/del-img', methods=['GET','POST'])
def del_article_img():
    """del img from db"""
    if request.method == 'POST':
        return str(Article_class.del_img_by_id(request.form['id']))

### create article
@articles_api.route('/api/article/create-article', methods=['GET','POST'])
def create_article():
    """create article"""
    if request.method == 'POST':
        Article_class.create_article(request.form['json'])
        return 'ok'

###find article
@articles_api.route('/api/article/get-article/<page_name>', methods=['GET','POST'])
def get_article(page_name):
    """возвращает статью и все данные о ней'"""
    return Article_class.get_article_by_name(page_name)
###find article
@articles_api.route('/api/article/get-all-article-title', methods=['GET','POST'])
def get_all_article_title():
    """возвращает ссылки с путями'"""
    return Article_class.get_all_article_title()
###find article
@articles_api.route('/api/article/is_exist/<name>', methods=['GET','POST'])
def article_is_exist(name):
    """возвращает ссылки с путями'"""
    return Article_class.article_in_base(name)

@articles_api.route('/api/article/check_pass', methods=['GET','POST'])
def check_pass_db():
    """проверяем пароль администратора'"""
    check_pass(password = request.form['pass'])
    return 'ok'
