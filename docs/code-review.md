# 🔍 บันทึกการตรวจสอบโค้ดแบบสามชั้น (Three-Layer Code Review Log)

**โครงงาน**: ระบบร้านขายหนังสือและอีบุ๊กออนไลน์ (E-Book Store Online Management System)  
**วิชา**: วิศวกรรมซอฟต์แวร์ในยุค AI (Software Engineering in AI Era)  
**มาตรฐานอ้างอิง**: Three-Layer Code Review Workflow (บทที่ 12 §12.4.3 & §12.4.4)

---

## 1. คำอธิบายแนวคิด Three-Layer Code Review

ทุกการเปลี่ยนแปลงสำคัญในโครงการได้รับการตรวจสอบผ่าน 3 เลเยอร์ตามแนวทางวิศวกรรมซอฟต์แวร์สมัยใหม่:
1. **Layer 1: Self-Review**: ผู้พัฒนาตรวจสอบความสมบูรณ์ของ Diff ของตนเองก่อนเปิด PR
2. **Layer 2: AI Review**: ใช้ AI Assistant ช่วยกวาดหาจุดบกพร่องด้านความปลอดภัย, Boundary Cases, และ Bad Smells
3. **Layer 3: Human Peer Review**: สมาชิกในทีมอ่านและตรวจสอบเชิงธุรกิจ สถาปัตยกรรม และอนุมัติการ Merge

---

## 2. บันทึกการ Review 5 Pull Requests สำคัญ (5 Key PR Logs)

### PR #01: ออกแบบโครงสร้างฐานข้อมูลและ DDL Scripts (`sql/schema.sql`)
* **ผู้พัฒนา (Author)**: นายสุรวัจน์ ชลเรืองทรัพย์ (Tech Lead)
* **ผู้ตรวจสอบ (Reviewer)**: นายสรวิชญ์ มีมาก (Backend Lead)
* **Layer 1 (Self-Review)**: ตรวจสอบตารางครบ 9 ตาราง ตรวจ Primary Key และ Foreign Key
* **Layer 2 (AI Review Feedback)**: 
  * AI ทักท้วง: *"ตาราง `order_items` ควรเก็บ `price_at_purchase` แยก เพื่อป้องกันปัญหายอดขายย้อนหลังเปลี่ยน และราคาหนังสือควรใช้ `DECIMAL(10,2)` แทน `FLOAT`"*
* **Layer 3 (Human Review & Action Taken)**: 
  * นายสรวิชญ์เห็นชอบกับข้อทักท้วง จึงเพิ่มฟิลด์ `price_at_purchase` และเปลี่ยนชนิดข้อมูลตามที่ AI แนะนำ ก่อนอนุมัติ Merge

---

### PR #02: พัฒนาระบบ Transactional Checkout (`routes/shop.js`)
* **ผู้พัฒนา (Author)**: นายสุรวัจน์ ชลเรืองทรัพย์
* **ผู้ตรวจสอบ (Reviewer)**: นายสรวิชญ์ มีมาก
* **Layer 1 (Self-Review)**: เขียน `BEGIN`, `COMMIT`, และ `ROLLBACK` ครอบคลุมการสร้าง Order และล้าง Cart
* **Layer 2 (AI Review Feedback)**: 
  * AI ทักท้วง: *"พบความเสี่ยง Connection Leak หากเกิด Exception ภายใน Transaction แล้วไม่ได้ปล่อย `client.release()` กลับคืนสู่ Pool"*
* **Layer 3 (Human Review & Action Taken)**: 
  * ผู้พัฒนาแก้ไขโดยเพิ่มบล็อก `finally { client.release(); }` เพื่อรับประกันว่า Connection จะถูกปิดเสมอไม่ว่าจะสำเร็จหรือล้มเหลว ตรวจสอบผ่านแล้วจึง Merge

---

### PR #03: กลไกควบคุมสิทธิ์การดาวน์โหลดไฟล์ดิจิทัล (`services/accessControl.js`)
* **ผู้พัฒนา (Author)**: นายสรวิชญ์ มีมาก (Security Lead)
* **ผู้ตรวจสอบ (Reviewer)**: นายสุรวัจน์ ชลเรืองทรัพย์
* **Layer 1 (Self-Review)**: สร้างฟังก์ชัน `getDownloadLinks` ตรวจสอบสถานะ `confirmed`
* **Layer 2 (AI Review Feedback)**: 
  * AI ทักท้วง: *"ระวังช่องโหว่ IDOR หากตรวจสอบเพียงสถานะคำสั่งซื้อ แต่ไม่ได้ตรวจสอบว่า `order.user_id` ตรงกับ `requester_id` หรือไม่ ผู้ใช้อื่นอาจสวมรอยขอลิงก์ได้"*
* **Layer 3 (Human Review & Action Taken)**: 
  * นายสรวิชญ์ได้เพิ่มเงื่อนไข `if (order.user_id !== requesterId) return [];` และเขียน Unit Test ดักจับกรณี IDOR Attack (TC-04) จนผ่าน 100% จึง Merge

---

### PR #04: บูรณาการระบบ AI Bookstore Assistant และ Graceful Fallback (`services/aiService.js`)
* **ผู้พัฒนา (Author)**: นายสุรวัจน์ ชลเรืองทรัพย์ (AI Engineer)
* **ผู้ตรวจสอบ (Reviewer)**: นายสรวิชญ์ มีมาก (QA Lead)
* **Layer 1 (Self-Review)**: เขียนการเรียก Gemini API และแปลงผลลัพธ์เป็น JSON
* **Layer 2 (AI Review Feedback)**: 
  * AI ทักท้วง: *"LLM อาจเกิด Hallucination คืนรหัสหนังสือที่ไม่มีอยู่จริงในร้านค้า และหาก API หมดโควตาจะเกิด Unhandled Rejection หน้าเว็บจะค้าง"*
* **Layer 3 (Human Review & Action Taken)**: 
  * ผู้พัฒนาสร้าง Catalog Whitelist Filter เพื่อตัดรหัสแปลกปลอมออก และพัฒนา Rule-based Fallback Engine ในบล็อก `catch` พร้อมตั้ง Timeout 3,000ms ตรวจสอบเสร็จสิ้นจึง Merge

---

### PR #05: การปรับปรุงการส่งออกรายงาน CSV มาตรฐานภาษาไทย (`routes/reports.js`)
* **ผู้พัฒนา (Author)**: นายสรวิชญ์ มีมาก
* **ผู้ตรวจสอบ (Reviewer)**: นายสุรวัจน์ ชลเรืองทรัพย์
* **Layer 1 (Self-Review)**: เขียน Query ดึงสถิติ 4 ด้าน และสร้าง CSV String
* **Layer 2 (AI Review Feedback)**: 
  * AI ทักท้วง: *"หากเปิดไฟล์ CSV บน Microsoft Excel ของผู้ใช้ Windows ภาษาไทยจะกลายเป็นตัวอักษรต่างดาว (Mojibake) เนื่องจากขาดการประกาศ BOM"*
* **Layer 3 (Human Review & Action Taken)**: 
  * ผู้พัฒนาแก้ไขโดยส่งรหัส `\uFEFF` (UTF-8 Byte Order Mark) นำหน้าเนื้อหา CSV และกำหนด Header `Content-Type: text/csv; charset=utf-8` ทดสอบเปิดบน Excel สำเร็จ ภาษาไทยถูกต้อง จึงอนุมัติ Merge
