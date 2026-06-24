let currentUser = null;
let books = [];

function showModal(modalId) {
    document.getElementById(modalId).classList.add('show');
}

function closeModal() {
    document.querySelectorAll('.modal').forEach(m => m.classList.remove('show'));
}

function toggleGuestMode() {
    const guestMode = document.getElementById('guest-mode').checked;
    document.getElementById('login-input').disabled = guestMode;
    document.getElementById('password-input').disabled = guestMode;
}

async function loadBooks() {
    try {
        const search = document.getElementById('search-input').value;
        const genre = document.getElementById('genre-filter').value;
        const inStock = document.getElementById('stock-filter').checked;
        const sort = document.getElementById('sort-select').value;
        
        let url = '/api/books?';
        if (search) url += `search=${encodeURIComponent(search)}&`;
        if (genre) url += `genre=${encodeURIComponent(genre)}&`;
        if (inStock) url += 'in_stock=true&';
        if (sort === 'publication_date') url += 'sort_by=publication_date&sort_order=desc&';
        if (sort === 'publication_date_asc') url += 'sort_by=publication_date&sort_order=asc&';
        
        const response = await fetch(url);
        books = await response.json();
        renderBooks(books);
    } catch (error) {
        console.error('Error loading books:', error);
    }
}

function renderBooks(books) {
    const grid = document.getElementById('books-grid');
    const today = new Date();
    const twoYearsAgo = new Date();
    twoYearsAgo.setFullYear(today.getFullYear() - 2);
    
    grid.innerHTML = books.map(book => {
        const pubDate = new Date(book.publication_date);
        const daysSincePub = (today - pubDate) / (1000 * 60 * 60 * 24);
        const isNew = daysSincePub < 30;
        const isOldStock = daysSincePub > 730 && book.stock > 5;
        
        let cardClass = 'book-card';
        if (isOldStock) cardClass += ' old-stock';
        
        let titleClass = 'book-title';
        if (isNew) titleClass += ' new';
        
        const genres = book.genre_names.join(', ');
        const rating = '⭐'.repeat(Math.round(book.rating));
        
        return `
            <div class="${cardClass}">
                <img src="${book.image_path || '/assets/placeholder.jpg'}" 
                     alt="${book.title}" 
                     class="book-image"
                     onerror="this.src='/assets/placeholder.jpg'">
                <div class="book-info">
                    <div class="${titleClass}">
                        ${book.title}
                        ${book.is_electronic ? '<span class="electronic-badge">E-book</span>' : ''}
                    </div>
                    <div class="book-genres">${genres}</div>
                    <div class="book-rating">${rating}</div>
                    <div class="book-price">${book.price} ₽</div>
                    <div style="font-size:0.8rem;color:#888;">${book.publication_date}</div>
                    ${currentUser && currentUser.role === 'admin' ? `
                        <button onclick="editBook(${book.book_id})" style="margin-top:0.5rem;padding:0.25rem 0.5rem;cursor:pointer;">Редактировать</button>
                        <button onclick="deleteBook(${book.book_id})" style="margin-top:0.5rem;padding:0.25rem 0.5rem;cursor:pointer;background:#ff4444;color:white;border:none;border-radius:3px;">Удалить</button>
                    ` : ''}
                </div>
            </div>
        `;
    }).join('');
}

async function loadGenres() {
    try {
        const response = await fetch('/api/books');
        const books = await response.json();
        const genres = new Set();
        books.forEach(book => {
            book.genre_names.forEach(g => genres.add(g));
        });
        
        const select = document.getElementById('genre-filter');
        genres.forEach(genre => {
            const option = document.createElement('option');
            option.value = genre;
            option.textContent = genre;
            select.appendChild(option);
        });
    } catch (error) {
        console.error('Error loading genres:', error);
    }
}