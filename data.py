from Compilator.categories import Category, CategoryValue, CategoryManifest
from Compilator.state import State
import yaml
import Compilator.error as error

def flatten_helper(lst: list):
    for k, v in lst:
        yield from v.categories.items()

class DataItem:
    dataItems = {}

    def __init__(self, yaml_main: dict, manifests: set):
        yaml_values = yaml_main.get('properties', {})
        self.values = {}
        self.manifests = manifests.copy()
        
        # name of manifest, .categories=cats
        used_manifests = filter(lambda pair: pair[0] in self.manifests, CategoryManifest.known.items())
        self.categories = list(flatten_helper(used_manifests))
        mandatory_categories = filter(lambda pair: True or pair[1].mandatory, self.categories)

        s = set(map(lambda x: x[0], mandatory_categories))
        if not s.issubset(yaml_values.keys()):
            s -= yaml_values.keys()
            raise ValueError('requiredKeysError', s)
        self.id = yaml_values['_n']
        invalid = []
        for key, value in yaml_values.items():
            if key not in Category.known.keys():
                continue
            try:
                self.values[key] = CategoryValue(Category.known[key], value)
            except ValueError as e:
                invalid.append(e)
        self.bad = False
        if len(invalid) > 0:
            self.bad = True
            raise ValueError('keyTypeArrayError', invalid)
        self.dataItems[self.id] = self

    def get_by_cat(self, category: Category):
        assert category in self.categories
        assert category.key in self.values.keys()

        return self.values[category.key]
    
    def get(self, key: str):
        assert key in self.values.keys()

        return self.values[key]

    def dump_md(self, path: str):
        with open(path, 'w') as fp:
            fp.write(f'# {self.id}\n\n')
            for key, cat in self.values.items():
                fp.write(f'## {cat.category.title}\n')
                if cat.category.description:
                    fp.write(f'{cat.category.description}\n')
                fp.write(f'Value: {cat.value}\n')
                if cat.extras:
                    fp.write('Extra values:\n')
                    for k, v in cat.extras.items():
                        fp.write(f'* {k} :: {v}\n')
                fp.write('\n\n')

    def dumps(self):
        return {'properties': {k: v.dumps() for k, v in self.values.items()}}

def open_item(path: str, manifests = set()) -> DataItem:
    yaml_main = yaml.load(open(path), Loader=yaml.Loader)
    
    try:
        res = DataItem(yaml_main, manifests)
        return res
    except (KeyError, ValueError) as e:
        error.InvalidList.push(('fileError', path, e))

