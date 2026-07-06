-- 1. Total revenue and profit
SELECT
    ROUND(SUM(oi.quantity * oi.unit_price), 2) AS total_revenue,
    ROUND(SUM(oi.quantity * (oi.unit_price - p.cost)), 2) AS total_profit
FROM order_items oi
         JOIN products p ON oi.product_id = p.product_id
         JOIN orders o ON oi.order_id = o.order_id
WHERE o.status != 'cancelled';

-- 2. Monthly revenue
SELECT
    DATE_FORMAT(o.order_date, '%Y-%m') AS month,
    ROUND(SUM(oi.quantity * oi.unit_price), 2) AS revenue
FROM orders o
         JOIN order_items oi ON o.order_id = oi.order_id
WHERE o.status != 'cancelled'
GROUP BY DATE_FORMAT(o.order_date, '%Y-%m')
ORDER BY month;

-- 3. Revenue and profit by category
SELECT
    p.category,
    ROUND(SUM(oi.quantity * oi.unit_price), 2) AS revenue,
    ROUND(SUM(oi.quantity * (oi.unit_price - p.cost)), 2) AS profit
FROM order_items oi
         JOIN products p ON oi.product_id = p.product_id
         JOIN orders o ON oi.order_id = o.order_id
WHERE o.status != 'cancelled'
GROUP BY p.category
ORDER BY profit DESC;

-- 4. Top 10 customers by total spending
SELECT
    c.customer_id,
    c.first_name,
    c.last_name,
    c.city,
    ROUND(SUM(oi.quantity * oi.unit_price), 2) AS total_spent
FROM customers c
         JOIN orders o ON c.customer_id = o.customer_id
         JOIN order_items oi ON o.order_id = oi.order_id
WHERE o.status != 'cancelled'
GROUP BY c.customer_id, c.first_name, c.last_name, c.city
ORDER BY total_spent DESC
LIMIT 10;

-- 5. Return rate by product category
SELECT
    p.category,
    COUNT(DISTINCT r.return_id) AS total_returns,
    COUNT(DISTINCT oi.order_item_id) AS total_sold_items,
    ROUND(
            COUNT(DISTINCT r.return_id) * 100.0 / COUNT(DISTINCT oi.order_item_id),
            2
    ) AS return_rate_percent
FROM products p
         JOIN order_items oi ON p.product_id = oi.product_id
         LEFT JOIN returns r ON p.product_id = r.product_id
GROUP BY p.category
ORDER BY return_rate_percent DESC;

-- 6. Average order value by month
SELECT
    month,
    ROUND(AVG(order_value), 2) AS average_order_value
FROM (
         SELECT
             o.order_id,
             DATE_FORMAT(o.order_date, '%Y-%m') AS month,
             SUM(oi.quantity * oi.unit_price) AS order_value
         FROM orders o
                  JOIN order_items oi ON o.order_id = oi.order_id
         WHERE o.status != 'cancelled'
         GROUP BY o.order_id, DATE_FORMAT(o.order_date, '%Y-%m')
     ) monthly_orders
GROUP BY month
ORDER BY month;

-- 7. Order status distribution
SELECT
    status,
    COUNT(*) AS number_of_orders,
    ROUND(COUNT(*) * 100.0 / (SELECT COUNT(*) FROM orders), 2) AS percentage
FROM orders
GROUP BY status
ORDER BY number_of_orders DESC;

-- 8. Return rate by category
SELECT
    p.category,
    COUNT(DISTINCT r.return_id) AS total_returns,
    COUNT(DISTINCT oi.order_item_id) AS total_sold_items,
    ROUND(
            COUNT(DISTINCT r.return_id) * 100.0 / COUNT(DISTINCT oi.order_item_id),
            2
    ) AS return_rate_percent
FROM products p
         JOIN order_items oi ON p.product_id = oi.product_id
         LEFT JOIN returns r ON p.product_id = r.product_id
GROUP BY p.category
ORDER BY return_rate_percent DESC;

-- 9. Payment method usage
SELECT
    payment_method,
    COUNT(*) AS number_of_payments,
    ROUND(SUM(amount), 2) AS total_paid_amount
FROM payments
GROUP BY payment_method
ORDER BY total_paid_amount DESC;

-- 10. Customers by city
SELECT
    city,
    COUNT(*) AS number_of_customers
FROM customers
GROUP BY city
ORDER BY number_of_customers DESC
LIMIT 10;