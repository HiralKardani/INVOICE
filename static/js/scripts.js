document.addEventListener('DOMContentLoaded', () => {
    // Product Page Script
    const productForm = document.getElementById('product-form');
    const productTableBody = document.getElementById('product-table').querySelector('tbody');

    productForm.addEventListener('submit', (event) => {
        event.preventDefault();
        
        const productName = document.getElementById('product-name').value;
        const productDescription = document.getElementById('product-description').value;
        const productPrice = document.getElementById('product-price').value;
        
        const newRow = productTableBody.insertRow();
        newRow.innerHTML = `
            <td>${productName}</td>
            <td>${productDescription}</td>
            <td>$${parseFloat(productPrice).toFixed(2)}</td>
            <td><button class="remove-item">Remove</button></td>
        `;

        productForm.reset();

        newRow.querySelector('.remove-item').addEventListener('click', () => {
            newRow.remove();
        });
    });

    // Customer Page Script
    const customerForm = document.getElementById('customer-form');
    const customerTableBody = document.getElementById('customer-table').querySelector('tbody');

    customerForm.addEventListener('submit', (event) => {
        event.preventDefault();

        const customerName = document.getElementById('customer-name').value;
        const customerAddress = document.getElementById('customer-address').value;
        const customerPhone = document.getElementById('customer-phone').value;
        const customerEmail = document.getElementById('customer-email').value;

        const newRow = customerTableBody.insertRow();
        newRow.innerHTML = `
            <td>${customerName}</td>
            <td>${customerAddress}</td>
            <td>${customerPhone}</td>
            <td>${customerEmail}</td>
            <td><button class="remove-item">Remove</button></td>
        `;

        customerForm.reset();

        newRow.querySelector('.remove-item').addEventListener('click', () => {
            newRow.remove();
        });
    });

    // New Invoice Page Script
    const addItemBtn = document.getElementById('add-item');
    const itemsTableBody = document.getElementById('items-table').querySelector('tbody');
    const subtotalEl = document.getElementById('subtotal');
    const taxEl = document.getElementById('tax');
    const totalEl = document.getElementById('total');
    const taxRate = 0.10;

    const updateTotals = () => {
        let subtotal = 0;

        itemsTableBody.querySelectorAll('tr').forEach(row => {
            const quantity = parseInt(row.querySelector('input[name="item-quantity"]').value);
            const price = parseFloat(row.querySelector('input[name="item-price"]').value);
            const total = quantity * price;
            subtotal += total;
            row.querySelector('.item-total').textContent = `$${total.toFixed(2)}`;
        });

        const tax = subtotal * taxRate;
        const total = subtotal + tax;

        subtotalEl.textContent = `$${subtotal.toFixed(2)}`;
        taxEl.textContent = `$${tax.toFixed(2)}`;
        totalEl.textContent = `$${total.toFixed(2)}`;
    };

    addItemBtn.addEventListener('click', () => {
        const newRow = itemsTableBody.insertRow();
        newRow.innerHTML = `
            <td><input type="text" name="item-description" required></td>
            <td><input type="number" name="item-quantity" value="1" min="1" required></td>
            <td><input type="number" name="item-price" value="0.00" min="0" step="0.01" required></td>
            <td class="item-total">$0.00</td>
            <td><button type="button" class="remove-item">Remove</button></td>
        `;

        newRow.querySelectorAll('input').forEach(input => {
            input.addEventListener('input', updateTotals);
        });

        newRow.querySelector('.remove-item').addEventListener('click', () => {
            newRow.remove();
            updateTotals();
        });

        updateTotals();
    });

    // Initial update for any default row in the table
    updateTotals();
});

