// observability/logger.js
// ระบบบันทึกและติดตามสมรรถนะ (Latency, Cost, Error Rate, Traces)
// สอดคล้องตามมาตรฐาน LLMOps บทที่ 13 §13.4.4

const traces = [];
const MAX_TRACES = 100;

// อัตราค่าบริการประมาณการ (Gemini Free Tier = $0, Commercial Est. = $0.0001 / 1K tokens)
const COST_PER_1K_TOKENS = 0.0001;

function logTrace(traceData) {
  const trace = {
    id: `trace-${Date.now()}-${Math.random().toString(36).substring(2, 7)}`,
    timestamp: new Date().toISOString(),
    operation: traceData.operation || 'unknown',
    query: traceData.query || '',
    mode: traceData.mode || 'ai', // 'ai' | 'fallback'
    prompt_version: traceData.prompt_version || 'v2',
    latency_ms: traceData.latency_ms || 0,
    status: traceData.status || 'success', // 'success' | 'error' | 'fallback'
    estimated_tokens: traceData.estimated_tokens || 120,
    estimated_cost_usd: (traceData.estimated_tokens || 120) * (COST_PER_1K_TOKENS / 1000),
    error_message: traceData.error_message || null,
    metadata: traceData.metadata || {}
  };

  traces.push(trace);
  if (traces.length > MAX_TRACES) {
    traces.shift();
  }

  // พิมพ์ Log ในรูปแบบ Structured JSON
  console.log(`[OBSERVABILITY] ${trace.timestamp} | ${trace.operation} | ${trace.mode.toUpperCase()} | ${trace.latency_ms}ms | Status: ${trace.status}`);
  return trace;
}

function getMetrics() {
  if (traces.length === 0) {
    return {
      total_requests: 0,
      p50_latency_ms: 0,
      p95_latency_ms: 0,
      p99_latency_ms: 0,
      ai_success_count: 0,
      fallback_count: 0,
      error_count: 0,
      error_rate_pct: 0,
      total_estimated_cost_usd: 0,
      recent_traces: []
    };
  }

  const latencies = traces.map(t => t.latency_ms).sort((a, b) => a - b);
  const p50 = latencies[Math.floor(latencies.length * 0.50)] || 0;
  const p95 = latencies[Math.floor(latencies.length * 0.95)] || 0;
  const p99 = latencies[Math.floor(latencies.length * 0.99)] || 0;

  const aiSuccess = traces.filter(t => t.status === 'success' && t.mode === 'ai').length;
  const fallbacks = traces.filter(t => t.mode === 'fallback' || t.status === 'fallback').length;
  const errors = traces.filter(t => t.status === 'error').length;
  const totalCost = traces.reduce((sum, t) => sum + (t.estimated_cost_usd || 0), 0);

  return {
    total_requests: traces.length,
    p50_latency_ms: p50,
    p95_latency_ms: p95,
    p99_latency_ms: p99,
    ai_success_count: aiSuccess,
    fallback_count: fallbacks,
    error_count: errors,
    error_rate_pct: ((errors / traces.length) * 100).toFixed(2),
    total_estimated_cost_usd: totalCost.toFixed(6),
    recent_traces: traces.slice(-10).reverse()
  };
}

module.exports = {
  logTrace,
  getMetrics,
  traces
};
