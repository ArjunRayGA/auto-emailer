import json
import re
import os
import copy
import webbrowser
import data_filters as data_filters_lib

def popup_compose (email, title, markdown, cc_emails):
    link_to_gmail = "https://mail.google.com/mail/?view=cm&fs=1&to={}&su={}&body={}&cc={}".format(email, title, markdown, cc_emails)
    webbrowser.open_new(link_to_gmail)

def rename_cols (df, col_rename_dict=None):
    if not col_rename_dict:
        return df
    col_names = list(df.columns)
    for col_data in col_rename_dict:
        col_names[col_data["index"]] = col_data["name"]
    df.columns = col_names
    return df

def run_data_filters(df, data_filters=None):
    if not data_filters:
        return df
    for data_filter in data_filters:
        try:
            kwargs = data_filter['kwargs']
            filter_func = getattr(data_filters_lib, data_filter["name"])
            df = filter_func(df, **kwargs)
        except AttributeError:
            pass    
    return df

def find_replace_refs(JSON_obj):

    filename = JSON_obj["filename"]
    file_path = os.path.abspath(filename)
    file_dir = os.path.dirname(file_path)

    find_ref = re.compile('\$ref=(?:[.]{0,2})(?:[\/]{0,1})[\w\-.\/]*.json::[\w\-. ]*')

    def find_regex(obj):

        def insert_json(ref):
            rel_path = ref.split('$ref=')[1].split('::')[0]
            json_index = ref.split('::')[1]

            load_path = os.path.normpath(os.path.join(file_dir, rel_path))
            insert_obj =json.load(open(load_path))

            if len(json_index) == 0:
                return insert_obj
            else:
                return eval('insert_obj{}'.format(json_index))

            
        def check_node(val):
            if type(val) in [dict, list]:
                return find_regex(val)
            elif type(val) is unicode and find_ref.search(val):
                return insert_json(val)
            else:
                return val

    
        if isinstance(obj, dict):
            new = {}
            for key, val in obj.iteritems():
                new_val = check_node(val)
                new[key] = new_val
            return new

        elif isinstance(obj, list):
            new = []
            for i, val in enumerate(obj):
                new_val = check_node(val)
                new.append(new_val)
            return new

    replaced_json = find_regex(JSON_obj["JSON"])
    return replaced_json


def settings_loader(files):
    json_list = [{"JSON": json.load(open(f)), "filename": f} for f in files]
    settings_dict = {}

    for item in json_list: 
        setting_name = os.path.basename(item['filename']).replace('.json', '')
        settings_dict[setting_name] = find_replace_refs(item)
    
    return settings_dict