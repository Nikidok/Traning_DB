import { sendRequest, calculateDiscount } from './util.js';

function showClientForm(action) {
    let formTitle = '';
    let formContent = '';
    let formButton = '';

    if (action === 'edit') {
        formTitle = `Изменить данные о клиенте`;
        formContent = `
            <input type="text" id="input-id" placeholder="Введите ID изменяемого клиента">
            <input type="text" id="input-full-name" placeholder="Введите полное имя">
            <input type="text" id="input-passport-num" placeholder="Введите номер паспорта">
            <label for="input-date-of-birth">Введите дату рождения:</label>
            <input type="date" id="input-date-of-birth" placeholder="Введите дату рождения">
            <input type="text" id="input-phone" placeholder="Введите номер телефона">
            <input type="text" id="input-total-amount" placeholder="Введите общую сумму покупок">
            <input type="text" id="input-passport-series" placeholder="Введите серию паспорта">
            <label for="input-issue-date">Введите дату выдачи паспорта:</label>
            <input type="date" id="input-issue-date" placeholder="Введите дату выдачи паспорта">
            <input type="text" id="input-issued-by" placeholder="Введите кем выдан паспорт">
        `;
        formButton = '<button class="btn-a" id="form-submit">Изменить</button>';
    } else if (action === 'add') {
        formTitle = `Добавить нового клиента`;
        formContent = `
            <input type="text" id="input-full-name" placeholder="Введите полное имя">
            <input type="text" id="input-passport-num" placeholder="Введите номер паспорта">
            <label for="input-date-of-birth">Введите дату рождения:</label>
            <input type="date" id="input-date-of-birth" placeholder="Введите дату рождения">
            <input type="text" id="input-phone" placeholder="Введите номер телефона">
            <input type="text" id="input-total-amount" placeholder="Введите общую сумму покупок">
            <input type="text" id="input-passport-series" placeholder="Введите серию паспорта">
            <label for="input-issue-date">Введите дату выдачи паспорта:</label>
            <input type="date" id="input-issue-date" placeholder="Введите дату выдачи паспорта">
            <input type="text" id="input-issued-by" placeholder="Введите кем выдан паспорт">
        `;
        formButton = '<button class="btn-a" id="form-submit">Добавить</button>';
    } else if (action === 'delete') {
        formTitle = `Удалить клиента из базы`;
        formContent = `<input type="text" id="input-id" placeholder="Введите ID удаляемого объекта">`;
        formButton = '<button class="btn-a" id="form-submit">Удалить</button>';
    }

    document.querySelector('.formButton').innerHTML = formButton;
    document.getElementById('formTitle').innerHTML = formTitle;
    document.getElementById('formContent').innerHTML = formContent;

    document.getElementById('form-submit').addEventListener('click', function() {
        if (action === 'add') {
            const client = {
                full_name: document.getElementById('input-full-name').value,
                passport_num: document.getElementById('input-passport-num').value,
                date_of_birth: document.getElementById('input-date-of-birth').value,
                phone: document.getElementById('input-phone').value,
                disc_card: (parseInt(document.getElementById('input-total-amount').value) > 10000) ? true : false,
                total_amount: document.getElementById('input-total-amount').value,
                passport_series: document.getElementById('input-passport-series').value,
                issue_date: document.getElementById('input-issue-date').value,
                issued_by: document.getElementById('input-issued-by').value,
                discount_percentage: calculateDiscount(document.getElementById('input-total-amount').value)
            };
            console.log("Добавил");
            sendRequest('http://127.0.0.1:5000/add_client', 'POST', client);
        } else if (action === 'delete') {
            const clientId = document.getElementById('input-id').value;
            sendRequest('http://127.0.0.1:5000/delete_client', 'DELETE', { id: clientId });
        } else if (action === 'edit') {
            const client = {
                id: document.getElementById('input-id').value,
                full_name: document.getElementById('input-full-name').value,
                passport_num: document.getElementById('input-passport-num').value,
                date_of_birth: document.getElementById('input-date-of-birth').value,
                phone: document.getElementById('input-phone').value,
                disc_card: (parseInt(document.getElementById('input-total-amount').value) > 10000) ? true : false,
                total_amount: document.getElementById('input-total-amount').value,
                passport_series: document.getElementById('input-passport-series').value,
                issue_date: document.getElementById('input-issue-date').value,
                issued_by: document.getElementById('input-issued-by').value,
                discount_percentage: calculateDiscount(document.getElementById('input-total-amount').value)
            };
            sendRequest('http://127.0.0.1:5000/update_client', 'PUT', client);
        }
    });
    
}

export { showClientForm };
