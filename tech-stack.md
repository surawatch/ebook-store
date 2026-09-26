# 🛠️ การตัดสินใจเลือกชุดเทคโนโลยี (Technology Stack Decision)

**โครงงาน**: ระบบร้านขายหนังสือและอีบุ๊กออนไลน์ (E-Book Store Online Management System)  
**วิชา**: วิศวกรรมซอฟต์แวร์ในยุค AI (Software Engineering in AI Era)  
**มาตรฐานอ้างอิง**: Architecture Trade-off Analysis, SE2014 Guidelines

---

## 1. ตารางสรุปชุดเทคโนโลยีที่เลือกใช้ (Selected Stack)

| เลเยอร์ของระบบ (Layer) | เทคโนโลยีที่เลือก (Selected) | เวอร์ชัน | วัตถุประสงค์หลัก |
| :--- | :--- | :--- | :--- |
| **Backend Runtime** | Node.js (JavaScript) | v20+ LTS | สภาพแวดล้อมการทำงานของระบบเซิร์ฟเวอร์แบบ Non-blocking I/O |
| **Web Framework** | Express.js | v5.x | จัดการ Routing, Middleware, และ REST API |
| **Database (RDBMS)** | PostgreSQL (Neon Cloud) | v16+ | จัดเก็บข้อมูลเชิงสัมพันธ์ 9 ตาราง, รองรับ ACID Transaction และ 3NF |
| **Client & UI** | HTML5 + Tailwind CSS (CDN) | v3.x | นำเสนอหน้าจอผู้ใช้แบบ Responsive ที่ทันสมัย รวดเร็ว และเบา |
| **Session Management** | `express-session` | v1.19 | จดจำสถานะผู้ใช้งาน (Authentication State) และควบคุมสิทธิ์ RBAC |
| **AI / LLM Engine** | Google Gemini API (Free Tier) | Gemini 1.5 / 2.5 | วิเคราะห์ความหมายภาษาธรรมชาติและแนะนำหนังสือจากแคตตาล็อก |
| **AI Fallback Engine** | SQL Category & Popularity Engine | Internal | ระบบสำรองข้อมูลกรณีเครือข่าย AI ล่ม (Graceful Degradation) |
| **Testing Framework** | Node.js Native Test Runner / Pytest | v20+ / v3.14 | รัน Unit Tests และ Access Control Verification (AAA Pattern) |
| **Deployment Platform** | Vercel Serverless / Node Container | Cloud | โฮสต์เว็บแอปพลิเคชันที่รองรับ Continuous Deployment จาก GitHub |

---

## 2. เหตุผลการเลือกใช้และทางเลือกอื่นที่พิจารณา (Trade-off Analysis)

### 2.1 Backend Framework: เลือก `Node.js + Express.js`

* **เหตุผลที่เลือก**:
  1. **Asynchronous I/O**: เหมาะกับเว็บแอปพลิเคชัน E-Commerce ที่มีการเรียกฐานข้อมูลและการเชื่อมต่อภายนอก (Neon Postgres, AI API) บ่อยครั้ง
  2. **Ecosystem & Simplicity**: มีแพ็กเกจไดรเวอร์ `pg` และ `@neondatabase/serverless` ที่เสถียร จัดการ Session และ Route Guard ได้กระชับ
  3. **Low Learning Curve**: สมาชิกในทีมมีความคุ้นเคยกับ JavaScript สามารถบูรณาการงานระหว่าง Frontend และ Backend ได้รวดเร็วใน 1 เทอม
* **ทางเลือกอื่นที่พิจารณาและเหตุผลที่ไม่เลือก (Alternatives Considered)**:
  * ❌ *Python (Django / FastAPI)*: แม้จะยอดเยี่ยมสำหรับ AI และ Data Science แต่ Django มีความซับซ้อนของ ORM สูงเกินความจำเป็นสำหรับโครงงานที่ต้องการแสดงทักษะ Raw SQL Queries และ Transaction Management แบบเจาะลึก
  * ❌ *Java (Spring Boot)*: มีความเสถียรและ Enterprise-grade สูงมาก แต่ต้องการทรัพยากรเครื่อง (Memory/CPU) สูง ใช้เวลาพัฒนา (Boilerplate) นาน และใช้เวลา Cold Start บน Free Cloud นานเกินไป

---

### 2.2 Database Platform: เลือก `PostgreSQL บน Neon Cloud Serverless`

