from .util import *

def sales_from_db():
    query = """
            SELECT
                s.id AS sale_id,
                c.full_name AS client_name, 
                p.name AS product_name,
                p.price AS product_price,
                sp.quantity AS quantity_sold, 
                s.date AS sale_date
            FROM sale s
            JOIN client c ON s.client_id = c.id
            JOIN sold_product sp ON s.id = sp.sale_id
            JOIN product p ON sp.product_id = p.id
            """
    return get_data_from_db(query)

def sale_insert_db(client_id, product_id, quantity, sale_date):
    try:
        # Вставка в таблицу sale и возврат id
        query = """
        INSERT INTO sale (client_id, date)
        VALUES (%s, %s)
        RETURNING id;
        """
        params = (client_id, sale_date)
        print("Insert sale query:", query)  # Отладочный вывод
        print("Insert sale params:", params)  # Отладочный вывод
        inserted_sale_id = post_data_from_db(query, params)
        
        print("inserted_sale_id:", inserted_sale_id)  # Отладочный вывод
        
        # Прямое использование возвращенного id
        if inserted_sale_id is not None:          
            # Вставка в таблицу sold_product
            query = """
            INSERT INTO sold_product (sale_id, product_id, quantity)
            VALUES (%s, %s, %s);
            """
            params = (inserted_sale_id, product_id, quantity)
            print("Insert sold product query:", query)  # Отладочный вывод
            print("Insert sold product params:", params)  # Отладочный вывод
            post_data_from_db(query, params)
            
            return inserted_sale_id
        else:
            print("Failed to insert into sale table")  # Отладочный вывод
            return None
    except Exception as e:
        print("An error occurred:", str(e))  # Вывод ошибки в консоль
        return None


def sale_update_db(sale_id, client_id, product_id, quantity, sale_date):
    try:
        query = """
        UPDATE sale
        SET client_id = %s, date = %s
        WHERE id = %s;
        """
        params = (client_id, sale_date, sale_id)
        post_data_from_db(query, params)

        query = """
        DELETE FROM sold_product
        WHERE sale_id = %s;
        """
        params = (sale_id,)
        post_data_from_db(query, params)

        query = """
        INSERT INTO sold_product (sale_id, product_id, quantity)
        VALUES (%s, %s, %s);
        """
        params = (sale_id, product_id, quantity)
        post_data_from_db(query, params)
    except Exception as e:
        print("An error occurred:", str(e))  # Вывод ошибки в консоль


def sale_delete_db(sale_id):
    try:
        query = """
        DELETE FROM sold_product
        WHERE sale_id = %s;
        """
        params = (sale_id,)
        post_data_from_db(query, params)

        query = """
        DELETE FROM sale
        WHERE id = %s;
        """
        params = (sale_id,)
        post_data_from_db(query, params)
    except Exception as e:
        print("An error occurred:", str(e))  # Вывод ошибки в консоль
