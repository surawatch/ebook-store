# 📘 เอกสารสรุปสารบัญโครงงาน (Capstone Project Submission Index)

---

<div align="center">

# โครงงานพัฒนาระบบร้านขายหนังสือและอีบุ๊กออนไลน์
## (E-Book Store Online Management System with AI Bookstore Assistant)

**โครงงานบูรณาการตลอดภาคการศึกษา (Capstone Project - 20 คะแนน)**  
**รายวิชาวิศวกรรมซอฟต์แวร์ในยุค AI (Software Engineering in AI Era)**  
สาขาวิชาวิศวกรรมคอมพิวเตอร์ คณะวิศวกรรมศาสตร์ มหาวิทยาลัยเทคโนโลยีราชมงคลอีสาน วิทยาเขตขอนแก่น

---

### ข้อมูลสมาชิกกลุ่มผู้จัดทำโครงงาน (Team Members)

| ลำดับ | ชื่อ-นามสกุล | รหัสนักศึกษา | บทบาทหน้าที่ในโครงงาน (Roles) | ความรับผิดชอบหลัก |
| :---: | :--- | :---: | :--- | :--- |
| **คนที่ 1** | **นายสุรวัจน์ ชลเรืองทรัพย์** | **67332110217-1** | **Tech Lead / Architect & AI Engineer** | ออกแบบสถาปัตยกรรมระบบและฐานข้อมูล, พัฒนาระบบหน้าร้าน, ตะกร้าสินค้า, Transactional Checkout, พัฒนาโมดูล AI Assistant และ Fallback Chain |
| **คนที่ 2** | **นายสรวิชญ์ มีมาก** | **67332110275-8** | **Backend & Security Lead & QA Lead** | ออกแบบระบบรักษาความปลอดภัย (RBAC & Route Guard), กลไกควบคุมการเข้าถึงไฟล์ดิจิทัล (Anti-IDOR), พัฒนา Unit Tests, AI Evals, และรายงานสถิติ |

</div>

---

## 🗺️ 1. แผนที่ระบุตำแหน่งชิ้นงานทั้งหมดในโครงงาน (Artifact Location Map)

