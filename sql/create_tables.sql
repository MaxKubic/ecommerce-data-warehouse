#Založení databáze
CREATE DATABASE Warehouse;

#Vytvoření Entity zákazník
CREATE TABLE customers (
                           customer_id INT PRIMARY KEY,
                           first_name VARCHAR(30),
                           last_name VARCHAR(30),
                           email VARCHAR(50),
                           city VARCHAR(50),
                           country VARCHAR(50),
                           created_at DATE
);

#Vytvoření Entity produkty
CREATE TABLE products (
                          product_id INT PRIMARY KEY,
                          product_name VARCHAR(100),
                          category VARCHAR(50),
                          brand VARCHAR(50),
                          price DECIMAL(7,2),
                          cost DECIMAL (7,2)
);

#Vytvoření Entity objednávky
CREATE TABLE orders (
                        order_id INT PRIMARY KEY,
                        customer_id INT,
                        order_date DATETIME,
                        status VARCHAR(20),
                        FOREIGN KEY (customer_id) REFERENCES customers(customer_id)
);

#Vytvoření Entity objednávky
CREATE TABLE order_items (
                             order_item_id INT PRIMARY KEY,
                             order_id INT,
                             product_id INT,
                             quantity INT,
                             unit_price DECIMAL(8,2),
                             FOREIGN KEY (order_id) REFERENCES orders(order_id),
                             FOREIGN KEY (product_id) REFERENCES products(product_id)
);

#Vytvoření Entity platby
CREATE TABLE payments
(
    payment_id     INT PRIMARY KEY,
    order_id       INT,
    payment_method VARCHAR(50),
    payment_status VARCHAR(20),
    paid_at        DATE,
    amount         DECIMAL(8, 2),
    FOREIGN KEY (order_id) REFERENCES orders (order_id)
);


#Vytvoření Entity vrácení zboží
CREATE TABLE returns (
                         return_id INT PRIMARY KEY,
                         order_id INT,
                         product_id INT,
                         return_date DATE,
                         reason VARCHAR(500),
                         refunded_amount DECIMAL(8,2),
                         FOREIGN KEY (order_id) REFERENCES orders(order_id),
                         FOREIGN KEY (product_id) REFERENCES products(product_id)
);