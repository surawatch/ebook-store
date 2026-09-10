const express = require('express');
const session = require('express-session');
const { Pool } = require('pg');

const app = express();

// ปรับรหัสผ่าน PostgreSQL ให้ตรงกับเครื่องของคุณ
const pool = new Pool({
  connectionString: process.env.DATABASE_URL || 'postgresql://postgres:admin123@localhost:5432/ebookdb',
  ssl: {
    rejectUnauthorized: false
  }
});

app.use(express.urlencoded({ extended: true }));
app.use(express.json());
app.use(session({
  secret: 'ebook-store-full-key-2026',
  resave: false,
  saveUninitialized: false,
  cookie: { maxAge: 24 * 60 * 60 * 1000 }
}));

// Navbar กลางแสดงผลตามสถานะผู้ใช้
async function getCartCount(userId) {
  if (!userId) return 0;
  const res = await pool.query(
    `SELECT COALESCE(SUM(ci.quantity), 0) AS total 
     FROM carts c 
     JOIN cart_items ci ON c.cart_id = ci.cart_id 
     WHERE c.user_id = $1`, [userId]
  );
  return parseInt(res.rows[0].total) || 0;
}

function renderNavbar(user, cartCount = 0) {
  return `
    <nav class="bg-white border-b border-gray-200 sticky top-0 z-50 shadow-sm">
      <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div class="flex justify-between h-16">
          <div class="flex items-center space-x-3">
            <span class="text-2xl">📚</span>
            <a href="/" class="text-xl font-black bg-gradient-to-r from-blue-600 to-indigo-600 bg-clip-text text-transparent">E-Book Store</a>
          </div>
          <div class="flex items-center space-x-4">
            <a href="/" class="text-gray-700 hover:text-blue-600 font-medium text-sm">หน้าร้าน</a>
            <a href="/reports" class="text-gray-700 hover:text-blue-600 font-medium text-sm">รายงานสถิติ</a>
            
            ${user ? `
              <a href="/cart" class="relative text-gray-700 hover:text-blue-600 font-medium text-sm flex items-center">
                🛒 ตะกร้า
                <span class="ml-1 bg-blue-600 text-white text-xs px-2 py-0.5 rounded-full font-bold">${cartCount}</span>
              </a>
              <a href="/my-orders" class="text-gray-700 hover:text-blue-600 font-medium text-sm">คำสั่งซื้อ</a>
              <a href="/profile" class="text-gray-700 hover:text-blue-600 font-medium text-sm">ข้อมูลส่วนตัว</a>
              
              ${user.role_name === 'admin' ? `
                <div class="relative group">
                  <button class="bg-purple-100 text-purple-700 px-3 py-1.5 rounded-lg font-bold text-sm hover:bg-purple-200">
                    ⚙️ จัดการร้าน (Admin) ▾
                  </button>
                  <div class="absolute right-0 hidden group-hover:block bg-white border border-gray-100 shadow-lg rounded-lg py-2 w-48 z-50">
                    <a href="/admin/orders" class="block px-4 py-2 text-sm text-gray-700 hover:bg-purple-50">จัดการคำสั่งซื้อ</a>
                    <a href="/admin/ebooks" class="block px-4 py-2 text-sm text-gray-700 hover:bg-purple-50">จัดการ E-Book</a>
                    <a href="/admin/categories" class="block px-4 py-2 text-sm text-gray-700 hover:bg-purple-50">จัดการหมวดหมู่</a>
                    <a href="/admin/users" class="block px-4 py-2 text-sm text-gray-700 hover:bg-purple-50">จัดการผู้ใช้งาน</a>
                  </div>
                </div>
              ` : ''}

              <div class="border-l pl-4 flex items-center space-x-3">
                <span class="text-sm font-semibold text-gray-800">${user.full_name} <span class="text-xs text-gray-400">(${user.role_name})</span></span>
                <a href="/logout" class="bg-rose-50 text-rose-600 px-3 py-1 rounded-lg text-xs font-semibold hover:bg-rose-100">ออก</a>
              </div>
            ` : `
              <div class="border-l pl-4 flex items-center space-x-2">
                <a href="/login" class="text-gray-700 hover:text-blue-600 font-medium text-sm px-3 py-1.5">เข้าสู่ระบบ</a>
                <a href="/register" class="bg-blue-600 hover:bg-blue-700 text-white font-medium text-sm px-4 py-1.5 rounded-lg shadow-sm">สมัครสมาชิก</a>
              </div>
            `}
          </div>
        </div>
      </div>
    </nav>
  `;
}

// ----------------------------------------------------
// 1. Authentication & Profile Management
// ----------------------------------------------------
app.get('/login', (req, res) => {
  res.send(`
    <!DOCTYPE html>
    <html lang="th">
    <head><meta charset="UTF-8"><title>เข้าสู่ระบบ</title><script src="https://cdn.tailwindcss.com"></script></head>
    <body class="bg-slate-50 min-h-screen flex flex-col justify-center py-12 sm:px-6 lg:px-8">
      <div class="sm:mx-auto sm:w-full sm:max-w-md text-center">
        <h2 class="text-3xl font-extrabold text-gray-900">เข้าสู่ระบบ E-Book Store</h2>
        <p class="mt-2 text-sm text-gray-600">หรือ <a href="/register" class="text-blue-600 hover:underline">สมัครสมาชิกใหม่</a></p>
      </div>
      <div class="mt-8 sm:mx-auto sm:w-full sm:max-w-md">
        <div class="bg-white py-8 px-6 shadow rounded-xl border border-gray-100 sm:px-10">
          <form method="POST" action="/login" class="space-y-4">
            <div>
              <label class="block text-sm font-medium text-gray-700">Username</label>
              <input type="text" name="username" required class="mt-1 block w-full px-3 py-2 border rounded-lg shadow-sm focus:ring-blue-500 focus:border-blue-500 sm:text-sm">
            </div>
            <div>
              <label class="block text-sm font-medium text-gray-700">Password</label>
              <input type="password" name="password" required class="mt-1 block w-full px-3 py-2 border rounded-lg shadow-sm focus:ring-blue-500 focus:border-blue-500 sm:text-sm">
            </div>
            <button type="submit" class="w-full py-2.5 px-4 rounded-lg shadow text-sm font-medium text-white bg-blue-600 hover:bg-blue-700">เข้าสู่ระบบ</button>
          </form>
          <div class="mt-6 border-t pt-4 text-xs text-gray-500 space-y-1">
            <p class="font-bold text-gray-700">บัญชีทดสอบเริ่มต้น:</p>
            <p>• ผู้ดูแลร้าน (Admin): <code>admin</code> / <code>admin123</code></p>
            <p>• สมาชิก (Customer): <code>somchai</code> / <code>pass123</code></p>
          </div>
        </div>
      </div>
    </body>
    </html>
  `);
});

