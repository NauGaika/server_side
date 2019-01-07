# -*- coding: utf-8 -*-
import json
from .. import db

class Glass_type_mixin(object):
    @classmethod
    def get_all_name_and_title(cls):
        """Берем все категории и возвращаем id
        имя и титул в словаре JSON формата
        """
        all_glass_type = []
        result = cls.query.all()
        all_glass_type.append({
            'id': -1,
            'name': 'all',
            'title': 'Все'
        })
        for el in result:
            all_glass_type.append({
                'id': el.id,
                'name': el.name,
                'title': el.title
            })
        return json.dumps(all_glass_type)

    @classmethod
    def get_all_glassoption(cls, class_name):
        if class_name == 'undefined' or class_name == 'all':
            result = cls.query.all()
        else:
            result = cls.query.filter(cls.name == class_name).all()
        glasses = []
        for k in result:
            for i in k.glass:
                g_name = i.name
                g_title = i.title
                g_description = i.description
                g_options = []
                for opt in i.glass_option:
                    g_options.append({
                        'price': opt.price,
                        'thick' : opt.thick,
                        'color' : opt.color,
                        'glass_count': opt.glass_count,
                        'article': opt.article,
                        'img': opt.img_src
                    })
                glasses.append({
                    'id': i.id,
                    'name' : g_name,
                    'title': g_title,
                    'description': g_description,
                    'options': g_options
                })
        return json.dumps(glasses)