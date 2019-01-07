# -*- coding: utf-8 -*-
import json
import html
import os
from .. import db
from sqlalchemy import or_, and_

#Категории товаров
class Category_mixin(object):

    @classmethod
    def get_all_category(cls):
        cats = cls.query.filter(or_(cls.name=='glass-products', cls.name=='mirrors', cls.name=='service')).all()
        cat_list = []
        for b in cats:
            for i in b.sub_category:
                link = '/' + i.name + '/'
                cat_list.append({'id': i.id, 'link': link, 'title': i.title, 'description': i.description, 'imgSrc': i.img_src, 'generalCat': i.general_category.name})
        return json.dumps(cat_list)

    @classmethod
    def get_category_data(cls, cat):
        data = {}
        category = cls.query.filter_by(name=cat).first()
        data['title'] = category.title
        data['description'] = category.description
        data['subcat'] = []
        data['goods'] = []
        cls.get_goods_by_cat(data['goods'], category)
        subcat = category.sub_category
        for i in subcat:
            data['subcat'].append({
                'name': i.name,
                'title': i.title,
                'description': i.description,
                'imgSrc': i.img_src,

            })
        return json.dumps(data)

    @classmethod
    def get_goods_by_cat(cls, data, category):
        for i in category.goods:
            data.append({
                'id': i.id,
                'name': i.name,
                'article': i.article,
                'imgSrc': i.img_src,
                'price': i.price
            })
        for i in category.sub_category:
            cls.get_goods_by_cat(data, i)

    @classmethod
    def get_category_name(cls, catName):
        return cls.query.filter_by(name=catName).first().title

    @classmethod
    def get_goods_by_cat_name(cls, cat_name):
        category = cls.query.filter_by(name=cat_name).first()
        data = []
        cls.get_goods_by_cat(data, category)
        return json.dumps(data)

    @classmethod
    def get_all_category_for_glass(cls):
        data = []
        generals = cls.query.filter_by(general_category=None).all()
        for i in generals:
            i.add_category_for_glass(data)
        return json.dumps(data)

    def add_category_for_glass(self, data):
        obj = {'data': self.CatDataAddGlass, 'children': []}
        data.append(obj)
        if len(self.sub_category) > 0:
            for i in self.sub_category:
                i.add_category_for_glass(obj['children'])

    @property
    def CatDataAddGlass(self):
        data = {}
        data['id'] = self.id
        data['title'] = self.title
        return data