app.post('/login', async (req, res) => {
  const { username, password } = req.body;
  try {
    const { rows } = await pool.query(
      `SELECT u.*, r.role_name FROM users u JOIN roles r ON u.role_id = r.role_id WHERE u.username = $1`,
      [username]
    );
    if (!rows.length || rows[0].password_hash !== password) {
      return res.send(`<script>alert('Username หรือ Password ไม่ถูกต้อง'); window.location='/login';</script>`);
    }
    req.session.user = rows[0];
    res.redirect('/');
  } catch (err) {
    res.status(500).send(err.message);
  }
});

app.get('/register', (req, res) => {
  res.send(`
    <!DOCTYPE html>
    <html lang="th">
    <head><meta charset="UTF-8"><title>สมัครสมาชิก</title><script src="https://cdn.tailwindcss.com"></script></head>
    <body class="bg-slate-50 min-h-screen flex flex-col justify-center py-12 sm:px-6 lg:px-8">
      <div class="sm:mx-auto sm:w-full sm:max-w-md text-center">
        <h2 class="text-3xl font-extrabold text-gray-900">สมัครสมาชิกใหม่</h2>
      </div>
      <div class="mt-8 sm:mx-auto sm:w-full sm:max-w-md">
        <div class="bg-white py-8 px-6 shadow rounded-xl border border-gray-100 sm:px-10">
          <form method="POST" action="/register" class="space-y-4">
            <div>
              <label class="block text-sm font-medium text-gray-700">ชื่อ-นามสกุล</label>
              <input type="text" name="full_name" required class="mt-1 block w-full px-3 py-2 border rounded-lg shadow-sm">
            </div>
            <div>
              <label class="block text-sm font-medium text-gray-700">Username</label>
              <input type="text" name="username" required class="mt-1 block w-full px-3 py-2 border rounded-lg shadow-sm">
            </div>
            <div>
              <label class="block text-sm font-medium text-gray-700">Email</label>
              <input type="email" name="email" required class="mt-1 block w-full px-3 py-2 border rounded-lg shadow-sm">
            </div>
            <div>
              <label class="block text-sm font-medium text-gray-700">Password</label>
              <input type="password" name="password" required class="mt-1 block w-full px-3 py-2 border rounded-lg shadow-sm">
            </div>
            <button type="submit" class="w-full py-2.5 px-4 rounded-lg text-sm font-medium text-white bg-blue-600 hover:bg-blue-700">ยืนยันการสมัครสมาชิก</button>
          </form>
          <div class="mt-4 text-center">
            <a href="/login" class="text-sm text-blue-600 hover:underline">มีบัญชีอยู่แล้ว? เข้าสู่ระบบ</a>
          </div>
        </div>
      </div>
    </body>
    </html>
  `);
});

app.post('/register', async (req, res) => {
  const { full_name, username, email, password } = req.body;
  try {
    const newUser = await pool.query(
      `INSERT INTO users (role_id, username, email, password_hash, full_name)
       VALUES (1, $1, $2, $3, $4) RETURNING user_id`,
      [username, email, password, full_name]
    );
    await pool.query(`INSERT INTO carts (user_id) VALUES ($1)`, [newUser.rows[0].user_id]);
    res.send(`<script>alert('สมัครสมาชิกสำเร็จ กรุณาเข้าสู่ระบบ'); window.location='/login';</script>`);
  } catch (err) {
    res.send(`<script>alert('Username หรือ Email ซ้ำในระบบ'); window.location='/register';</script>`);
  }
});

app.get('/profile', async (req, res) => {
  if (!req.session.user) return res.redirect('/login');
  const userRes = await pool.query('SELECT * FROM users WHERE user_id = $1', [req.session.user.user_id]);
  const user = userRes.rows[0];
  const cartCount = await getCartCount(req.session.user.user_id);

  res.send(`
    <!DOCTYPE html>
    <html lang="th">
    <head><meta charset="UTF-8"><title>แก้ไขข้อมูลพื้นฐาน</title><script src="https://cdn.tailwindcss.com"></script></head>
    <body class="bg-slate-50 min-h-screen">
      ${renderNavbar(req.session.user, cartCount)}
      <div class="max-w-xl mx-auto px-4 py-12">
        <div class="bg-white p-8 rounded-xl border shadow-sm">
          <h1 class="text-xl font-bold text-gray-900 mb-6">แก้ไขข้อมูลพื้นฐานสมาชิก</h1>
          <form method="POST" action="/profile/update" class="space-y-4">
            <div>
              <label class="block text-sm font-medium text-gray-700">Username (ไม่สามารถแก้ไขได้)</label>
              <input type="text" disabled value="${user.username}" class="mt-1 block w-full px-3 py-2 border rounded-lg bg-gray-50 text-gray-500">
            </div>
            <div>
              <label class="block text-sm font-medium text-gray-700">ชื่อ-นามสกุล</label>
              <input type="text" name="full_name" value="${user.full_name}" required class="mt-1 block w-full px-3 py-2 border rounded-lg">
            </div>
            <div>
              <label class="block text-sm font-medium text-gray-700">Email</label>
              <input type="email" name="email" value="${user.email}" required class="mt-1 block w-full px-3 py-2 border rounded-lg">
            </div>
            <button type="submit" class="w-full bg-blue-600 hover:bg-blue-700 text-white font-medium py-2 rounded-lg text-sm">บันทึกการเปลี่ยนแปลง</button>
          </form>
        </div>
      </div>
    </body>
    </html>
  `);
});

app.post('/profile/update', async (req, res) => {
  if (!req.session.user) return res.redirect('/login');
  const { full_name, email } = req.body;
  await pool.query('UPDATE users SET full_name = $1, email = $2 WHERE user_id = $3', [full_name, email, req.session.user.user_id]);
  req.session.user.full_name = full_name;
  req.session.user.email = email;
  res.send(`<script>alert('บันทึกข้อมูลเรียบร้อย'); window.location='/profile';</script>`);
});

app.get('/logout', (req, res) => {
  req.session.destroy(() => res.redirect('/login'));
});

