import os
import yaml
import itertools
from Compilator.categories import CategoryManifest, Category, CategoryValue
from Compilator.data import open_item
from Compilator.graphs import export_all
# parse folders and find relevant files to parse

def find_files_for_compilation(path, enabled_categories=set(['default'])):
    """Iterator that returns a tuple with path and a set of categories that should be evaluated by the compilator for specified file."""
    files = os.listdir(path)
    cur_categories = enabled_categories.copy()

    if ('.enableCompilator' in files):
        manifest = yaml.load(open(path+'/.enableCompilator'), Loader=yaml.Loader)
        if manifest.get("clearAll", None):
            cur_categories = set()
        else:
            assert 'default' not in manifest['unapplyCategories']
            cur_categories.update(manifest['applyCategories'])
            cur_categories = filter(lambda x: x not in manifest['unapplyCategories'], cur_categories)
            cur_categories = set(cur_categories)
    for file in files:
        new_path = path + '/' + file
        if os.path.isdir(new_path):
            yield from find_files_for_compilation(new_path, cur_categories)
        elif os.path.isfile(new_path):
            if (len(enabled_categories) != 0 and file.endswith('.c.yaml')):
                yield (new_path, cur_categories)

def get_files(path):
    invalid = []
    files = {}

    for path, manifests in find_files_for_compilation(path):
        files[path] = open_item(path, manifests)

    return files

def populate_fields():
    "OUTDATED"
    """Populate object with empty fields""" 
    pass

def compile():
    """Compiles data"""
    files = get_files('src/')    
    print(files)
    # apply graphs / known algos
    export_all()
    # * maybe check if file is stale and then apply algos
     
    # merge with static files

    # output to dist dir
