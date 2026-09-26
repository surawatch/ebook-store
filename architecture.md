# 🏛️ สถาปัตยกรรมระบบ (System Architecture & C4 Model)

**โครงงาน**: ระบบร้านขายหนังสือและอีบุ๊กออนไลน์ (E-Book Store Online Management System)  
**วิชา**: วิศวกรรมซอฟต์แวร์ในยุค AI (Software Engineering in AI Era)  
**มาตรฐานอ้างอิง**: C4 Model (Context, Container, Component), AI Component Architecture (บทที่ 6 §6.3)

---

## 1. C4 Model Architecture Diagrams

### 1.1 ระดับที่ 1: แผนภาพบริบทของระบบ (System Context Diagram)
แสดงความสัมพันธ์ระหว่างผู้ใช้งานกลุ่มต่าง ๆ กับระบบ E-Book Store และระบบภายนอก

```mermaid
graph TD
    User["👤 ลูกค้า / นักอ่าน (Customer)<br>[ค้นหา ซื้อ ชำระเงิน อ่าน E-Book]"]
    Admin["👨‍💼 ผู้ดูแลร้านค้า (Store Admin)<br>[จัดการสินค้า ตรวจสอบสลิป ดูรายงาน]"]
    
    System["📚 E-Book Store Online System<br>[ระบบเว็บแอปพลิเคชันร้านค้าและผู้ช่วย AI]"]
    
    NeonDB[("🐘 Neon PostgreSQL Cloud<br>[จัดเก็บข้อมูล 9 ตาราง และ Snapshot Transactions]")]
    GeminiAPI["🧠 Google Gemini API<br>[ประมวลผลคำแนะนำหนังสือภาษาธรรมชาติ]"]
    
    User -->|เรียกดู สั่งซื้อ ขอคำแนะนำ| System
    Admin -->|อนุมัติคำสั่งซื้อ เรียกดูรายงาน| System
    System -->|อ่าน/เขียนข้อมูล| NeonDB
    System -->|ส่ง Query เพื่อวิเคราะห์ความชอบ| GeminiAPI
```

---

### 1.2 ระดับที่ 2: แผนภาพคอนเทนเนอร์ (Container Diagram)
แสดงองค์ประกอบเทคโนโลยีและการแลกเปลี่ยนข้อมูลภายในระบบ

```mermaid
graph TD
    Browser["🌐 เว็บเบราว์เซอร์ของผู้ใช้<br>[HTML5 + Tailwind CSS Client]"]
    
    subgraph "Server Application (Node.js & Express)"
        WebServer["🖥️ Express Web Server<br>[พอร์ต 3000 / Vercel Serverless]"]
        AuthModule["🔐 Auth & Session Middleware<br>[express-session + RBAC Guard]"]
        StoreModule["🛒 Storefront & Checkout Engine<br>[Transaction Manager]"]
        AIModule["🤖 AI Assistant & Fallback Service<br>[Hybrid Recommendation Engine]"]
        ReportsModule["📊 Analytics & CSV Exporter<br>[UTF-8 BOM Generator]"]
    end
    
    subgraph "External Cloud Services"
        NeonPostgres[("🐘 Neon PostgreSQL<br>[Connection Pooling over SSL]")]
        ExternalLLM["☁️ LLM Provider (Gemini / Mock)<br>[REST API over HTTPS]"]
    end
    
    Browser -->|HTTPS Requests| WebServer
    WebServer --> AuthModule
    WebServer --> StoreModule
    WebServer --> AIModule
    WebServer --> ReportsModule
    
    StoreModule -->|SQL Connection / pg Pool| NeonPostgres
    ReportsModule -->|SQL Aggregate Queries| NeonPostgres
    AuthModule -->|User Verification| NeonPostgres
    AIModule -->|Catalog Context + User Prompt| ExternalLLM
    AIModule -.->|Fallback to Popular Books| NeonPostgres
```

---

### 1.3 ระดับที่ 3: แผนภาพคอมโพเนนต์ (Component Diagram - AI & Storefront Layer)
แสดงการทำงานภายในของโมดูลร้านค้าและการเชื่อมต่อกับ AI Service

```mermaid
graph TD
    ClientReq["Client HTTP Request<br>/ai/recommend หรือ /download/:id"]
    
    subgraph "Application Core"
        RouteGuard["🛡️ Route Guard & Access Control<br>[สิทธิ์ RBAC & ตรวจสอบการเป็นเจ้าของ]"]
        AIService["🧠 AI Service (aiService.js)<br>[Context Builder & Prompt Orchestrator]"]
        FallbackEngine["⚙️ Rule-Based Fallback Engine<br>[SQL Category / Popularity Matching]"]
        DBPool["🔌 Database Connection Pool (db.js)<br>[pg.Pool with SSL]"]
    end
    
    ClientReq --> RouteGuard
    RouteGuard -->|คำขอดาวน์โหลด| DBPool
    RouteGuard -->|คำขอ AI แนะนำ| AIService
    
    AIService -->|1. ดึงแคตตาล็อกหนังสือ| DBPool
    AIService -->|2. เรียก LLM API (Timeout 3s)| RemoteLLM["External LLM"]
    
    RemoteLLM -->|3a. สำเร็จ (Valid JSON)| Response["ส่งคำแนะนำให้ผู้ใช้"]
    RemoteLLM -.->|3b. ล้มเหลว / Timeout / Error| FallbackEngine
    FallbackEngine -->|ดึงหนังสือยอดนิยมตามหมวดหมู่| DBPool
    FallbackEngine --> Response
```