// ----------------------------------------------------
// 2. Storefront (หน้าร้าน)
// ----------------------------------------------------
app.get('/', async (req, res) => {
  try {
    const { search, category_id } = req.query;
    let query = `
      SELECT e.*, c.category_name, a.author_name 
      FROM ebooks e
      JOIN categories c ON e.category_id = c.category_id
      JOIN authors a ON e.author_id = a.author_id
      WHERE e.is_active = TRUE
    `;
    const params = [];

    if (search) {
      params.push(`%${search}%`);
      query += ` AND (e.title ILIKE $${params.length} OR a.author_name ILIKE $${params.length})`;
    }
    if (category_id) {
      params.push(category_id);
      query += ` AND e.category_id = $${params.length}`;
    }

    const ebooks = await pool.query(query, params);
    const categories = await pool.query('SELECT * FROM categories');
    const cartCount = await getCartCount(req.session.user?.user_id);

    res.send(`
      <!DOCTYPE html>
      <html lang="th">
      <head><meta charset="UTF-8"><title>ร้านขาย E-Book ออนไลน์</title><script src="https://cdn.tailwindcss.com"></script></head>
      <body class="bg-slate-50 min-h-screen">
        ${renderNavbar(req.session.user, cartCount)}

        <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
          <div class="bg-gradient-to-r from-blue-700 to-indigo-800 rounded-2xl p-8 mb-8 text-white shadow-lg">
            <h1 class="text-3xl font-extrabold mb-2">ระบบฐานข้อมูลร้านค้า E-Book</h1>
            <p class="text-blue-100 mb-6">ค้นหา ใส่ตะกร้า ชำระเงินจำลอง และรับไฟล์ลิขสิทธิ์เฉพาะคุณ</p>
            
            <form method="GET" action="/" class="flex flex-col md:flex-row gap-3 bg-white p-2 rounded-xl shadow-md text-gray-800">
              <input type="text" name="search" placeholder="ค้นหาชื่อหนังสือ หรือชื่อผู้แต่ง..." value="${search || ''}" class="flex-1 px-4 py-2 rounded-lg border-0 focus:ring-0 text-sm">
              <select name="category_id" class="px-4 py-2 border-l border-gray-200 text-sm bg-transparent">
                <option value="">ทุกหมวดหมู่หนังสือ</option>
                ${categories.rows.map(c => `<option value="${c.category_id}" ${category_id == c.category_id ? 'selected' : ''}>${c.category_name}</option>`).join('')}
              </select>
              <button type="submit" class="bg-blue-600 hover:bg-blue-700 text-white px-6 py-2 rounded-lg text-sm font-semibold transition">ค้นหา</button>
            </form>
          </div>

          <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-6">
            ${ebooks.rows.map(book => `
              <div class="bg-white border rounded-xl overflow-hidden shadow-sm hover:shadow-md transition flex flex-col justify-between">
                <div class="p-6">
                  <div class="flex justify-between items-start mb-3">
                    <span class="bg-blue-50 text-blue-700 text-xs px-2.5 py-1 rounded-full font-semibold">${book.category_name}</span>
                    <span class="text-xs text-gray-400">PDF E-Book</span>
                  </div>
                  <h3 class="font-bold text-lg text-gray-900 mb-1 leading-snug">${book.title}</h3>
                  <p class="text-xs text-gray-500 mb-3">โดย <span class="font-medium text-gray-700">${book.author_name}</span></p>
                  <p class="text-sm text-gray-600 line-clamp-3 leading-relaxed">${book.description}</p>
                </div>
                <div class="px-6 py-4 bg-gray-50 border-t flex justify-between items-center">
                  <div>
                    <span class="text-xs text-gray-400 block">ราคา</span>
                    <span class="text-xl font-extrabold text-blue-600">${Number(book.price).toLocaleString()} ฿</span>
                  </div>
                  <form method="POST" action="/cart/add">
                    <input type="hidden" name="ebook_id" value="${book.ebook_id}">
                    <button type="submit" class="bg-blue-600 hover:bg-blue-700 text-white font-medium text-sm px-4 py-2 rounded-lg transition shadow-sm flex items-center space-x-1">
                      <span>🛒 เพิ่มลงตะกร้า</span>
                    </button>
                  </form>
                </div>
              </div>
            `).join('')}
          </div>
        </div>
      </body>
      </html>
    `);
  } catch (err) {
    console.error('SERVER DB ERROR:', err);
    res.status(500).send(`เกิดข้อผิดพลาด: ${err.message}`);
  }
});

// ----------------------------------------------------
// 3. Cart System (เพิ่ม / แก้ไข / ลบ / สรุปยอดรวม)
// ----------------------------------------------------
app.get('/cart', async (req, res) => {
  if (!req.session.user) return res.redirect('/login');

  const cartRes = await pool.query(
    `SELECT c.cart_id, ci.cart_item_id, ci.quantity, e.ebook_id, e.title, e.price, (ci.quantity * e.price) AS subtotal
     FROM carts c
     JOIN cart_items ci ON c.cart_id = ci.cart_id
     JOIN ebooks e ON ci.ebook_id = e.ebook_id
     WHERE c.user_id = $1`, [req.session.user.user_id]
  );

  const cartItems = cartRes.rows;
  const totalAmount = cartItems.reduce((sum, item) => sum + Number(item.subtotal), 0);
  const cartCount = await getCartCount(req.session.user.user_id);

  res.send(`
    <!DOCTYPE html>
    <html lang="th">
    <head><meta charset="UTF-8"><title>ตะกร้าสินค้า</title><script src="https://cdn.tailwindcss.com"></script></head>
    <body class="bg-slate-50 min-h-screen">
      ${renderNavbar(req.session.user, cartCount)}

      <div class="max-w-4xl mx-auto px-4 py-8">
        <h1 class="text-2xl font-bold text-gray-900 mb-6">ตะกร้าสินค้าของคุณ</h1>
        
        ${cartItems.length === 0 ? `
          <div class="bg-white p-12 text-center rounded-xl border">
            <span class="text-5xl block mb-3">🛒</span>
            <p class="text-gray-500 mb-4">ยังไม่มีสินค้าในตะกร้า</p>
            <a href="/" class="bg-blue-600 text-white px-4 py-2 rounded-lg text-sm font-medium">เลือกซื้อหนังสือเลย</a>
          </div>
        ` : `
          <div class="bg-white rounded-xl border shadow-sm overflow-hidden mb-6">
            <table class="w-full text-left divide-y divide-gray-200">
              <thead class="bg-gray-50 text-xs font-semibold text-gray-500 uppercase">
                <tr>
                  <th class="px-6 py-3">หนังสือ</th>
                  <th class="px-6 py-3">ราคา/หน่วย</th>
                  <th class="px-6 py-3 text-center">จำนวน</th>
                  <th class="px-6 py-3">ยอดรวม</th>
                  <th class="px-6 py-3 text-center">ลบ</th>
                </tr>
              </thead>
              <tbody class="divide-y divide-gray-200 text-sm">
                ${cartItems.map(item => `
                  <tr>
                    <td class="px-6 py-4 font-bold text-gray-900">${item.title}</td>
                    <td class="px-6 py-4 text-gray-600">${Number(item.price).toLocaleString()} ฿</td>
                    <td class="px-6 py-4 text-center">
                      <div class="flex items-center justify-center space-x-2">
                        <form method="POST" action="/cart/update-qty" class="inline">
                          <input type="hidden" name="cart_item_id" value="${item.cart_item_id}">
                          <input type="hidden" name="delta" value="-1">
                          <button class="bg-gray-200 text-gray-700 w-6 h-6 rounded font-bold">-</button>
                        </form>
                        <span class="font-bold">${item.quantity}</span>
                        <form method="POST" action="/cart/update-qty" class="inline">
                          <input type="hidden" name="cart_item_id" value="${item.cart_item_id}">
                          <input type="hidden" name="delta" value="1">
                          <button class="bg-gray-200 text-gray-700 w-6 h-6 rounded font-bold">+</button>
                        </form>
                      </div>
                    </td>
                    <td class="px-6 py-4 font-bold text-blue-600">${Number(item.subtotal).toLocaleString()} ฿</td>
                    <td class="px-6 py-4 text-center">
                      <form method="POST" action="/cart/remove">
                        <input type="hidden" name="cart_item_id" value="${item.cart_item_id}">
                        <button class="text-rose-500 hover:text-rose-700 text-sm">ลบ</button>
                      </form>
                    </td>
                  </tr>
                `).join('')}
              </tbody>
            </table>
            
            <div class="p-6 bg-gray-50 border-t flex flex-col md:flex-row justify-between items-center gap-4">
              <div>
                <span class="text-sm text-gray-500">ยอดชำระสุทธิทั้งสิ้น:</span>
                <span class="text-2xl font-black text-blue-600 ml-2">${Number(totalAmount).toLocaleString()} ฿</span>
              </div>
              <form method="POST" action="/checkout-cart">
                <button type="submit" class="bg-emerald-600 hover:bg-emerald-700 text-white font-bold px-6 py-2.5 rounded-lg shadow transition">
                  ยืนยันสั่งซื้อและชำระเงินจำลอง →
                </button>
              </form>
            </div>
          </div>
        `}
      </div>
    </body>
    </html>
  `);
});

