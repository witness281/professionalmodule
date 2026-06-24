-- Добавление ролей пользователей
INSERT INTO users (full_name, login, password_hash, role) VALUES
('Администратор', 'admin', '$2b$12$...', 'admin'),
('Менеджер', 'manager', '$2b$12$...', 'manager'),
('Продавец', 'seller', '$2b$12$...', 'seller');

-- Добавление издателей
INSERT INTO publishers (publisher_name) VALUES
('АСТ'), ('Росмэн'), ('Азбука'), ('МИФ'), ('Эксмо');

-- Добавление жанров
INSERT INTO genres (genre_name) VALUES
('Антиутопия'), ('Фэнтези'), ('Ужасы'), ('Детектив'),
('Классическая проза'), ('Приключения'), ('Научная фантастика'),
('Военная проза'), ('Нон-фикшн');

-- Добавление книг (примеры из файла Books.xlsx)
INSERT INTO books (title, author, publisher_id, rating, price, stock, is_electronic, publication_date, description) VALUES
('1984', 'Джордж Оруэлл', 1, 4.8, 550, 12, FALSE, '1949-06-08', 'Культовый роман-антиутопия о тоталитарном обществе будущего'),
('Гарри Поттер и философский камень', 'Дж. К. Роулинг', 2, 4.9, 890, 7, FALSE, '1997-06-26', 'Первая книга серии о юном волшебнике'),
('Мастер и Маргарита', 'Михаил Булгаков', 3, 4.9, 750, 3, FALSE, '1967-01-01', 'Мистический роман о визите дьявола в Москву'),
('451 градус по Фаренгейту', 'Рэй Брэдбери', 3, 4.6, 490, 9, FALSE, '1953-10-19', 'Роман о будущем, где книги сжигают'),
('Атомные привычки', 'Джеймс Клир', 4, 4.7, 690, 0, TRUE, '2018-10-16', 'Как маленькие изменения приводят к большим результатам');

-- Связи книг с жанрами
INSERT INTO book_genres (book_id, genre_id) VALUES
(1, 1), -- 1984 -> Антиутопия
(2, 2), -- Гарри Поттер -> Фэнтези
(3, 5), -- Мастер и Маргарита -> Классическая проза
(4, 7), -- 451 градус -> Научная фантастика
(5, 9); -- Атомные привычки -> Нон-фикшн

-- Добавление тестовых заказов
INSERT INTO orders (customer_id, order_date, delivery_date, status) VALUES
(1, CURRENT_DATE - INTERVAL '10 days', CURRENT_DATE - INTERVAL '5 days', 'Завершен'),
(2, CURRENT_DATE - INTERVAL '3 days', CURRENT_DATE + INTERVAL '2 days', 'В обработке'),
(3, CURRENT_DATE - INTERVAL '7 days', CURRENT_DATE - INTERVAL '1 day', 'Просрочен');

INSERT INTO order_items (order_id, book_id, quantity, price_at_time) VALUES
(1, 1, 2, 550),
(1, 3, 1, 750),
(2, 2, 1, 890),
(3, 4, 3, 490);