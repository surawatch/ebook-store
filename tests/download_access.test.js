// tests/download_access.test.js
// ชุดทดสอบ Unit Test สำหรับกฎความปลอดภัยการเข้าถึงไฟล์ดิจิทัล (Digital Access Control)
// ใช้ Node.js Built-in Test Runner (node --test) ตามรูปแบบ Arrange-Act-Assert (AAA)
// ป้องกัน Broken Access Control และ IDOR ตามมาตรฐาน OWASP Top 10

const { test, describe } = require('node:test');
const assert = require('node:assert/strict');
const { getDownloadLinks } = require('../services/accessControl');

function makeOrder(status = 'confirmed', userId = 1, bookIds = [1, 2]) {
  return {
    order_id: 101,
    status: status,
    user_id: userId,
    book_ids: bookIds
  };
}

describe('🧪 กฎการเข้าถึงลิงก์ดาวน์โหลดหนังสือดิจิทัล (Digital Asset Access Control)', () => {

  test('TC-01: เจ้าของคำสั่งซื้อที่ยืนยันแล้ว (confirmed) ต้องได้รับลิงก์ดาวน์โหลดครบทุกเล่ม', () => {
    // Arrange (เตรียม)
    const order = makeOrder('confirmed', 1, [10, 11]);
    const requesterId = 1;

    // Act (เรียก)
    const result = getDownloadLinks(order, requesterId);

    // Assert (ตรวจ)
    assert.deepEqual(result, ['/download/10', '/download/11']);
  });

  test('TC-02: คำสั่งซื้อที่ยังรอตรวจสอบ (pending) ต้องไม่ได้รับลิงก์ดาวน์โหลด (ต้องได้อาเรย์ว่าง)', () => {
    // Arrange (เตรียม)
    const order = makeOrder('pending', 1, [10, 11]);
    const requesterId = 1;

    // Act (เรียก)
    const result = getDownloadLinks(order, requesterId);

    // Assert (ตรวจ)
    assert.deepEqual(result, []);
  });

  test('TC-03: คำสั่งซื้อที่ถูกยกเลิก (cancelled) ต้องไม่ได้รับลิงก์ดาวน์โหลด', () => {
    // Arrange (เตรียม)
    const order = makeOrder('cancelled', 1, [10, 11]);
    const requesterId = 1;

    // Act (เรียก)
    const result = getDownloadLinks(order, requesterId);

    // Assert (ตรวจ)
    assert.deepEqual(result, []);
  });

  test('TC-04: ผู้ขอที่ไม่ใช่เจ้าของคำสั่งซื้อ (IDOR Attack) ต้องถูกปฏิเสธ แม้คำสั่งซื้อจะยืนยันแล้ว', () => {
    // Arrange (เตรียม - เจ้าของคือ user_id: 1 แต่ผู้ขอคือ user_id: 999)
    const order = makeOrder('confirmed', 1, [10, 11]);
    const requesterId = 999;

    // Act (เรียก)
    const result = getDownloadLinks(order, requesterId);

    // Assert (ตรวจ - ป้องกันข้อมูลรั่วไหล)
    assert.deepEqual(result, []);
  });

  test('TC-05: คำสั่งซื้อที่มีข้อมูลผิดพลาดหรือไม่สมบูรณ์ (Malformed Input) ต้องปลอดภัยและไม่เกิด Exception', () => {
    assert.deepEqual(getDownloadLinks(null, 1), []);
    assert.deepEqual(getDownloadLinks(undefined, 1), []);
    assert.deepEqual(getDownloadLinks({}, 1), []);
  });
});