app.post('/cart/add', async (req, res) => {
  if (!req.session.user) return res.redirect('/login');
  const { ebook_id } = req.body;

  let cart = await pool.query('SELECT cart_id FROM carts WHERE user_id = $1', [req.session.user.user_id]);
  let cartId = cart.rows[0]?.cart_id;
  if (!cartId) {
    const newCart = await pool.query('INSERT INTO carts (user_id) VALUES ($1) RETURNING cart_id', [req.session.user.user_id]);
    cartId = newCart.rows[0].cart_id;
  }

  await pool.query(
    `INSERT INTO cart_items (cart_id, ebook_id, quantity) 
     VALUES ($1, $2, 1)
     ON CONFLICT (cart_id, ebook_id) 
     DO UPDATE SET quantity = cart_items.quantity + 1`,
    [cartId, ebook_id]
  );

  res.redirect('/cart');
});

app.post('/cart/update-qty', async (req, res) => {
  const { cart_item_id, delta } = req.body;
  const item = await pool.query('SELECT quantity FROM cart_items WHERE cart_item_id = $1', [cart_item_id]);
  if (item.rows.length) {
    const newQty = item.rows[0].quantity + parseInt(delta);
    if (newQty <= 0) {
      await pool.query('DELETE FROM cart_items WHERE cart_item_id = $1', [cart_item_id]);
    } else {
      await pool.query('UPDATE cart_items SET quantity = $1 WHERE cart_item_id = $2', [newQty, cart_item_id]);
    }
  }
  res.redirect('/cart');
});

app.post('/cart/remove', async (req, res) => {
  await pool.query('DELETE FROM cart_items WHERE cart_item_id = $1', [req.body.cart_item_id]);
  res.redirect('/cart');
});

app.post('/checkout-cart', async (req, res) => {
  if (!req.session.user) return res.redirect('/login');

  const client = await pool.connect();
  try {
    await client.query('BEGIN');
    const itemsRes = await client.query(
      `SELECT ci.ebook_id, ci.quantity, e.price 
       FROM carts c 
       JOIN cart_items ci ON c.cart_id = ci.cart_id
       JOIN ebooks e ON ci.ebook_id = e.ebook_id
       WHERE c.user_id = $1`, [req.session.user.user_id]
    );

    if (itemsRes.rows.length === 0) {
      await client.query('ROLLBACK');
      return res.redirect('/cart');
    }

    const totalAmount = itemsRes.rows.reduce((sum, r) => sum + (Number(r.price) * r.quantity), 0);

    const orderInsert = await client.query(
      `INSERT INTO orders (user_id, total_amount, order_status, payment_slip_url) 
       VALUES ($1, $2, 'pending', 'https://mock-slip.local/qr-checkout.png') RETURNING order_id`,
      [req.session.user.user_id, totalAmount]
    );
    const orderId = orderInsert.rows[0].order_id;

    for (const item of itemsRes.rows) {
      for (let i = 0; i < item.quantity; i++) {
        await client.query(
          `INSERT INTO order_items (order_id, ebook_id, price_at_purchase) VALUES ($1, $2, $3)`,
          [orderId, item.ebook_id, item.price]
        );
      }
    }

    // ล้างตะกร้าหลังสั่งซื้อ
    await client.query(
      `DELETE FROM cart_items WHERE cart_id = (SELECT cart_id FROM carts WHERE user_id = $1)`,
      [req.session.user.user_id]
    );

    await client.query('COMMIT');
    res.redirect('/my-orders');
  } catch (err) {
    await client.query('ROLLBACK');
    res.status(500).send(err.message);
  } finally {
    client.release();
  }
});