ตารางด้านล่างนี้รวบรวมชิ้นงานและเอกสารสำคัญทั้งหมดของโครงงาน เพื่อความสะดวกในการตรวจประเมินตามกรอบ [Capstone Framework](https://ecp-rmuti.gitbook.io/software-engineering-in-ai-era/capstone/capstone-framework):

| หมวดหมู่ของชิ้นงาน | รายการเอกสาร / ชิ้นงาน | ตำแหน่งไฟล์ใน Repository (Clickable Link) | วัตถุประสงค์และสาระสำคัญ |
| :--- | :--- | :--- | :--- |
| **ภาพรวมโครงการ** | **README** | [`README.md`](file:///c:/Users/Lenovo/ebook-store/README.md) | ที่มาของปัญหา, Stakeholders, ขอบเขต In/Out, สถาปัตยกรรม, และคำสั่งติดตั้งระบบ |
| **ช่วงที่ 1: ความต้องการ** | **Requirements Spec** | [`requirements.md`](file:///c:/Users/Lenovo/ebook-store/requirements.md) | User Stories 12 ข้อ, Acceptance Criteria (Given-When-Then), FURPS+, 4 NFRs สำหรับ AI |
|  | **Tech Stack Decision** | [`tech-stack.md`](file:///c:/Users/Lenovo/ebook-store/tech-stack.md) | ชุดเทคโนโลยีที่เลือก (Node.js, Postgres Neon, Gemini) และรายการทางเลือกที่พิจารณาแล้วปฏิเสธ |
|  | **Team Charter** | [`team-charter.md`](file:///c:/Users/Lenovo/ebook-store/team-charter.md) | บทบาทสมาชิก, ช่องทางสื่อสาร, ข้อตกลงการทำงาน, Definition of Done, และนโยบายการใช้ AI |
|  | **AI Use Disclosure** | [`AI_USE_LOG.md`](file:///c:/Users/Lenovo/ebook-store/AI_USE_LOG.md) | บันทึกการใช้งาน AI ทุกช่วง, Trust Levels, ข้อเสนอที่มนุษย์ปฏิเสธ/แก้ไข (Rejected Proposals) |
|  | **PR Standards** | [`.github/PULL_REQUEST_TEMPLATE.md`](file:///c:/Users/Lenovo/ebook-store/.github/PULL_REQUEST_TEMPLATE.md) | แบบฟอร์มมาตรฐานสำหรับ Pull Request ที่บังคับระบุ AI Use Note และ Three-Layer Review |
| **ช่วงที่ 2: สถาปัตยกรรม** | **Architecture Model** | [`architecture.md`](file:///c:/Users/Lenovo/ebook-store/architecture.md) | C4 Model (Context, Container, Component), Decision Tree (เมื่อใดใช้ AI vs Rule), Fallback Strategy |
|  | **ADR 001** | [`adr/ADR-001-backend-framework.md`](file:///c:/Users/Lenovo/ebook-store/adr/ADR-001-backend-framework.md) | บันทึกการตัดสินใจเลือกใช้ Node.js และ Express.js |
|  | **ADR 002** | [`adr/ADR-002-database-cloud.md`](file:///c:/Users/Lenovo/ebook-store/adr/ADR-002-database-cloud.md) | บันทึกการตัดสินใจเลือกใช้ PostgreSQL บน Neon Cloud Serverless |
|  | **ADR 003** | [`adr/ADR-003-ai-book-recommendation-assistant.md`](file:///c:/Users/Lenovo/ebook-store/adr/ADR-003-ai-book-recommendation-assistant.md) | บันทึกการตัดสินใจเลือกใช้ Hybrid Gemini API + Local Fallback Rule Engine |
|  | **ADR 004** | [`adr/ADR-004-deployment-platform.md`](file:///c:/Users/Lenovo/ebook-store/adr/ADR-004-deployment-platform.md) | บันทึกการตัดสินใจเลือกใช้แพลตฟอร์มคลาวด์ Vercel / Render |
|  | **Sprint Retrospective** | [`docs/retrospective.md`](file:///c:/Users/Lenovo/ebook-store/docs/retrospective.md) | บันทึกผลการทบทวนกระบวนการทำงาน Sprint 1-2 และ Sprint 3-4 พร้อม Action Items ที่ทำจริง |
| **ช่วงที่ 3: โค้ด & การทดสอบ** | **AI Assistant Service** | [`services/aiService.js`](file:///c:/Users/Lenovo/ebook-store/services/aiService.js) | โมดูลแนะนำหนังสือด้วยภาษาธรรมชาติ, Context Builder, Fallback Engine, และตัวกรอง Zero-Hallucination |
|  | **AI Routes & UI** | [`routes/ai.js`](file:///c:/Users/Lenovo/ebook-store/routes/ai.js) | หน้าจอเว็บผู้ช่วย AI (`/ai`) และ REST API (`/ai/recommend`) พร้อมตัวจับเวลา Latency |
|  | **Access Control Logic** | [`services/accessControl.js`](file:///c:/Users/Lenovo/ebook-store/services/accessControl.js) | ฟังก์ชันตรวจสิทธิ์การเข้าถึงไฟล์ดิจิทัล (อนุญาตเฉพาะสถานะ `confirmed` + ผู้ใช้เป็นเจ้าของ) |
|  | **Python Logic** | [`access.py`](file:///c:/Users/Lenovo/ebook-store/access.py) | โค้ด Python สำหรับตรวจสิทธิ์ตามใบความรู้เสริม Capstone ร้านขายหนังสือดิจิทัล |
|  | **Unit Tests (Node.js)** | [`tests/download_access.test.js`](file:///c:/Users/Lenovo/ebook-store/tests/download_access.test.js)<br>[`tests/ai_service.test.js`](file:///c:/Users/Lenovo/ebook-store/tests/ai_service.test.js) | ชุดทดสอบ Unit Tests ด้วย Node.js Built-in Runner (TC-01 ถึง TC-05 และ TC-AI-01 ถึง 05) ผ่าน 100% |
|  | **Unit Tests (Python)** | [`tests/test_download_access.py`](file:///c:/Users/Lenovo/ebook-store/tests/test_download_access.py) | ชุดทดสอบ Python ด้วย unittest / pytest ตามคู่มือวิชา ผ่าน 100% |
|  | **Golden Dataset** | [`evals/golden_dataset.json`](file:///c:/Users/Lenovo/ebook-store/evals/golden_dataset.json) | ชุดทดสอบประเมินผล AI 25 ข้อ (Happy Path 15 ข้อ, Edge Cases 5 ข้อ, Adversarial Injections 5 ข้อ) |
|  | **AI Eval Runner** | [`evals/eval_runner.js`](file:///c:/Users/Lenovo/ebook-store/evals/eval_runner.js) | สคริปต์รันประเมินผล AI อัตโนมัติ เปรียบเทียบ Prompt v1 vs Prompt v2 |
|  | **Eval Results Report** | [`evals/eval_results.md`](file:///c:/Users/Lenovo/ebook-store/evals/eval_results.md) | รายงานผลการประเมิน AI: ความแม่นยำ 84.0%, Zero Hallucination 100%, ป้องกัน Injection 100% |
|  | **Code Review Log** | [`docs/code-review.md`](file:///c:/Users/Lenovo/ebook-store/docs/code-review.md) | บันทึกการทำ Three-Layer Code Review (Self + AI + Peer) ของ 5 PR สำคัญ |
| **ช่วงที่ 4: ความปลอดภัย & Production** | **Observability Dashboard** | [`observability/dashboard.md`](file:///c:/Users/Lenovo/ebook-store/observability/dashboard.md) | บันทึกสถิติ Latency p50 (260ms), p95 (264ms), p99, Error Rate 0%, ค่าใช้จ่าย $0, และ 10 Traces |
|  | **Observability Logger** | [`observability/logger.js`](file:///c:/Users/Lenovo/ebook-store/observability/logger.js) | มิดเดิลแวร์และฟังก์ชันบันทึก Traces, Tokens, Latency และคำนวณ Metrics |
|  | **Ethics & Safety Review** | [`docs/ethics-review.md`](file:///c:/Users/Lenovo/ebook-store/docs/ethics-review.md) | ตอบคำถามจริยธรรม 5 ข้อ, 10-Item Checklist, PDPA (มาตรา 24/28), และฟีเจอร์ที่ไม่ทำ |
|  | **Incident Runbook** | [`docs/runbook.md`](file:///c:/Users/Lenovo/ebook-store/docs/runbook.md) | คู่มือรับมือเหตุการณ์ฉุกเฉิน 4 สถานการณ์ (AI Outage, DB Pool Full, Hallucination, IDOR Breach) |
| **ฐานข้อมูล (Database)** | **Database Scope** | [`docs/scope.md`](file:///c:/Users/Lenovo/ebook-store/docs/scope.md) | ขอบเขตฐานข้อมูล กฎลิงก์ดาวน์โหลด และสิ่งที่ตัดสินแล้ว 3 ข้อตามใบความรู้เสริม |
|  | **Mermaid ERD** | [`docs/erd.md`](file:///c:/Users/Lenovo/ebook-store/docs/erd.md) | แผนภาพ ERD 9 ตารางแบบ Mermaid และคำอธิบายความสัมพันธ์ 3NF |
|  | **DDL Schema Script** | [`sql/schema.sql`](file:///c:/Users/Lenovo/ebook-store/sql/schema.sql) / [`sql/01_schema.sql`](file:///c:/Users/Lenovo/ebook-store/sql/01_schema.sql) | คำสั่ง SQL สร้าง 9 ตาราง พร้อม Integrity Constraints และ Foreign Keys |
|  | **Seed Data Script** | [`sql/seed.sql`](file:///c:/Users/Lenovo/ebook-store/sql/seed.sql) / [`sql/02_seed.sql`](file:///c:/Users/Lenovo/ebook-store/sql/02_seed.sql) | ข้อมูลทดสอบระบบจริง 35 คำสั่งซื้อ (Orders) และ 54 รายการย่อย (Order Items) |
|  | **Analytics Queries** | [`sql/reports.sql`](file:///c:/Users/Lenovo/ebook-store/sql/reports.sql) / [`sql/03_reports.sql`](file:///c:/Users/Lenovo/ebook-store/sql/03_reports.sql) | SQL Aggregate Queries รายงาน 4 ด้าน พร้อมจัดการ Fan-out และ Timezone ไทย |

---

## 💡 2. จุดเด่นการบูรณาการทางวิศวกรรมซอฟต์แวร์ (Engineering Highlights)

ระบบ E-Book Store นี้สร้างขึ้นตามสถาปัตยกรรมแบบ **Hybrid Software Engineering** ที่ผสานรากฐานคลาสสิกเข้ากับวิศวกรรม AI สมัยใหม่:

1. **Classical SE & Database Foundations**:
   * โครงสร้างฐานข้อมูลสอดคล้องตามเกณฑ์ **3NF ครบ 9 ตาราง** ปราศจากความซ้ำซ้อน
   * การบันทึกราคาซื้อขายประวัติศาสตร์ (**Snapshot Price** ผ่าน `price_at_purchase` ใน `order_items`) ทำให้ยอดขายในอดีตไม่ผันผวนเมื่อราคาสินค้าปัจจุบันเปลี่ยนแปลง
   * กระบวนการสั่งซื้อทำงานภายใต้ **Database Transaction (`BEGIN / COMMIT / ROLLBACK`)** เพื่อรับประกันความถูกต้องสมบูรณ์ของข้อมูล (ACID)
   * การส่งออกรายงาน CSV รองรับภาษาไทยสมบูรณ์แบบด้วยการฝังรหัส **UTF-8 BOM (`\uFEFF`)** เปิดอ่านใน Microsoft Excel ได้โดยตรง
2. **Security & Access Control (OWASP Top 10 Mitigation)**:
   * **Anti-IDOR Digital Asset Protection**: การเข้าถึงไฟล์ดิจิทัลผ่าน URL `/download/:ebookId` มีการตรวจสอบสิทธิ์ซ้ำซ้อนสองชั้น (Defense in Depth) ทั้งสถานะคำสั่งซื้อต้องเป็น `confirmed` และผู้ขอต้องเป็นเจ้าของคำสั่งซื้อนั้นจริง หากไม่ตรงเงื่อนไขจะส่งกลับรหัส `403 Forbidden`
   * **Route Guard & RBAC**: แบ่งแยกสิทธิ์ระหว่างผู้ใช้ทั่วไป (`customer`) และผู้ดูแลระบบ (`admin`) ป้องกันการพิมพ์ URL แอบเข้าหน้าหลังบ้าน
3. **AI Engineering & LLMOps**:
   * **Semantic Recommender Engine**: ช่วยแนะนำหนังสือด้วยความเข้าใจภาษาธรรมชาติและเจตนาของผู้ใช้ (User Intent)
   * **3-Stage Graceful Fallback Chain**: มีระบบสำรองอัจฉริยะ (Rule-Based SQL Category Matching) ที่ทำงานอัตโนมัติเมื่อบริการ AI ภายนอกขัดข้อง รับประกัน **High Availability 100%**
   * **Zero-Hallucination Filter**: ตัวกรองรหัสหนังสือในระดับโค้ดที่ตรวจสอบกับแคตตาล็อกจริง ป้องกันไม่ให้ AI กุชื่อหนังสือหรือข้อมูลเท็จ
   * **AI Regression Evaluation Suite**: ชุดประเมินผลอัตโนมัติจำนวน 25 ข้อ พร้อมรายงานเปรียบเทียบ Prompt v1 vs v2
   * **Observability Logging**: บันทึกและคำนวณค่า Latency (p50, p95, p99), Error Rate, Token Usage, และต้นทุนต่อคำขออย่างเป็นระบบ

---

## 🧪 3. สรุปผลการทดสอบระบบ (Testing & Verification Summary)

* **Unit Tests (Node.js Test Runner)**:
  * จำนวนการทดสอบ: **10 Tests** (Access Control 5 ข้อ, AI & Fallback Service 5 ข้อ)
  * ผลลัพธ์: **ผ่าน 10 ข้อ (100% Pass Rate)**, 0 Failures, 0 Crashes
* **Unit Tests (Python Runner)**:
  * จำนวนการทดสอบ: **3 Tests** (`tests/test_download_access.py`)
  * ผลลัพธ์: **ผ่านครบ 3 ข้อ (100% Pass Rate)**
* **AI Evals Suite (Golden Dataset 25 ข้อ)**:
  * ความแม่นยำ (Accuracy): **84.0%** (21/25 ข้อ)
  * อัตราการเกิด Hallucination: **0 เล่ม (0% Hallucination Rate)**
  * ความปลอดภัยจากการโจมตี (Adversarial Resistance): **5/5 (ผ่าน 100%)**
  * เวลาตอบสนองเฉลี่ย (Average Latency): **260.3 ms** (สอดคล้องตาม NFR p95 ≤ 2,500ms)

---

## 🚀 4. คำสั่งสำหรับรันและทดสอบระบบ (Quick Execution Commands)

```bash
# 1. ติดตั้ง Dependencies
npm install

# 2. รันชุดทดสอบ Unit Tests ของระบบ
node --test

# 3. รันชุดทดสอบความปลอดภัยฝั่ง Python
python -m unittest tests/test_download_access.py

# 4. รันชุดประเมินผล AI Regression Evals
node evals/eval_runner.js

# 5. เปิดใช้งานเซิร์ฟเวอร์
node server.js
# เข้าใช้งานเว็บได้ที่ http://localhost:3000
# เข้าใช้งานผู้ช่วย AI ได้ที่ http://localhost:3000/ai
# เข้าดูรายงานวิเคราะห์ยอดขายได้ที่ http://localhost:3000/reports
```

---
*เอกสารฉบับนี้จัดทำขึ้นเพื่อใช้เป็นสารบัญหลักในการส่งโครงงาน Capstone รายวิชาวิศวกรรมซอฟต์แวร์ในยุค AI (Software Engineering in AI Era)*
