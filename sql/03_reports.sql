-- ============================================================================
-- โครงงานพัฒนาระบบฐานข้อมูลร้านขายหนังสือและอีบุ๊กออนไลน์ (E-Book Store)
-- ไฟล์: sql/reports.sql (คำสั่ง SQL Query จริงสำหรับรายงานวิเคราะห์ธุรกิจ 4 ด้าน)
-- คัดลอกและอ้างอิงตรงจาก routes/reports.js ของระบบ ebook-store
-- สอดคล้องตามข้อกำหนดใบงานข้อ 5
-- ============================================================================

-- ----------------------------------------------------------------------------
-- รายงานที่ 1: ยอดขายตามช่วงเวลา (Sales Over Time by Date)
-- คำถามทางธุรกิจ: ยอดขาย จำนวนคำสั่งซื้อ และยอดซื้อเฉลี่ยต่อคำสั่งซื้อ (AOV) เป็นอย่างไรในแต่ละวัน?
-- ----------------------------------------------------------------------------
SELECT 
    DATE(created_at) AS date, 
    COUNT(order_id) AS total_orders, 
    SUM(total_amount) AS total_sales, 
    ROUND(AVG(total_amount), 2) AS avg_sale
FROM orders 
WHERE order_status = 'confirmed'
GROUP BY DATE(created_at) 
ORDER BY date DESC 
LIMIT 7;


-- ----------------------------------------------------------------------------
-- รายงานที่ 2: E-Book ขายดีที่สุด 5 อันดับแรก (Top-Selling Books)
-- คำถามทางธุรกิจ: E-Book ใดขายได้มากที่สุด 5 อันดับแรกตามจำนวนเล่มและยอดขายรวม?
-- ----------------------------------------------------------------------------
SELECT 
    e.title, 
    a.author_name, 
    COUNT(oi.order_item_id) AS units_sold, 
    SUM(oi.price_at_purchase) AS sales
FROM order_items oi
JOIN orders o ON oi.order_id = o.order_id
JOIN ebooks e ON oi.ebook_id = e.ebook_id
JOIN authors a ON e.author_id = a.author_id
WHERE o.order_status = 'confirmed'
GROUP BY e.title, a.author_name 
ORDER BY units_sold DESC 
LIMIT 5;


-- ----------------------------------------------------------------------------
-- รายงานที่ 3: สรุปยอดขายตามหมวดหมู่หนังสือ (Sales by Category)
-- คำถามทางธุรกิจ: หมวดหมู่หนังสือใดสร้างยอดขายรวมและจำนวนเล่มที่ขายได้สูงสุด?
-- ----------------------------------------------------------------------------
SELECT 
    c.category_name, 
    COUNT(oi.order_item_id) AS items_count, 
    SUM(oi.price_at_purchase) AS sales
FROM categories c
JOIN ebooks e ON c.category_id = e.category_id
JOIN order_items oi ON e.ebook_id = oi.ebook_id
JOIN orders o ON oi.order_id = o.order_id
WHERE o.order_status = 'confirmed'
GROUP BY c.category_name 
ORDER BY sales DESC;


-- ----------------------------------------------------------------------------
-- รายงานที่ 4: พฤติกรรมลูกค้าและยอดซื้อสะสม (Customer Lifetime Spending)
-- คำถามทางธุรกิจ: สมาชิกลูกค้ารายใดมียอดซื้อสะสมสูงสุดในระบบ และมีจำนวนออเดอร์เท่าใด?
-- ----------------------------------------------------------------------------
SELECT 
    u.username, 
    u.full_name, 
    COUNT(o.order_id) AS orders_count, 
    SUM(o.total_amount) AS spent
FROM users u 
JOIN orders o ON u.user_id = o.user_id
WHERE o.order_status = 'confirmed'
GROUP BY u.username, u.full_name 
ORDER BY spent DESC 
LIMIT 5;
