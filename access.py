"""
access.py
ตัดสินว่าผู้ขอได้ลิงก์ดาวน์โหลดของคำสั่งซื้อนี้หรือไม่
สอดคล้องตามเกณฑ์ความปลอดภัย OWASP Top 10 และใบงานเสริม Capstone ร้านขายหนังสือดิจิทัล
"""


def download_links(order, requester_id):
    """คืนลิงก์ดาวน์โหลด เฉพาะคำสั่งซื้อที่ยืนยันแล้ว และผู้ขอเป็นเจ้าของ"""
    if not order or not isinstance(order, dict):
        return []
    if order.get("status") != "confirmed":
        return []
    if order.get("user_id") != requester_id:
        return []
    return [f"/downloads/{book_id}.epub" for book_id in order.get("book_ids", [])]
