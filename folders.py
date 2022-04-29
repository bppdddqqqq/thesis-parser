import os
from yaml import load, Loader, dump
import itertools
from Compilator.categories import get_relevant_categories
from Compilator.data import validate
from Compilator.schema import enabler_schema
from Compilator.graphs import export_all
from Compilator.error import raise_invalids
from Compilator.state import State
# parse folders and find relevant files to parse

def find_files_for_compilation(path, enabled_categories=set()):
    """Iterator that returns a tuple with path and a set of categories that should be evaluated by the compilator for specified file."""
    files = os.listdir(path)
    cur_categories = enabled_categories.copy()

    if ('.enableCompilator' in files):
        manifest = load(open(path+'/.enableCompilator'), Loader=Loader)
        if manifest.get("clearAll", None):
            cur_categories = set()
        else:
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

    manifest_all = set()
    for file, manifest in find_files_for_compilation(path):
        #print(file, manifest)
        obj_main = load(open(file), Loader=Loader)
        obj_main['file'] = file
        res = validate(obj_main, manifest, invalid)
        files[file] = obj_main
        if files[file] is None:
            files[file] = {}
        manifest_all.update(manifest)

    return (files, manifest_all, invalid)

def populate_fields(path= 'src/'):
    """Populate object with empty fields""" 
    (files, manifest_all, invalid) = get_files(path)
    for i in invalid:
        if i[1] == "missingKeyError":
            # (file, "typeError", missingItems)
            for field in i[2]:
                print(f"Added missing {field} to {i[0]}")
                files[i[0]]['properties'][field] = None
    if State.dry_run > 0:
        return
    for k, v in files.items():
        with open(k, 'w') as output:
            dump(v, output, default_flow_style=False)


def compile(path = 'src/', distpath = 'dist/'):
    """Compiles data"""
    (files, manifest_all, invalid) = get_files(path)
    if len(invalid) != 0:
        raise_invalids(invalid)

    # apply graphs / known algos
    manifest_data = get_relevant_categories(frozenset(manifest_all))
    if State.dry_run == 0:
        export_all(files, manifest_data)
    # * maybe check if file is stale and then apply algos
     
    # merge with static files

    # output to dist dir