* **เหตุผลที่เลือก**:
  1. **Data Integrity & Standard Compliance**: PostgreSQL มีระบบ Constraint (`CHECK`, `FOREIGN KEY ON DELETE RESTRICT`, `TIMESTAMPTZ`) ที่เข้มงวดที่สุดตัวหนึ่งในบรรดา Open-source RDBMS
  2. **Serverless Architecture**: Neon สามารถ Scale-to-zero ได้เมื่อไม่มีผู้ใช้ ทำให้ไม่มีค่าใช้จ่าย และมีฟีเจอร์ Database Branching ที่เหมาะกับการทำ CI/CD
  3. **Native UTF-8 Support**: จัดการข้อมูลภาษาไทยได้อย่างถูกต้อง รวมถึงการทำ Aggregate Queries ร่วมกับ `to_char(created_at AT TIME ZONE 'Asia/Bangkok', 'YYYY-MM')`
* **ทางเลือกอื่นที่พิจารณาและเหตุผลที่ไม่เลือก (Alternatives Considered)**:
  * ❌ *MySQL / MariaDB*: ฟังก์ชันเกี่ยวกับ Timezone และ Date Formatting มีความยุ่งยากกว่า Postgres และตัวแปรชนิด Identity ใน Postgres (`GENERATED ALWAYS AS IDENTITY`) ปลอดภัยกว่า Auto-Increment
  * ❌ *MongoDB (NoSQL Document)*: ไม่ตอบโจทย์ความสัมพันธ์แบบเข้มงวดของระบบ E-Commerce (เช่น ตารางคำสั่งซื้อกับรายการสินค้า Many-to-Many) และไม่สามารถฝึกทักษะการทำ Database Normalization (3NF) ตามวัตถุประสงค์วิชาได้

---

### 2.3 AI Provider & Architecture: เลือก `Hybrid Gemini API + Local Fallback Rule Engine`

* **เหตุผลที่เลือก**:
  1. **Generous Free Tier**: Google Gemini มีโควตา Free Tier ที่เพียงพอสำหรับการทดสอบตลอดเทอม โดยไม่ต้องผูกบัตรเครดิต
  2. **Thai Language Understanding**: โมเดล Gemini มีความเข้าใจบริบทคำศัพท์ภาษาไทยและการจัดหมวดหมู่อย่างเป็นธรรมชาติ
  3. **High Availability via Fallback Chain**: สอดคล้องกับบทเรียนบทที่ 6 §6.3 ระบบต้องไม่ล่มเมื่อ AI Provider มีปัญหา โดยมี Fallback เป็น Rule-based SQL Query แนะนำหนังสือยอดนิยมแทนอัตโนมัติ
* **ทางเลือกอื่นที่พิจารณาและเหตุผลที่ไม่เลือก (Alternatives Considered)**:
  * ❌ *OpenAI GPT-4o*: คุณภาพสูงแต่ไม่มี Free Tier ที่แท้จริง (ต้องเติมเงินขั้นต่ำ $5) ขัดแย้งกับข้อกำหนดด้าน Cost Ceiling ของโครงงานการศึกษา
  * ❌ *Local LLM (Ollama / Llama 3 8B)*: การรัน Local LLM บนเครื่องโน้ตบุ๊กของนักศึกษาต้องการ GPU VRAM ขั้นต่ำ 8GB ทำให้ไม่สามารถการันตีว่าสมาชิกทุกคนในทีมและผู้ตรวจงานจะรันได้เหมือนกัน

---

### 2.4 Frontend & UI: เลือก `Tailwind CSS via CDN + Server-Side Rendered HTML`

* **เหตุผลที่เลือก**:
  1. **Zero Build Step**: การใช้ Tailwind CSS ผ่าน CDN ช่วยตัดขั้นตอนการตั้งค่า Webpack/Vite ที่ซับซ้อน ทำให้แก้ไขโค้ดและรันดูผลได้ทันที
  2. **Fast Delivery & Light Weight**: เรนเดอร์ HTML ออกจาก Express โดยตรง หน้าเว็บโหลดเร็วมาก ใช้หน่วยความจำน้อย ไม่มีปัญหา Hydration Mismatch
  3. **Consistency**: การใช้ Utility-first class ทำให้การตกแต่งปุ่ม สถานะคำสั่งซื้อ (`confirmed`, `pending`, `cancelled`) และข้อความแจ้งเตือนเป็นระเบียบชัดเจน
* **ทางเลือกอื่นที่พิจารณาและเหตุผลที่ไม่เลือก (Alternatives Considered)**:
  * ❌ *React / Next.js (SPA + Client Components)*: การแยกแอปพลิเคชันเป็น Frontend SPA แยกกับ Backend API เพิ่มภาระการจัดการ CORS, JWT Token Refresh และ State Management ซ้ำซ้อน ซึ่งเกินความจำเป็นสำหรับขอบเขตงาน 1 เทอม
