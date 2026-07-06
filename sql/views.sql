USE Warehouse;

DROP VIEW IF EXISTS sales_fact;

CREATE VIEW sales_fact AS
SELECT
    o.order_id,
    oi.order_item_id,
    o.customer_id,
    oi.product_id,
    o.order_date,
    DATE_FORMAT(o.order_date, '%Y-%m') AS order_month,
    o.status AS order_status,
    p.product_name,
    p.category,
    p.brand,
    oi.quantity,
    oi.unit_price,
    p.cost,
    ROUND(oi.quantity * oi.unit_price, 2) AS revenue,
    ROUND(oi.quantity * (oi.unit_price - p.cost), 2) AS profit
FROM orders o
         JOIN order_items oi ON o.order_id = oi.order_id
         JOIN products p ON oi.product_id = p.product_id
WHERE o.status != 'cancelled';