// ----------------------------------------------------
// 4. คำสั่งซื้อ และ Secure Download
// ----------------------------------------------------
app.get('/my-orders', async (req, res) => {
  if (!req.session.user) return res.redirect('/login');

  const orders = await pool.query(`
    SELECT o.order_id, o.total_amount, o.order_status, o.created_at,
           json_agg(json_build_object('title', e.title, 'price', oi.price_at_purchase, 'ebook_id', e.ebook_id)) AS items
    FROM orders o
    JOIN order_items oi ON o.order_id = oi.order_id
    JOIN ebooks e ON oi.ebook_id = e.ebook_id
    WHERE o.user_id = $1
    GROUP BY o.order_id
    ORDER BY o.created_at DESC
  `, [req.session.user.user_id]);

  const cartCount = await getCartCount(req.session.user.user_id);

  res.send(`
    <!DOCTYPE html>
    <html lang="th">
    <head><meta charset="UTF-8"><title>คำสั่งซื้อของฉัน</title><script src="https://cdn.tailwindcss.com"></script></head>
    <body class="bg-slate-50 min-h-screen">
      ${renderNavbar(req.session.user, cartCount)}

      <div class="max-w-5xl mx-auto px-4 py-8">
        <h1 class="text-2xl font-bold text-gray-900 mb-6">ประวัติคำสั่งซื้อทั้งหมด</h1>
        
        <div class="space-y-4">
          ${orders.rows.length === 0 ? `<div class="bg-white p-8 text-center rounded-xl border text-gray-500">ยังไม่มีประวัติคำสั่งซื้อ</div>` : ''}
          ${orders.rows.map(o => `
            <div class="bg-white rounded-xl border p-6 shadow-sm">
              <div class="flex flex-wrap justify-between items-center border-b pb-4 mb-4 gap-2">
                <div>
                  <span class="text-xs text-gray-400 block">หมายเลขคำสั่งซื้อ</span>
                  <span class="font-bold text-gray-900">#ORD-${String(o.order_id).padStart(5, '0')}</span>
                  <span class="text-xs text-gray-500 ml-2">(${new Date(o.created_at).toLocaleString('th-TH')})</span>
                </div>
                <div>
                  ${o.order_status === 'confirmed' ? `<span class="bg-emerald-100 text-emerald-800 text-xs px-3 py-1 rounded-full font-semibold">ยืนยันแล้ว (ชำระสำเร็จ)</span>` : ''}
                  ${o.order_status === 'pending' ? `<span class="bg-amber-100 text-amber-800 text-xs px-3 py-1 rounded-full font-semibold">รอผู้ดูแลร้านตรวจสอบสลิป</span>` : ''}
                  ${o.order_status === 'cancelled' ? `<span class="bg-rose-100 text-rose-800 text-xs px-3 py-1 rounded-full font-semibold">ยกเลิกคำสั่งซื้อ</span>` : ''}
                </div>
              </div>

              <div class="space-y-3">
                ${o.items.map(item => `
                  <div class="flex justify-between items-center py-2">
                    <div>
                      <p class="font-medium text-gray-800">${item.title}</p>
                      <p class="text-xs text-gray-400">Digital PDF License</p>
                    </div>
                    <div class="flex items-center space-x-4">
                      <span class="font-semibold text-gray-700">${Number(item.price).toLocaleString()} ฿</span>
                      ${o.order_status === 'confirmed' ? `
                        <a href="/download/${item.ebook_id}" target="_blank" class="bg-emerald-600 hover:bg-emerald-700 text-white text-xs px-3 py-1.5 rounded-lg flex items-center space-x-1">
                          <span>⬇️ เปิดอ่าน / ดาวน์โหลด</span>
                        </a>
                      ` : `
                        <button disabled class="bg-gray-100 text-gray-400 text-xs px-3 py-1.5 rounded-lg cursor-not-allowed">
                          🔒 ล็อกไฟล์ (รออนุมัติ)
                        </button>
                      `}
                    </div>
                  </div>
                `).join('')}
              </div>

              <div class="border-t pt-4 mt-4 flex justify-between items-center text-sm">
                <span class="text-gray-500">วิธีชำระ: สลิปโอนเงิน PromptPay QR</span>
                <div>
                  <span class="text-gray-500 mr-2">ยอดรวม:</span>
                  <span class="text-xl font-extrabold text-blue-600">${Number(o.total_amount).toLocaleString()} ฿</span>
                </div>
              </div>
            </div>
          `).join('')}
        </div>
      </div>
    </body>
    </html>
  `);
});

app.get('/download/:ebookId', async (req, res) => {
  if (!req.session.user) return res.status(401).send('กรุณาเข้าสู่ระบบ');
  const { ebookId } = req.params;

  const check = await pool.query(`
    SELECT e.title FROM orders o
    JOIN order_items oi ON o.order_id = oi.order_id
    JOIN ebooks e ON oi.ebook_id = e.ebook_id
    WHERE o.user_id = $1 AND e.ebook_id = $2 AND o.order_status = 'confirmed'
  `, [req.session.user.user_id, ebookId]);

  if (!check.rows.length) {
    return res.status(403).send('Forbidden: คุณยังไม่ได้สั่งซื้อเล่มนี้ หรือคำสั่งซื้อยังไม่ได้รับการยืนยัน');
  }

  res.send(`
    <!DOCTYPE html>
    <html lang="th">
    <head><meta charset="UTF-8"><title>เปิดอ่านหนังสือ</title><script src="https://cdn.tailwindcss.com"></script></head>
    <body class="bg-gray-900 min-h-screen flex items-center justify-center p-4">
      <div class="bg-white max-w-xl w-full p-8 rounded-2xl text-center shadow-xl">
        <span class="text-6xl">📖</span>
        <h1 class="text-xl font-bold text-gray-900 mt-4">${check.rows[0].title}</h1>
        <p class="text-sm text-gray-500 mt-1 mb-6">ไฟล์ดิจิทัลลิขสิทธิ์ถูกต้อง สำหรับผู้เรียน Mini Project</p>
        <div class="bg-emerald-50 border border-emerald-200 text-emerald-800 p-4 rounded-xl text-sm mb-6">
          ตรวจสอบสิทธิ์เรียบร้อย สิทธิ์การเข้าถึงเป็นของ User ID: <b>#${req.session.user.user_id} (${req.session.user.full_name})</b>
        </div>
        <button onclick="window.close()" class="bg-gray-800 text-white px-6 py-2 rounded-lg text-sm">ปิดหน้าต่าง</button>
      </div>
    </body>
    </html>
  `);
});

// ----------------------------------------------------
// 5. Admin Backoffice (คำสั่งซื้อ, E-Book, หมวดหมู่, ผู้ใช้)
// ----------------------------------------------------
// Guard ตรวจสอบ Role Admin
function adminGuard(req, res, next) {
  if (!req.session.user || req.session.user.role_name !== 'admin') {
    return res.status(403).send('Access Denied: เฉพาะผู้ดูแลระบบ (Admin) เท่านั้น');
  }
  next();
}

// 5.1 จัดการคำสั่งซื้อ
app.get('/admin/orders', adminGuard, async (req, res) => {
  const { rows } = await pool.query(`
    SELECT o.order_id, u.full_name, u.email, o.total_amount, o.order_status, o.created_at
    FROM orders o JOIN users u ON o.user_id = u.user_id
    ORDER BY o.order_id DESC LIMIT 50
  `);

  res.send(`
    <!DOCTYPE html>
    <html lang="th">
    <head><meta charset="UTF-8"><title>จัดการคำสั่งซื้อ (Admin)</title><script src="https://cdn.tailwindcss.com"></script></head>
    <body class="bg-slate-100 min-h-screen">
      ${renderNavbar(req.session.user)}
      <div class="max-w-7xl mx-auto px-4 py-8">
        <h1 class="text-2xl font-bold text-gray-900 mb-6">📦 จัดการคำสั่งซื้อทั้งหมด</h1>
        <div class="bg-white rounded-xl shadow-sm border overflow-hidden">
          <table class="w-full text-left divide-y divide-gray-200 text-sm">
            <thead class="bg-gray-50 text-gray-500 font-semibold">
              <tr>
                <th class="p-4">Order ID</th>
                <th class="p-4">ลูกค้า</th>
                <th class="p-4">ยอดรวม</th>
                <th class="p-4">สถานะ</th>
                <th class="p-4 text-center">ดำเนินการ</th>
              </tr>
            </thead>
            <tbody class="divide-y divide-gray-200">
              ${rows.map(o => `
                <tr>
                  <td class="p-4 font-bold">#ORD-${o.order_id}</td>
                  <td class="p-4">${o.full_name} <br><span class="text-xs text-gray-400">${o.email}</span></td>
                  <td class="p-4 font-bold text-blue-600">${Number(o.total_amount).toLocaleString()} ฿</td>
                  <td class="p-4 font-bold">${o.order_status}</td>
                  <td class="p-4 text-center space-x-2">
                    <form method="POST" action="/admin/orders/${o.order_id}/update" class="inline">
                      <input type="hidden" name="status" value="confirmed">
                      <button class="bg-emerald-600 hover:bg-emerald-700 text-white text-xs px-3 py-1.5 rounded-lg">ยืนยัน</button>
                    </form>
                    <form method="POST" action="/admin/orders/${o.order_id}/update" class="inline">
                      <input type="hidden" name="status" value="cancelled">
                      <button class="bg-rose-600 hover:bg-rose-700 text-white text-xs px-3 py-1.5 rounded-lg">ยกเลิก</button>
                    </form>
                  </td>
                </tr>
              `).join('')}
            </tbody>
          </table>
        </div>
      </div>
    </body>
    </html>
  `);
});

