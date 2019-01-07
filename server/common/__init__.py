import json
from ..models import *
import sqlalchemy
from .. import db
from sqlalchemy import inspect
import flask_sqlalchemy
import os

class GetAllRecords:

    def __init__(self, tableName):
        """инициализирует поиск всех полей в базе данных """
        self.tableName = tableName.capitalize() #переданное имя таблицы с большой буквы
        self.is_exist = True #стартовое значение существования таблицы
        if self.tableName in globals(): #ищем имя таблицы в глобальной области видимости
            self.classDB = globals()[self.tableName]
        else:
            self.is_exist = False

    @property
    def columnNames(self):
        return inspect(self.classDB).attrs.keys()

    @property
    def allRecords(self):
        mass = []
        elems = self.classDB.query.all()
        for el in elems:
            propDict = {}
            for prop in self.columnNames:
                if isinstance(el.__getattribute__(prop), db.Model):
                    propDict.update({prop: el.__getattribute__(prop).__getattribute__(self._name)})
                elif isinstance(el.__getattribute__(prop), sqlalchemy.orm.collections.InstrumentedList):
                    propDict.update({prop: ''})
                elif 'SELECT' in str(el.__getattribute__(prop)):
                    propDict.update({prop: ''})
                else:
                    propDict.update({prop: el.__getattribute__(prop)})
            mass.append(propDict)
        return mass


    @property
    def data(self):
        """формирование даты для отправлки"""
        el = {}
        el['RowName'] = self.columnNames #статический метод
        el['RowType'] = self.columnTypes #статический метод
        el['RowData'] = self.allRecords #статический метод
        return json.dumps(el)

    @property
    def columnTypes(self):
        col_types = [] #initialize coltype array
        names = inspect(self.classDB).attrs.keys() # get all key for property of object (all elements attribute)
        _name = ''
        if 'title' in names:
            _name = 'title'
        elif 'name' in names:
            _name = 'name'
        else:
            _name = 'id'
        self._name = _name
        for i in self.classDB.__table__.columns: #go through all the columns of our table
            fc = i.foreign_keys #get foreign_keys if it exist
            if fc:
                fc_name = list(fc)[0].target_fullname.split('.')[0].capitalize() #get full name table of foreign key table
                cur_class = globals()[fc_name] #get table foreign key of db
                cur_elems = cur_class.query.all() #get all elements of sub element
                cur_types = [] #all types
                for c in cur_elems:
                    cur_types.append({
                        'id': c.id,
                        'name': c.__getattribute__(_name)
                    })
                col_types.append({
                    'type': 'other',
                    'value': cur_types,
                    'name': i.name
                })
            else:
                el_type = str(i.type)
                if 'INTEGER' in el_type:
                    col_types.append({
                        'type': 'integer',
                        'name': i.name
                    })
                elif 'VARCHAR' or 'TEXT' in el_type:
                    if 'img' in i.name.lower():
                        col_types.append({
                            'type': 'img',
                            'name': i.name
                        })
                    else:
                        col_types.append({
                            'type': 'string',
                            'name': i.name
                        })
        return col_types

    def __call__(self):
        """при вызове данного класса как функции отправляем сформированную дату"""
        if self.is_exist:
            return self.data
        return 'Таблицы {} не существует'.format(self.tableName)



class SetNewRecord:
    def __init__(self, tableName, request):
        #корневая папка для загрузки файлов
        self.UPLOAD_FOLDER = os.path.join(os.path.dirname(os.getcwd()), r'site/static/img/')
        #корневая папка для отправки в базу
        self.UPLOAD_FOLDER_DB = r'/static/img/'
        #объект класса
        self.classDB = None
        #all files for add to db
        self.all_files = {}
        #all records in input fields from form
        self.form_input = {}
        #name table from form
        self.tableName = tableName
        self.all_form_field_name = []
        self.column_equal = False
        self.file_names = {}

        self.get_class_db()
        self.get_all_files(request)
        self.get_other_props(request)
        self.get_all_form_field_name()
        self.compare_names_column()
        if self.column_equal:
            self.set_correct_type()
            self.add_img_src()
            self.create_new_record()
            self.create_path_to_file()
            self.create_file_name()
            self.create_file()
            self.set_file_path_to_db()

    def create_file(self):
        file_path = self.UPLOAD_FOLDER
        for file in self.all_files:
            file_elem = self.all_files[file]
            file_name = self.file_names[file]

            file_elem.save(os.path.join(file_path, file_name))

    def set_file_path_to_db(self):
        file_path = self.UPLOAD_FOLDER_DB
        for file in self.all_files:
            all_path = os.path.join(file_path, self.file_names[file])
            self.new_elem.__setattr__(file, all_path)
            db.session.commit()
        self.message = 'Запись добавлена'


    def create_file_name(self):
        file_count = 0
        for file in self.all_files:
            file_count += 1
            file_name = self.all_files[file].filename
            file_ext = os.path.splitext(file_name)[1]
            if file_count == 1:
                file_name = str(self.new_elem.id) + file_ext
            else:
                file_name = str(self.new_elem.id)+ '_' + str(file_count) + file_ext
            self.file_names[file] = file_name

    def create_path_to_file(self):
        self.UPLOAD_FOLDER = os.path.join(self.UPLOAD_FOLDER, self.tableName.lower())
        self.UPLOAD_FOLDER_DB = os.path.join(self.UPLOAD_FOLDER_DB, self.tableName.lower())
        if os.path.exists(self.UPLOAD_FOLDER):
            if os.path.isdir(self.UPLOAD_FOLDER):
                return
        os.makedirs(self.UPLOAD_FOLDER)


    def create_new_record(self):
        elem = self.classDB(**self.form_input)
        db.session.add(elem)
        db.session.commit()
        self.new_elem = elem

    def add_img_src(self):
        for i in self.all_files.keys():
            self.form_input[i] = '/'

    def set_correct_type(self):
        for i in self.classDB.__table__.columns:
            if 'INTEGER' in str(i.type) and i.name != 'id':
                self.form_input[i.name] = int(self.form_input[i.name])
                if 'id' in i.name:
                    if int(self.form_input[i.name]) < 0:
                        self.form_input[i.name] = None

    def compare_names_column(self):
        self.column_equal = True
        for i in self.class_column_names:
            if i not in self.all_form_field_name and i != 'id':
                return
        self.column_equal = True

    def get_other_props(self, request):
        self.form_input = {}
        for i in request.form:
            self.form_input[i] = request.form[i]

    @property
    def class_column_names(self):
       return self.classDB.__table__.columns.keys()

    def get_all_form_field_name(self):
        self.all_form_field_name = []
        for i in self.all_files.keys():
            self.all_form_field_name.append(i)
        for i in self.form_input.keys():
            self.all_form_field_name.append(i)

    def get_all_files(self, request):
        self.all_files = {}
        for i in request.files:
            self.all_files[i] = request.files[i]

    def get_class_db(self):
        if self.tableName.capitalize() in globals():
            self.classDB = globals()[self.tableName.capitalize()]
        else:
            self.classDB = False
    def __call__(self):
        return self.message
