# 🤖 บันทึกการใช้งานปัญญาประดิษฐ์ในการพัฒนา (AI Use Disclosure Log)

**โครงงาน**: ระบบร้านขายหนังสือและอีบุ๊กออนไลน์ (E-Book Store Online Management System)  
**วิชา**: วิศวกรรมซอฟต์แวร์ในยุค AI (Software Engineering in AI Era)  
**มาตรฐานอ้างอิง**: AI Use Disclosure Guidelines (บทที่ 1 §1.5, บทที่ 14 §14.4.14)

---

## 1. นโยบายและเครื่องมือ AI ที่ใช้ในโครงการ (Tools & Policies)

* **เครื่องมือหลักที่ใช้งาน**:
  1. Google Antigravity & Gemini CLI Assistant (สำหรับ Pair Programming, สถาปัตยกรรม และการจัดโครงสร้าง)
  2. GitHub Copilot / Cursor (สำหรับการ Generate โครงร่างโค้ด Boilerplate และ Unit Test Scaffolding)
  3. Claude 3.5 Sonnet / ChatGPT 4o (สำหรับการตรวจสอบโค้ดแบบ Three-layer Review และช่วยร่าง Golden Dataset)
* **ระดับความไว้วางใจในการทำงาน (Trust Level Breakdown)**:
  * **Level 1 (Human-in-control)**: สถาปัตยกรรมระบบ, โครงสร้าง ERD, กฎความปลอดภัย Access Control, และ Ethics Review
  * **Level 2 (Co-pilot / Suggestion)**: การเขียนคำสั่ง SQL Aggregate รายงาน, การเขียนฟังก์ชันช่วยแปลงเวลา Timezone, และการปรับแต่งสไตล์ Tailwind
  * **Level 3 (Automated Assist)**: การสร้าง Mock Data (`seed.sql`), การร่างคำถามทดสอบสำหรับ Eval Golden Dataset (ผ่านการคัดกรองโดยมนุษย์)

---

## 2. บันทึกการใช้งาน AI รายช่วงการพัฒนา (Phase-by-Phase Log)

### ช่วงที่ 1: Requirements Engineering & Spec-Driven Design (สัปดาห์ 3-4)

* **งานที่ใช้ AI**:
  * ช่วยร่างรายการ User Stories จาก Pain Point ของร้านค้า E-Book ดั้งเดิม
  * ช่วยจัดหมวดหมู่ความต้องการตาม FURPS+ Framework
* **Prompt ตัวอย่างที่ใช้**:
  > *"จาก Pain Point ของร้านขายหนังสือดิจิทัลที่มีปัญหาเรื่องลูกค้าเข้าถึงไฟล์ได้โดยไม่ได้จ่ายเงิน และราคาในอดีตเปลี่ยนเมื่อร้านลดราคา จงร่าง User Stories 10 ข้อในรูปแบบ As a... I want to... So that... พร้อมระบุ Acceptance Criteria แบบ Given-When-Then"*
* **สิ่งที่ทีมตรวจทานและแก้ไข (Human Override)**:
  * AI เสนอฟังก์ชัน "การรีวิวหนังสือพร้อมให้ดาว" และ "ระบบแจ้งเตือนทาง SMS" ทีมตัดสินใจ **ตัดออก (Out of Scope)** เพราะทำให้ขอบเขตงานบานปลาย (Scope Creep) เกินกว่าระยะเวลา 1 เทอม
  * AI ลืมกำหนดเงื่อนไขว่าเมื่อผู้ใช้ไม่ใช่เจ้าของคำสั่งซื้อต้องส่งกลับรหัส `403 Forbidden` ทีมจึงได้เขียนเพิ่มเติมด้วยตนเอง

---

### ช่วงที่ 2: Architecture & Database Design (สัปดาห์ 7-8)

* **งานที่ใช้ AI**:
  * ช่วยแปลงความต้องการเป็นแผนภาพ Mermaid `erDiagram` และ C4 Container Diagram
  * ช่วยร่างโครงร่างคำสั่ง DDL สร้างตารางบน PostgreSQL
* **Prompt ตัวอย่างที่ใช้**:
  > *"สร้าง Mermaid erDiagram สำหรับระบบร้านค้า E-Book ที่มี 9 ตาราง โดยคำสั่งซื้อต้องเก็บราคา ณ เวลาที่ซื้อแยกจากราคาปัจจุบันของหนังสือ เพื่อรองรับ 3NF"*
* **สิ่งที่ทีมตรวจทานและแก้ไข (Human Override)**:
  * **ปฏิเสธข้อเสนอ AI เรื่องการเก็บราคาใน `order_items`**: AI เสนอให้ใช้ `FOREIGN KEY` อ้างอิงราคาจากตาราง `books` โดยตรงเพื่อความกระชับ แต่ทีม **ปฏิเสธและยืนยันเพิ่มฟิลด์ `price_at_purchase`** เพื่อทำ Snapshot Price ป้องกันปัญหายอดขายในอดีตเปลี่ยนแปลง
  * **ปฏิเสธการใช้ Type `FLOAT`**: AI ใส่ชนิดข้อมูลราคาเป็น `FLOAT` ทีมสั่งแก้ไขให้เป็น `DECIMAL(10,2)` ทั้งหมด เพื่อป้องกันปัญหา Floating-point Rounding Error

