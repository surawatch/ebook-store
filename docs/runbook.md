# 🚨 คู่มือการเผชิญเหตุการณ์และแก้ไขปัญหาฉุกเฉิน (Operational Incident Runbook)

**โครงงาน**: ระบบร้านขายหนังสือและอีบุ๊กออนไลน์ (E-Book Store Online Management System)  
**วิชา**: วิศวกรรมซอฟต์แวร์ในยุค AI (Software Engineering in AI Era)  
**มาตรฐานอ้างอิง**: Site Reliability Engineering (SRE) & LLMOps Operations (บทที่ 13 §13.4.4)

---

## 1. ข้อมูลการติดต่อผู้รับผิดชอบระบบ (On-call Contacts)

* **Primary On-call Engineer**: นายสุรวัจน์ ชลเรืองทรัพย์ (Tech Lead / Architect)
* **Secondary On-call Engineer**: นายสรวิชญ์ มีมาก (Backend & Security Lead)
* **Escalation Channel**: แจ้งเตือนฉุกเฉินผ่านห้อง Discord Alert หรือโทรศัพท์สายตรง

---

## 2. สถานการณ์ฉุกเฉินและแนวทางการรับมือ (Incident Response Scenarios)

### สถานการณ์ที่ 1: LLM Provider ล่ม หรือ เครือข่ายขัดข้อง (AI Outage / Timeout)
* **อาการที่พบ (Symptoms)**:
  * หน้า `/ai` มีคำขอค้างเกิน 3 วินาที หรือเกิดข้อความแจ้งเตือน Error จาก API
  * ใน Observability Dashboard พบว่าโหมด Fallback ถูกเรียกใช้งานอย่างต่อเนื่อง
* **ระดับความรุนแรง**: 🟡 ระดับ P2 (High Availability ยังคงอยู่เพราะมี Fallback แต่ความฉลาดลดลง)
* **ขั้นตอนการตรวจสอบและแก้ไข (Action Steps)**:
  1. เข้าตรวจสอบสถานะการทำงานของ Google Gemini ผ่าน [Google AI Status Dashboard](https://status.cloud.google.com/)
  2. ตรวจสอบว่าโควตาการเรียกใช้งาน Free Tier รายวัน/รายนาทีของ API Key ถูกใช้จนหมดหรือไม่
  3. หาก API Key มีปัญหา ให้สร้าง API Key สำรองอันใหม่จาก Google AI Studio แล้วอัปเดตใน Environment Variables ของ Vercel
  4. ทำการ Redeploy ระบบบน Vercel เพื่อโหลด Key ใหม่
  5. ตรวจสอบว่า `services/aiService.js` ยังคงทำงานในโหมด Fallback ได้อย่างราบรื่นโดยไม่โยน Error 500 หาผู้ใช้

---

### สถานการณ์ที่ 2: การเชื่อมต่อฐานข้อมูล Neon เต็ม (Connection Pool Exhaustion)
* **อาการที่พบ (Symptoms)**:
  * หน้าเว็บตอบสนองช้ามาก และ Terminal / Log แสดงข้อความ: `remaining connection slots are reserved for non-replication superuser connections` หรือ `timeout waiting for connection`
* **ระดับความรุนแรง**: 🔴 ระดับ P1 (ระบบหลักใช้งานไม่ได้ กระทบการสั่งซื้อ)
* **ขั้นตอนการตรวจสอบและแก้ไข (Action Steps)**:
  1. เข้าสู่ Console ของ Neon Cloud แล้วเลือกดูแท็บ **Operations / Monitoring** เพื่อสังเกต Active Connections
  2. ตรวจสอบโค้ดใน `routes/shop.js` ว่ามีฟังก์ชันใดที่เรียก `const client = await pool.connect()` แล้ว **ลืมเรียก `client.release()` ในบล็อก `finally`** หรือไม่
  3. หากเกิด Connection ค้างจากเซิร์ฟเวอร์ ให้กดปุ่ม **Restart Compute Endpoint** บนหน้าแดชบอร์ดของ Neon ทันทีเพื่อล้างการเชื่อมต่อค้าง
  4. ตรวจสอบว่าในไฟล์ `db.js` มีการใช้ `pg.Pool` แบบ Shared Instance เพียงตัวเดียว และไม่สร้าง `new Pool()` ซ้ำในแต่ละ Request

---

### สถานการณ์ที่ 3: ตรวจพบอัตรา Hallucination หรือพฤติกรรมผิดปกติของ AI พุ่งสูง
* **อาการที่พบ (Symptoms)**:
  * ผู้ใช้รายงานว่า AI แนะนำหนังสือที่ไม่เกี่ยวข้อง หรือแนะนำหนังสือที่ไม่มีอยู่ในร้าน
  * ค่า Confidence ในร่องรอยการบันทึกลดลงต่ำกว่า 0.40 อย่างมีนัยสำคัญ
* **ระดับความรุนแรง**: 🟡 ระดับ P2 (กระทบประสบการณ์และความน่าเชื่อถือ)
* **ขั้นตอนการตรวจสอบและแก้ไข (Action Steps)**:
  1. เปิดไฟล์ `evals/eval_runner.js` แล้วรันคำสั่ง `node evals/eval_runner.js` เพื่อทดสอบเทียบกับ Golden Dataset ล่าสุด
  2. ตรวจสอบ System Prompt ใน `services/aiService.js` (ฟังก์ชัน `buildPromptV2`) ว่ามีการระบุ `[STRICT CATALOG CONTEXT]` ครบถ้วนหรือไม่
  3. ตรวจสอบตัวกรองรหัสหนังสือ (Catalog ID Whitelist Filter) ว่ายังคงตรวจสอบ `catalogMap.has(id)` ก่อนคืนค่าหรือไม่
  4. หากโมเดล Gemini อัปเดตรุ่นใหม่แล้วพฤติกรรมเปลี่ยน ให้ปรับลดพารามิเตอร์ `temperature` ลงมาที่ `0.1` เพื่อลดความสุ่ม

---

### สถานการณ์ที่ 4: ตรวจพบความพยายามลักลอบดาวน์โหลดไฟล์โดยไม่ได้รับอนุญาต (Broken Access Control / IDOR Attempt)
* **อาการที่พบ (Symptoms)**:
  * ใน Server Log มีรหัสสถานะ `403 Forbidden` ถี่ผิดปกติบน URL เส้นทาง `/download/:ebookId`
  * มีการยิงคำขอเปลี่ยนหมายเลข ID ของหนังสือหรือคำสั่งซื้อวนซ้ำ (Enumeration Attack)
* **ระดับความรุนแรง**: 🟠 ระดับ P2 (มีผู้พยายามเจาะระบบ แต่ระบบป้องกันได้)
* **ขั้นตอนการตรวจสอบและแก้ไข (Action Steps)**:
  1. ตรวจสอบ IP Address ของผู้ส่งคำขอใน Log
  2. ตรวจสอบว่าไม่มีคำขอใดที่สามารถทะลุการตรวจสอบสิทธิ์ `o.order_status = 'confirmed' AND o.user_id = $1` ได้
  3. หากการยิงมาจาก IP เดิมเกิน 50 ครั้งต่อนาที ให้ทำการบล็อก IP ชั่วคราวผ่าน Vercel Firewall / WAF
  4. รันชุดทดสอบความปลอดภัย `npm test` เพื่อยืนยันว่ากฎ Access Control ทั้ง 5 ข้อยังคงผ่าน 100%
