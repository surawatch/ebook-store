"""
tests/test_download_access.py
ชุดทดสอบ Python สำหรับกฎความปลอดภัยการเข้าถึงไฟล์ดิจิทัล (Digital Access Control)
รองรับการรันผ่านทั้ง `python -m unittest` และ `pytest`
ตามแนวทางในใบความรู้เสริม Capstone ร้านขายหนังสือดิจิทัล
"""

import unittest
from access import download_links


def make_order(status="confirmed", user_id=1, book_ids=(10, 11)):
    return {"status": status, "user_id": user_id, "book_ids": list(book_ids)}


class TestDownloadAccess(unittest.TestCase):

    def test_เจ้าของคำสั่งซื้อที่ยืนยันแล้วได้ลิงก์ครบ(self):
        # Arrange (เตรียม)
        order = make_order()
        # Act (เรียก)
        result = download_links(order, requester_id=1)
        # Assert (ตรวจ)
        self.assertEqual(result, ["/downloads/10.epub", "/downloads/11.epub"])

    def test_คำสั่งซื้อที่ยังไม่ยืนยันต้องไม่ได้ลิงก์(self):
        for status in ("pending", "cancelled"):
            order = make_order(status=status)
            result = download_links(order, requester_id=1)
            self.assertEqual(result, [])

    def test_คนที่ไม่ใช่เจ้าของต้องไม่ได้ลิงก์แม้ยืนยันแล้ว(self):
        order = make_order(user_id=1)
        result = download_links(order, requester_id=2)
        self.assertEqual(result, [])


# รองรับการรันแบบ Standalone script
if __name__ == "__main__":
    unittest.main()
