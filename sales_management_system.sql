CREATE DATABASE IF NOT EXISTS sales_management_system;
USE sales_management_system;

DROP TABLE IF EXISTS sales;
DROP TABLE IF EXISTS employees;

CREATE TABLE employees (
    employee_id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100),
    position VARCHAR(50),
    commission_rate DECIMAL(5,2)
);

CREATE TABLE sales (
    sale_id INT AUTO_INCREMENT PRIMARY KEY,
    employee_id INT,
    sale_date DATE,
    amount DECIMAL(10,2),
    FOREIGN KEY (employee_id) REFERENCES employees(employee_id)
);

INSERT INTO employees (name, position, commission_rate) VALUES
('Anan Sukjai', 'Sales Executive', 5.00),
('Kanya Meesuk', 'Sales Executive', 6.00),
('Narin Thongdee', 'Senior Sales', 7.00),
('Pimchanok Lertsri', 'Sales Coordinator', 4.50),
('Thanawat Boonmee', 'Sales Staff', 5.50);

INSERT INTO sales (employee_id, sale_date, amount) VALUES
(1, '2026-04-01', 12000.00),
(1, '2026-04-02', 8500.00),
(1, '2026-04-03', 15000.00),
(2, '2026-04-01', 9500.00),
(2, '2026-04-02', 11000.00),
(2, '2026-04-03', 7000.00),
(3, '2026-04-01', 20000.00),
(3, '2026-04-02', 18000.00),
(3, '2026-04-03', 22000.00),
(4, '2026-04-01', 6000.00),
(4, '2026-04-02', 7500.00),
(5, '2026-04-01', 13000.00),
(5, '2026-04-03', 9000.00);