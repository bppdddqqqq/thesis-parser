from ctypes import Union
from tokenize import String
from typing import Dict
from typing_extensions import Self
import pandas
import yaml
import os

import re
import itertools

import validators

base_types = ['Bool', 'String', 'StringNone', 'Integer', 'IntegerNone', 'Link']

type_glob = re.compile(r"^([A-Z][A-Za-z]*)(\[\])?(\{\})?$")

CATEGORIES_LOCATION = 'Compilator/categories/'
INITTED = False

def validate(primitive_type, value):
    if primitive_type == "Bool" and type(value) is bool:
        return True
    if primitive_type == "String" and type(value) is str:
        return True
    if primitive_type == "StringNone" and (type(value) is str or value is None):
        return True
    if primitive_type == "Integer" and type(value) is int:
        return True
    if primitive_type == "IntegerNone" and (type(value) is int or value is None):
        return True
    if primitive_type == "Link":
        if value is None:
            return True
        try:
            if type(value) is str and validators.url(value):        
                return True
        except:
            return False
    return False

class Category:
    known : Dict[str, Self] = {}
    def __init__(self, key, yaml_sub):
        self.mandatory = yaml_sub['mandatory']
        self.title = yaml_sub['title']
        self.description = yaml_sub.get('description', None)
        self.hint = yaml_sub.get('hint', None)
        self.type = yaml_sub['type']
        self.key = key
        self.associated_value = []

        match = type_glob.match(self.type)
        try:
            assert match
            assert match.group(1) in base_types
        except:
            raise ValueError(yaml_sub)
        self.primitive_type = match.group(1)
        self.is_array = True if match.group(2) else False
        self.is_complex = True if match.group(3) else False
        
        Category.known[key] = self
    def validate_value(self, value):
        if self.is_array and type(value) is list:
            return all(map(lambda x: validate(self.primitive_type, x), value))
        return validate(self.primitive_type, value)
    def __lt__(self, rhs):
        return self.key < rhs.key
    def __eq__(self, rhs):
        if not isinstance(rhs, Category):
            return False
        return self.key == rhs.key

class CategoryManifest:
    known = {}

    def __init__(self, key: str, yaml_manifest: dict):
        categories = yaml_manifest.get('properties', {})
        self.categories = {}
        self.key = key
        for k, v in categories.items():
            self.categories[k] = Category(k, v)
        CategoryManifest.known[key] = self
        
        
class CategoryValue:
    def __init__(self, category: Category, yaml_value):
        self.category = category
        if self.category.is_complex:
            self.value = yaml_value['_v']
            self.extras = yaml_value.copy()
            self.extras.pop('_v')
        else:
            self.value = yaml_value
            self.extras = {}
        if not self.category.validate_value(self.value):
            raise ValueError(('keyTypeError', self.value, self.category.primitive_type, self.category.key))
        self.category.associated_value.append(self)
    def type(self):
        return self.category.type
    def dumps(self):
        if (self.extras == {}):
            return self.value
        return {
            '_v': self.value,
            **self.extras
        }
    def __del__(self):
        self.category.associated_value.remove(self)

def load_file(file):
    grp = yaml.load(open(CATEGORIES_LOCATION+file), Loader=yaml.Loader)
    return grp

def list_categories():
    return filter(lambda x: x.endswith('.yaml'), os.listdir(CATEGORIES_LOCATION))

def get_category_info(key: str) -> String:
    if key == '_ALL':
        pandas.set_option('display.max_colwidth', None)
        table = pandas.DataFrame()

        for k,v in Category.known.items():
            table.at[k, 'Title'] = v.title
            table.at[k, 'Description'] = v.description
            table.at[k, 'Type'] = v.type
        
        return table.to_markdown()

    cat : Category = Category.known.get(key, None)

    if cat is None:
        return "No such category"
    
    return f"{cat.title} - {cat.description} - {cat.type}"

def init_script():
    global INITTED
    if INITTED:
        return
    for file in list_categories():
        key = file.replace('.yaml', '', 1)
        CategoryManifest(key, load_file(file))
    INITTED = True
init_script()
