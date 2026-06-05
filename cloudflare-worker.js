/**
 * Cloudflare Worker — Anthropic API 프록시 (lab-wiki 챗봇용)
 *
 * 배포 방법:
 * 1. https://dash.cloudflare.com → Workers & Pages → Create Worker
 * 2. 이 코드 붙여넣기
 * 3. Settings → Variables → ANTHROPIC_API_KEY 추가 (Encrypt / secret)
 * 4. 배포 후 URL 복사해서 Quarto 사이트의 WORKER_URL에 입력
 * 5. (권장) Cloudflare 대시보드에서 이 Worker에 Rate Limiting 규칙 추가
 */

const ALLOWED_ORIGINS = [
  "https://kkonoo.github.io",   // GitHub Pages 도메인
  "http://localhost:4321",      // 로컬 개발용
  "http://localhost:8080",
];

// 챗봇 성격을 여기서 고정 (클라이언트가 못 바꿈)
const SYSTEM_PROMPT = `You are a teaching assistant for a bioinformatics graduate lab wiki.
Answer concisely and accurately about bioinformatics, genomics, and statistical genetics.
If a question is outside this scope, politely redirect to bioinformatics topics.`;

// 입력 길이/개수 제한 (토큰·비용 방지)
const MAX_MESSAGES = 20;
const MAX_CHARS_PER_MSG = 4000;

export default {
  async fetch(request, env) {
    const origin = request.headers.get("Origin") || "";

    if (request.method === "OPTIONS") {
      return corsResponse(null, origin, 204);
    }
    if (request.method !== "POST") {
      return corsResponse(JSON.stringify({ error: "Method not allowed" }), origin, 405);
    }

    // Origin 정확히 일치하는 것만 허용
    if (!ALLOWED_ORIGINS.includes(origin)) {
      return corsResponse(JSON.stringify({ error: "Origin not allowed" }), origin, 403);
    }

    if (!env.ANTHROPIC_API_KEY) {
      return corsResponse(JSON.stringify({ error: "API key not configured" }), origin, 500);
    }

    let body;
    try {
      body = await request.json();
    } catch {
      return corsResponse(JSON.stringify({ error: "Invalid JSON" }), origin, 400);
    }

    // messages 정리: 개수 제한 + 길이 제한
    let messages = Array.isArray(body.messages) ? body.messages : [];
    messages = messages.slice(-MAX_MESSAGES).map((m) => ({
      role: m.role,
      content:
        typeof m.content === "string"
          ? m.content.slice(0, MAX_CHARS_PER_MSG)
          : m.content,
    }));

    if (messages.length === 0) {
      return corsResponse(JSON.stringify({ error: "No messages" }), origin, 400);
    }

    // Anthropic API 호출 (모델·system은 서버에서 고정)
    let anthropicRes, data;
    try {
      anthropicRes = await fetch("https://api.anthropic.com/v1/messages", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          "x-api-key": env.ANTHROPIC_API_KEY,
          "anthropic-version": "2023-06-01",
        },
        body: JSON.stringify({
          model: "claude-sonnet-4-6", // 비용 우선이면 "claude-haiku-4-5-20251001"
          max_tokens: Math.min(body.max_tokens || 1024, 2048),
          system: SYSTEM_PROMPT,
          messages,
        }),
      });
      data = await anthropicRes.json();
    } catch (err) {
      return corsResponse(
        JSON.stringify({ error: "Upstream error", detail: String(err) }),
        origin,
        502
      );
    }

    return corsResponse(JSON.stringify(data), origin, anthropicRes.status);
  },
};

function corsResponse(body, origin, status) {
  const headers = {
    "Content-Type": "application/json",
    "Access-Control-Allow-Origin": ALLOWED_ORIGINS.includes(origin)
      ? origin
      : ALLOWED_ORIGINS[0],
    "Access-Control-Allow-Methods": "POST, OPTIONS",
    "Access-Control-Allow-Headers": "Content-Type",
  };
  return new Response(body, { status, headers });
}