app.post('/admin/orders/:id/update', adminGuard, async (req, res) => {
  await pool.query('UPDATE orders SET order_status = $1 WHERE order_id = $2', [req.body.status, req.params.id]);
  res.redirect('/admin/orders');
});

// 5.2 จัดการ E-Book (เพิ่มหนังสือ, เปิด-ปิดการขาย)
app.get('/admin/ebooks', adminGuard, async (req, res) => {
  const ebooks = await pool.query(`
    SELECT e.*, c.category_name, a.author_name 
    FROM ebooks e
    JOIN categories c ON e.category_id = c.category_id
    JOIN authors a ON e.author_id = a.author_id
    ORDER BY e.ebook_id DESC
  `);
  const categories = await pool.query('SELECT * FROM categories');
  const authors = await pool.query('SELECT * FROM authors');

  res.send(`
    <!DOCTYPE html>
    <html lang="th">
    <head><meta charset="UTF-8"><title>จัดการ E-Book</title><script src="https://cdn.tailwindcss.com"></script></head>
    <body class="bg-slate-100 min-h-screen">
      ${renderNavbar(req.session.user)}
      <div class="max-w-7xl mx-auto px-4 py-8">
        <h1 class="text-2xl font-bold text-gray-900 mb-6">📚 จัดการหนังสือ E-Book</h1>
        
        <!-- ฟอร์มเพิ่มหนังสือใหม่ -->
        <div class="bg-white p-6 rounded-xl border mb-8 shadow-sm">
          <h2 class="font-bold text-lg mb-4 text-gray-800">➕ เพิ่มหนังสือเล่มใหม่</h2>
          <form method="POST" action="/admin/ebooks/add" class="grid grid-cols-1 md:grid-cols-3 gap-4">
            <div>
              <label class="text-xs font-medium text-gray-600">ชื่อหนังสือ</label>
              <input type="text" name="title" required class="w-full border p-2 rounded-lg text-sm mt-1">
            </div>
            <div>
              <label class="text-xs font-medium text-gray-600">หมวดหมู่</label>
              <select name="category_id" required class="w-full border p-2 rounded-lg text-sm mt-1">
                ${categories.rows.map(c => `<option value="${c.category_id}">${c.category_name}</option>`).join('')}
              </select>
            </div>
            <div>
              <label class="text-xs font-medium text-gray-600">ผู้แต่ง</label>
              <select name="author_id" required class="w-full border p-2 rounded-lg text-sm mt-1">
                ${authors.rows.map(a => `<option value="${a.author_id}">${a.author_name}</option>`).join('')}
              </select>
            </div>
            <div>
              <label class="text-xs font-medium text-gray-600">ราคา (บาท)</label>
              <input type="number" step="0.01" min="0" name="price" required class="w-full border p-2 rounded-lg text-sm mt-1">
            </div>
            <div class="md:col-span-2">
              <label class="text-xs font-medium text-gray-600">คำอธิบายย่อ</label>
              <input type="text" name="description" required class="w-full border p-2 rounded-lg text-sm mt-1">
            </div>
            <button type="submit" class="md:col-span-3 bg-blue-600 hover:bg-blue-700 text-white py-2 rounded-lg font-medium text-sm">
              บันทึก E-Book
            </button>
          </form>
        </div>

        <!-- รายการหนังสือ -->
        <div class="bg-white rounded-xl border shadow-sm overflow-hidden">
          <table class="w-full text-left divide-y divide-gray-200 text-sm">
            <thead class="bg-gray-50 text-gray-500 font-semibold">
              <tr>
                <th class="p-4">ID</th>
                <th class="p-4">ชื่อหนังสือ</th>
                <th class="p-4">หมวดหมู่</th>
                <th class="p-4">ราคา</th>
                <th class="p-4">สถานะขาย</th>
                <th class="p-4 text-center">สลับสถานะ</th>
              </tr>
            </thead>
            <tbody class="divide-y divide-gray-200">
              ${ebooks.rows.map(b => `
                <tr>
                  <td class="p-4">#${b.ebook_id}</td>
                  <td class="p-4 font-bold text-gray-900">${b.title}</td>
                  <td class="p-4">${b.category_name}</td>
                  <td class="p-4 font-bold text-blue-600">${Number(b.price).toLocaleString()} ฿</td>
                  <td class="p-4">
                    <span class="px-2.5 py-1 text-xs rounded-full font-bold ${b.is_active ? 'bg-emerald-100 text-emerald-800' : 'bg-gray-100 text-gray-500'}">
                      ${b.is_active ? 'พร้อมขาย' : 'ปิดการขาย'}
                    </span>
                  </td>
                  <td class="p-4 text-center">
                    <form method="POST" action="/admin/ebooks/${b.ebook_id}/toggle-status">
                      <button class="text-xs border px-3 py-1.5 rounded-lg hover:bg-gray-50">
                        ${b.is_active ? 'ปิดขาย' : 'เปิดขาย'}
                      </button>
                    </form>
                  </td>
                </tr>
              `).join('')}
            </tbody>
          </table>
        </div>
      </div>
    </body>
    </html>
  `);
});

app.post('/admin/ebooks/add', adminGuard, async (req, res) => {
  const { title, category_id, author_id, price, description } = req.body;
  await pool.query(
    `INSERT INTO ebooks (title, category_id, author_id, price, description, file_download_url, is_active)
     VALUES ($1, $2, $3, $4, $5, 'https://mock-files.local/sample.pdf', TRUE)`,
    [title, category_id, author_id, price, description]
  );
  res.redirect('/admin/ebooks');
});

app.post('/admin/ebooks/:id/toggle-status', adminGuard, async (req, res) => {
  await pool.query('UPDATE ebooks SET is_active = NOT is_active WHERE ebook_id = $1', [req.params.id]);
  res.redirect('/admin/ebooks');
});

