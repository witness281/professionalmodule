function toggleAuth() {
    if (currentUser) {
        logout();
    } else {
        showModal('auth-modal');
    }
}

async function login(event) {
    event.preventDefault();
    const guestMode = document.getElementById('guest-mode').checked;
    
    if (guestMode) {
        currentUser = { role: 'guest', full_name: 'Гость' };
        updateUI();
        closeModal();
        return;
    }
    
    const login = document.getElementById('login-input').value;
    const password = document.getElementById('password-input').value;
    
    try {
        const response = await fetch('/api/auth/login', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ login, password })
        });
        
        if (!response.ok) {
            const error = await response.json();
            alert(error.detail || 'Ошибка входа');
            return;
        }
        
        const data = await response.json();
        currentUser = data;
        localStorage.setItem('token', data.access_token);
        updateUI();
        closeModal();
        
        if (currentUser.role === 'admin') {
            document.getElementById('admin-panel').classList.remove('hidden');
        }
        if (['admin', 'manager'].includes(currentUser.role)) {
            document.getElementById('orders-panel').classList.remove('hidden');
            loadOrders();
        }
        
        loadBooks();
    } catch (error) {
        alert('Ошибка подключения к серверу');
    }
}

function logout() {
    currentUser = null;
    localStorage.removeItem('token');
    updateUI();
    document.getElementById('admin-panel').classList.add('hidden');
    document.getElementById('orders-panel').classList.add('hidden');
    loadBooks();
}

function updateUI() {
    const userName = document.getElementById('user-name');
    const authBtn = document.getElementById('auth-btn');
    
    if (currentUser) {
        userName.textContent = currentUser.full_name || currentUser.login || 'Пользователь';
        authBtn.textContent = 'Выйти';
    } else {
        userName.textContent = 'Гость';
        authBtn.textContent = 'Войти';
    }
}

// Проверяем токен при загрузке
async function checkAuth() {
    const token = localStorage.getItem('token');
    if (!token) return;
    
    try {
        const response = await fetch('/api/auth/me', {
            headers: { 'Authorization': `Bearer ${token}` }
        });
        
        if (response.ok) {
            const user = await response.json();
            currentUser = user;
            currentUser.role = user.role;
            currentUser.full_name = user.full_name;
            updateUI();
            
            if (currentUser.role === 'admin') {
                document.getElementById('admin-panel').classList.remove('hidden');
            }
            if (['admin', 'manager'].includes(currentUser.role)) {
                document.getElementById('orders-panel').classList.remove('hidden');
                loadOrders();
            }
        } else {
            localStorage.removeItem('token');
        }
    } catch (error) {
        console.error('Auth check error:', error);
    }
}