# -*- coding: utf-8 -*-
import json
from .. import db

class Delivery_mixin:
    @classmethod
    def set_new_region(cls, region, price):
        price = float(price)
        region = str(region)
        new_region = cls(region = region, price = price)
        db.session.add(new_region)
        db.session.commit()
        return {'id': new_region.id, 'region': new_region.region, 'price': new_region.price}

    @classmethod
    def get_all_region(cls):
        all_region = cls.query.all()
        region_list = []
        for i in all_region:
            region_list.append({
                'region': i.region,
                'price': i.price,
                'id': i.id
            })
        return region_list

    @classmethod
    def del_region(cls, id):
        id = int(id)
        el = cls.query.get(id)
        name = el.region
        db.session.delete(el)
        db.session.commit()
        return 'Регион ' + name + ' удален'
