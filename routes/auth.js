const express = require('express');
const router = express.Router();
const pool = require('../db');

// Helper: นับจำนวนในตะกร้า
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

// Login
router.get('/login', (req, res) => {
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

router.post('/login', async (req, res) => {
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

// Register
router.get('/register', (req, res) => {
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

router.post('/register', async (req, res) => {
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

// Profile
router.get('/profile', async (req, res) => {
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

router.post('/profile/update', async (req, res) => {
  if (!req.session.user) return res.redirect('/login');
  const { full_name, email } = req.body;
  await pool.query('UPDATE users SET full_name = $1, email = $2 WHERE user_id = $3', [full_name, email, req.session.user.user_id]);
  req.session.user.full_name = full_name;
  req.session.user.email = email;
  res.send(`<script>alert('บันทึกข้อมูลเรียบร้อย'); window.location='/profile';</script>`);
});

// Logout
router.get('/logout', (req, res) => {
  req.session.destroy(() => res.redirect('/login'));
});

module.exports = router;