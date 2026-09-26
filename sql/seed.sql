-- ============================================================================
-- โครงงานพัฒนาระบบฐานข้อมูลร้านขายหนังสือและอีบุ๊กออนไลน์ (E-Book Store)
-- ไฟล์: sql/seed.sql (ข้อมูลตัวอย่างทดสอบระบบจริงจากฐานข้อมูล Neon Cloud)
-- ครอบคลุม 35 คำสั่งซื้อ (orders) และ 54 รายการย่อย (order_items)
-- ============================================================================

-- 1. ตาราง roles
INSERT INTO roles (role_id, role_name) VALUES
  (1, 'customer'),
  (2, 'admin')
ON CONFLICT (role_id) DO NOTHING;

-- 2. ตาราง users
INSERT INTO users (user_id, role_id, username, email, password_hash, full_name, created_at) VALUES
  (1, 2, 'admin', 'admin@ebookstore.local', 'admin123', 'System Administrator', '2026-09-19T03:29:54.351Z'),
  (2, 1, 'somchai', 'somchai@email.local', 'pass123', 'Somchai Prasert', '2026-09-19T03:29:54.351Z'),
  (3, 1, 'suda', 'suda@email.local', 'pass123', 'Suda Jaidee', '2026-09-19T03:29:54.351Z'),
  (4, 1, 'anucha', 'anucha@email.local', 'pass123', 'Anucha Wongsuwan', '2026-09-19T03:29:54.351Z'),
  (5, 1, 'pimporn', 'pimporn@email.local', 'pass123', 'Pimporn Rattanaporn', '2026-09-19T03:29:54.351Z'),
  (6, 1, 'kittisak', 'kittisak@email.local', 'pass123', 'Kittisak Meesuk', '2026-09-19T03:29:54.351Z'),
  (7, 1, 'อดีดเบต้าเทสเตอร์อย่างงั้นหรอ', 'mikmin3366@gmail.com', 'rickc137', 'อดีดเบต้าเทสเตอร์อย่างงั้นหรอ', '2026-09-19T03:34:29.462Z'),
  (8, 1, 'Rakgunmai', 'Rakgunmai.44@gmail.com', 'Rakgunmai4444', 'รักมั้ย ตอบมา', '2026-09-20T01:30:38.693Z')
ON CONFLICT (user_id) DO NOTHING;

-- 3. ตาราง authors
INSERT INTO authors (author_id, author_name, bio) VALUES
  (1, 'Dr. Alan Turing', 'Computer scientist and mathematician'),
  (2, 'Benjamin Graham', 'Economist and professional investor'),
  (3, 'Robert C. Martin', 'Software craftsman and clean code pioneer'),
  (4, 'James Clear', 'Author and speaker on habits and decision making'),
  (5, 'Michael F.', '')
ON CONFLICT (author_id) DO NOTHING;

-- 4. ตาราง categories
INSERT INTO categories (category_id, category_name, description) VALUES
  (1, 'Computer & Programming', 'Software engineering, algorithms, and system design'),
  (2, 'Business & Finance', 'Investment, stock market, and business administration'),
  (3, 'Science & Engineering', 'Electronics, microprocessors, and physics'),
  (4, 'Self Improvement', 'Mindset, productivity, and lifestyle')
ON CONFLICT (category_id) DO NOTHING;

