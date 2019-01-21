# -*- coding: utf-8 -*-
import json
from .. import db

class Menu_points_mixin:
    def __init__(self):
        pass

    @classmethod
    def get_all_menu_points(cls):
        return json.dumps(cls.get_all_element())

    @classmethod
    def get_all_element(cls):
        data = []
        all_elem = cls.query.filter_by(general_point=None).all()
        for i in all_elem:
            data.append({
                'id': i.id,
                'title': i.title,
                'src': i.src,
                'position': i.position,
                'sub_point': cls.get_sub_point(i.sub_point)
            })
        return data

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
