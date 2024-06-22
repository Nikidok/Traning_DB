from typing import OrderedDict
from flask import Flask, render_template, request, jsonify
from query.client import *
from query.product import *
from query.recived import *
from query.sale import *
from query.util import *
from query.unit import *
from query.product_type import *

app = Flask(__name__)

# Смена страниц
@app.route("/")
def mainPage():
    return render_template("base.html")

@app.route('/analysis_data')
def analysis_data():
    return render_template('analysis.html')

@app.route('/edit_data')
def edit_data():
    return render_template('edit.html')

# Обращение к запросам
# Выборка данных
@app.route('/get_clients', methods=['GET'])
def get_clients():
    clients = clients_from_db()
    clients_data = [
        OrderedDict([
            ("id", client[0]),
            ("ФИО", client[1]),
            ("Дата рождения", client[3]),
            ("Номер телефона", client[4]),
            ("Наличие дисконтной карты", client[5]),
            ("Сумма трат", client[6]),
            ("Скидка", client[10])
        ]) for client in clients
    ]
    return jsonify(clients_data)

@app.route('/get_products', methods=['GET'])
def get_products():
    products = products_from_db()
    products_data = [
        OrderedDict([
            ("id", product[0]),
            ("Название", product[1]),
            ("Остаток", product[2]),
            ("Цена", product[6])
        ]) for product in products
    ]
    return jsonify(products_data)

@app.route('/get_sales', methods=['GET'])
def get_sales():
    sales = sales_from_db()
    sales_data = [
        OrderedDict([
            ("id", sale[0]),
            ("Имя клиента", sale[1]),
            ("Продукт", sale[2]),
            ("Цена", sale[3]),
            ("Кол-во", sale[4]),
            ("Дата", sale[5])
        ]) for sale in sales
    ]
    return jsonify(sales_data)

@app.route('/get_received', methods=['GET'])
def get_received():
    received_products = recived_products_from_db()
    received_products_data = [
    OrderedDict([
            ("id", product[0]),
            ("Название продукта", product[1]),
            ("Количество", product[2]),
            ("Цена", product[3]),
            ("Дата поступления", product[4])
        ]) for product in received_products 
    ]
    return jsonify(received_products_data)

@app.route('/get_unit', methods=['GET'])
def get_unit():
    units = unit_from_db()
    units_data = [
        OrderedDict([
            ("id", unit[0]),
            ("Название", unit[1])
        ]) for unit in units
    ]
    return jsonify(units_data)

@app.route('/get_product_type', methods=['GET'])
def get_product_type():
    types = product_type_from_db()
    types_data = [
        OrderedDict([
            ("id", type_item[0]),
            ("Название", type_item[1])
        ]) for type_item in types
    ]
    return jsonify(types_data)

@app.route('/get_clients_discount_10', methods=['GET'])
def get_clients_discount_10():
    clients = clients_with_discount_10()
    clients_data = [
        OrderedDict([
            ("id", client[0]),
            ("ФИО", client[1]),
            ("Дата рождения", client[3]),
            ("Номер телефона", client[4]),
            ("Наличие дисконтной карты", client[5]),
            ("Сумма трат", client[6]),
            ("Скидка", client[10])
        ]) for client in clients
    ]
    return jsonify(clients_data)

@app.route('/get_clients_birthday_in_10_days/<date>', methods=['GET'])
def get_clients_birthday_in_10_days(date):
    clients = clients_with_birthday_in_10_days(date)
    clients_data = [
        OrderedDict([
            ("id", client[0]),
            ("ФИО", client[1]),
            ("Дата рождения", client[3]),
            ("Номер телефона", client[4]),
            ("Наличие дисконтной карты", client[5]),
            ("Сумма трат", client[6]),
            ("Скидка", client[10])
        ]) for client in clients
    ]
    return jsonify(clients_data)

@app.route('/sales-dynamics', methods=['GET'])
def get_sales_dynamics():
    product_id = request.args.get('product_id', type=int)
    start_date = request.args.get('start_date', default='2000-01-01', type=str)
    end_date = request.args.get('end_date', default='2024-12-31', type=str)

    if not product_id:
        return jsonify({"error": "Product ID is required"}), 400
    
    sales_dynamics = sales_dynamics_from_db(start_date, end_date, product_id)
    
    if not sales_dynamics:
        return jsonify({"error": "No data found"}), 404

    sales_dynamics_data = [
        OrderedDict([
            ("Месяц", sale[0]),
            ("Кол-во проданного товара", sale[1]),
            ("Кол-во поступившего товара", sale[2])
        ]) for sale in sales_dynamics 
    ]
    
    return jsonify(sales_dynamics_data)

# Изменение данных
# Изменение данных о клиентах
@app.route('/add_client', methods=['POST'])
def add_client():
    client_data = request.json
    add_client_data(
        client_data['full_name'],
        client_data['passport_num'],
        client_data['date_of_birth'],
        client_data['phone'],
        client_data['disc_card'],
        client_data['total_amount'],
        client_data['passport_series'],
        client_data['issue_date'],
        client_data['issued_by'],
        client_data['discount_percentage']
    )
    return jsonify({'message': 'Client added successfully'}), 201

