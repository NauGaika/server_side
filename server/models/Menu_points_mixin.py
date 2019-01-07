# -*- coding: utf-8 -*-
import json
from .. import db

class Menu_points_mixin:
    data = []
    def __init__(self):
        pass

    @classmethod
    def get_all_menu_points(cls):
        cls.get_all_element()
        return json.dumps(cls.data)

    @classmethod
    def get_all_element(cls):
        if not cls.data:
            all_elem = cls.query.filter_by(general_point=None).all()
            for i in all_elem:
                cls.data.append({
                    'id': i.id,
                    'title': i.title,
                    'src': i.src,
                    'position': i.position,
                    'sub_point': cls.get_sub_point(i.sub_point)
                })

    @classmethod
    def get_sub_point(cls, point):
        arr = []
        if len(point):
            for i in point:
                arr.append({
                    'id': i.id,
                    'title': i.title,
                    'src': i.src,
                    'position': i.position,
                    'sub_point': cls.get_sub_point(i.sub_point)
                })
        return arr
