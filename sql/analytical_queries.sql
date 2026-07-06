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