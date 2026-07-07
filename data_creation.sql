CREATE DATABASE bookstore_db;
USE bookstore_db;

show tables;
desc inventory_borrow;

USE bookstore_db;

-- ===========================
-- INSERT INTO inventory_category
-- ===========================

INSERT INTO inventory_category (name, description, created_at)
VALUES
('Fiction', 'Fictional novels and stories', NOW()),
('Science', 'Science and Technology books', NOW()),
('History', 'Historical books', NOW()),
('Programming', 'Programming and Software Development', NOW()),
('Biography', 'Life stories of famous people', NOW());


-- ===========================
-- INSERT INTO inventory_book
-- ===========================

INSERT INTO inventory_book
(title, author, isbn, price, stock_quantity, publication_date, created_at, updated_at, category_id)
VALUES
('The Alchemist', 'Paulo Coelho', '9780061122415', 499.00, 10, '1988-04-15', NOW(), NOW(), 1),

('A Brief History of Time', 'Stephen Hawking', '9780553380163', 650.00, 5, '1988-03-01', NOW(), NOW(), 2),

('Sapiens', 'Yuval Noah Harari', '9780099590088', 799.00, 8, '2011-09-04', NOW(), NOW(), 3),

('Python Crash Course', 'Eric Matthes', '9781593279288', 950.00, 12, '2019-05-03', NOW(), NOW(), 4),

('Steve Jobs', 'Walter Isaacson', '9781451648539', 720.00, 6, '2011-10-24', NOW(), NOW(), 5);



select * from auth_user;

delete from auth_user;

SET SQL_SAFE_UPDATES = 0;