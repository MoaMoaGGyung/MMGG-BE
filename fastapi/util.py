import json

def read_department_name_by_id(id):
    with open ('./static/site_nm.json', 'r') as f:
        site_nm_dict = json.load(f)
    
    department_name = [k for k, v in site_nm_dict.items() if v == id][0]
    return department_name

def read_site_nm_dict():
    with open ('./static/site_nm.json', 'r') as f:
        site_nm_dict = json.load(f)
        
    return site_nm_dict

def get_base_url(id):
    with open ('./static/site_attach_base_url.json', 'r') as f:
        site_nm_dict = json.load(f)
        
        
    url = site_nm_dict.get(str(id))
    print(url)
    
        
    return url