-- 5. ตาราง ebooks
INSERT INTO ebooks (ebook_id, title, author_id, category_id, price, cover_image_url, description, file_download_url, is_active, created_at) VALUES
  (1, 'Mastering Database Design', 1, 1, 350.00, 'https://picsum.photos/200/300?1', 'Complete guide to relational schema and normalization', 'https://mock-files.local/download/db-design.pdf', true, '2026-09-19T03:29:55.141Z'),
  (2, 'Clean Architecture in Practice', 3, 1, 420.00, 'https://picsum.photos/200/300?2', 'Software structure, design patterns, and testability', 'https://mock-files.local/download/clean-arch.pdf', true, '2026-09-19T03:29:55.141Z'),
  (3, 'Microprocessor Architecture & C', 1, 3, 290.00, 'https://picsum.photos/200/300?3', 'Assembly instruction cycles and low-level hardware design', 'https://mock-files.local/download/microprocessor.pdf', true, '2026-09-19T03:29:55.141Z'),
  (4, 'Intelligent Tech Investor', 2, 2, 380.00, 'https://picsum.photos/200/300?4', 'Guide to value investing in modern semiconductor and technology sectors', 'https://mock-files.local/download/tech-investor.pdf', true, '2026-09-19T03:29:55.141Z'),
  (5, 'Atomic Productivity', 4, 4, 250.00, 'https://picsum.photos/200/300?5', 'Small routine changes that lead to remarkable results', 'https://mock-files.local/download/atomic-prod.pdf', true, '2026-09-19T03:29:55.141Z'),
  (6, 'Data Structures with Big-O', 1, 1, 310.00, 'https://picsum.photos/200/300?6', 'Tree traversal, graph theory, and algorithmic complexity', 'https://mock-files.local/download/data-structures.pdf', true, '2026-09-19T03:29:55.141Z')
ON CONFLICT (ebook_id) DO NOTHING;

-- 6. ตาราง carts
INSERT INTO carts (cart_id, user_id, updated_at) VALUES
  (1, 2, '2026-09-19T03:29:55.413Z'),
  (2, 3, '2026-09-19T03:29:55.413Z'),
  (3, 4, '2026-09-19T03:29:55.413Z'),
  (4, 5, '2026-09-19T03:29:55.413Z'),
  (5, 6, '2026-09-19T03:29:55.413Z'),
  (6, 7, '2026-09-19T03:34:29.683Z'),
  (7, 8, '2026-09-20T01:30:38.717Z')
ON CONFLICT (cart_id) DO NOTHING;

