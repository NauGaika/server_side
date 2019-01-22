# -*- coding: utf-8 -*-
from flask import Blueprint
from ..common import Menu_points
menu_points_api = Blueprint('menu_points_api', __name__)

@menu_points_api.route('/api/get-menu-point/', methods=['GET','POST'])
def get_all_menu_points():
    """Возвращает все пункты меню 'name', 'title'"""
    elems = Menu_points.get_all_menu_points()
    return elems
