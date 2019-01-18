# -*- coding: utf-8 -*-
import os
from .. import app
from flask import Flask, flash, request, redirect, url_for, abort
from werkzeug.utils import secure_filename
from ..models import Article_pages, Article_container, Article_text, Article_img_containers, Article_img, Common_props
from .. import db
import json

letters = {u'а': u'a',
                   u'б': u'b',
                   u'в': u'v',
                   u'г': u'g',
                   u'д': u'd',
                   u'е': u'e',
                   u'ё': u'e',
                   u'ж': u'zh',
                   u'з': u'z',
                   u'и': u'i',
                   u'й': u'y',
                   u'к': u'k',
                   u'л': u'l',
                   u'м': u'm',
                   u'н': u'n',
                   u'о': u'o',
                   u'п': u'p',
                   u'р': u'r',
                   u'с': u's',
                   u'т': u't',
                   u'у': u'u',
                   u'ф': u'f',
                   u'х': u'h',
                   u'ц': u'ts',
                   u'ч': u'ch',
                   u'ш': u'sh',
                   u'щ': u'sch',
                   u'ъ': u'',
                   u'ы': u'y',
                   u'ь': u'',
                   u'э': u'e',
                   u'ю': u'yu',
                   u'я': u'ya',
                   u' ': u'-',
                   u'.': '',
                   u',': ''}
class Article_class:
    def __init__(self):
        pass

    @classmethod
    def last_img_id(cls):
        last_id = Article_img.query.order_by(Article_img.id.desc()).first()
        if not last_id:
            last_id = 1
        else:
            last_id = last_id.id + 1
        return str(last_id)

    @classmethod
    def add_new_img_to_db(cls, request):
        file_path = cls.create_img_file(request)
        file_path = '/img/articles/'+ file_path
        file_alt = request.form['alt']
        new_img = Article_img(alt=file_alt, src=file_path)
        db.session.add(new_img)
        db.session.commit()
        img_info = {'src': file_path, 'alt': file_alt, 'id': new_img.id}
        return json.dumps(img_info)

    @classmethod
    def create_img_file(cls, request):
        if 'img' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['img']
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file and file.filename:
            filename, file_extension = os.path.splitext(secure_filename(file.filename))
            filename = cls.last_img_id() + file_extension
            fullname = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(fullname)
            return filename

    @classmethod
    def del_img_by_id(cls, id):
        delimg = Article_img.query.get(int(id))
        db.session.delete(delimg)
        db.session.commit()
        return 'OK'

    @classmethod
    def create_article(cls, json_ob):
        big_data = json.loads(json_ob)
        password = big_data['pass']
        if Common_props.check_pass(password):
            containers = big_data['containers']
            name = big_data['name']
            description = big_data['description']
            translit = big_data['translit']
            container_fillers = []
            page = cls.create_page_obj(name, description, translit)
            containers = cls.create_containers(containers, page, container_fillers)
            db.session.commit()

    @classmethod
    def create_page_obj(cls, name, description, translit):
        page = Article_pages(page_name = name, page_transcription = translit, page_description = description)
        db.session.add(page)
        return page

    @classmethod
    def create_containers(cls, containers, page, container_fillers):
        container_obj = []
        k = 0
        for i in containers:
            title = i.get('title')
            if not i.get('title'):
                title = ""
            k += 1
            new_a_c  = Article_container(title=title, position = k)
            new_a_c.article = page
            db.session.add(new_a_c)
            cont_by_type = cls.create_containers_by_type(i, new_a_c)
            container_fillers.append(cont_by_type)
            container_obj.append(new_a_c)
        return container_obj

    @classmethod
    def create_containers_by_type(cls, cont, parent):
        new_cont = None
        type_cont = cont.get('type')
        if type_cont == "text":
            new_cont = Article_text(text = cont['content'])
        elif type_cont == "img":
            new_cont = Article_img_containers()
            cls.find_all_img(cont['files'], new_cont)
        new_cont.article_container = parent
        db.session.add(new_cont)
        return new_cont

    @classmethod
    def find_all_img(cls, arr_imgs, parent):
        for i in arr_imgs:
            img = Article_img.query.get(i['id'])
            img.article_img_container = parent
    #################################################
    ################################################
    ################################################
    ################################################
    @classmethod
    def get_article_by_name(cls, article_name):
        big_data = {
        'title': "",
        'description': "",
        'containers': []
        }
        page = cls.article_by_name(article_name)
        if page:
            big_data['title'] = page.page_name
            big_data['description'] = page.page_description
            for i in page.article_containers:
                if i.article_text:
                    big_data['containers'].append({
                        "title": i.title,
                        "text": i.article_text[0].text,
                        "type": 'text'
                        })
                elif i.article_img:
                    big_data['containers'].append({'type': 'img', 'images': []})
                    newArr = big_data['containers'][-1]['images']
                    print(newArr)
                    for b in i.article_img[0].imges:
                        newArr.append({
                        'alt': b.alt,
                        'src': b.src
                        })
            return json.dumps(big_data)
        return abort(404)

    @classmethod
    def article_by_name(cls, name):
        page = Article_pages.query.filter_by(page_transcription = name).first()
        return page

    @classmethod
    def get_all_article_title(cls):
        all_art = Article_pages.query.all()
        to_deliv = []
        for i in all_art:
            to_deliv.append({
            'href': i.page_transcription,
            'title': i.page_name
            })
        return json.dumps(to_deliv)

    @classmethod
    def create_transcript(cls, name):
        name.lower()
        translit_string = name
        for char in letters.keys():
            translit_string = translit_string.replace(char, letters[char])
        return translit_string

    @classmethod
    def article_in_base(cls, name):
        translit = cls.create_transcript(name)
        # print(translit)
        if cls.article_by_name(translit):
            return ""
        return translit

__all__ = ['Article_class']
