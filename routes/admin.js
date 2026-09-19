const express = require('express');
const router = express.Router();
const pool = require('../db');

// Middleware ตรวจสอบสิทธิ์ Admin
function adminGuard(req, res, next) {
  if (!req.session.user || req.session.user.role_name !== 'admin') {
    return res.status(403).send('Access Denied: เฉพาะผู้ดูแลระบบ (Admin) เท่านั้น');
  }
  next();
}

// ใช้งาน Guard กับทุกเส้นทางใน Admin
router.use(adminGuard);

// ฟังก์ชันดึงจำนวนในตะกร้าสำหรับ Navbar
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
// 1. จัดการคำสั่งซื้อ
// ----------------------------------------------------
router.get('/orders', async (req, res) => {
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

router.post('/orders/:id/update', async (req, res) => {
  await pool.query('UPDATE orders SET order_status = $1 WHERE order_id = $2', [req.body.status, req.params.id]);
  res.redirect('/admin/orders');
});

// ----------------------------------------------------
// 2. จัดการ E-Book และเพิ่มผู้แต่ง
// ----------------------------------------------------
router.get('/ebooks', async (req, res) => {
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
        
        <!-- ฟอร์มเพิ่มผู้แต่งใหม่ -->
        <div class="bg-white p-6 rounded-xl border mb-6 shadow-sm">
          <h2 class="font-bold text-lg mb-4 text-gray-800">➕ เพิ่มผู้แต่งใหม่</h2>
          <form method="POST" action="/admin/add-author" class="grid grid-cols-1 md:grid-cols-3 gap-4">
            <div>
              <label class="text-xs font-medium text-gray-600">ชื่อผู้แต่ง</label>
              <input type="text" name="name" required placeholder="เช่น Eiichiro Oda" class="w-full border p-2 rounded-lg text-sm mt-1">
            </div>
            <div class="md:col-span-2">
              <label class="text-xs font-medium text-gray-600">ประวัติย่อ / คำอธิบาย (เว้นว่างได้)</label>
              <input type="text" name="bio" placeholder="ประวัติย่อของผู้แต่ง..." class="w-full border p-2 rounded-lg text-sm mt-1">
            </div>
            <button type="submit" class="md:col-span-3 bg-emerald-600 hover:bg-emerald-700 text-white py-2 rounded-lg font-medium text-sm">
              บันทึกผู้แต่ง
            </button>
          </form>
        </div>

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

router.post('/ebooks/add', async (req, res) => {
  const { title, category_id, author_id, price, description } = req.body;
  await pool.query(
    `INSERT INTO ebooks (title, category_id, author_id, price, description, file_download_url, is_active)
     VALUES ($1, $2, $3, $4, $5, 'https://mock-files.local/sample.pdf', TRUE)`,
    [title, category_id, author_id, price, description]
  );
  res.redirect('/admin/ebooks');
});

router.post('/ebooks/:id/toggle-status', async (req, res) => {
  await pool.query('UPDATE ebooks SET is_active = NOT is_active WHERE ebook_id = $1', [req.params.id]);
  res.redirect('/admin/ebooks');
});

router.post('/add-author', async (req, res) => {
  try {
    const { name, bio } = req.body;
    if (!name || !name.trim()) {
      return res.status(400).send('กรุณากรอกชื่อผู้แต่ง');
    }
    await pool.query(
      'INSERT INTO authors (author_name, bio) VALUES ($1, $2)',
      [name.trim(), bio ? bio.trim() : '']
    );
    res.redirect('/admin/ebooks');
  } catch (err) {
    console.error('ERROR ADDING AUTHOR:', err);
    res.status(500).send(`เกิดข้อผิดพลาด: ${err.message}`);
  }
});

// ----------------------------------------------------
// 3. จัดการหมวดหมู่
// ----------------------------------------------------
router.get('/categories', async (req, res) => {
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
                <th class="p-4 text-center">จัดการ</th>
              </tr>
            </thead>
            <tbody class="divide-y divide-gray-200">
              ${categories.rows.map(c => `
                <tr>
                  <td class="p-4">#${c.category_id}</td>
                  <td class="p-4 font-bold text-gray-800">${c.category_name}</td>
                  <td class="p-4 text-gray-500">${c.description || '-'}</td>
                  <td class="p-4 text-center font-bold text-blue-600">${c.total_books} เล่ม</td>
                  <td class="p-4 text-center">
                    <form method="POST" action="/admin/categories/${c.category_id}/delete" onsubmit="return confirm('ต้องการลบหมวดหมู่นี้หรือไม่?');">
                      <button type="submit" class="text-xs bg-rose-50 text-rose-600 hover:bg-rose-100 border border-rose-200 px-3 py-1.5 rounded-lg font-medium">
                        🗑️ ลบ
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

router.post('/categories/add', async (req, res) => {
  const { category_name, description } = req.body;
  await pool.query('INSERT INTO categories (category_name, description) VALUES ($1, $2)', [category_name, description]);
  res.redirect('/admin/categories');
});

router.post('/categories/:id/delete', async (req, res) => {
  const categoryId = req.params.id;
  const client = await pool.connect();

  try {
    const checkBooks = await client.query('SELECT COUNT(*) FROM ebooks WHERE category_id = $1', [categoryId]);
    if (parseInt(checkBooks.rows[0].count) > 0) {
      client.release();
      return res.send(`<script>alert('ไม่สามารถลบได้ เนื่องจากยังมีหนังสืออยู่ในหมวดหมู่นี้'); window.location='/admin/categories';</script>`);
    }

    await client.query('BEGIN');

    // 1. ลบหมวดหมู่ที่เลือก
    await client.query('DELETE FROM categories WHERE category_id = $1', [categoryId]);

    // 2. ดึงรายการที่เหลือมาจัดลำดับใหม่
    const remaining = await client.query('SELECT category_id FROM categories ORDER BY category_id ASC');

    // 3. วนลูปปรับ ID ให้เรียง 1, 2, 3... ต่อเนื่องกัน
    for (let i = 0; i < remaining.rows.length; i++) {
      const oldId = remaining.rows[i].category_id;
      const newId = i + 1;

      if (oldId !== newId) {
        await client.query('UPDATE ebooks SET category_id = $1 WHERE category_id = $2', [newId, oldId]);
        await client.query('UPDATE categories SET category_id = $1 WHERE category_id = $2', [newId, oldId]);
      }
    }

    // 4. รีเซ็ต Sequence ให้รันต่อจากเลขตัวสุดท้าย
    if (remaining.rows.length > 0) {
      await client.query(`
        SELECT setval(
          pg_get_serial_sequence('categories', 'category_id'), 
          (SELECT MAX(category_id) FROM categories), 
          true
        )
      `);
    } else {
      await client.query(`
        SELECT setval(
          pg_get_serial_sequence('categories', 'category_id'), 
          1, 
          false
        )
      `);
    }

    await client.query('COMMIT');
    res.redirect('/admin/categories');
  } catch (err) {
    await client.query('ROLLBACK');
    console.error('ERROR DELETING CATEGORY:', err);
    res.status(500).send(`เกิดข้อผิดพลาด: ${err.message}`);
  } finally {
    client.release();
  }
});

// ----------------------------------------------------
// 4. จัดการรายชื่อสมาชิกและสิทธิ์ (Roles)
// ----------------------------------------------------
router.get('/users', async (req, res) => {
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

router.post('/users/:id/toggle-role', async (req, res) => {
  const current = await pool.query('SELECT role_id FROM users WHERE user_id = $1', [req.params.id]);
  const newRoleId = current.rows[0].role_id === 1 ? 2 : 1;
  await pool.query('UPDATE users SET role_id = $1 WHERE user_id = $2', [newRoleId, req.params.id]);
  res.redirect('/admin/users');
});

module.exports = router;