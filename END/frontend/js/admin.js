function showAddBookForm() {
    const form = document.getElementById('add-book-form');
    form.classList.toggle('hidden');
}

async function addBook(event) {
    event.preventDefault();
    
    const formData = new FormData();
    formData.append('title', document.getElementById('book-title').value);
    formData.append('author', document.getElementById('book-author').value);
    formData.append('publisher_name', document.getElementById('book-publisher').value);
    formData.append('price', document.getElementById('book-price').value);
    formData.append('stock', document.getElementById('book-stock').value);
    formData.append('publication_date', document.getElementById('book-date').value);
    formData.append('genre_names', document.getElementById('book-genres').value);
    
    const imageFile = document.getElementById('book-image').files[0];
    if (imageFile) {
        formData.append('image', imageFile);
    }
    
    try {
        const response = await fetch('/api/books', {
            method: 'POST',
            headers: {
                'Authorization': `Bearer ${localStorage.getItem('token')}`
            },
            body: formData
        });
        
        if (response.ok) {
            alert('Книга добавлена успешно');
            document.getElementById('book-form').reset();
            document.getElementById('add-book-form').classList.add('hidden');
            loadBooks();
        } else {
            const error = await response.json();
            alert(error.detail || 'Ошибка добавления книги');
        }
    } catch (error) {
        alert('Ошибка подключения к серверу');
    }
}

async function deleteBook(bookId) {
    if (!confirm('Вы уверены, что хотите удалить эту книгу?')) return;
    
    try {
        const response = await fetch(`/api/books/${bookId}`, {
            method: 'DELETE',
            headers: {
                'Authorization': `Bearer ${localStorage.getItem('token')}`
            }
        });
        
        if (response.ok) {
            alert('Книга удалена');
            loadBooks();
        } else {
            const error = await response.json();
            alert(error.detail || 'Ошибка удаления книги');
        }
    } catch (error) {
        alert('Ошибка подключения к серверу');
    }
}

async function editBook(bookId) {
    // Реализация редактирования книги (можно сделать модальное окно с формой)
    alert('Функция редактирования книги (задание для самостоятельной реализации)');
}