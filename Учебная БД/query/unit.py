from .util import *

def unit_from_db():
    query = "SELECT * FROM unit"
    return get_data_from_db(query)