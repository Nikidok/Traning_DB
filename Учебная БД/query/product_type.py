from .util import *

def product_type_from_db():
    query = "SELECT * FROM product_type"
    return get_data_from_db(query)