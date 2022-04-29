import re

base_types = ['Bool', 'String', 'StringNone', 'Integer', 'IntegerNone']
extensions = ['', '{}', '[]']

types = list(map(lambda x,y: x+y, zip(base_types, extensions)))
type_glob = re.

def type_correct(_type):
    return _type in types

class Category:
    def __init__(self, yaml_sub):
        self.mandatory = yaml_sub['mandatory']
        self.title = yaml_sub['title']
        self.description = yaml_sum['description']
        self.type = yaml_sum['type']
        
        assert type_correct(self.type)

    def validate_value(self, value):

