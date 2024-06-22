import { sendRequest } from './util.js';

function showSaleForm(action) {
    let formTitle = '';
    let formContent = '';
    let formButton = '';

    if (action === 'edit') {
        formTitle = `Изменить данные о продаже`;
        formContent = `
            <input type="text" id="input-id" placeholder="Введите ID">
            <input type="text" id="input-client-id" placeholder="Введите ID клиента">
            <input type="text" id="input-product-id" placeholder="Введите ID продукта">
            <input type="text" id="input-quantity-sold" placeholder="Введите количество проданного товара">
            <label for="input-sale-date">Введите дату продажи:</label>
            <input type="date" id="input-sale-date" placeholder="Введите дату продажи">
        `;
        formButton = '<button class="btn-a" id="form-submit">Изменить</button>';
    } else if (action === 'add') {
        formTitle = `Добавить новую продажу`;
        formContent = `
            <input type="text" id="input-client-id" placeholder="Введите ID клиента">
            <input type="text" id="input-product-id" placeholder="Введите ID продукта">
            <input type="text" id="input-quantity-sold" placeholder="Введите количество проданного товара">
            <label for="input-sale-date">Введите дату продажи:</label>
            <input type="date" id="input-sale-date" placeholder="Введите дату продажи">
        `;
        formButton = '<button class="btn-a" id="form-submit">Добавить</button>';
    } else if (action === 'delete') {
        formTitle = `Удалить продажу из базы`;
        formContent = `<input type="text" id="input-id" placeholder="Введите ID удаляемой продажи">`;
        formButton = '<button class="btn-a" id="form-submit">Удалить</button>';
    }

    document.querySelector('.formButton').innerHTML = formButton;
    document.getElementById('formTitle').innerHTML = formTitle;
    document.getElementById('formContent').innerHTML = formContent;

    document.getElementById('form-submit').addEventListener('click', function() {
        if (action === 'add') {
            const sale = {
                client_id: document.getElementById('input-client-id').value,
                product_id: document.getElementById('input-product-id').value,
                quantity: document.getElementById('input-quantity-sold').value,
                sale_date: document.getElementById('input-sale-date').value
            };
            sendRequest('http://127.0.0.1:5000/add_sale', 'POST', sale);
        } else if (action === 'delete') {
            const saleId = document.getElementById('input-id').value;
            sendRequest('http://127.0.0.1:5000/delete_sale', 'DELETE', { id: saleId });
        } else if (action === 'edit') {
            const sale = {
                id: document.getElementById('input-id').value,
                client_id: document.getElementById('input-client-id').value,
                product_id: document.getElementById('input-product-id').value,
                quantity: document.getElementById('input-quantity-sold').value,
                sale_date: document.getElementById('input-sale-date').value
            };
            sendRequest('http://127.0.0.1:5000/update_sale', 'PUT', sale);
        }
    });
}

export { showSaleForm };
