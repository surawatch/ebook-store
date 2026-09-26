-- ============================================================================
-- โครงงานพัฒนาระบบฐานข้อมูลร้านขายหนังสือและอีบุ๊กออนไลน์ (E-Book Store)
-- ไฟล์: sql/schema.sql (DDL Scripts ของระบบฐานข้อมูลจริงในโปรเจกต์ ebook-store)
-- ระบบฐานข้อมูล: PostgreSQL (บนระบบ Neon Cloud)
-- สอดคล้องตามเกณฑ์ 3NF ครบถ้วนทั้ง 9 ตาราง
-- ============================================================================

-- 1. ตาราง roles (บทบาทผู้ใช้งานในระบบ)
CREATE TABLE IF NOT EXISTS roles (
    role_id SERIAL PRIMARY KEY,
    role_name VARCHAR(50) NOT NULL UNIQUE
);

-- 2. ตาราง users (ข้อมูลสมาชิกและผู้ดูแลระบบ)
CREATE TABLE IF NOT EXISTS users (
    user_id SERIAL PRIMARY KEY,
    role_id INTEGER NOT NULL DEFAULT 1 REFERENCES roles(role_id),
    username VARCHAR(50) NOT NULL UNIQUE,
    email VARCHAR(100) NOT NULL UNIQUE,
    password_hash VARCHAR(255) NOT NULL,
    full_name VARCHAR(100) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 3. ตาราง authors (ข้อมูลผู้แต่ง / นักเขียน)
CREATE TABLE IF NOT EXISTS authors (
    author_id SERIAL PRIMARY KEY,
    author_name VARCHAR(100) NOT NULL,
    bio TEXT
);

-- 4. ตาราง categories (หมวดหมู่หนังสือ)
CREATE TABLE IF NOT EXISTS categories (
    category_id SERIAL PRIMARY KEY,
    category_name VARCHAR(100) NOT NULL,
    description TEXT
);

-- 5. ตาราง ebooks (ข้อมูลหนังสือดิจิทัล E-Book)
CREATE TABLE IF NOT EXISTS ebooks (
    ebook_id SERIAL PRIMARY KEY,
    title VARCHAR(200) NOT NULL,
    author_id INTEGER NOT NULL REFERENCES authors(author_id),
    category_id INTEGER NOT NULL REFERENCES categories(category_id),
    price NUMERIC(10, 2) NOT NULL CHECK (price >= 0),
    cover_image_url TEXT,
    description TEXT,
    file_download_url TEXT NOT NULL,
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 6. ตาราง carts (ตะกร้าสินค้าประจำตัวผู้ใช้)
CREATE TABLE IF NOT EXISTS carts (
    cart_id SERIAL PRIMARY KEY,
    user_id INTEGER NOT NULL REFERENCES users(user_id),
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 7. ตาราง cart_items (รายการสินค้าในตะกร้า)
CREATE TABLE IF NOT EXISTS cart_items (
    cart_item_id SERIAL PRIMARY KEY,
    cart_id INTEGER NOT NULL REFERENCES carts(cart_id),
    ebook_id INTEGER NOT NULL REFERENCES ebooks(ebook_id),
    quantity INTEGER NOT NULL DEFAULT 1 CHECK (quantity > 0)
);

-- 8. ตาราง orders (ข้อมูลคำสั่งซื้อหลักและหลักฐานสลิปจำลอง)
CREATE TABLE IF NOT EXISTS orders (
    order_id SERIAL PRIMARY KEY,
    user_id INTEGER NOT NULL REFERENCES users(user_id),
    total_amount NUMERIC(10, 2) NOT NULL CHECK (total_amount >= 0),
    order_status VARCHAR(30) NOT NULL DEFAULT 'pending',
    payment_slip_url TEXT,
    slip_note VARCHAR(255) DEFAULT 'ชำระผ่าน PromptPay QR จำลอง',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 9. ตาราง order_items (รายการหนังสือที่สั่งซื้อจริง พร้อมบันทึกราคาประวัติศาสตร์)
CREATE TABLE IF NOT EXISTS order_items (
    order_item_id SERIAL PRIMARY KEY,
    order_id INTEGER NOT NULL REFERENCES orders(order_id),
    ebook_id INTEGER NOT NULL REFERENCES ebooks(ebook_id),
    price_at_purchase NUMERIC(10, 2) NOT NULL CHECK (price_at_purchase >= 0)
);
