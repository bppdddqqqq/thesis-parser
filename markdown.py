import os
import re
from Compilator.data import DataItem
def markdown_files_iterator(path = 'src/'):
    files = os.listdir(path)

    for file in files:
        new_path = path + '/' + file
        if os.path.isdir(new_path):
            yield from markdown_files_iterator(new_path)
        elif os.path.isfile(new_path):
            if file.endswith('.md'):
                yield new_path

markdown_func = re.compile(r"#!([^\(]+\([^\)]+\))")

def markdown_functions_finder():
    for file in markdown_files_iterator():
        with open(file, 'r', encoding='utf-8') as md:
            buf = md.read()
            
            changes = []
            for match in markdown_func.findall(buf):
                res = {'res': None}
                exec(f"res = {match}", commands, res)
                changes.append((match, res['res']))

            if len(changes) == 0:
                continue
            for pair in changes:
#                print(pair)
                buf = buf.replace('#!'+pair[0], pair[1], 1)

            new_path = file.replace('src/', 'dist/', 1)
            os.makedirs('/'.join(new_path.split('/')[:-1]), exist_ok=True)
            with open(new_path, 'w') as md_new:
                md_new.write(buf)

def markdown_get(key, category):
    item = DataItem.dataItems[key]

    return item.values.get(category, 'N/A')
commands = {'markdown_get': markdown_get}

def markdown_compiler():
    markdown_functions_finder()
