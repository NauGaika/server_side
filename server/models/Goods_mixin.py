# -*- coding: utf-8 -*-
import json
class Good_mixin:
    def get_price(self):
        formula_name = self.formula_name
        param = json.loads(self.default)
        if formula_name == 'common':
            return self.price

    @classmethod
    def get_good_data(cls, id):
        data = {}
        good = cls.query.get(id)
        data['imgSrc'] = good.img_src
        data['title'] = good.name
        data['description'] = good.description
        data['option'] = good.default
        data['formula'] = good.formula_name
        data['price'] = good.price
        return json.dumps(data)

    @classmethod
    def get_other_good_data(cls, id):
        data = {}
        good = cls.query.get(int(id))
        data['imgSrc'] = good.img_src
        data['title'] = good.name
        data['price'] = good.price
        return json.dumps(data)
