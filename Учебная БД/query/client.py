from .util import *

def clients_from_db():
    query = "SELECT * FROM client"
    return get_data_from_db(query)

def add_client_data(full_name, passport_num, date_of_birth, phone, disc_card, total_amount, passport_series, issue_date, issued_by, discount_percentage):
    query = """
            INSERT INTO public.client (full_name, passport_num, date_of_birth, phone, disc_card, total_amount, passport_series, issue_date, "Issued_by", discount_percentage)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            """
    params = (full_name, passport_num, date_of_birth, phone, disc_card, total_amount, passport_series, issue_date, issued_by, discount_percentage)
    return post_data_from_db(query, params)

def clients_with_discount_10():
    query = """
    SELECT *
    FROM client
    WHERE discount_percentage = 10
    """
    return get_data_from_db(query)

    
def update_client_data(client_id, full_name, passport_num, date_of_birth, phone, disc_card, total_amount, passport_series, issue_date, issued_by, discount_percentage):
    query = """
            UPDATE public.client
            SET full_name = %s,
                passport_num = %s,
                date_of_birth = %s,
                phone = %s,
                disc_card = %s,
                total_amount = %s,
                passport_series = %s,
                issue_date = %s,
                "Issued_by" = %s,
                discount_percentage = %s
            WHERE id = %s;
            """
    params = (full_name, passport_num, date_of_birth, phone, disc_card, total_amount, passport_series, issue_date, issued_by, discount_percentage, client_id)
    return post_data_from_db(query, params)
    
def delete_client_data(client_id):
    
    delete_sold_products_query = """
    DELETE FROM public.sold_product
    WHERE sale_id IN (
        SELECT id
        FROM public.sale
        WHERE client_id = %s
    );
    """
    sold_products_params = (client_id,)
    post_data_from_db(delete_sold_products_query, sold_products_params)

    
    delete_sales_query = """
    DELETE FROM public.sale
    WHERE client_id = %s;
    """
    sales_params = (client_id,)
    post_data_from_db(delete_sales_query, sales_params)

    
    delete_client_query = """
    DELETE FROM public.client
    WHERE id = %s;
    """
    client_params = (client_id,)
    post_data_from_db(delete_client_query, client_params)
    
def clients_with_birthday_in_10_days(date):
    query = """
    SELECT *
    FROM public.client
    WHERE EXTRACT(DAY FROM date_of_birth) BETWEEN EXTRACT(DAY FROM %s::date) AND EXTRACT(DAY FROM %s::date + INTERVAL '10 days')
    AND EXTRACT(MONTH FROM date_of_birth) = EXTRACT(MONTH FROM %s::date)
    """
    return get_data_from_db(query, (date, date, date,))

