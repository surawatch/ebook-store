# 📚 E-Book Store Online Management System (ระบบร้านขายหนังสือและอีบุ๊กออนไลน์)

[![Node.js CI](https://img.shields.io/badge/Node.js-v20+-green.svg)](https://nodejs.org/)
[![Database](https://img.shields.io/badge/PostgreSQL-Neon%20Serverless-blue.svg)](https://neon.tech/)
[![AI-Integrated](https://img.shields.io/badge/AI-Gemini%20%2F%20Fallback%20Chain-purple.svg)]()
[![SE-Framework](https://img.shields.io/badge/SE%20in%20AI%20Era-Capstone%20Ready-orange.svg)](https://ecp-rmuti.gitbook.io/software-engineering-in-ai-era/capstone/capstone-framework)

> โครงงานบูรณาการวิศวกรรมซอฟต์แวร์ยุค AI (Software Engineering in AI Era Capstone Project)  
> สาขาวิชาวิศวกรรมคอมพิวเตอร์ คณะวิศวกรรมศาสตร์ มหาวิทยาลัยเทคโนโลยีราชมงคลอีสาน วิทยาเขตขอนแก่น

---

## 📌 1. ปัญหาและที่มาของโครงการ (Problem Statement)

ในยุคปัจจุบัน การเข้าถึงหนังสือดิจิทัล (E-Book) เติบโตอย่างรวดเร็ว ทว่าระบบร้านค้าดิจิทัลส่วนใหญ่ประสบปัญหา 3 ประการหลัก: 
1. **Broken Access Control & Content Leakage**: ผู้ใช้สามารถลักลอบดาวน์โหลดไฟล์ลิขสิทธิ์ผ่าน URL ตรง หรือเข้าถึงคำสั่งซื้อของผู้อื่นโดยไม่ได้รับอนุญาต (IDOR Vulnerability)
2. **Lack of Intelligent Personalization**: ระบบค้นหาแบบเดิมจำกัดอยู่เพียงคำสำคัญตรงตัว (Exact Keyword Match) ขาดความเข้าใจความต้องการเชิงความหมายของผู้อ่าน 
3. **Data Integrity & Reporting Pitfalls**: ความผิดพลาดในการบันทึกราคาซื้อขายประวัติศาสตร์ (Snapshot Price) ทำให้ยอดขายในอดีตผันผวนเมื่อราคาสินค้าปัจจุบันเปลี่ยนแปลง 

โครงการ **E-Book Store** จึงถูกพัฒนาขึ้นเป็นระบบเว็บแอปพลิเคชันแบบ Hybrid SE ที่ผสานสถาปัตยกรรมคลาสสิก (Classical Relational DB, Strict RBAC, Transactional Checkout) เข้ากับเทคโนโลยี AI วิศวกรรมสมัยใหม่ (Semantic Book Recommendation Assistant, Structured Output, Fallback Chain, Observability Logging, AI Evals Regression Suite) เพื่อสร้างมาตรฐานระบบจัดจำหน่ายสื่อดิจิทัลที่ปลอดภัย ซื่อสัตย์ และมีประสิทธิภาพ

---

## 👥 2. ผู้มีส่วนได้ส่วนเสีย (Stakeholders)

* **ลูกค้า / ผู้อ่านทั่วไป (Readers / Customers)**: ผู้ค้นหา สั่งซื้อ ชำระเงินจำลอง และดาวน์โหลดไฟล์ E-Book เฉพาะรายการที่มีสิทธิ์ พร้อมรับคำแนะนำหนังสือที่ตรงใจผ่าน AI Bookstore Assistant
* **ผู้ดูแลระบบร้านค้า (Store Administrators)**: ผู้ตรวจสอบหลักฐานการโอนเงิน ปรับสถานะคำสั่งซื้อ จัดการสินค้าและหมวดหมู่ และเรียกดูรายงานวิเคราะห์ยอดขาย
* **ผู้บริหาร / เจ้าของธุรกิจ (Business Owners)**: ผู้ใช้รายงานเชิงลึก 4 มิติในการตัดสินใจทิศทางธุรกิจ พร้อมติดตามต้นทุนและ Latency ของ AI
* **วิศวกรซอฟต์แวร์ / ผู้ตรวจสอบ (Engineers & Evaluators)**: ผู้ดูแลเสถียรภาพระบบ คุณภาพโค้ด ความปลอดภัยตามมาตรฐาน PDPA/OWASP และการประเมินผล AI

---

## 🎯 3. ขอบเขตของระบบ (System Scope)

### ✅ อยู่ในขอบเขต (In Scope)
* **ระบบสมาชิกและการควบคุมสิทธิ์ (Auth & RBAC)**: สมัครสมาชิก, ล็อกอิน, แบ่งสิทธิ์ `customer` และ `admin` พร้อม Route Guard
* **หน้าร้านและตะกร้าสินค้า (Catalog & Shopping Cart)**: รายการ E-Book, ค้นหาตามชื่อ/ผู้แต่ง/หมวดหมู่, เพิ่ม/ลด/ลบสินค้าในตะกร้า
* **กระบวนการชำระเงินและบันทึกประวัติศาสตร์ (Checkout Transaction)**: รองรับ `BEGIN / COMMIT / ROLLBACK` พร้อมบันทึก `price_at_purchase`
* **การปกป้องสินค้าดิจิทัล (Digital Asset Access Control)**: ลิงก์ดาวน์โหลดเปิดได้เฉพาะคำสั่งซื้อสถานะ `confirmed` และผู้ขอต้องเป็นเจ้าของเท่านั้น (ป้องกัน IDOR)
* **ระบบปัญญาประดิษฐ์แนะนำหนังสือ (AI Bookstore Assistant)**: ผู้ช่วยค้นหาและแนะนำหนังสือตามความต้องการเชิงความหมาย พร้อม Graceful Fallback Chain
* **รายงานวิเคราะห์ข้อมูล (Business Analytics)**: ยอดขายรายเดือน/ช่วงเวลา, 5 อันดับหนังสือขายดี, ยอดขายตามหมวดหมู่, ลูกค้าสะสม พร้อมปุ่ม Export CSV UTF-8 BOM
* **การประกันคุณภาพ (Testing & AI Evals)**: Unit Test (AAA Pattern) และ AI Regression Eval Suite จำนวน 25 ชุดทดสอบ

### ❌ อยู่นอกขอบเขต (Out of Scope)
* การตัดบัตรเครดิตผ่าน Payment Gateway ของธนาคารจริง (ใช้ระบบอัปโหลดสลิปจำลองและอนุมัติโดย Admin)
* การจัดเก็บไฟล์ PDF ขนาดใหญ่ระดับ Terabyte บน Cloud Object Storage เฉพาะ (ใช้ Mock Protected URL ในชั้นการทดสอบ)
* ระบบ Digital Rights Management (DRM) ระดับฮาร์ดแวร์ / ลายน้ำเอกสารแบบไดนามิก (เป็นแผนระยะต่อไป)
* การส่งอีเมลแจ้งเตือนภายนอกผ่าน SMTP จริง (ลดความซับซ้อนตามกรอบ 1 เทอม)

---

## 🏗️ 4. สถาปัตยกรรมระบบ (System Architecture)

ระบบออกแบบตามสถาปัตยกรรม **3-Tier / Layered Hybrid Architecture** ดังนี้:
* **Presentation Layer**: Responsive Web UI พัฒนาด้วย Tailwind CSS
* **Application / Business Logic Layer**: Node.js & Express.js พร้อม Session Authentication และ AI Assistant Engine
* **Data Layer**: PostgreSQL บน Neon Serverless Cloud จัดเก็บข้อมูล 9 ตาราง รองรับ 3NF และ ACID Transaction
* **AI & Fallback Layer**: Gemini / LLM Provider เชื่อมต่อด้วย Fallback Adapter เมื่อเครือข่ายขัดข้องจะสลับใช้ Category-based Rule Engine อัตโนมัติ

ดูรายละเอียดแผนภาพ C4 Diagram และ Decision Tree ได้ที่ [architecture.md](file:///c:/Users/Lenovo/ebook-store/architecture.md)

---

## 🚀 5. วิธีติดตั้งและเปิดใช้งานระบบ (Quick Start)

### ข้อกำหนดขั้นต่ำ
* Node.js v20 ขึ้นไป (`node -v`)
* PostgreSQL Database (หรือใช้ Neon Cloud Connection String ที่กำหนดใน `.env`)

### ขั้นตอนการรัน
```bash
# 1. ติดตั้ง Dependencies
npm install

# 2. ตั้งค่า Environment Variable (สร้างไฟล์ .env หรือตั้งค่าในเครื่อง)
# DATABASE_URL=postgresql://user:pass@host/neondb?sslmode=require
# GEMINI_API_KEY=your_gemini_api_key_optional

# 3. รันระบบเซิร์ฟเวอร์
npm start
# เซิร์ฟเวอร์จะเปิดที่ http://localhost:3000

# 4. รันชุดทดสอบความถูกต้อง (Unit Tests)
npm test

# 5. รันชุดประเมินผล AI (AI Evals Suite)
npm run eval
```

---

## 📑 6. แผนที่เอกสารโครงงาน (Project Artifacts Index)

ตามข้อกำหนดของ [Capstone Framework](https://ecp-rmuti.gitbook.io/software-engineering-in-ai-era/capstone/capstone-framework) สามารถตรวจดูเอกสารหลักของโครงการได้ดังนี้:

| หมวดหมู่ | เอกสารหลัก | รายละเอียด |
| :--- | :--- | :--- |
| **ภาพรวมการส่งงาน** | [`PROJECT.md`](file:///c:/Users/Lenovo/ebook-store/PROJECT.md) | **สารบัญหลักของ Capstone ระบุที่ตั้งของชิ้นงานทุกชิ้น** |
| **Requirements** | [`requirements.md`](file:///c:/Users/Lenovo/ebook-store/requirements.md) | User Stories 12 ข้อ, Given-When-Then, FURPS+, 4 NFRs |
| **Tech Stack** | [`tech-stack.md`](file:///c:/Users/Lenovo/ebook-store/tech-stack.md) | เหตุผลการเลือกเทคโนโลยีและรายการ Alternatives ที่ไม่เลือก |
| **Team Charter** | [`team-charter.md`](file:///c:/Users/Lenovo/ebook-store/team-charter.md) | บทบาทสมาชิก ข้อตกลง และ AI Use Policy ของทีม |
| **AI Disclosure** | [`AI_USE_LOG.md`](file:///c:/Users/Lenovo/ebook-store/AI_USE_LOG.md) | บันทึกการใช้งาน AI, Trust Levels, และ Override Decisions |
| **PR Standards** | [`.github/PULL_REQUEST_TEMPLATE.md`](file:///c:/Users/Lenovo/ebook-store/.github/PULL_REQUEST_TEMPLATE.md) | แบบฟอร์ม Pull Request ที่บังคับระบุ AI Use Note |
| **Architecture** | [`architecture.md`](file:///c:/Users/Lenovo/ebook-store/architecture.md) | C4 Model (Context/Container/Component), Decision Tree, Fallback |
| **ADR Records** | [`adr/`](file:///c:/Users/Lenovo/ebook-store/adr) | ADR-001 ถึง ADR-004 บันทึกการตัดสินใจทางสถาปัตยกรรม |
| **Testing** | [`tests/`](file:///c:/Users/Lenovo/ebook-store/tests) | Unit Tests ตรวจสอบสิทธิ์ Access Control และ AI Service |
| **AI Evals** | [`evals/`](file:///c:/Users/Lenovo/ebook-store/evals) | Golden Dataset 25 ข้อ, Eval Runner, ผลลัพธ์ Prompt v1 vs v2 |
| **Observability** | [`observability/`](file:///c:/Users/Lenovo/ebook-store/observability) | Dashboard บันทึก Latency p50/p95/p99, Cost, Sample Traces |
| **Ethics Review** | [`docs/ethics-review.md`](file:///c:/Users/Lenovo/ebook-store/docs/ethics-review.md) | การตอบ 5 คำถามจริยธรรม, 10-Item Checklist, PDPA |
| **Runbook** | [`docs/runbook.md`](file:///c:/Users/Lenovo/ebook-store/docs/runbook.md) | คู่มือ Incident Response สำหรับ 4 สถานการณ์ฉุกเฉิน |
| **Code Review** | [`docs/code-review.md`](file:///c:/Users/Lenovo/ebook-store/docs/code-review.md) | Three-Layer Code Review บันทึก 5 PR สำคัญ |
| **Database** | [`docs/scope.md`](file:///c:/Users/Lenovo/ebook-store/docs/scope.md), [`docs/erd.md`](file:///c:/Users/Lenovo/ebook-store/docs/erd.md), [`sql/`](file:///c:/Users/Lenovo/ebook-store/sql) | ขอบเขต ERD Mermaid, DDL Schema, Seed, Reports |

---
**พัฒนาโดย**: ทีมโครงงานพัฒนาระบบร้านขายหนังสือและอีบุ๊กออนไลน์ (สาขาวิชาวิศวกรรมคอมพิวเตอร์ มทร.อีสาน ขอนแก่น)
