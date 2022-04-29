from Compilator.categories import validate
from Compilator.categories import get_relevant_categories
from Compilator.state import State

def valid_data_type(value, value_t):
    if value_t == "Bool" and type(value) is bool:
        return True
    if value_t == "String" and type(value) is str:
        return True
    if value_t == "StringNone" and (type(value) is str or value is None):
        return True
    if value_t == "Integer" and type(value) is int:
        return True
    if value_t == "Integer[]" and type(value) is list and all(map(lambda x: type(x) is int, value)):
        return True
    return False

def fetch_value(obj_main: dict, key: str, value_t: str, invalid = []):
    value = obj_main['properties'].get(key, None)
    #print(k, t, val)
    #if val is None:
    #    continue

    if value_t.endswith('{}'):
        value_t = value_t[:-2]
        
        if value is dict:
            dct = value
            value = dct['value']
            if valid_data_type(value, value_t):
                return (value, dct)
    elif valid_data_type(value, value_t):
        return (value,)
    
    if State.force > 0:
        if (obj_main.get(key) is not None):
            obj_main.pop(key)
        return (None,)

    error_msg = (obj_main['file'], "typeError", value, "| expected:", value_t, "on:", key)
    if invalid is None:
        raise ValueError(error_msg)
    else:
        invalid.append(error_msg)
    return (None,)
def validate(obj_main, manifest, invalid = []):
    """Checks for validity of the .c.yaml file according to set categories. If the files fail to pass, it appends the data into `invalid` array argument for error handling"""
    manifest_data = get_relevant_categories(frozenset(manifest))
    obj = obj_main.get('properties', {})
    obj_main['properties'] = obj
    #check if mandatory data are filled
    required = map(lambda kvs: kvs[0], filter(lambda kvs: kvs[1]['mandatory'] == True, manifest_data.items()))
    s = set(required)
    if not s.issubset(obj.keys()):
        s -= set(obj.keys()) 
        invalid.append((obj_main['file'], 'missingKeyError', s))
    
    #check data integrity
    for key, value in obj_main['properties'].items():
        fetch_value(obj_main, key, manifest_data[key]['type'], invalid)  

