# ADR-004: การเลือกแพลตฟอร์มการเผยแพร่ระบบบนคลาวด์ (Cloud Deployment Platform)

* **สถานะ**: อนุมัติแล้ว (Accepted)
* **วันที่ตัดสินใจ**: สัปดาห์ที่ 8
* **ผู้มีส่วนร่วมในการตัดสินใจ**: นายสุรวัจน์ ชลเรืองทรัพย์ (Tech Lead), นายสรวิชญ์ มีมาก (Backend Lead)
* **บริบทและปัญหา (Context)**: ตามข้อกำหนดช่วงที่ 4 ของ Capstone Framework ระบบต้องสามารถ Deploy ขึ้นสภาพแวดล้อมคลาวด์จริง เพื่อให้ผู้สอนและกรรมการสามารถเข้าทดสอบระบบผ่านอินเทอร์เน็ตได้โดยไม่ต้องรันบนเครื่อง Local

---

## การตัดสินใจ (Decision)
ทีมตัดสินใจเลือกใช้ **Vercel Cloud Platform** (ร่วมกับไฟล์คอนฟิก `vercel.json`) เป็นทางเลือกหลัก และรองรับ **Render / Railway** เป็นระบบสำรอง

---

## ทางเลือกอื่นที่พิจารณา (Alternatives Considered)

1. **AWS EC2 / Virtual Private Server (VPS)**:
   * *ข้อดี*: ปรับแต่งระบบปฏิบัติการและคอนฟิกได้ 100%
   * *เหตุผลที่ไม่เลือก*: ต้องเสียเวลาดูแลการตั้งค่า Linux, Nginx, SSL Certbot, Firewall และเสี่ยงต่อการถูกเรียกเก็บเงินหากลืมปิด Instance
2. **Google Cloud Run (Containerized)**:
   * *ข้อดี*: รองรับ Docker และสเกลได้ดี
   * *เหตุผลที่ไม่เลือก*: ต้องการการตั้งค่า Dockerfile และ GCP Service Account ซึ่งมีความซับซ้อนเกินจำเป็นเมื่อเทียบกับ Vercel Git-integration

---

## ผลลัพธ์และการประเมิน (Consequences)

* **ผลเชิงบวก**:
  * ทุกการ Push ขึ้น Branch `main` บน GitHub จะถูก Build และ Deploy ใหม่อัตโนมัติ (CI/CD)
  * มี HTTPS และ SSL Certificate ฟรีให้ในตัว
  * มีระบบ Environment Variables จัดเก็บความลับ (`DATABASE_URL`, `GEMINI_API_KEY`) แยกจากโค้ด
* **ผลเชิงลบและความเสี่ยง**:
  * Vercel Serverless Function มีเวลาประมวลผลสูงสุด (Timeout) 10-15 วินาทีในแผนฟรี (ระบบได้ตั้งค่า Timeout ของ AI ไว้ที่ 3 วินาที จึงไม่ได้รับผลกระทบ)
