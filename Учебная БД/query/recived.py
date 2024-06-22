from .util import *

def recived_products_from_db():
    query =  """
            SELECT rp.id AS "Received Product ID",
                p.name AS "Product Name",
                rp.quantity AS "Quantity",
                rp.price AS "Price",
                i.date AS "Received Date"
            FROM public.recived_product rp
            JOIN public.product p ON rp.product_id = p.id
            JOIN public.invoice i ON rp.invoice_id = i.id;
            """
    return get_data_from_db(query)

def received_product_insert_db(product_id, quantity, price, delivery_date):
    try:
        
        invoice_query = """
        INSERT INTO invoice (date)
        VALUES (%s)
        RETURNING id;
        """
        invoice_params = (delivery_date,)
        print("Insert invoice query:", invoice_query) 
        print("Insert invoice params:", invoice_params) 

        invoice_result = get_data_from_db(invoice_query, invoice_params)
        invoice_id = invoice_result[0][0] if invoice_result else None

        if invoice_id is None:
            raise Exception("Failed to insert invoice and retrieve invoice_id.")

        received_product_query = """
        INSERT INTO recived_product (invoice_id, product_id, quantity, price)
        VALUES (%s, %s, %s, %s);
        """
        received_product_params = (invoice_id, product_id, quantity, price)
        print("Insert received product query:", received_product_query)  
        print("Insert received product params:", received_product_params) 
        
        post_data_from_db(received_product_query, received_product_params)
        
    except Exception as e:
        print("An error occurred:", str(e))  

def update_received_product_db(id, product_id, quantity, price, delivery_date):
    try:
        # Обновление данных в таблице invoice
        update_invoice_query = """
        UPDATE invoice
        SET date = %s
        WHERE id = %s;
        """
        update_invoice_params = (delivery_date, id)
        print("Update invoice query:", update_invoice_query)
        print("Update invoice params:", update_invoice_params)
        
        post_data_from_db(update_invoice_query, update_invoice_params)

        # Обновление данных в таблице recived_product
        update_received_product_query = """
        UPDATE recived_product
        SET quantity = %s, price = %s
        WHERE invoice_id = %s AND product_id = %s;
        """
        update_received_product_params = (quantity, price, id, product_id)
        print("Update received product query:", update_received_product_query)
        print("Update received product params:", update_received_product_params)
        
        post_data_from_db(update_received_product_query, update_received_product_params)
        
    except Exception as e:
        print("Произошла ошибка:", str(e))


def delete_received_product_db(id):
    try:
        # Запрос на удаление данных из таблицы recived_product
        delete_received_product_query = """
        DELETE FROM recived_product
        WHERE id = %s;
        """
        delete_received_product_params = (id,)
        print("Delete received product query:", delete_received_product_query)
        print("Delete received product params:", delete_received_product_params)
        
        post_data_from_db(delete_received_product_query, delete_received_product_params)
        
    except Exception as e:
        print("Произошла ошибка:", str(e))










def sales_dynamics_from_db(start_date, end_date, product_id):
    received_products = recived_products_from_db()

    query = """
            SELECT 
                TO_CHAR(months.month, 'YYYY-MM') AS "Месяц",
                COALESCE(SUM(sp.quantity), 0) AS "Проданное количество",
                COALESCE(SUM(rp.quantity), 0) AS "Полученное количество"
            FROM 
                (SELECT generate_series(
                    DATE_TRUNC('month', %s::date), 
                    DATE_TRUNC('month', %s::date) + INTERVAL '1 month' - INTERVAL '1 day', 
                    '1 month'::interval
                )::date) AS months(month)
            LEFT JOIN 
                public.sale s ON TO_CHAR(s.date, 'YYYY-MM') = TO_CHAR(months.month, 'YYYY-MM')
            LEFT JOIN 
                public.sold_product sp ON s.id = sp.sale_id AND sp.product_id = %s
            LEFT JOIN 
                (SELECT 
                    DATE_TRUNC('month', i.date) AS month, 
                    SUM(rp.quantity) AS quantity
                FROM 
                    public.recived_product rp
                JOIN 
                    public.invoice i ON rp.invoice_id = i.id
                WHERE 
                    rp.product_id = %s
                GROUP BY 
                    month) rp 
                ON TO_CHAR(rp.month, 'YYYY-MM') = TO_CHAR(months.month, 'YYYY-MM')
            WHERE 
                sp.product_id = %s
            GROUP BY 
                TO_CHAR(months.month, 'YYYY-MM')
            ORDER BY 
                TO_CHAR(months.month, 'YYYY-MM');
            """
    try:
        print("Запрос:", query)  # Отладочный вывод
        params = (start_date, end_date, product_id, product_id, product_id)
        print("Параметры:", params)  # Отладочный вывод
        sales_data = get_data_from_db(query, params)
        
        # Объединяем данные о продажах и поступлениях
        for row in sales_data:
            month = row[0]  # Используем числовой индекс для доступа к данным
            received_quantity = next((rp[2] for rp in received_products if rp[4].strftime('%Y-%m') == month), 0)
            row = list(row)  # Преобразуем кортеж в список, чтобы обновить значение
            row[2] = received_quantity  # Обновляем полученное количество
        return sales_data
    except Exception as e:
        print(f"Ошибка базы данных: {e}")
        return None