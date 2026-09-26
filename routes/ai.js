// routes/ai.js
// เส้นทางบริการสำหรับผู้ช่วยปัญญาประดิษฐ์แนะนำหนังสือ (AI Bookstore Assistant Routes)

const express = require('express');
const router = express.Router();
const { recommendBooks } = require('../services/aiService');
const pool = require('../db');

// Helper: นับจำนวนสินค้าในตะกร้า
async function getCartCount(userId) {
  if (!userId) return 0;
  try {
    const res = await pool.query(
      `SELECT COALESCE(SUM(ci.quantity), 0) AS total 
       FROM carts c 
       JOIN cart_items ci ON c.cart_id = ci.cart_id 
       WHERE c.user_id = $1`, [userId]
    );
    return parseInt(res.rows[0].total) || 0;
  } catch {
    return 0;
  }
}

// ----------------------------------------------------
// 1. หน้าจอเว็บผู้ช่วย AI (AI Assistant UI)
// ----------------------------------------------------
router.get('/', async (req, res) => {
  const cartCount = await getCartCount(req.session.user?.user_id);
  const user = req.session.user;

  res.send(`
    <!DOCTYPE html>
    <html lang="th">
    <head>
      <meta charset="UTF-8">
      <meta name="viewport" content="width=device-width, initial-scale=1.0">
      <title>ผู้ช่วย AI แนะนำหนังสือ | E-Book Store</title>
      <script src="https://cdn.tailwindcss.com"></script>
    </head>
    <body class="bg-slate-50 min-h-screen flex flex-col">
      <!-- Navbar -->
      <nav class="bg-white border-b border-gray-200 sticky top-0 z-50 shadow-sm">
        <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div class="flex justify-between h-16">
            <div class="flex items-center space-x-3">
              <span class="text-2xl">📚</span>
              <a href="/" class="text-xl font-black bg-gradient-to-r from-blue-600 to-indigo-600 bg-clip-text text-transparent">E-Book Store</a>
              <span class="bg-purple-100 text-purple-700 text-xs px-2.5 py-0.5 rounded-full font-bold ml-2">🤖 AI Powered</span>
            </div>
            <div class="flex items-center space-x-4">
              <a href="/" class="text-gray-700 hover:text-blue-600 font-medium text-sm">หน้าร้าน</a>
              <a href="/ai" class="text-blue-600 font-bold text-sm border-b-2 border-blue-600 py-1">ผู้ช่วย AI</a>
              <a href="/reports" class="text-gray-700 hover:text-blue-600 font-medium text-sm">รายงานสถิติ</a>
              ${user ? `
                <a href="/cart" class="relative text-gray-700 hover:text-blue-600 font-medium text-sm flex items-center">
                  🛒 ตะกร้า
                  <span class="ml-1 bg-blue-600 text-white text-xs px-2 py-0.5 rounded-full font-bold">${cartCount}</span>
                </a>
                <a href="/my-orders" class="text-gray-700 hover:text-blue-600 font-medium text-sm">คำสั่งซื้อ</a>
                <div class="border-l pl-4 flex items-center space-x-3">
                  <span class="text-sm font-semibold text-gray-800">${user.full_name}</span>
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

      <!-- Main Assistant UI -->
      <main class="max-w-4xl mx-auto px-4 py-8 flex-1 w-full">
        <div class="bg-gradient-to-r from-purple-700 via-indigo-700 to-blue-700 rounded-3xl p-8 mb-8 text-white shadow-xl relative overflow-hidden">
          <div class="relative z-10">
            <div class="inline-flex items-center space-x-2 bg-white/20 backdrop-blur-md px-3 py-1 rounded-full text-xs font-semibold mb-3">
              <span>✨ Generative & Semantic Recommendation Engine</span>
            </div>
            <h1 class="text-3xl sm:text-4xl font-extrabold mb-3">ผู้ช่วยค้นหาและแนะนำหนังสืออัจฉริยะ</h1>
            <p class="text-purple-100 text-sm sm:text-base max-w-2xl leading-relaxed">
              พิมพ์บอกเป้าหมายการเรียนรู้ อารมณ์ หรือความสนใจของคุณ เช่น "อยากเริ่มศึกษาการลงทุนในหุ้นเทคโนโลยี" หรือ "หนังสือสำหรับพัฒนาตนเองและสร้างวินัย" AI จะจับคู่หนังสือที่ตรงใจที่สุดจากแคตตาล็อกร้านให้ทันที
            </p>
          </div>
        </div>

        <!-- Sample Query Chips -->
        <div class="mb-6">
          <p class="text-xs font-semibold text-gray-500 uppercase tracking-wider mb-2">ตัวอย่างคำค้นหายอดนิยม (คลิกเพื่อลอง):</p>
          <div class="flex flex-wrap gap-2">
            <button onclick="setQuery('อยากเริ่มต้นศึกษาด้าน Data และออกแบบฐานข้อมูล')" class="bg-white border border-gray-200 hover:border-purple-400 text-gray-700 hover:text-purple-700 text-xs px-3 py-1.5 rounded-full transition shadow-2xs">
              📊 ออกแบบฐานข้อมูล & Data
            </button>
            <button onclick="setQuery('มีหนังสือเกี่ยวกับการลงทุนและหุ้นเทคโนโลยีไหม')" class="bg-white border border-gray-200 hover:border-purple-400 text-gray-700 hover:text-purple-700 text-xs px-3 py-1.5 rounded-full transition shadow-2xs">
              📈 การลงทุนในหุ้นเทคโนโลยี
            </button>
            <button onclick="setQuery('หนังสือสำหรับสร้างนิสัยที่ดีและเพิ่มประสิทธิภาพการทำงาน')" class="bg-white border border-gray-200 hover:border-purple-400 text-gray-700 hover:text-purple-700 text-xs px-3 py-1.5 rounded-full transition shadow-2xs">
              ⚡ พัฒนานิสัย & Productivity
            </button>
            <button onclick="setQuery('เขียนโปรแกรมโครงสร้างข้อมูลและสถาปัตยกรรมซอฟต์แวร์')" class="bg-white border border-gray-200 hover:border-purple-400 text-gray-700 hover:text-purple-700 text-xs px-3 py-1.5 rounded-full transition shadow-2xs">
              💻 สถาปัตยกรรมซอฟต์แวร์ & Clean Code
            </button>
          </div>
        </div>

        <!-- Search Input Form -->
        <div class="bg-white p-4 rounded-2xl border shadow-sm mb-8">
          <form id="aiForm" class="flex flex-col sm:flex-row gap-3">
            <input 
              type="text" 
              id="userQuery" 
              name="query" 
              required
              placeholder="พิมพ์สิ่งที่คุณต้องการอ่าน เช่น 'อยากเข้าใจระบบคอมพิวเตอร์ลึกซึ้ง'..." 
              class="flex-1 px-4 py-3 border border-gray-200 rounded-xl focus:ring-2 focus:ring-purple-500 focus:outline-hidden text-sm"
            >
            <button 
              type="submit" 
              id="submitBtn"
              class="bg-gradient-to-r from-purple-600 to-indigo-600 hover:from-purple-700 hover:to-indigo-700 text-white font-semibold px-6 py-3 rounded-xl text-sm transition shadow-md flex items-center justify-center space-x-2"
            >
              <span id="btnText">🪄 ขอคำแนะนำ AI</span>
              <span id="btnSpinner" class="hidden animate-spin">⏳</span>
            </button>
          </form>
        </div>

        <!-- Recommendation Output Area -->
        <div id="resultContainer" class="hidden space-y-6">
          <div id="aiMetaCard" class="bg-purple-50 border border-purple-200 rounded-2xl p-5">
            <div class="flex flex-wrap items-center justify-between gap-2 mb-2">
              <div class="flex items-center space-x-2">
                <span class="text-xl">🤖</span>
                <h3 class="font-bold text-purple-900 text-sm">การวิเคราะห์จากผู้ช่วย AI</h3>
                <span id="badgeMode" class="text-xs px-2.5 py-0.5 rounded-full font-bold"></span>
              </div>
              <span id="latencySpan" class="text-xs text-purple-600 font-mono"></span>
            </div>
            <p id="aiReasoning" class="text-purple-800 text-sm leading-relaxed"></p>
          </div>

          <h3 class="font-extrabold text-lg text-gray-900">หนังสือที่แนะนำสำหรับคุณ:</h3>
          <div id="booksGrid" class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6"></div>
        </div>
      </main>

      <footer class="bg-white border-t py-6 text-center text-xs text-gray-400 mt-auto">
        โครงงานบูรณาการวิศวกรรมซอฟต์แวร์ในยุค AI (Capstone Framework) | ภาควิชาวิศวกรรมคอมพิวเตอร์ มทร.อีสาน ขอนแก่น
      </footer>

      <script>
        function setQuery(text) {
          document.getElementById('userQuery').value = text;
          document.getElementById('aiForm').dispatchEvent(new Event('submit'));
        }

        document.getElementById('aiForm').addEventListener('submit', async (e) => {
          e.preventDefault();
          const query = document.getElementById('userQuery').value.trim();
          if (!query) return;

          const submitBtn = document.getElementById('submitBtn');
          const btnText = document.getElementById('btnText');
          const btnSpinner = document.getElementById('btnSpinner');
          const resultContainer = document.getElementById('resultContainer');
          const booksGrid = document.getElementById('booksGrid');
          const aiReasoning = document.getElementById('aiReasoning');
          const badgeMode = document.getElementById('badgeMode');
          const latencySpan = document.getElementById('latencySpan');

          submitBtn.disabled = true;
          btnText.textContent = 'กำลังคิด...';
          btnSpinner.classList.remove('hidden');

          try {
            const res = await fetch('/ai/recommend', {
              method: 'POST',
              headers: { 'Content-Type': 'application/json' },
              body: JSON.stringify({ query })
            });

            const data = await res.json();
            if (!data.success) throw new Error(data.error || 'ประมวลผลล้มเหลว');

            aiReasoning.textContent = data.reasoning;
            latencySpan.textContent = '⏱️ ' + data.latency_ms + ' ms';

            if (data.mode === 'ai') {
              badgeMode.className = 'bg-emerald-100 text-emerald-800 text-xs px-2.5 py-0.5 rounded-full font-bold';
              badgeMode.textContent = 'Gemini AI Mode';
            } else {
              badgeMode.className = 'bg-amber-100 text-amber-800 text-xs px-2.5 py-0.5 rounded-full font-bold';
              badgeMode.textContent = 'Fallback Mode (ระบบสำรอง)';
            }

            booksGrid.innerHTML = '';
            if (data.books.length === 0) {
              booksGrid.innerHTML = '<div class="col-span-full bg-white p-6 rounded-xl border text-center text-gray-500">ไม่พบหนังสือที่ตรงกับคำขอนี้ กรุณาลองสอบถามด้วยคำอธิบายอื่น</div>';
            } else {
              data.books.forEach(b => {
                const card = document.createElement('div');
                card.className = 'bg-white border rounded-2xl p-5 shadow-sm hover:shadow-md transition flex flex-col justify-between';
                card.innerHTML = \`
                  <div>
                    <span class="bg-blue-50 text-blue-700 text-xs px-2.5 py-1 rounded-full font-semibold">\${b.category_name}</span>
                    <h4 class="font-bold text-gray-900 mt-2 text-base leading-snug">\${b.title}</h4>
                    <p class="text-xs text-gray-500 mb-2">โดย \${b.author_name}</p>
                    <p class="text-xs text-gray-600 line-clamp-2 leading-relaxed mb-4">\${b.description || ''}</p>
                  </div>
                  <div class="border-t pt-3 flex justify-between items-center">
                    <span class="text-lg font-black text-blue-600">\${Number(b.price).toLocaleString()} ฿</span>
                    <form method="POST" action="/cart/add">
                      <input type="hidden" name="ebook_id" value="\${b.ebook_id}">
                      <button type="submit" class="bg-blue-600 hover:bg-blue-700 text-white text-xs px-3.5 py-2 rounded-xl font-semibold transition shadow-sm">
                        🛒 ใส่ตะกร้า
                      </button>
                    </form>
                  </div>
                \`;
                booksGrid.appendChild(card);
              });
            }

            resultContainer.classList.remove('hidden');
          } catch (err) {
            alert('เกิดข้อผิดพลาด: ' + err.message);
          } finally {
            submitBtn.disabled = false;
            btnText.textContent = '🪄 ขอคำแนะนำ AI';
            btnSpinner.classList.add('hidden');
          }
        });
      </script>
    </body>
    </html>
  `);
});

// ----------------------------------------------------
// 2. REST API: /ai/recommend
// ----------------------------------------------------
router.post('/recommend', async (req, res) => {
  const { query, promptVersion, forceFallback } = req.body;
  if (!query || typeof query !== 'string') {
    return res.status(400).json({ success: false, error: 'กรุณาระบุคำค้นหา (query)' });
  }

  try {
    const result = await recommendBooks(query, {
      promptVersion: promptVersion || 'v2',
      forceFallback: Boolean(forceFallback)
    });
    res.json(result);
  } catch (err) {
    res.status(500).json({ success: false, error: err.message });
  }
});

module.exports = router;
