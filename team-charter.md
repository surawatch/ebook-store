# 🤝 กฎบัตรทีมและข้อตกลงการทำงานร่วมกัน (Team Charter & Working Agreement)

**โครงงาน**: ระบบร้านขายหนังสือและอีบุ๊กออนไลน์ (E-Book Store Online Management System)  
**วิชา**: วิศวกรรมซอฟต์แวร์ในยุค AI (Software Engineering in AI Era)  
**สถาบัน**: มหาวิทยาลัยเทคโนโลยีราชมงคลอีสาน วิทยาเขตขอนแก่น  
**มาตรฐานอ้างอิง**: SE2014 Team Guidelines, Agile Sprint Zero (บทที่ 2), AI Trust Levels (บทที่ 1 & 14)

---

## 1. ข้อมูลสมาชิกและบทบาทหน้าที่ความรับผิดชอบ (Roles & Responsibilities)

เพื่อให้สอดคล้องกับกรอบ Capstone Framework สมาชิกในทีมรับผิดชอบบทบาทหลักและบทบาทรองดังนี้:

| ลำดับ | ชื่อ-นามสกุล | รหัสนักศึกษา | บทบาทหลัก (Primary Role) | บทบาทรอง (Secondary Role) | ความรับผิดชอบหลักในโครงการ |
| :---: | :--- | :---: | :--- | :--- | :--- |
| **1** | **นายสุรวัจน์ ชลเรืองทรัพย์** | **67332110217-1** | **Tech Lead / Architect** | **AI Engineer** | • ออกแบบสถาปัตยกรรมระบบและฐานข้อมูล (ERD, 3NF)<br>• พัฒนาระบบหน้าร้าน ตะกร้าสินค้า และ Transactional Checkout<br>• ออกแบบ Prompt และ Fallback Chain สำหรับ AI Assistant<br>• จัดทำ ADR และดูแล Git Workflow |
| **2** | **นายสรวิชญ์ มีมาก** | **67332110275-8** | **Backend & Security Lead** | **QA & Eval Lead** | • ออกแบบระบบความปลอดภัย (RBAC, Route Guard, Session)<br>• พัฒนากลไกการเข้าถึงไฟล์ดิจิทัล (Digital Access Control)<br>• ออกแบบและรันชุดทดสอบ Unit Tests และ AI Evals Suite<br>• พัฒนาระบบรายงานวิเคราะห์และ Export CSV (UTF-8 BOM) |

*หมายเหตุ: สมาชิกทุกคนในทีมมีส่วนร่วมในการ Commit โค้ด, ทำ Three-layer Code Review ร่วมกัน, และทำความเข้าใจสถาปัตยกรรมทุกส่วนเพื่อเตรียมความพร้อมสำหรับการสอบ Oral Defense*

---

## 2. ช่องทางการสื่อสารและการประสานงาน (Communication Channels)

| ช่องทาง | วัตถุประสงค์การใช้งาน | ความถี่ / เวลาตอบกลับ |
| :--- | :--- | :--- |
| **Discord / LINE Group** | สื่อสารทั่วไป นัดหมายประชุมด่วน แจ้งเตือน Git push | ใช้งานประจำวัน ตอบกลับภายใน 2 ชั่วโมง |
| **GitHub Repository & Issues** | จัดการงานแบบ Backlog, ติดตาม Bug, และเปิด Pull Request | ตรวจสอบทุกวันก่อนเริ่มทำงาน |
| **Weekly Sync (Face-to-Face)** | ประชุมทบทวนความก้าวหน้า และทำ Sprint Retrospective | สัปดาห์ละ 1 ครั้ง (ทุกวันพุธหลังเลิกเรียน) |

---

## 3. ข้อตกลงการทำงานร่วมกัน (Working Agreements)

1. **Git Flow & Branching Strategy**:
   * Branch `main` คือโค้ดที่ผ่านการทดสอบและพร้อมรันเสมอ ห้าม push ตรงเข้า `main` เด็ดขาด
   * พัฒนาฟีเจอร์ใหม่บน Branch เช่น `feature/ai-recommendation` หรือ `fix/access-control`
   * การ Merge เข้า `main` ต้องทำผ่าน Pull Request (PR) และผ่านการ Review จากเพื่อนร่วมทีมอย่างน้อย 1 คนเสมอ
2. **Commit Message Discipline**:
   * Commit Message ต้องสื่อสารว่า **"ทำไม (Why)"** ไม่ใช่แค่ **"ทำอะไร (What)"**
   * ใช้โครงสร้าง Conventional Commits เช่น:
     * `feat: implement graceful fallback for ai book recommendation`
     * `fix: restrict download links to confirmed orders only (prevent IDOR)`
     * `test: add 25 golden eval cases for semantic search`
3. **Definition of Done (DoD)**:
   * งานหนึ่งชิ้นจะถือว่าเสร็จสมบูรณ์เมื่อ:
     1. โค้ดทำงานได้ถูกต้องตาม Acceptance Criteria ที่ระบุไว้ใน `requirements.md`
     2. มีการเขียน Unit Test หรือ Eval ครอบคลุม และรันผ่าน 100%
     3. โค้ดไม่มี Credential / Secret Key หลุดเข้าไปใน Git
     4. มีการกรอกข้อมูล AI Use Disclosure ในคำอธิบาย PR ครบถ้วน

---

## 4. นโยบายการใช้ AI ภายในทีม (Team AI Use Policy)

อ้างอิงตามกรอบจริยธรรมของรายวิชา (บทที่ 1 §1.5 และบทที่ 14 §14.4):

* **ระดับความไว้วางใจที่กำหนด (Trust Level Policy)**:
  * **Trust Level 1 (Human Decides, AI Suggests)**: ใช้สำหรับการตัดสินใจทางสถาปัตยกรรมหลัก (Architecture Decisions), การออกแบบตารางฐานข้อมูล, กฎความปลอดภัยการเข้าถึงไฟล์, และข้อสรุปทางจริยธรรม (Ethics Review) — *มนุษย์ต้องเป็นผู้ตัดสินใจสุดท้ายและเข้าใจผลกระทบ 100%*
  * **Trust Level 2-3 (Co-Pilot / Pair Programming)**: ใช้สำหรับการเขียน Boilerplate Code, การจัดแต่ง CSS, การสร้าง Mock Data และแบบทดสอบ Unit Test — *ต้องมีการตรวจสอบ Diff ทุกบรรทัดก่อน Commit*
* **ข้อห้ามเด็ดขาด (Strict Prohibitions)**:
  * ❌ ห้ามส่งโค้ดที่สร้างโดย AI เข้าสู่ระบบโดยไม่ผ่านการอ่านและทำความเข้าใจด้วยตนเอง
  * ❌ ห้ามให้ AI สร้างเล่มรายงานจริยธรรม หรือแต่งข้อเท็จจริง (Fabrication) ในการสอบหรือการนำเสนอ
  * ❌ ห้ามบันทึก API Key หรือข้อมูลส่วนตัวของสมาชิก/ผู้ใช้ลงใน Prompt ของ Public AI
* **การบันทึกความโปร่งใส (Transparency)**:
  * ทุกการใช้งาน AI ที่มีนัยสำคัญต่อโครงสร้างโค้ด ต้องบันทึกรายการลงใน `AI_USE_LOG.md` และระบุเหตุผลหากมีการแก้ไขหรือปฏิเสธคำแนะนำของ AI
