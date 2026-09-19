const express = require('express');
const router = express.Router();
const pool = require('../db');

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

// นำ Navbar มาใช้
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

// 1. หน้าแสดงรายงานสถิติ
router.get('/', async (req, res) => {
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

// 2. Export CSV
router.get('/export-csv', async (req, res) => {
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

module.exports = router;