// 5.3 จัดการหมวดหมู่
app.get('/admin/categories', adminGuard, async (req, res) => {
  const categories = await pool.query(`
    SELECT c.*, COUNT(e.ebook_id) AS total_books
    FROM categories c
    LEFT JOIN ebooks e ON c.category_id = e.category_id
    GROUP BY c.category_id
    ORDER BY c.category_id ASC
  `);

  res.send(`
    <!DOCTYPE html>
    <html lang="th">
    <head><meta charset="UTF-8"><title>จัดการหมวดหมู่</title><script src="https://cdn.tailwindcss.com"></script></head>
    <body class="bg-slate-100 min-h-screen">
      ${renderNavbar(req.session.user)}
      <div class="max-w-4xl mx-auto px-4 py-8">
        <h1 class="text-2xl font-bold text-gray-900 mb-6">🏷️ จัดการหมวดหมู่หนังสือ</h1>
        
        <div class="bg-white p-6 rounded-xl border mb-6 shadow-sm">
          <h2 class="font-bold text-lg mb-3">➕ เพิ่มหมวดหมู่ใหม่</h2>
          <form method="POST" action="/admin/categories/add" class="flex gap-3">
            <input type="text" name="category_name" placeholder="ชื่อหมวดหมู่ใหม่..." required class="border p-2 rounded-lg flex-1 text-sm">
            <input type="text" name="description" placeholder="คำอธิบาย..." class="border p-2 rounded-lg flex-1 text-sm">
            <button type="submit" class="bg-blue-600 text-white px-5 py-2 rounded-lg text-sm font-semibold hover:bg-blue-700">เพิ่ม</button>
          </form>
        </div>

        <div class="bg-white rounded-xl border shadow-sm overflow-hidden">
          <table class="w-full text-left divide-y divide-gray-200 text-sm">
            <thead class="bg-gray-50 text-gray-500 font-semibold">
              <tr>
                <th class="p-4">ID</th>
                <th class="p-4">ชื่อหมวดหมู่</th>
                <th class="p-4">คำอธิบาย</th>
                <th class="p-4 text-center">จำนวนหนังสือในหมวด</th>
              </tr>
            </thead>
            <tbody class="divide-y divide-gray-200">
              ${categories.rows.map(c => `
                <tr>
                  <td class="p-4">#${c.category_id}</td>
                  <td class="p-4 font-bold text-gray-800">${c.category_name}</td>
                  <td class="p-4 text-gray-500">${c.description || '-'}</td>
                  <td class="p-4 text-center font-bold text-blue-600">${c.total_books} เล่ม</td>
                </tr>
              `).join('')}
            </tbody>
          </table>
        </div>
      </div>
    </body>
    </html>
  `);
});

app.post('/admin/categories/add', adminGuard, async (req, res) => {
  const { category_name, description } = req.body;
  await pool.query('INSERT INTO categories (category_name, description) VALUES ($1, $2)', [category_name, description]);
  res.redirect('/admin/categories');
});

// 5.4 จัดการผู้ใช้ (ดูรายชื่อ / ปรับ Role)
app.get('/admin/users', adminGuard, async (req, res) => {
  const users = await pool.query(`
    SELECT u.user_id, u.username, u.email, u.full_name, u.role_id, r.role_name, u.created_at
    FROM users u
    JOIN roles r ON u.role_id = r.role_id
    ORDER BY u.user_id ASC
  `);

  res.send(`
    <!DOCTYPE html>
    <html lang="th">
    <head><meta charset="UTF-8"><title>จัดการผู้ใช้</title><script src="https://cdn.tailwindcss.com"></script></head>
    <body class="bg-slate-100 min-h-screen">
      ${renderNavbar(req.session.user)}
      <div class="max-w-5xl mx-auto px-4 py-8">
        <h1 class="text-2xl font-bold text-gray-900 mb-6">👥 จัดการรายชื่อสมาชิกและสิทธิ์ (Roles)</h1>
        
        <div class="bg-white rounded-xl border shadow-sm overflow-hidden">
          <table class="w-full text-left divide-y divide-gray-200 text-sm">
            <thead class="bg-gray-50 text-gray-500 font-semibold">
              <tr>
                <th class="p-4">ID</th>
                <th class="p-4">ชื่อ-นามสกุล / Email</th>
                <th class="p-4">Username</th>
                <th class="p-4">Role ปัจจุบัน</th>
                <th class="p-4 text-center">เปลี่ยน Role</th>
              </tr>
            </thead>
            <tbody class="divide-y divide-gray-200">
              ${users.rows.map(u => `
                <tr>
                  <td class="p-4">#${u.user_id}</td>
                  <td class="p-4">
                    <p class="font-bold text-gray-900">${u.full_name}</p>
                    <p class="text-xs text-gray-400">${u.email}</p>
                  </td>
                  <td class="p-4 text-gray-600">@${u.username}</td>
                  <td class="p-4">
                    <span class="px-2.5 py-1 text-xs rounded-full font-bold ${u.role_name === 'admin' ? 'bg-purple-100 text-purple-700' : 'bg-blue-100 text-blue-700'}">
                      ${u.role_name}
                    </span>
                  </td>
                  <td class="p-4 text-center">
                    ${u.user_id === req.session.user.user_id ? `<span class="text-xs text-gray-400">บัญชีปัจจุบัน</span>` : `
                      <form method="POST" action="/admin/users/${u.user_id}/toggle-role">
                        <button class="text-xs border px-3 py-1.5 rounded-lg hover:bg-gray-50">
                          สลับเป็น ${u.role_name === 'admin' ? 'Customer' : 'Admin'}
                        </button>
                      </form>
                    `}
                  </td>
                </tr>
              `).join('')}
            </tbody>
          </table>
        </div>
      </div>
    </body>
    </html>
  `);
});

app.post('/admin/users/:id/toggle-role', adminGuard, async (req, res) => {
  const current = await pool.query('SELECT role_id FROM users WHERE user_id = $1', [req.params.id]);
  const newRoleId = current.rows[0].role_id === 1 ? 2 : 1;
  await pool.query('UPDATE users SET role_id = $1 WHERE user_id = $2', [newRoleId, req.params.id]);
  res.redirect('/admin/users');
});

