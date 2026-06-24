async function loadOrders() {
    try {
        const response = await fetch('/api/orders');
        const orders = await response.json();
        renderOrders(orders);
    } catch (error) {
        console.error('Error loading orders:', error);
    }
}

function renderOrders(orders) {
    const container = document.getElementById('orders-list');
    const today = new Date();
    
    container.innerHTML = orders.map(order => {
        const deliveryDate = new Date(order.delivery_date);
        const isOverdue = deliveryDate < today && order.status !== 'Завершен';
        
        return `
            <div class="order-card ${isOverdue ? 'overdue' : ''}">
                <div class="order-header">
                    <strong>Заказ №${order.order_id}</strong>
                    <span>${order.customer_name}</span>
                    <span>${order.status}</span>
                </div>
                <div style="color:#888;font-size:0.9rem;">
                    Дата заказа: ${new Date(order.order_date).toLocaleDateString()}
                    | Дата доставки: ${new Date(order.delivery_date).toLocaleDateString()}
                    ${isOverdue ? ' ⚠️ ПРОСРОЧЕН!' : ''}
                </div>
                <div class="order-items">
                    ${order.items.map(item => `
                        <div>${item.book_title} × ${item.quantity} = ${item.price_at_time * item.quantity} ₽</div>
                    `).join('')}
                </div>
                ${currentUser && ['admin', 'manager'].includes(currentUser.role) ? `
                    <div class="order-controls">
                        <select onchange="updateOrder(${order.order_id}, 'status', this.value)">
                            <option value="Новый" ${order.status === 'Новый' ? 'selected' : ''}>Новый</option>
                            <option value="В обработке" ${order.status === 'В обработке' ? 'selected' : ''}>В обработке</option>
                            <option value="Отправлен" ${order.status === 'Отправлен' ? 'selected' : ''}>Отправлен</option>
                            <option value="Завершен" ${order.status === 'Завершен' ? 'selected' : ''}>Завершен</option>
                            <option value="Просрочен" ${order.status === 'Просрочен' ? 'selected' : ''}>Просрочен</option>
                        </select>
                        <input type="date" value="${order.delivery_date}" 
                               onchange="updateOrder(${order.order_id}, 'delivery_date', this.value)">
                        <button onclick="updateOrder(${order.order_id}, 'delivery_date', '${order.delivery_date}')">Сохранить</button>
                    </div>
                ` : ''}
            </div>
        `;
    }).join('');
}

async function updateOrder(orderId, field, value) {
    const data = { [field]: value };
    try {
        const response = await fetch(`/api/orders/${orderId}`, {
            method: 'PUT',
            headers: { 
                'Content-Type': 'application/json',
                'Authorization': `Bearer ${localStorage.getItem('token')}`
            },
            body: JSON.stringify(data)
        });
        
        if (response.ok) {
            loadOrders();
        } else {
            alert('Ошибка обновления заказа');
        }
    } catch (error) {
        alert('Ошибка подключения к серверу');
    }
}