---

## 2. แผนผังการตัดสินใจเลือกใช้ AI vs Classical SE (Decision Tree)

ตามหลักการในบทที่ 6 §6.3 และบทที่ 14 §14.4 ซอฟต์แวร์วิศวกรรมที่ดีต้องไม่ใช้ LLM กับทุกปัญหา การตัดสินใจในโครงการ E-Book Store เป็นไปตามแผนผังดังนี้:

```mermaid
graph TD
    Start["ฟังก์ชันการทำงานใหม่"] --> Q1{"เป็นงานที่ต้องการความแน่นอน 100%<br>หรือไม่ (เช่น การเงิน, สิทธิ์เข้าถึง)"}
    
    Q1 -- ใช่ --> ClassicalSE["🛠️ ใช้ Classical SE / RDBMS Rules<br>• การคำนวณเงินในตะกร้า<br>• Database Transaction (BEGIN/COMMIT)<br>• กฎการเข้าถึงไฟล์ (Access Control)<br>• รายงานสถิติและผลรวมยอดขาย"]
    
    Q1 -- ไม่ใช่ --> Q2{"ต้องการความเข้าใจความหมายภาษาธรรมชาติ<br>หรือความต้องการที่กำกวมหรือไม่"}
    
    Q2 -- ใช่ --> AIHybrid["🤖 ใช้ AI Component แบบมี Fallback<br>• ผู้ช่วยแนะนำหนังสือตามอารมณ์/ความสนใจ<br>• การจัดกลุ่มความต้องการเชิงความหมาย<br>• สรุปย่อสาระสำคัญของหนังสือ"]
    
    Q2 -- ไม่ใช่ --> RuleML["⚙️ ใช้ Deterministic Algorithm / Regex<br>• การค้นหาด้วยคำสำคัญตรงตัว (ILIKE)<br>• การตรวจสอบรูปแบบอีเมล"]
```

### สรุปเหตุผลของการจัดแบ่ง:
1. **การเงินและการชำระเงิน**: ใช้ SQL Constraints และ ACID Transaction 100% ห้ามใช้ LLM ในการคำนวณยอดเงินเด็ดขาด
2. **การดาวน์โหลดไฟล์ดิจิทัล**: ตรวจสอบความเป็นเจ้าของคำสั่งซื้อผ่าน SQL Query แบบ Strict Authorization ห้ามพึ่งพาการตัดสินใจของ AI
3. **การแนะนำหนังสือ**: เหมาะสมอย่างยิ่งสำหรับ LLM เพราะผู้ใช้อาจพิมพ์คำค้นหาที่ไม่มีคำสำคัญตรงในชื่อเรื่อง เช่น *"อยากหาแรงบันดาลใจเริ่มทำธุรกิจ"* ซึ่ง AI สามารถเชื่อมโยงกับหนังสือหมวดการเงิน/การพัฒนาตนเองได้

---

## 3. ยุทธศาสตร์การรับมือความล้มเหลว (Graceful Fallback Strategy)

เมื่อระบบภายนอก (LLM Provider) เกิดปัญหา เช่น เครือข่ายล่ม, Rate Limit เกิน, หรือ API Key ขัดข้อง ระบบ E-Book Store จะดำเนินตาม **3-Stage Fallback Chain**:

```mermaid
sequenceDiagram
    autonumber
    actor User as ผู้ใช้งาน
    participant App as เว็บเซิร์ฟเวอร์
    participant AI as Gemini API
    participant DB as Neon PostgreSQL

    User->>App: ส่งคำขอ: "แนะนำหนังสือเทคโนโลยีสำหรับมือใหม่"
    App->>App: ดึงข้อมูลแคตตาล็อกหนังสือสั้นจาก Cache/DB
    
    alt ขั้นที่ 1: เรียก LLM Provider หลัก
        App->>AI: ส่ง Prompt พร้อม Context (Timeout = 3000ms)
        Note over AI: กรณีเครือข่ายขัดข้อง หรือ Timeout
        AI--xApp: Error: ETIMEDOUT หรือ 429 Too Many Requests
    end
    
    alt ขั้นที่ 2: Graceful Degradation (Fallback Engine)
        Note over App: ดักจับ Error ไม่โยน 500 หาผู้ใช้
        App->>DB: Query หนังสือขายดีในหมวดเทคโนโลยี (SQL Fallback)
        DB-->>App: รายการ 3 เล่มยอดนิยม
    end
    
    App-->>User: แสดงผลหนังสือแนะนำ พร้อมป้ายกำกับ "[ระบบสำรอง: แนะนำตามหมวดหมู่ยอดนิยม]"
```

### ผลลัพธ์:
* **User Experience (UX)**: ผู้ใช้ยังคงได้รับรายการหนังสือแนะนำที่เกี่ยวข้องเสมอ ไม่พบหน้าต่าง Error หรือระบบค้าง
* **System Observability**: บันทึกเหตุการณ์ Fallback ลงใน Observability Logger เพื่อแจ้งเตือนวิศวกรผู้ดูแลระบบ
