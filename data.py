from Compilator.categories import Category, CategoryValue, CategoryManifest
from Compilator.state import State
import yaml

def flatten_helper(lst: list):
    for k, v in lst:
        yield from v.categories.items()

class DataItem:
    def __init__(self, yaml_main: dict, manifests: set):
        yaml_values = yaml_main.get('properties', {})
        self.values = {}
        self.manifests = manifests.copy()
        
        # name of manifest, .categories=cats
        used_manifests = filter(lambda pair: pair[0] in self.manifests, CategoryManifest.known.items())
        self.categories = list(flatten_helper(used_manifests))
        mandatory_categories = filter(lambda pair: pair[1].mandatory, self.categories)

        s = set(map(lambda x: x[0], mandatory_categories))
        if not s.issubset(yaml_values.keys()):
            s -= yaml_values.keys()
            raise ValueError('requiredKeysError', s)
        self.id = yaml_values['_n']
        for key, value in yaml_values.items():
            self.values[key] = CategoryValue(Category.known[key], value)

    def get_by_cat(category: Category):
        assert category in self.categories
        assert category.key in self.values.keys()

        return self.values[category.key]
    
    def get(key: str):
        assert key in self.values.keys()

        return self.values[key]

def open_item(path: str, manifests = set()):
    yaml_main = yaml.load(open(path), Loader=yaml.Loader)
    
    try:
        res = DataItem(yaml_main, manifests)
    except (KeyError, ValueError) as e:
        print(path)
        raise e
    return res

