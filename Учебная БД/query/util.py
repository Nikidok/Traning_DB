import psycopg2
from config import host, user as db_user, password, db_name

# Подключение к бд
# Подключение к бд
# Подключение к бд
def execute_query(query, params=None, fetch=False, return_id=False):
    try:
        with psycopg2.connect(host=host, user=db_user, password=password, database=db_name) as conn:
            with conn.cursor() as cur:
                if params:
                    cur.execute(query, params)
                else:
                    cur.execute(query)
                if return_id:
                    return cur.fetchone()[0] if cur.description else None  # Проверка на наличие данных
                if fetch:
                    return cur.fetchall()
                conn.commit()
    except psycopg2.Error as e:
        print("Ошибка при работе с PostgreSQL:", e)
        conn.rollback()


# Выборка данных из бд
def get_data_from_db(query, params=None):
    return execute_query(query, params, fetch=True)

def post_data_from_db(query, params=None):
    return execute_query(query, params, fetch=False, return_id=True)
