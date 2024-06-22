import { sendRequest } from './util.js';

function showInvoiceForm(action) {
    let formTitle = '';
    let formContent = '';
    let formButton = '';

    if (action === 'edit') {
        formTitle = `Изменить данные о поступлении`;
        formContent = `
            <input type="text" id="input-id" placeholder="Введите ID">
            <input type="text" id="input-price" placeholder="Введите цену">
            <input type="text" id="input-product-id" placeholder="Введите ID продукта">
            <input type="text" id="input-quantity-received" placeholder="Введите количество полученного товара">
            <input type="date" id="input-receipt-date" placeholder="Введите дату поступления">
        `;
        formButton = '<button class="btn-a" id="form-submit">Изменить</button>';
    } else if (action === 'add') {
        formTitle = `Добавить новое поступление`;
        formContent = `
            <input type="text" id="input-price" placeholder="Введите цену товара">
            <input type="text" id="input-product-id" placeholder="Введите ID продукта">
            <input type="text" id="input-quantity-received" placeholder="Введите количество полученного товара">
            <input type="date" id="input-receipt-date" placeholder="Введите дату поступления">
        `;
        formButton = '<button class="btn-a" id="form-submit">Добавить</button>';
    } else if (action === 'delete') {
        formTitle = `Удалить поступление из базы`;
        formContent = `<input type="text" id="input-id" placeholder="Введите ID удаляемого поступления">`;
        formButton = '<button class="btn-a" id="form-submit">Удалить</button>';
    }

    document.querySelector('.formButton').innerHTML = formButton;
    document.getElementById('formTitle').innerHTML = formTitle;
    document.getElementById('formContent').innerHTML = formContent;

    document.getElementById('form-submit').addEventListener('click', function() {
        if (action === 'add') {
            const invoice = {
                product_id: document.getElementById('input-product-id').value,
                quantity: document.getElementById('input-quantity-received').value,
                price: document.getElementById('input-price').value,
                receipt_date: document.getElementById('input-receipt-date').value
            };
            sendRequest('http://127.0.0.1:5000/add_received_product', 'POST', invoice);
        } else if (action === 'delete') {
            const invoiceId = document.getElementById('input-id').value;
            sendRequest('http://127.0.0.1:5000/delete_received_product', 'DELETE', { id: invoiceId });
        } else if (action === 'edit') {
            const invoice = {
                id: document.getElementById('input-id').value,
                price: document.getElementById('input-price').value,
                product_id: document.getElementById('input-product-id').value,
                quantity: document.getElementById('input-quantity-received').value,
                receipt_date: document.getElementById('input-receipt-date').value
            };
            sendRequest('http://127.0.0.1:5000/update_received_product', 'PUT', invoice);
        }
    });
}

export { showInvoiceForm };
