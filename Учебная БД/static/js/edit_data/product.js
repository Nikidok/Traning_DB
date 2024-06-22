import { sendRequest } from './util.js';

function showProductForm(action) {
    let formTitle = '';
    let formContent = '';
    let formButton = '';

    if (action === 'edit') {
        formTitle = `Изменить данные о товаре`;
        formContent = `
            <input type="text" id="input-id" placeholder="Введите ID изменяемого товара">
            <input type="text" id="input-name" placeholder="Введите название">
            <input type="text" id="input-remains" placeholder="Введите количество">
            <input type="text" id="input-product-type-id" placeholder="Введите ID типа продукта">
            <input type="text" id="input-unit-id" placeholder="Введите ID единицы измерения">
            <input type="text" id="input-price" placeholder="Введите цену">
        `;
        formButton = '<button class="btn-a" id="form-submit">Изменить</button>';
    } else if (action === 'add') {
        formTitle = `Добавить новый товар`;
        formContent = `
            <input type="text" id="input-name" placeholder="Введите название">
            <input type="text" id="input-remains" placeholder="Введите количество">
            <input type="text" id="input-product-type-id" placeholder="Введите ID типа продукта">
            <input type="text" id="input-unit-id" placeholder="Введите ID единицы измерения">
            <input type="text" id="input-price" placeholder="Введите цену">
        `;
        formButton = '<button class="btn-a" id="form-submit">Добавить</button>';
    } else if (action === 'delete') {
        formTitle = `Удалить товар из базы`;
        formContent = `<input type="text" id="input-id" placeholder="Введите ID удаляемого объекта">`;
        formButton = '<button class="btn-a" id="form-submit">Удалить</button>';
    }

    document.querySelector('.formButton').innerHTML = formButton;
    document.getElementById('formTitle').innerHTML = formTitle;
    document.getElementById('formContent').innerHTML = formContent;

    document.getElementById('form-submit').addEventListener('click', function() {
        if (action === 'add') {
            const product = {
                name: document.getElementById('input-name').value,
                remains: document.getElementById('input-remains').value,
                product_type_id: document.getElementById('input-product-type-id').value,
                store_id: 58,
                unit_id: document.getElementById('input-unit-id').value,
                price: document.getElementById('input-price').value
            };
            sendRequest('http://127.0.0.1:5000/add_product', 'POST', product);
        } else if (action === 'delete') {
            const productId = document.getElementById('input-id').value;
            sendRequest('http://127.0.0.1:5000/delete_product', 'DELETE', { id: productId });
        } else if (action === 'edit') {
            const product = {
                id: document.getElementById('input-id').value,
                name: document.getElementById('input-name').value,
                remains: document.getElementById('input-remains').value,
                product_type_id: document.getElementById('input-product-type-id').value,
                store_id: 58,
                unit_id: document.getElementById('input-unit-id').value,
                price: document.getElementById('input-price').value
            };
            sendRequest('http://127.0.0.1:5000/update_product', 'PUT', product);
        }
    });
}

export { showProductForm };
