from Compilator.categories import Category
from Compilator.data import DataItem
import pandas as pd
import functools

@functools.lru_cache()
def fetch_cats():
    trunc_hidden = lambda x: not x.key.startswith('_')
    all_cats = filter(trunc_hidden, Category.known.values())
    return all_cats

def fetch_table(dataItems = DataItem.dataItems):
    all_cats = fetch_cats()
    table = pd.DataFrame(index=dataItems.keys(), columns=list(map(lambda x: x.key, all_cats)))
    for k,v in dataItems.items():
        for cat in all_cats:
            table.at[k,cat.key] = 'N/A'

        for valKey, valValue in filter(lambda x: not x[0].startswith('_'), v.values.items()):
            table.at[k,valKey] = str(valValue.value)
    return table

def export_table():
    all_cats = fetch_cats()
    table = fetch_table()
    # gathered all fields into a so-so table

    sorted(all_cats)
    with open('dist/autotable.md', 'w') as fp:
        fp.write('# Autotable \n\n')
        fp.write(table.to_markdown())
        fp.write('\n\n')
