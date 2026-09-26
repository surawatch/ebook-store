// services/accessControl.js
// ระบบตรวจสอบสิทธิ์การเข้าถึงและดาวน์โหลดไฟล์ดิจิทัล (Digital Asset Access Control)
// ป้องกัน Broken Access Control และ Insecure Direct Object References (IDOR)
// สอดคล้องตามเกณฑ์ความปลอดภัย OWASP Top 10 และใบงานเสริม Capstone

/**
 * ตัดสินว่าผู้ขอมีสิทธิ์ได้รับลิงก์ดาวน์โหลดของคำสั่งซื้อนี้หรือไม่
 * @param {Object} order - ข้อมูลคำสั่งซื้อ { order_id, user_id, status, book_ids }
 * @param {number} requesterId - รหัสประจำตัวของผู้ใช้ที่ส่งคำขอ
 * @returns {Array<string>} รายการ URL ดาวน์โหลดที่ได้รับอนุญาต หรือ อาเรย์ว่างหากถูกปฏิเสธ
 */
function getDownloadLinks(order, requesterId) {
  if (!order || typeof order !== 'object') {
    return [];
  }

  // กฎข้อที่ 1: สถานะคำสั่งซื้อต้องเป็น 'confirmed' เท่านั้น (pending หรือ cancelled ต้องถูกปฏิเสธ)
  if (order.status !== 'confirmed') {
    return [];
  }

  // กฎข้อที่ 2: ผู้ขอต้องเป็นเจ้าของคำสั่งซื้อนั้นจริง (user_id ตรงกัน ป้องกัน IDOR)
  if (Number(order.user_id) !== Number(requesterId)) {
    return [];
  }

  // เมื่อผ่านเงื่อนไขครบถ้วน จึงคืนลิงก์ดาวน์โหลดของหนังสือทุกเล่มในคำสั่งซื้อ
  const bookIds = Array.isArray(order.book_ids) ? order.book_ids : [];
  return bookIds.map(bookId => `/download/${bookId}`);
}

module.exports = {
  getDownloadLinks
};