---

### ช่วงที่ 3: Implementation, Tests & AI Evals (สัปดาห์ 11-12)

* **งานที่ใช้ AI**:
  * ช่วยเขียน Boilerplate โค้ดสำหรับเชื่อมต่อฐานข้อมูล และโครงสร้าง Express Route Guard
  * ช่วยสร้าง Test Scaffolding สำหรับ Unit Tests และสร้างชุดทดสอบ Golden Dataset (25 ตัวอย่าง) สำหรับ AI Evals
* **Prompt ตัวอย่างที่ใช้**:
  > *"สร้างชุดทดสอบ 25 ตัวอย่างสำหรับระบบแนะนำหนังสือ E-Book โดยแบ่งเป็น Happy Path 15 ข้อ, Edge Cases 5 ข้อ, และ Adversarial / Prompt Injection 5 ข้อ ในรูปแบบ JSON"*
* **สิ่งที่ทีมตรวจทานและแก้ไข (Human Override)**:
  * **คัดกรองหนังสือที่ไม่มีอยู่จริง**: ในตอนแรก AI สร้างชื่อหนังสือสมมติขึ้นมาเองในคำตอบอ้างอิง ทีมได้ทำการกรองและจับคู่กับ `ebook_id` ที่มีอยู่จริงใน `seed.sql` ของร้านเท่านั้น เพื่อให้เป็น Ground Truth ที่ถูกต้อง 100%
  * **การสร้าง Fallback Chain**: AI เสนอให้โยน Error 500 กลับไปหาผู้ใช้เมื่อ API ขัดข้อง ทีมเขียนโค้ดเพิ่มในส่วน Catch Block ให้เรียก Rule-based Engine แนะนำหนังสือยอดนิยมแทน ทำให้ระบบไม่ล่ม

---

### ช่วงที่ 4: Production, Observability & Ethics Review (สัปดาห์ 14-15)

* **งานที่ใช้ AI**:
  * ช่วยร่าง Incident Runbook ขั้นตอนการแก้ปัญหาเมื่อ Database Connection เต็ม
  * ช่วยตรวจสอบรูปแบบการเขียน UTF-8 BOM สำหรับการ Export CSV ภาษาไทย
* **Prompt ตัวอย่างที่ใช้**:
  > *"อธิบายขั้นตอนการฝัง UTF-8 BOM ใน Node.js เมื่อส่งออก CSV response เพื่อให้เปิดใน Microsoft Excel บน Windows แล้วภาษาไทยไม่เป็นภาษาต่างดาว"*
* **สิ่งที่ทีมตรวจทานและแก้ไข (Human Override)**:
  * **การทำ Ethics Review**: ทีมเป็นผู้ตอบคำถามทั้ง 5 ข้อใน `docs/ethics-review.md` ด้วยตนเองทั้งหมด โดยใช้ AI เพียงเป็นคู่คิดตรวจสอบความครอบคลุมของประเด็น PDPA (มาตรา 24 และ 28) เท่านั้น
  * **การปรับจูน Prompt v1 สู่ v2**: ทีมนำผลลัพธ์จากการรัน Eval Suite ที่พบว่า Prompt v1 ตอบคำถามนอกเรื่องบ่อย มาปรับปรุง System Prompt ด้วยการเพิ่ม Guardrails จนได้คะแนนความแม่นยำสูงขึ้น

---

## 3. สรุปรายการข้อเสนอแนะของ AI ที่ทีมตัดสินใจปฏิเสธ (Rejected AI Proposals)

| หัวข้อ | สิ่งที่ AI แนะนำ | เหตุผลที่ทีมตัดสินใจปฏิเสธ (Rationale) | การตัดสินใจสุดท้ายของทีม |
| :---: | :--- | :--- | :--- |
| **Data Types** | ใช้ `FLOAT` สำหรับราคาหนังสือ | เลขทศนิยมแบบ Float เกิดข้อผิดพลาดทางคณิตศาสตร์ได้ | ใช้ `DECIMAL(10,2)` ทุกจุด |
| **History Price** | ดึงราคาปัจจุบันจากตาราง `books` ตอนคำนวณยอดขาย | หากร้านปรับราคาในอนาคต ยอดขายย้อนหลังจะเพี้ยน | สร้างฟิลด์ `price_at_purchase` ใน `order_items` |
| **AI Fallback** | ปล่อยให้ฟังก์ชันโยน Exception 500 เมื่อ LLM ล่ม | ทำให้ประสบการณ์ผู้ใช้เสียหาย หน้าเว็บค้าง | เขียน Graceful Fallback สลับไปใช้ Category Matching |
| **Access Control** | ซ่อนปุ่มดาวน์โหลดที่หน้าเว็บอย่างเดียว | ผู้ใช้สามารถยิง URL `/download/:id` ได้ตรง ๆ (IDOR) | ตรวจสอบสิทธิ์ซ้ำที่ระดับ SQL ก่อนส่งไฟล์ |
| **Authentication** | ใช้ Firebase Auth ภายนอก | ซับซ้อนและอยู่นอกเหนือวัตถุประสงค์การเรียนรู้ RDBMS | พัฒนา Session Auth และตาราง `users` ด้วยตนเอง |
