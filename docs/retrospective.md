# 🔄 รายงานการทบทวนกระบวนการทำงาน (Sprint Retrospectives)

**โครงงาน**: ระบบร้านขายหนังสือและอีบุ๊กออนไลน์ (E-Book Store Online Management System)  
**วิชา**: วิศวกรรมซอฟต์แวร์ในยุค AI (Software Engineering in AI Era)  
**มาตรฐานอ้างอิง**: Agile / Scrum Retrospective Workflow (บทที่ 2 §2.4)

---

## 1. บันทึกผลการทบทวน Sprint 1-2: สัปดาห์ที่ 4 ถึง 8 (Inception, Requirements & Architecture)

* **ช่วงเวลา**: สัปดาห์ที่ 4 - 8
* **เป้าหมายของ Sprint**: กำหนดขอบเขตโครงการ, User Stories, ออกแบบ ERD 9 ตาราง, และสร้าง Walking Skeleton ที่ต่อฐานข้อมูล Neon ได้จริง
* **สิ่งที่ทำได้ดี (What Went Well)**:
  * การตัดสินใจใช้ Neon Serverless Cloud ช่วยให้สมาชิกในทีมเข้าถึงข้อมูลจริงชุดเดียวกันโดยไม่ต้องเสียเวลาติดตั้ง DB บนเครื่อง
  * การใช้ Mermaid ในการวาด ERD ทำให้สามารถปรับแก้ความสัมพันธ์ของตารางผ่าน Git ได้อย่างรวดเร็ว
  * การจัดทำ ADR ช่วยให้ทีมมีหลักฐานและเหตุผลที่ชัดเจนในการตัดสินใจเลือก Stack
* **ปัญหาและอุปสรรคที่พบ (What Could Be Improved)**:
  * ในตอนแรกทีมเกือบหลงไปทำฟีเจอร์ "รีวิวหนังสือและตัดเงินผ่านบัตรเครดิตจริง" ซึ่งเสี่ยงต่อการเกิด Scope Creep จนงานไม่ทัน
  * ฐานข้อมูล Neon มีการ Sleep (Cold Start) ในครั้งแรกของการเปิดเว็บ ทำให้คิดว่าโค้ดมีบั๊ก
* **มาตรการปรับปรุงใน Sprint ถัดไป (Action Items)**:
  1. ตรึงขอบเขต (Scope Freeze) โดยเขียนหัวข้อ "อยู่นอกขอบเขต (Out of Scope)" ให้ชัดเจนใน `requirements.md`
  2. เพิ่มข้อความแจ้งเตือนผู้ใช้ในหน้าเว็บและเอกสารตรวจงานเรื่อง Cold Start 2-3 วินาที

---

## 2. บันทึกผลการทบทวน Sprint 3-4: สัปดาห์ที่ 9 ถึง 14 (Implementation, Tests, AI Evals & Production)

* **ช่วงเวลา**: สัปดาห์ที่ 9 - 14
* **เป้าหมายของ Sprint**: พัฒนาระบบร้านค้าครบวงจร, ระบบ Transactional Checkout, กลไก Access Control, บูรณาการ AI Bookstore Assistant, รันชุดทดสอบ Unit Tests และ AI Evals
* **สิ่งที่ทำได้ดี (What Went Well)**:
  * การออกแบบฟังก์ชัน `getDownloadLinks` ให้แยกจาก Express ทำให้สามารถรัน Unit Test ได้อย่างรวดเร็วทั้งด้วย Node.js Built-in Test Runner และ Python Pytest
  * การสร้าง Graceful Fallback Engine ช่วยให้ระบบแนะนำหนังสือทำงานได้ 100% แม้ไม่มี API Key หรือเครือข่ายขัดข้อง
  * การรัน Eval Suite ช่วยจับจุดบกพร่องของคำค้นหาแบบ Prompt Injection ได้อย่างชัดเจน
* **ปัญหาและอุปสรรคที่พบ (What Could Be Improved)**:
  * การ Export CSV ภาษาไทยเปิดใน Microsoft Excel แล้วเกิดภาษาต่างดาว (Mojibake) ในช่วงแรก
  * การทดสอบแบบ Async บนฐานข้อมูลจริงบางครั้งปิด Pool ไม่สนิท ทำให้กระบวนการเทสต์ค้าง
* **มาตรการปรับปรุงและการแก้ไขที่ทำจริง (Action Taken & Verified)**:
  1. แก้ไขระบบ Export CSV โดยฝังรหัส **UTF-8 BOM (`\uFEFF`)** นำหน้าไฟล์ ทำให้ Excel เปิดภาษาไทยได้อย่างถูกต้อง 100%
  2. เพิ่ม Hook `after(() => pool.end())` ในชุดทดสอบ ทำให้การรัน Test จบได้อย่างรวดเร็วและสะอาด
