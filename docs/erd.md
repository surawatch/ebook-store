# ผังความสัมพันธ์ข้อมูล (Entity-Relationship Diagram: ERD)

```mermaid
erDiagram
    roles ||--o{ users : "assigns"
    users ||--o{ carts : "owns"
    users ||--o{ orders : "places"
    categories ||--o{ ebooks : "categorizes"
    authors ||--o{ ebooks : "writes"
    carts ||--o{ cart_items : "contains"
    ebooks ||--o{ cart_items : "added_to"
    orders ||--o{ order_items : "includes"
    ebooks ||--o{ order_items : "ordered_as"

    roles {
        int role_id PK
        string role_name UK
    }

    users {
        int user_id PK
        int role_id FK
        string username UK
        string email UK
        string password_hash
        string full_name
        timestamp created_at
    }

    authors {
        int author_id PK
        string author_name
        text bio
    }

    categories {
        int category_id PK
        string category_name UK
        text description
    }

    ebooks {
        int ebook_id PK
        string title
        int author_id FK
        int category_id FK
        numeric price
        string cover_image_url
        text description
        string file_download_url
        boolean is_active
        timestamp created_at
    }

    carts {
        int cart_id PK
        int user_id FK
        timestamp updated_at
    }

    cart_items {
        int cart_item_id PK
        int cart_id FK
        int ebook_id FK
        int quantity
    }

    orders {
        int order_id PK
        int user_id FK
        numeric total_amount
        string order_status
        string payment_slip_url
        string slip_note
        timestamp created_at
    }

    order_items {
        int order_item_id PK
        int order_id FK
        int ebook_id FK
        numeric price_at_purchase
    }
```

## คำอธิบายความสัมพันธ์และโครงสร้าง 3NF:
1. **`roles` และ `users` (1:N)**: ผู้ใช้งานแต่ละคนมีบทบาทเดียว (`customer` หรือ `admin`) เพื่อใช้ในการควบคุมสิทธิ์แบบ RBAC
2. **`categories` และ `ebooks` (1:N)**: หนังสือแต่ละเล่มสังกัดหนึ่งหมวดหมู่หลัก
3. **`authors` และ `ebooks` (1:N)**: หนังสือแต่ละเล่มมีผู้แต่งหลัก
4. **`carts` และ `cart_items` (1:N)**: ผู้ใช้ 1 คนมี 1 ตะกร้าสินค้า ซึ่งบรรจุรายการหนังสือที่กำลังเลือกซื้อ
5. **`orders` และ `order_items` (1:N)**: เมื่อสั่งซื้อ ข้อมูลจะถูกถ่ายโอนจากตะกร้ามายังคำสั่งซื้อ โดย `order_items` ทำหน้าที่เป็น Junction Table
6. **Snapshot Price**: ฟิลด์ `price_at_purchase` ใน `order_items` จัดเก็บราคา ณ วินาทีที่ซื้อ ป้องกันปัญหาการแก้ไขราคาในตาราง `ebooks` แล้วกระทบยอดรวมคำสั่งซื้อในอดีต
