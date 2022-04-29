from ..schema import category_schema
from jsonschema import validate
import functools
import itertools
import yaml
import os

CATEGORIES_LOCATION = 'Compilator/categories/'

def parse_category(yamlObject):
    for key, category in yamlObject['properties'].items():
        validate(instance=category, schema=category_schema)

@functools.lru_cache()
def load_file(file):
    grp = yaml.load(open(CATEGORIES_LOCATION+file), Loader=yaml.Loader)
    parse_category(grp)
    return grp

@functools.lru_cache()
def list_categories():
    return filter(lambda x: x.endswith('.yaml'), os.listdir(CATEGORIES_LOCATION))

@functools.lru_cache()
def get_category_manifests():
    categories = {}
    for file in list_categories():
        categories[file.replace('.yaml', '', 1)] = load_file(file)
    return categories

@functools.lru_cache()
def get_flat_categories():
    categories = get_category_manifests()

    flattened = map(lambda tupl: tupl[1]['properties'], categories.items())

    res = {}
    for i in flattened:
        for k,v in i.items():
            res[k] = v
    return res

def get_category_info(name: str):
    return get_flat_categories()[name]

@functools.lru_cache()
def get_relevant_categories(enabled_categories = frozenset()):
    categories = get_category_manifests()

    filtered = filter(lambda tupl: tupl[0] in enabled_categories, categories.items())

    flattened = map(lambda tupl: tupl[1]['properties'], filtered)

    res = {}
    for i in flattened:
        for k,v in i.items():
            res[k] = v
    return res
