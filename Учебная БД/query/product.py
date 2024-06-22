from .util import *

def products_from_db():
    query = "SELECT * FROM product"
    return get_data_from_db(query)

# Изменение данных о товаре
def product_insert_db(name, remains, product_type_id, store_id, unit_id, price):
    query = """
    INSERT INTO public.product (name, remains, product_type_id, store_id, unit_id, price)
    VALUES (%s, %s, %s, %s, %s, %s);
    """
    params = (name, remains, product_type_id, store_id, unit_id, price)
    return post_data_from_db(query, params)

def del_product(product_id):
    delete_received_product_query = 'DELETE FROM recived_product WHERE product_id = %s'
    post_data_from_db(delete_received_product_query, (product_id,))
    
    delete_sold_product_query = 'DELETE FROM sold_product WHERE product_id = %s'
    post_data_from_db(delete_sold_product_query, (product_id,))

    delete_product_query = 'DELETE FROM product WHERE id = %s'
    return post_data_from_db(delete_product_query, (product_id,))


def product_update_db(id, name, remains, product_type_id, store_id, unit_id, price):
    query = """
    UPDATE public.product
    SET name = %s,
        remains = %s,
        product_type_id = %s,
        store_id = %s,
        unit_id = %s,
        price = %s
    WHERE id = %s;
    """
    params = (name, remains, product_type_id, store_id, unit_id, price, id)
    return post_data_from_db(query, params)