@app.route('/update_client', methods=['PUT'])
def update_client():
    client_data = request.json
    update_client_data(
        client_data['id'],
        client_data['full_name'],
        client_data['passport_num'],
        client_data['date_of_birth'],
        client_data['phone'],
        client_data['disc_card'],
        client_data['total_amount'],
        client_data['passport_series'],
        client_data['issue_date'],
        client_data['issued_by'],
        client_data['discount_percentage']
    )
    return jsonify({'message': 'Client updated successfully'}), 200

@app.route('/delete_client', methods=['DELETE'])
def delete_client_route():
    data = request.get_json()
    client_id = data['id']
    delete_client_data(client_id)
    return jsonify({'message': 'Client deleted successfully'}), 200


# Изменение товаров
@app.route('/add_product', methods=['POST'])
def add_product():
    product_data = request.json
    product_insert_db(
        product_data['name'],
        product_data['remains'],
        product_data['product_type_id'],
        product_data['store_id'],
        product_data['unit_id'],
        product_data['price']
    )
    return jsonify({'message': 'Product added successfully'}), 201


@app.route('/delete_product', methods=['DELETE'])
def delete_product():
    product_id = request.json.get('id')
    del_product(product_id)
    return jsonify({'message': 'Product deleted successfully'}), 200

@app.route('/update_product', methods=['PUT'])
def update_product():
    product_data = request.json
    product_update_db(
        product_data['id'],
        product_data['name'],
        product_data['remains'],
        product_data['product_type_id'],
        product_data['store_id'],
        product_data['unit_id'],
        product_data['price']
    )
    return jsonify({'message': 'Product updated successfully'}), 200

# Изменение данных
@app.route('/add_sale', methods=['POST'])
def add_sale():
    try:
        sale_data = request.json
        
        sale_id = sale_insert_db(
            sale_data['client_id'],
            sale_data['product_id'],
            sale_data['quantity'],
            sale_data['sale_date']
        )
        
        if sale_id is not None:
            print("Sale added successfully with ID:", sale_id)  # Отладочный вывод
            return jsonify({'message': 'Sale added successfully', 'sale_id': sale_id}), 201
        else:
            print("Failed to add sale: inserted_sale_id is None")  # Отладочный вывод
            return jsonify({'message': 'Failed to add sale: inserted_sale_id is None'}), 500
    except Exception as e:
        print("An error occurred:", str(e))  
        return jsonify({'message': 'An error occurred', 'error': str(e)}), 500


@app.route('/delete_sale', methods=['DELETE'])
def delete_sale():
    data = request.get_json()
    sale_id = data['id']
    if sale_delete_db(sale_id):
        return jsonify({'message': 'Sale deleted successfully'}), 200
    else:
        return jsonify({'message': 'Failed to delete sale'}), 500

@app.route('/update_sale', methods=['PUT'])
def update_sale():
    data = request.get_json()
    sale_id = data['id']
    client_id = data['client_id']
    product_id = data['product_id']
    quantity = data['quantity']
    sale_date = data['sale_date']
    if sale_update_db(sale_id, client_id, product_id, quantity, sale_date):
        return jsonify({'message': 'Sale updated successfully'}), 200
    else:
        return jsonify({'message': 'Failed to update sale'}), 500
    
    
@app.route('/add_received_product', methods=['POST'])
def add_received_product():
    try:
        received_product_data = request.json
        
        product_id = received_product_data['product_id']
        quantity = received_product_data['quantity']
        price = received_product_data['price']
        delivery_date = received_product_data['receipt_date']

        
        received_product_insert_db(product_id, quantity, price, delivery_date)
        
        return jsonify({'message': 'Received product added successfully'}), 201
    except Exception as e:
        print("An error occurred:", str(e)) 
        return jsonify({'message': 'An error occurred', 'error': str(e)}), 500

@app.route('/update_received_product', methods=['PUT'])
def update_received_product():
    try:
        received_product_data = request.json 
        
        # Извлечение параметров из полученных данных JSON
        id = received_product_data['id']
        product_id = received_product_data['product_id']
        quantity = received_product_data['quantity']
        price = received_product_data['price']
        receipt_date = received_product_data['receipt_date']  

        # Обновление данных о полученном товаре в базе данных
        update_received_product_db(id, product_id, quantity, price, receipt_date)
        
        return jsonify({'message': 'Данные о поставленном товаре успешно обновлены'}), 200
    except Exception as e:
        print("Произошла ошибка:", str(e))  
        return jsonify({'message': 'Произошла ошибка', 'error': str(e)}), 500

@app.route('/delete_received_product', methods=['DELETE'])
def delete_received_product_route():
    try:
        data = request.get_json()
        received_product_id = data['id']
        if delete_received_product_db(received_product_id):
            return jsonify({'message': 'Received product deleted successfully'}), 200
        else:
            return jsonify({'message': 'Failed to delete received product'}), 500
    except Exception as e:
        print("Произошла ошибка:", str(e))
        return jsonify({'message': 'Failed to delete received product', 'error': str(e)}), 500


# Запуск приложения
if __name__ == '__main__':
    app.run(debug=True)