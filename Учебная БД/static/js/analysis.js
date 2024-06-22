import { formatter, fetchData } from './util.js';

document.addEventListener("DOMContentLoaded", function() {
    const main = document.querySelector('main');
    const datePicker = document.getElementById('date-picker');
    const startDateInput = document.getElementById('start-date');
    const endDateLabel = document.getElementById('end-date-label');
    const endDateInput = document.getElementById('end-date');
    const productIdInput = document.getElementById('product-id');
    const dataContainer = document.getElementById('data-container');
    const functionButton = document.getElementById('function');
    const product_idLabel = document.getElementById('label-product-id');
    

    let currentHandler = null;

    function hideDatePicker() {
        datePicker.style.display = 'none';
        endDateLabel.style.display = 'none';
        endDateInput.style.display = 'none';
        productIdInput.style.display = 'none';
    }

    function showDatePicker(showEndDate = false) {
        datePicker.style.display = 'block';
        endDateLabel.style.display = showEndDate ? 'inline' : 'none';
        endDateInput.style.display = showEndDate ? 'inline' : 'none';
        productIdInput.style.display = showEndDate ? 'inline' : 'none';
        product_idLabel.style.display = showEndDate ? 'inline' : 'none';
    }

    function createTableHeader(table, keysOrder) {
        const header = table.createTHead();
        const headerRow = header.insertRow();
        keysOrder.forEach(key => {
            const th = document.createElement('th');
            th.textContent = key;
            headerRow.appendChild(th);
        });
    }

    function createTable(data, keysOrder) {
        const table = document.createElement('table');
        table.classList.add('custom-table');
        createTableHeader(table, keysOrder);

        const tbody = table.createTBody();
        data.forEach(item => {
            const row = tbody.insertRow();
            keysOrder.forEach(key => {
                const cell = row.insertCell();
                if (['Дата', 'Дата рождения', 'Дата поступления'].includes(key)) {
                    cell.textContent = new Date(item[key]).toLocaleDateString();
                } else if (typeof item[key] === 'boolean') {
                    cell.textContent = item[key] ? 'Есть' : 'Нет';
                } else if (['Цена', 'Сумма трат'].includes(key)) {
                    cell.textContent = formatter.format(item[key]);
                } else if (key === "Скидка") {
                    cell.textContent = item[key] + "%";
                } else {
                    cell.textContent = item[key];
                }
            });
        });

        return table;
    }

    function addEventListenerOnce(buttonId, eventHandler) {
        if (currentHandler) {
            functionButton.removeEventListener('click', currentHandler);
        }
        functionButton.addEventListener('click', eventHandler);
        currentHandler = eventHandler;
    }

    function salesDynamicsClickHandler() {
        dataContainer.innerHTML = '';
        const startDate = startDateInput.value;
        const endDate = endDateInput.value;
        const productId = productIdInput.value;
        const url = `http://127.0.0.1:5000/sales-dynamics?start_date=${startDate}&end_date=${endDate}&product_id=${productId}`;
        fetchData(url).then(data => {
            console.log(data);
            if (data) {
                dataContainer.appendChild(createTable(data, ['Месяц', 'Кол-во проданного товара', 'Кол-во поступившего товара']));
            }
        });
    }

    function birthdayClientsClickHandler() {
        dataContainer.innerHTML = '';
        const startDate = startDateInput.value;
        const endDate = endDateInput.value;
        const url = `http://127.0.0.1:5000/get_clients_birthday_in_10_days/${startDate}`;
        fetchData(url).then(data => {
            if (data) {
                dataContainer.appendChild(createTable(data, ['id', 'ФИО', 'Дата рождения', 'Номер телефона', 'Сумма трат']));
            }
        });
    }

    document.querySelectorAll('.analysis-btn').forEach(btn => {
        btn.addEventListener('click', async function() {
            dataContainer.innerHTML = '';
            hideDatePicker();

            switch (btn.id) {
                case 'products':
                    const productsData = await fetchData('http://127.0.0.1:5000/get_products');
                    if (productsData) dataContainer.appendChild(createTable(productsData, ['id', 'Название', 'Остаток', 'Цена']));
                    break;
                case 'clients':
                    const clientsData = await fetchData('http://127.0.0.1:5000/get_clients');
                    if (clientsData) dataContainer.appendChild(createTable(clientsData, ['id', 'ФИО', 'Дата рождения', 'Номер телефона', 'Наличие дисконтной карты', 'Сумма трат', "Скидка"]));
                    break;
                case 'sales':
                    const salesData = await fetchData('http://127.0.0.1:5000/get_sales');
                    if (salesData) dataContainer.appendChild(createTable(salesData, ['id', 'Имя клиента', 'Продукт', 'Кол-во', 'Цена', 'Дата']));
                    break;
                case 'invoices':
                    const invoicesData = await fetchData('http://127.0.0.1:5000/get_received');
                    if (invoicesData) dataContainer.appendChild(createTable(invoicesData, ['id', 'Название продукта', 'Количество', 'Цена', 'Дата поступления']));
                    break;
                case 'unit':
                    const unitData = await fetchData('http://127.0.0.1:5000/get_unit');
                    if (unitData) dataContainer.appendChild(createTable(unitData, ['id', 'Название']));
                    console.log("Ед. измерения");
                    break;
                case 'type-product':
                    const typeProductData = await fetchData('http://127.0.0.1:5000/get_product_type');
                    if (typeProductData) dataContainer.appendChild(createTable(typeProductData, ['id', 'Название']));
                    console.log("Тип товара");
                    break;
                case 'client-disc':
                    const clientDiscData = await fetchData('http://127.0.0.1:5000/get_clients_discount_10');
                    if (clientDiscData) dataContainer.appendChild(createTable(clientDiscData, ['id', 'ФИО', 'Дата рождения', 'Номер телефона', 'Наличие дисконтной карты', 'Сумма трат', "Скидка"]));
                    break;
                case 'clients-birthdays':
                    showDatePicker();
                    addEventListenerOnce(btn.id, birthdayClientsClickHandler);
                    break;
                case 'sales-dynamics':
                    showDatePicker(true);
                    addEventListenerOnce(btn.id, salesDynamicsClickHandler);
                    break;
                default:
                    break;
            }
        });
    });
});
