const express = require('express');
const router = express.Router();
const pool = require('../db');

// Helper: นับจำนวนสินค้าในตะกร้า
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

// Helper: Render Navbar
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
            <a href="/ai" class="text-purple-600 hover:text-purple-800 font-bold text-sm flex items-center gap-1"><span>🤖</span> ผู้ช่วย AI</a>
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
// 2. Storefront (หน้าร้าน)
// ----------------------------------------------------
router.get('/', async (req, res) => {
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
            <div class="flex flex-wrap items-center justify-between gap-4 mb-6">
              <p class="text-blue-100 text-sm">ค้นหา ใส่ตะกร้า ชำระเงินจำลอง และรับไฟล์ลิขสิทธิ์เฉพาะคุณ</p>
              <a href="/ai" class="inline-flex items-center gap-1.5 bg-white text-purple-700 hover:bg-purple-50 font-bold text-xs px-4 py-2 rounded-xl shadow-md transition">
                <span>🤖</span> ลองถามผู้ช่วย AI แนะนำหนังสือ ✨
              </a>
            </div>
            
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
// 3. Cart System
// ----------------------------------------------------
router.get('/cart', async (req, res) => {
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

router.post('/cart/add', async (req, res) => {
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

router.post('/cart/update-qty', async (req, res) => {
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

router.post('/cart/remove', async (req, res) => {
  await pool.query('DELETE FROM cart_items WHERE cart_item_id = $1', [req.body.cart_item_id]);
  res.redirect('/cart');
});

router.post('/checkout-cart', async (req, res) => {
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
router.get('/my-orders', async (req, res) => {
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

router.get('/download/:ebookId', async (req, res) => {
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

module.exports = router;