-- 7. ตาราง orders (รวม 35 คำสั่งซื้อ)
INSERT INTO orders (order_id, user_id, total_amount, order_status, payment_slip_url, slip_note, created_at) VALUES
  (1, 2, 350.00, 'confirmed', 'https://mock-slip.local/s1.jpg', 'ชำระผ่าน PromptPay QR จำลอง', '2026-08-01T03:15:00.000Z'),
  (2, 3, 420.00, 'confirmed', 'https://mock-slip.local/s2.jpg', 'ชำระผ่าน PromptPay QR จำลอง', '2026-08-02T04:30:00.000Z'),
  (3, 4, 290.00, 'confirmed', 'https://mock-slip.local/s3.jpg', 'ชำระผ่าน PromptPay QR จำลอง', '2026-08-03T07:00:00.000Z'),
  (4, 5, 630.00, 'confirmed', 'https://mock-slip.local/s4.jpg', 'ชำระผ่าน PromptPay QR จำลอง', '2026-08-04T09:45:00.000Z'),
  (5, 6, 250.00, 'cancelled', '', 'ชำระผ่าน PromptPay QR จำลอง', '2026-08-05T02:20:00.000Z'),
  (6, 2, 770.00, 'confirmed', 'https://mock-slip.local/s6.jpg', 'ชำระผ่าน PromptPay QR จำลอง', '2026-08-06T11:10:00.000Z'),
  (7, 3, 380.00, 'confirmed', 'https://mock-slip.local/s7.jpg', 'ชำระผ่าน PromptPay QR จำลอง', '2026-08-07T05:05:00.000Z'),
  (8, 4, 310.00, 'confirmed', 'https://mock-slip.local/s8.jpg', 'ชำระผ่าน PromptPay QR จำลอง', '2026-08-08T08:30:00.000Z'),
  (9, 5, 290.00, 'confirmed', 'https://mock-slip.local/s9.jpg', 'ชำระผ่าน PromptPay QR จำลอง', '2026-08-09T13:00:00.000Z'),
  (10, 6, 420.00, 'pending', 'https://mock-slip.local/s10.jpg', 'ชำระผ่าน PromptPay QR จำลอง', '2026-08-10T06:40:00.000Z'),
  (11, 2, 250.00, 'confirmed', 'https://mock-slip.local/s11.jpg', 'ชำระผ่าน PromptPay QR จำลอง', '2026-08-12T03:50:00.000Z'),
  (12, 3, 730.00, 'confirmed', 'https://mock-slip.local/s12.jpg', 'ชำระผ่าน PromptPay QR จำลอง', '2026-08-14T10:15:00.000Z'),
  (13, 4, 350.00, 'cancelled', '', 'ชำระผ่าน PromptPay QR จำลอง', '2026-08-15T04:00:00.000Z'),
  (14, 5, 380.00, 'confirmed', 'https://mock-slip.local/s14.jpg', 'ชำระผ่าน PromptPay QR จำลอง', '2026-08-16T02:40:00.000Z'),
  (15, 6, 600.00, 'confirmed', 'https://mock-slip.local/s15.jpg', 'ชำระผ่าน PromptPay QR จำลอง', '2026-08-18T12:25:00.000Z'),
  (16, 2, 420.00, 'confirmed', 'https://mock-slip.local/s16.jpg', 'ชำระผ่าน PromptPay QR จำลอง', '2026-08-20T07:10:00.000Z'),
  (17, 3, 310.00, 'confirmed', 'https://mock-slip.local/s17.jpg', 'ชำระผ่าน PromptPay QR จำลอง', '2026-08-21T09:30:00.000Z'),
  (18, 4, 670.00, 'confirmed', 'https://mock-slip.local/s18.jpg', 'ชำระผ่าน PromptPay QR จำลอง', '2026-08-23T03:20:00.000Z'),
  (19, 5, 250.00, 'pending', 'https://mock-slip.local/s19.jpg', 'ชำระผ่าน PromptPay QR จำลอง', '2026-08-24T06:00:00.000Z'),
  (20, 6, 380.00, 'confirmed', 'https://mock-slip.local/s20.jpg', 'ชำระผ่าน PromptPay QR จำลอง', '2026-08-25T11:40:00.000Z'),
  (21, 2, 290.00, 'confirmed', 'https://mock-slip.local/s21.jpg', 'ชำระผ่าน PromptPay QR จำลอง', '2026-08-26T04:15:00.000Z'),
  (22, 3, 350.00, 'confirmed', 'https://mock-slip.local/s22.jpg', 'ชำระผ่าน PromptPay QR จำลอง', '2026-08-27T08:50:00.000Z'),
  (23, 4, 420.00, 'confirmed', 'https://mock-slip.local/s23.jpg', 'ชำระผ่าน PromptPay QR จำลอง', '2026-08-28T14:10:00.000Z'),
  (24, 5, 560.00, 'confirmed', 'https://mock-slip.local/s24.jpg', 'ชำระผ่าน PromptPay QR จำลอง', '2026-08-29T01:30:00.000Z'),
  (25, 6, 350.00, 'cancelled', '', 'ชำระผ่าน PromptPay QR จำลอง', '2026-08-30T05:45:00.000Z'),
  (26, 2, 630.00, 'confirmed', 'https://mock-slip.local/s26.jpg', 'ชำระผ่าน PromptPay QR จำลอง', '2026-09-01T07:20:00.000Z'),
  (27, 3, 250.00, 'confirmed', 'https://mock-slip.local/s27.jpg', 'ชำระผ่าน PromptPay QR จำลอง', '2026-09-02T10:00:00.000Z'),
  (28, 4, 380.00, 'confirmed', 'https://mock-slip.local/s28.jpg', 'ชำระผ่าน PromptPay QR จำลอง', '2026-09-03T03:05:00.000Z'),
  (29, 5, 420.00, 'pending', 'https://mock-slip.local/s29.jpg', 'ชำระผ่าน PromptPay QR จำลอง', '2026-09-04T09:15:00.000Z'),
  (30, 6, 660.00, 'confirmed', 'https://mock-slip.local/s30.jpg', 'ชำระผ่าน PromptPay QR จำลอง', '2026-09-05T12:30:00.000Z'),
  (31, 7, 1000.00, 'confirmed', 'https://mock-slip.local/qr-checkout.png', 'ชำระผ่าน PromptPay QR จำลอง', '2026-09-19T03:36:50.536Z'),
  (32, 7, 310.00, 'confirmed', 'https://mock-slip.local/qr-checkout.png', 'ชำระผ่าน PromptPay QR จำลอง', '2026-09-19T03:39:48.559Z'),
  (33, 7, 2970.00, 'confirmed', 'https://mock-slip.local/qr-checkout.png', 'ชำระผ่าน PromptPay QR จำลอง', '2026-09-19T03:41:12.328Z'),
  (34, 2, 1080.00, 'confirmed', 'https://mock-slip.local/qr-checkout.png', 'ชำระผ่าน PromptPay QR จำลอง', '2026-09-19T06:10:19.310Z'),
  (35, 8, 420.00, 'confirmed', 'https://mock-slip.local/qr-checkout.png', 'ชำระผ่าน PromptPay QR จำลอง', '2026-09-20T01:31:07.167Z')
