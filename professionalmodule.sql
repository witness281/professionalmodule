-- ============================================================
-- НАЗВАНИЕ: BookStore - База данных интернет-магазина книг
-- СУБД: MySQL 8.0+
-- ============================================================

-- ============================================================
-- 1. СОЗДАНИЕ И ВЫБОР БАЗЫ ДАННЫХ
-- ============================================================
CREATE DATABASE IF NOT EXISTS bookstore;
USE bookstore;

-- ============================================================
-- 2. УДАЛЕНИЕ СТАРЫХ ТАБЛИЦ (ЕСЛИ СУЩЕСТВУЮТ)
-- ============================================================
DROP TABLE IF EXISTS order_items;
DROP TABLE IF EXISTS orders;
DROP TABLE IF EXISTS book_genres;
DROP TABLE IF EXISTS books;
DROP TABLE IF EXISTS genres;
DROP TABLE IF EXISTS publishers;
DROP TABLE IF EXISTS users;

-- ============================================================
-- 3. СОЗДАНИЕ ТАБЛИЦ
-- ============================================================

-- 3.1. ТАБЛИЦА ПОЛЬЗОВАТЕЛЕЙ
CREATE TABLE users (
    user_id INT AUTO_INCREMENT PRIMARY KEY,
    full_name VARCHAR(100) NOT NULL,
    login VARCHAR(50) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    role ENUM('admin', 'manager', 'seller', 'guest') DEFAULT 'guest',
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- 3.2. ТАБЛИЦА ИЗДАТЕЛЕЙ
CREATE TABLE publishers (
    publisher_id INT AUTO_INCREMENT PRIMARY KEY,
    publisher_name VARCHAR(100) UNIQUE NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- 3.3. ТАБЛИЦА ЖАНРОВ
CREATE TABLE genres (
    genre_id INT AUTO_INCREMENT PRIMARY KEY,
    genre_name VARCHAR(50) UNIQUE NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- 3.4. ТАБЛИЦА КНИГ
CREATE TABLE books (
    book_id INT AUTO_INCREMENT PRIMARY KEY,
    title VARCHAR(200) NOT NULL,
    author VARCHAR(100) NOT NULL,
    publisher_id INT,
    rating DECIMAL(3,2) DEFAULT 0.00 CHECK (rating >= 0 AND rating <= 5),
    price DECIMAL(10,2) NOT NULL CHECK (price >= 0),
    stock INT NOT NULL DEFAULT 0 CHECK (stock >= 0),
    is_electronic BOOLEAN DEFAULT FALSE,
    publication_date DATE NOT NULL,
    description TEXT,
    image_path VARCHAR(255),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (publisher_id) REFERENCES publishers(publisher_id) ON DELETE SET NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- 3.5. ТАБЛИЦА СВЯЗИ КНИГ И ЖАНРОВ (МНОГИЕ-КО-МНОГИМ)
CREATE TABLE book_genres (
    book_id INT NOT NULL,
    genre_id INT NOT NULL,
    PRIMARY KEY (book_id, genre_id),
    FOREIGN KEY (book_id) REFERENCES books(book_id) ON DELETE CASCADE,
    FOREIGN KEY (genre_id) REFERENCES genres(genre_id) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- 3.6. ТАБЛИЦА ЗАКАЗОВ
CREATE TABLE orders (
    order_id INT AUTO_INCREMENT PRIMARY KEY,
    customer_id INT,
    order_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    delivery_date DATE,
    status ENUM('Новый', 'В обработке', 'Отправлен', 'Завершен', 'Просрочен') DEFAULT 'Новый',
    total_amount DECIMAL(10,2) DEFAULT 0.00,
    FOREIGN KEY (customer_id) REFERENCES users(user_id) ON DELETE SET NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- 3.7. ТАБЛИЦА ПОЗИЦИЙ ЗАКАЗА
CREATE TABLE order_items (
    order_id INT NOT NULL,
    book_id INT NOT NULL,
    quantity INT NOT NULL CHECK (quantity > 0),
    price_at_time DECIMAL(10,2) NOT NULL CHECK (price_at_time >= 0),
    PRIMARY KEY (order_id, book_id),
    FOREIGN KEY (order_id) REFERENCES orders(order_id) ON DELETE CASCADE,
    FOREIGN KEY (book_id) REFERENCES books(book_id) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- ============================================================
-- 4. СОЗДАНИЕ ИНДЕКСОВ ДЛЯ ПРОИЗВОДИТЕЛЬНОСТИ
-- ============================================================
CREATE INDEX idx_books_title ON books(title);
CREATE INDEX idx_books_author ON books(author);
CREATE INDEX idx_books_publication_date ON books(publication_date);
CREATE INDEX idx_books_price ON books(price);
CREATE INDEX idx_books_rating ON books(rating);
CREATE INDEX idx_orders_status ON orders(status);
CREATE INDEX idx_orders_delivery_date ON orders(delivery_date);
CREATE INDEX idx_orders_customer_id ON orders(customer_id);
CREATE INDEX idx_order_items_book_id ON order_items(book_id);
CREATE INDEX idx_users_login ON users(login);

-- ============================================================
-- 5. ВСТАВКА ТЕСТОВЫХ ДАННЫХ
-- ============================================================

-- 5.1. ПОЛЬЗОВАТЕЛИ
INSERT INTO users (full_name, login, password_hash, role) VALUES
('Администратор', 'admin', '$2b$12$5Xk5T7QK5KXk5T7QK5KXkO', 'admin'),
('Менеджер', 'manager', '$2b$12$5Xk5T7QK5KXk5T7QK5KXkO', 'manager'),
('Продавец', 'seller', '$2b$12$5Xk5T7QK5KXk5T7QK5KXkO', 'seller'),
('Иванов Иван', 'ivanov', '$2b$12$5Xk5T7QK5KXk5T7QK5KXkO', 'guest'),
('Петрова Анна', 'petrova', '$2b$12$5Xk5T7QK5KXk5T7QK5KXkO', 'guest');

-- 5.2. ИЗДАТЕЛИ
INSERT INTO publishers (publisher_name) VALUES
('АСТ'),
('Росмэн'),
('Азбука'),
('МИФ'),
('Эксмо');

-- 5.3. ЖАНРЫ
INSERT INTO genres (genre_name) VALUES
('Антиутопия'),
('Фэнтези'),
('Ужасы'),
('Детектив'),
('Классическая проза'),
('Приключения'),
('Научная фантастика'),
('Военная проза'),
('Нон-фикшн');

-- 5.4. КНИГИ
INSERT INTO books (title, author, publisher_id, rating, price, stock, is_electronic, publication_date, description) VALUES
('1984', 'Джордж Оруэлл', 1, 4.8, 550.00, 12, FALSE, '1949-06-08', 'Культовый роман-антиутопия о тоталитарном обществе будущего'),
('Гарри Поттер и философский камень', 'Дж. К. Роулинг', 2, 4.9, 890.00, 7, FALSE, '1997-06-26', 'Первая книга серии о юном волшебнике'),
('Мастер и Маргарита', 'Михаил Булгаков', 3, 4.9, 750.00, 3, FALSE, '1967-01-01', 'Мистический роман о визите дьявола в Москву'),
('451 градус по Фаренгейту', 'Рэй Брэдбери', 3, 4.6, 490.00, 9, FALSE, '1953-10-19', 'Роман о будущем, где книги сжигают'),
('Атомные привычки', 'Джеймс Клир', 4, 4.7, 690.00, 0, TRUE, '2018-10-16', 'Как маленькие изменения приводят к большим результатам'),
('Сияние', 'Стивен Кинг', 1, 4.5, 620.00, 8, FALSE, '1977-01-28', 'Леденящий кровь роман о проклятом отеле'),
('Код да Винчи', 'Дэн Браун', 1, 4.3, 480.00, 0, FALSE, '2003-03-18', 'Интеллектуальный детектив о тайнах Ватикана'),
('Дюна', 'Фрэнк Герберт', 1, 4.7, 855.00, 11, FALSE, '1965-08-01', 'Эпическая сага о пустынной планете Арракис'),
('Голодные игры', 'Сьюзен Коллинз', 1, 4.4, 520.00, 10, FALSE, '2008-09-14', 'Подростки сражаются за выживание в смертельном шоу'),
('Война и мир', 'Лев Толстой', 3, 4.8, 1110.00, 4, FALSE, '1869-01-01', 'Масштабная эпопея о России начала XIX века'),
('Преступление и наказание', 'Фёдор Достоевский', 3, 4.7, 580.00, 6, FALSE, '1866-01-01', 'Роман о преступлении и нравственных страданиях'),
('Три товарища', 'Эрих Мария Ремарк', 1, 4.8, 580.00, 6, FALSE, '1936-12-01', 'История дружбы на фоне послевоенной Германии'),
('Анна Каренина', 'Лев Толстой', 3, 4.7, 750.00, 5, FALSE, '1877-01-01', 'Трагическая история любви на фоне светского общества'),
('Идиот', 'Фёдор Достоевский', 3, 4.5, 540.00, 7, FALSE, '1869-01-01', 'Роман о трагической судьбе человека высокой души'),
('Граф Монте-Кристо', 'Александр Дюма', 5, 4.6, 860.00, 8, FALSE, '1846-01-01', 'История несправедливо осужденного и его мести'),
('Скотный двор', 'Джордж Оруэлл', 1, 4.6, 380.00, 14, FALSE, '1945-08-17', 'Сатирическая притча о природе власти'),
('Оно', 'Стивен Кинг', 1, 4.4, 780.00, 2, FALSE, '1986-09-15', 'Дети сталкиваются с древним злом в облике клоуна'),
('Хроники Нарнии', 'Клайв С. Льюис', 5, 4.5, 920.00, 5, FALSE, '1950-10-16', 'Дети попадают в волшебную страну через платяной шкаф'),
('Убийство в восточном экспрессе', 'Агата Кристи', 5, 4.5, 470.00, 8, FALSE, '1934-01-01', 'Эркюль Пуаро расследует убийство в поезде'),
('Как завоевывать друзей', 'Дейл Карнеги', 4, 4.5, 540.00, 0, TRUE, '1936-10-01', 'Классика жанра саморазвития и психологии общения');

-- 5.5. СВЯЗИ КНИГ С ЖАНРАМИ
INSERT INTO book_genres (book_id, genre_id) VALUES
(1, 1), (2, 2), (3, 5), (4, 7), (5, 9),
(6, 3), (7, 4), (8, 7), (9, 1), (10, 5),
(11, 5), (12, 8), (13, 5), (14, 5), (15, 6),
(16, 1), (17, 3), (18, 2), (19, 4), (20, 9);

-- 5.6. ЗАКАЗЫ
INSERT INTO orders (customer_id, order_date, delivery_date, status) VALUES
(4, '2026-05-10 10:30:00', '2026-05-15', 'Завершен'),
(5, '2026-06-01 14:20:00', '2026-06-10', 'В обработке'),
(4, '2026-05-20 09:15:00', '2026-05-25', 'Просрочен'),
(5, '2026-06-05 16:45:00', '2026-06-12', 'Новый');

-- 5.7. ПОЗИЦИИ ЗАКАЗОВ
INSERT INTO order_items (order_id, book_id, quantity, price_at_time) VALUES
(1, 1, 2, 550.00),
(1, 3, 1, 750.00),
(2, 2, 1, 890.00),
(3, 4, 3, 490.00),
(4, 10, 1, 1110.00),
(4, 11, 2, 580.00);

-- ============================================================
-- 6. ПРОВЕРКА
-- ============================================================
SELECT '✅ База данных BookStore успешно создана!' AS status;
SELECT CONCAT('📚 Всего книг: ', COUNT(*)) AS info FROM books;
SELECT CONCAT('👥 Всего пользователей: ', COUNT(*)) AS info FROM users;
SELECT CONCAT('📦 Всего заказов: ', COUNT(*)) AS info FROM orders;