// ----------------------------------------------------
// 6. Reports & Export CSV
// ----------------------------------------------------
app.get('/reports', async (req, res) => {
  const report1 = await pool.query(`
    SELECT DATE(created_at) AS date, COUNT(order_id) AS total_orders, SUM(total_amount) AS total_sales, ROUND(AVG(total_amount), 2) AS avg_sale
    FROM orders WHERE order_status = 'confirmed'
    GROUP BY DATE(created_at) ORDER BY date DESC LIMIT 7
  `);

  const report2 = await pool.query(`
    SELECT e.title, a.author_name, COUNT(oi.order_item_id) AS units_sold, SUM(oi.price_at_purchase) AS sales
    FROM order_items oi
    JOIN orders o ON oi.order_id = o.order_id
    JOIN ebooks e ON oi.ebook_id = e.ebook_id
    JOIN authors a ON e.author_id = a.author_id
    WHERE o.order_status = 'confirmed'
    GROUP BY e.title, a.author_name ORDER BY units_sold DESC LIMIT 5
  `);

  const report3 = await pool.query(`
    SELECT c.category_name, COUNT(oi.order_item_id) AS items_count, SUM(oi.price_at_purchase) AS sales
    FROM categories c
    JOIN ebooks e ON c.category_id = e.category_id
    JOIN order_items oi ON e.ebook_id = oi.ebook_id
    JOIN orders o ON oi.order_id = o.order_id
    WHERE o.order_status = 'confirmed'
    GROUP BY c.category_name ORDER BY sales DESC
  `);

  const report4 = await pool.query(`
    SELECT u.username, u.full_name, COUNT(o.order_id) AS orders_count, SUM(o.total_amount) AS spent
    FROM users u JOIN orders o ON u.user_id = o.user_id
    WHERE o.order_status = 'confirmed'
    GROUP BY u.username, u.full_name ORDER BY spent DESC LIMIT 5
  `);

  const cartCount = await getCartCount(req.session.user?.user_id);

  res.send(`
    <!DOCTYPE html>
    <html lang="th">
    <head><meta charset="UTF-8"><title>Analytics Dashboard</title><script src="https://cdn.tailwindcss.com"></script></head>
    <body class="bg-slate-50 min-h-screen">
      ${renderNavbar(req.session.user, cartCount)}

      <div class="max-w-7xl mx-auto px-4 py-8">
        <div class="flex flex-col md:flex-row justify-between items-start md:items-center mb-8 gap-4">
          <div>
            <h1 class="text-3xl font-extrabold text-gray-900 mb-1">รายงานวิเคราะห์ฐานข้อมูล (4 Analytics Reports)</h1>
            <p class="text-sm text-gray-500">ประมวลผล Aggregate Query จากฐานข้อมูล PostgreSQL จริง</p>
          </div>
          <a href="/reports/export-csv" class="bg-emerald-600 hover:bg-emerald-700 text-white text-sm font-bold px-4 py-2 rounded-lg shadow flex items-center space-x-2">
            <span>📥 Export สรุปยอดขาย (.CSV)</span>
          </a>
        </div>

        <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
          <div class="bg-white p-6 rounded-xl border shadow-sm">
            <h2 class="font-bold text-gray-900 border-b pb-3 mb-4">📈 1. ยอดขายตามช่วงเวลา (รายวันล่าสุด)</h2>
            <div class="space-y-3">
              ${report1.rows.map(r => `
                <div class="flex justify-between items-center text-sm border-b pb-2">
                  <span class="font-medium text-gray-700">${new Date(r.date).toISOString().slice(0, 10)}</span>
                  <div>
                    <span class="text-xs text-gray-400 mr-2">(${r.total_orders} รายการ, เฉลี่ย ${r.avg_sale} ฿)</span>
                    <span class="font-bold text-blue-600">${Number(r.total_sales).toLocaleString()} ฿</span>
                  </div>
                </div>
              `).join('')}
            </div>
          </div>

          <div class="bg-white p-6 rounded-xl border shadow-sm">
            <h2 class="font-bold text-gray-900 border-b pb-3 mb-4">🏆 2. Top 5 E-Book ขายดีที่สุด</h2>
            <div class="space-y-3">
              ${report2.rows.map((r, i) => `
                <div class="flex justify-between items-center text-sm border-b pb-2">
                  <div>
                    <span class="font-bold text-blue-600 mr-2">#${i + 1}</span>
                    <span class="font-medium text-gray-800">${r.title}</span>
                    <span class="block text-xs text-gray-400">โดย ${r.author_name}</span>
                  </div>
                  <div class="text-right">
                    <span class="font-bold text-gray-900">${r.units_sold} เล่ม</span>
                    <span class="block text-xs text-emerald-600">${Number(r.sales).toLocaleString()} ฿</span>
                  </div>
                </div>
              `).join('')}
            </div>
          </div>

          <div class="bg-white p-6 rounded-xl border shadow-sm">
            <h2 class="font-bold text-gray-900 border-b pb-3 mb-4">🏷️ 3. สรุปยอดขายตามหมวดหมู่</h2>
            <div class="space-y-3">
              ${report3.rows.map(r => `
                <div class="flex justify-between items-center text-sm border-b pb-2">
                  <span class="font-medium text-gray-800">${r.category_name}</span>
                  <div class="text-right">
                    <span class="font-bold text-gray-900">${Number(r.sales).toLocaleString()} ฿</span>
                    <span class="text-xs text-gray-400 block">${r.items_count} เล่มที่ขายได้</span>
                  </div>
                </div>
              `).join('')}
            </div>
          </div>

          <div class="bg-white p-6 rounded-xl border shadow-sm">
            <h2 class="font-bold text-gray-900 border-b pb-3 mb-4">👑 4. ลูกค้าที่มีประวัติยอดซื้อสะสมสูงสุด</h2>
            <div class="space-y-3">
              ${report4.rows.map((r, i) => `
                <div class="flex justify-between items-center text-sm border-b pb-2">
                  <div>
                    <span class="font-bold text-purple-600 mr-2">#${i + 1}</span>
                    <span class="font-medium text-gray-800">${r.full_name}</span>
                    <span class="text-xs text-gray-400">(@${r.username})</span>
                  </div>
                  <div class="text-right">
                    <span class="font-bold text-blue-600">${Number(r.spent).toLocaleString()} ฿</span>
                    <span class="text-xs text-gray-400 block">${r.orders_count} ออเดอร์</span>
                  </div>
                </div>
              `).join('')}
            </div>
          </div>
        </div>
      </div>
    </body>
    </html>
  `);
});

// ฟังก์ชันส่งออก CSV
app.get('/reports/export-csv', async (req, res) => {
  const { rows } = await pool.query(`
    SELECT o.order_id, u.username, o.total_amount, o.order_status, o.created_at
    FROM orders o JOIN users u ON o.user_id = u.user_id
    ORDER BY o.order_id ASC
  `);

  let csv = 'Order ID,Username,Total Amount,Status,Created At\n';
  rows.forEach(r => {
    csv += `"${r.order_id}","${r.username}","${r.total_amount}","${r.order_status}","${new Date(r.created_at).toISOString()}"\n`;
  });

  res.setHeader('Content-Type', 'text/csv; charset=utf-8');
  res.setHeader('Content-Disposition', 'attachment; filename=sales_report.csv');
  res.status(200).send('\uFEFF' + csv);
});

const PORT = process.env.PORT || 3000;
app.listen(PORT, () => console.log(`Server running on port ${PORT}`));