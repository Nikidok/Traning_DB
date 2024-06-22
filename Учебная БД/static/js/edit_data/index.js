import { showProductForm } from './product.js';
import { showClientForm } from './client.js';
import { showSaleForm } from './sale.js';
import { showInvoiceForm } from './invoice.js';

document.addEventListener("DOMContentLoaded", function() {
    let currentCategory = '';

    function initializePopup() {
        function togglePopUp(category) {
            const popUp = document.getElementById('pop_up');
            if (popUp) {
                popUp.style.display = 'block';
                currentCategory = category;
            }
        }

        function closePopUp() {
            const popUp = document.getElementById('pop_up');
            const initialActions = document.getElementById('initialActions');
            const formContainer = document.getElementById('formContainer');
            if (popUp && initialActions && formContainer) {
                popUp.style.display = 'none';
                initialActions.style.display = 'block';
                formContainer.style.display = 'none';
                currentCategory = '';
            }
        }

        function showForm(action) {
            const initialActions = document.getElementById('initialActions');
            const formContainer = document.getElementById('formContainer');

            if (initialActions && formContainer) {
                initialActions.style.display = 'none';
                formContainer.style.display = 'block';

                if (currentCategory === 'товар') {
                    showProductForm(action);
                } else if (currentCategory === 'клиент') {
                    showClientForm(action);
                } else if (currentCategory === 'продажа') {
                    showSaleForm(action);
                } else if (currentCategory === 'поступление') {
                    showInvoiceForm(action);
                }
            }
        }

        const productsEditBtn = document.getElementById('products-edit');
        if (productsEditBtn) {
            productsEditBtn.addEventListener('click', function() {
                togglePopUp('товар');
            });
        }

        const clientsEditBtn = document.getElementById('clients-edit');
        if (clientsEditBtn) {
            clientsEditBtn.addEventListener('click', function() {
                togglePopUp('клиент');
            });
        }

        const salesEditBtn = document.getElementById('sales-edit');
        if (salesEditBtn) {
            salesEditBtn.addEventListener('click', function() {
                togglePopUp('продажа');
            });
        }

        const invoicesEditBtn = document.getElementById('invoices-edit');
        if (invoicesEditBtn) {
            invoicesEditBtn.addEventListener('click', function() {
                togglePopUp('поступление');
            });
        }

        const editBtn = document.getElementById('edit-btn');
        if (editBtn) {
            editBtn.addEventListener('click', function() {
                showForm('edit');
            });
        }

        const addBtn = document.getElementById('add-btn');
        if (addBtn) {
            addBtn.addEventListener('click', function() {
                showForm('add');
            });
        }

        const deleteBtn = document.getElementById('delete-btn');
        if (deleteBtn) {
            deleteBtn.addEventListener('click', function() {
                showForm('delete');
            });
        }

        const popUpCloseBtn = document.getElementById('pop_up_close');
        if (popUpCloseBtn) {
            popUpCloseBtn.addEventListener('click', closePopUp);
        }
    }

    initializePopup();
});
