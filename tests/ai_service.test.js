// tests/ai_service.test.js
// ชุดทดสอบ Unit Test สำหรับระบบ AI Bookstore Assistant และ Graceful Fallback Engine

const { test, describe, after } = require('node:test');
const assert = require('node:assert/strict');
const pool = require('../db');
const { 
  buildPromptV1, 
  buildPromptV2, 
  ruleBasedFallback, 
  recommendBooks, 
  DEFAULT_FALLBACK_CATALOG 
} = require('../services/aiService');

describe('🤖 การทดสอบโมดูล AI Assistant และ Fallback Chain', () => {

  test('TC-AI-01: buildPromptV2 ต้องบรรจุคำสั่ง Strict JSON และ Safety Guardrails', () => {
    const prompt = buildPromptV2('อยากเรียนรู้เรื่องฐานข้อมูล', DEFAULT_FALLBACK_CATALOG);
    assert.match(prompt, /STRICT CATALOG CONTEXT/);
    assert.match(prompt, /recommended_ids/);
    assert.match(prompt, /NEVER invent or hallucinate/);
    assert.match(prompt, /User Query: "อยากเรียนรู้เรื่องฐานข้อมูล"/);
  });

  test('TC-AI-02: Rule-based Fallback สามารถจับคู่คำค้นหาด้านการเงินและการลงทุนได้อย่างถูกต้อง', () => {
    const result = ruleBasedFallback('อยากได้หนังสือเกี่ยวกับการลงทุนและหุ้น', DEFAULT_FALLBACK_CATALOG);
    assert.ok(Array.isArray(result.recommended_ids));
    assert.ok(result.recommended_ids.includes(4), 'ควรแนะนำ Intelligent Tech Investor (ID: 4)');
    assert.ok(result.confidence > 0.5);
  });

  test('TC-AI-03: Rule-based Fallback สามารถจับคู่คำค้นหาด้านเทคโนโลยีและฐานข้อมูลได้อย่างถูกต้อง', () => {
    const result = ruleBasedFallback('database design and architecture', DEFAULT_FALLBACK_CATALOG);
    assert.ok(result.recommended_ids.includes(1) || result.recommended_ids.includes(2));
  });

  test('TC-AI-04: Graceful Degradation - recommendBooks ต้องทำงานได้และไม่เกิด Crash เมื่อไม่มี API Key (Force Fallback)', async () => {
    const result = await recommendBooks('อยากพัฒนาตนเอง', { forceFallback: true });
    assert.equal(result.success, true);
    assert.equal(result.mode, 'fallback');
    assert.ok(Array.isArray(result.books));
    assert.ok(result.books.length > 0);
    assert.ok(result.latency_ms >= 0);
  });

  test('TC-AI-05: Zero-Hallucination - หนังสือทุกเล่มที่ส่งกลับต้องมี ID อยู่ในแคตตาล็อกจริง', async () => {
    const result = await recommendBooks('ขอหนังสือที่ไม่มีอยู่จริงในโลกหน่อย', { forceFallback: true });
    const catalogIds = DEFAULT_FALLBACK_CATALOG.map(b => b.ebook_id);
    for (const book of result.books) {
      assert.ok(catalogIds.includes(book.ebook_id), `ID ${book.ebook_id} ต้องอยู่ในแคตตาล็อก`);
    }
  });

  after(async () => {
    try {
      await pool.end();
    } catch {
      // ignore
    }
  });
});