ON CONFLICT (order_id) DO NOTHING;

-- 8. ตาราง order_items (รวม 54 รายการสินค้าที่สั่งซื้อจริง)
INSERT INTO order_items (order_item_id, order_id, ebook_id, price_at_purchase) VALUES
  (1, 1, 1, 350.00),
  (2, 2, 2, 420.00),
  (3, 3, 3, 290.00),
  (4, 4, 2, 420.00),
  (5, 4, 4, 210.00),
  (6, 5, 5, 250.00),
  (7, 6, 1, 350.00),
  (8, 6, 2, 420.00),
  (9, 7, 4, 380.00),
  (10, 8, 6, 310.00),
  (11, 9, 3, 290.00),
  (12, 10, 2, 420.00),
  (13, 11, 5, 250.00),
  (14, 12, 1, 350.00),
  (15, 12, 4, 380.00),
  (16, 13, 1, 350.00),
  (17, 14, 4, 380.00),
  (18, 15, 1, 350.00),
  (19, 15, 5, 250.00),
  (20, 16, 2, 420.00),
  (21, 17, 6, 310.00),
  (22, 18, 3, 290.00),
  (23, 18, 4, 380.00),
  (24, 19, 5, 250.00),
  (25, 20, 4, 380.00),
  (26, 21, 3, 290.00),
  (27, 22, 1, 350.00),
  (28, 23, 2, 420.00),
  (29, 24, 6, 310.00),
  (30, 24, 5, 250.00),
  (31, 25, 1, 350.00),
  (32, 26, 4, 380.00),
  (33, 26, 5, 250.00),
  (34, 27, 5, 250.00),
  (35, 28, 4, 380.00),
  (36, 29, 2, 420.00),
  (37, 30, 1, 350.00),
  (38, 30, 6, 310.00),
  (39, 31, 6, 310.00),
  (40, 31, 6, 310.00),
  (41, 31, 4, 380.00),
  (42, 32, 6, 310.00),
  (43, 33, 2, 420.00),
  (44, 33, 2, 420.00),
  (45, 33, 2, 420.00),
  (46, 33, 2, 420.00),
  (47, 33, 1, 350.00),
  (48, 33, 4, 380.00),
  (49, 33, 6, 310.00),
  (50, 33, 5, 250.00),
  (51, 34, 2, 420.00),
  (52, 34, 1, 350.00),
  (53, 34, 6, 310.00),
  (54, 35, 2, 420.00)
ON CONFLICT (order_item_id) DO NOTHING;

