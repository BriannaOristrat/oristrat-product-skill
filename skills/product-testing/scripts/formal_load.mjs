import { createHash } from "node:crypto";
import { mkdir, writeFile } from "node:fs/promises";
import { join } from "node:path";

const config = {
  baseUrl: process.env.BASE_URL || "http://103.39.67.155:8999",
  apiPrefix: process.env.API_PREFIX || "/api/service",
  account: process.env.ACCOUNT || "",
  password: process.env.PASSWORD || "",
  tenantCode: (process.env.TENANT_CODE || "").toLowerCase(),
  vus: Number(process.env.LOAD_VUS || 100),
  durationSec: Number(process.env.LOAD_DURATION_SEC || 7200),
  rampUpSec: Number(process.env.LOAD_RAMP_UP_SEC || 300),
  rampDownSec: Number(process.env.LOAD_RAMP_DOWN_SEC || 300),
  thinkMsMin: Number(process.env.LOAD_THINK_MS_MIN || 250),
  thinkMsMax: Number(process.env.LOAD_THINK_MS_MAX || 1000),
  p95ThresholdMs: Number(process.env.LOAD_P95_THRESHOLD_MS || 2000),
  errorRateThreshold: Number(process.env.LOAD_ERROR_RATE_THRESHOLD || 0.001),
  progressIntervalSec: Number(process.env.LOAD_PROGRESS_INTERVAL_SEC || 30),
  failureSampleLimit: Number(process.env.LOAD_FAILURE_SAMPLE_LIMIT || 200),
  failureBodyMaxChars: Number(process.env.LOAD_FAILURE_BODY_MAX_CHARS || 1200),
  outputDir:
    process.env.LOAD_OUTPUT_DIR ||
    join(process.cwd(), "evidence", "performance_results"),
};

if (!config.account || !config.password || !config.tenantCode) {
  throw new Error("Missing ACCOUNT, PASSWORD, or TENANT_CODE.");
}

const scenarios = [
  {
    name: "session",
    weight: 5,
    method: "GET",
    path: `${config.apiPrefix}/tenant/main/session`,
  },
  {
    name: "workbench_statistic",
    weight: 15,
    method: "POST",
    path: `${config.apiPrefix}/tenant/workbench/statistic`,
    body: () => ({ tenantCode: config.tenantCode }),
  },
  {
    name: "user_list",
    weight: 15,
    method: "POST",
    path: `${config.apiPrefix}/tenant/main/user/list`,
    body: () => ({
      tenantCode: config.tenantCode,
      keyword: "",
      status: 0,
      roleCode: null,
      page: 1,
      pageSize: 10,
    }),
  },
  {
    name: "org_tree",
    weight: 10,
    method: "POST",
    path: `${config.apiPrefix}/tenant/org/tree`,
    body: () => ({ tenantCode: config.tenantCode }),
  },
  {
    name: "role_list",
    weight: 10,
    method: "POST",
    path: `${config.apiPrefix}/tenant/role/list`,
    body: () => ({
      tenantCode: config.tenantCode,
      keyword: "",
      status: 0,
      page: 1,
      pageSize: 10,
    }),
  },
  {
    name: "role_statistic",
    weight: 5,
    method: "POST",
    path: `${config.apiPrefix}/tenant/role/statistic`,
    body: () => ({ tenantCode: config.tenantCode }),
  },
  {
    name: "log_statistic",
    weight: 10,
    method: "POST",
    path: `${config.apiPrefix}/tenant/log/statistic`,
    body: () => ({ keyword: "", type: "", startTime: "", endTime: "" }),
  },
  {
    name: "log_list",
    weight: 15,
    method: "POST",
    path: `${config.apiPrefix}/tenant/log/list`,
    body: () => ({
      keyword: "",
      type: "",
      result: "",
      risk: "",
      startTime: "",
      endTime: "",
      page: 1,
      pageSize: 50,
    }),
  },
  {
    name: "llms_model_list",
    weight: 5,
    method: "POST",
    path: `${config.apiPrefix}/tenant/llms/model/list`,
    body: () => ({}),
  },
  {
    name: "assets_material_list",
    weight: 10,
    method: "POST",
    path: `${config.apiPrefix}/agent/assets/material/list`,
    body: () => ({ type: "", status: "", page: 1, pageSize: 10 }),
  },
];

const weightedScenarios = scenarios.flatMap((scenario) =>
  Array.from({ length: scenario.weight }, () => scenario),
);

const sleep = (ms) => new Promise((resolve) => setTimeout(resolve, ms));
const md5 = (value) => createHash("md5").update(value).digest("hex");
const nowIso = () => new Date().toISOString();
const FAILURE_RESPONSE_FILE = "formal_load_failure_responses.json";

function sanitizeText(value) {
  return String(value ?? "")
    .replaceAll(config.account, "[ACCOUNT]")
    .replaceAll(config.password, "[PASSWORD]")
    .replaceAll(config.tenantCode, "[TENANT]");
}

function truncateText(value, maxChars = config.failureBodyMaxChars) {
  const text = sanitizeText(value);
  if (text.length <= maxChars) return text;
  return `${text.slice(0, maxChars)}... [truncated ${text.length - maxChars} chars]`;
}

function selectedHeaders(headers) {
  const out = {};
  const blocked = new Set(["set-cookie", "cookie", "authorization"]);
  for (const [key, value] of headers.entries()) {
    const normalized = key.toLowerCase();
    if (!blocked.has(normalized)) out[normalized] = truncateText(value, 300);
  }
  return out;
}

function parsedSummary(parsed) {
  const model = unwrapModel(parsed);
  if (!model || typeof model !== "object") return null;
  return {
    success: model.success,
    code: model.code,
    message: truncateText(model.message || ""),
    messageKey: truncateText(model.messageKey || ""),
  };
}

function unwrapModel(payload) {
  return payload?.model && typeof payload.model === "object" ? payload.model : payload;
}

function errorDetails(error) {
  const cause = error?.cause;
  return {
    name: error?.name || "",
    message: truncateText(error?.message || String(error)),
    cause: cause
      ? {
          name: cause.name || "",
          code: cause.code || "",
          message: truncateText(cause.message || ""),
        }
      : null,
  };
}

function percentile(values, p) {
  if (values.length === 0) return 0;
  const sorted = [...values].sort((a, b) => a - b);
  const index = Math.min(sorted.length - 1, Math.ceil(sorted.length * p) - 1);
  return sorted[index];
}

function summarizeLatencies(values) {
  if (values.length === 0) {
    return { count: 0, avgMs: 0, minMs: 0, p50Ms: 0, p95Ms: 0, p99Ms: 0, maxMs: 0 };
  }

  const total = values.reduce((sum, value) => sum + value, 0);
  const sorted = [...values].sort((a, b) => a - b);
  const pick = (p) => {
    const index = Math.min(sorted.length - 1, Math.ceil(sorted.length * p) - 1);
    return sorted[index];
  };

  return {
    count: values.length,
    avgMs: Math.round(total / values.length),
    minMs: sorted[0],
    p50Ms: pick(0.5),
    p95Ms: pick(0.95),
    p99Ms: pick(0.99),
    maxMs: sorted[sorted.length - 1],
  };
}

function targetVusForElapsed(elapsedMs) {
  const elapsedSec = elapsedMs / 1000;
  const steadyEnd = Math.max(config.rampUpSec, config.durationSec - config.rampDownSec);

  if (elapsedSec < config.rampUpSec) {
    return Math.max(1, Math.ceil((elapsedSec / config.rampUpSec) * config.vus));
  }

  if (elapsedSec >= steadyEnd && config.rampDownSec > 0) {
    const remaining = Math.max(0, config.durationSec - elapsedSec);
    return Math.max(0, Math.ceil((remaining / config.rampDownSec) * config.vus));
  }

  return config.vus;
}

function pickScenario(workerId, iteration) {
  const index = (workerId * 17 + iteration * 13) % weightedScenarios.length;
  return weightedScenarios[index];
}

function thinkTime(workerId, iteration) {
  const span = Math.max(0, config.thinkMsMax - config.thinkMsMin);
  return config.thinkMsMin + ((workerId * 97 + iteration * 37) % (span + 1));
}

async function login() {
  const response = await fetch(`${config.baseUrl}${config.apiPrefix}/tenant/main/login`, {
    method: "POST",
    headers: { "content-type": "application/json" },
    body: JSON.stringify({
      loginType: "password",
      accountType: 2,
      account: config.account,
      password: md5(config.password),
      code: "",
      codeType: "",
      tenantCode: config.tenantCode,
    }),
  });

  const text = await response.text();
  let parsed;
  try {
    parsed = JSON.parse(text);
  } catch {
    throw new Error(`Login returned non-JSON response: HTTP ${response.status}`);
  }

  const model = unwrapModel(parsed);
  if (!response.ok || model?.success === false) {
    throw new Error(`Login failed: HTTP ${response.status}, ${model.message || text.slice(0, 200)}`);
  }

  const setCookie = response.headers.get("set-cookie") || "";
  const cookie = setCookie.split(/,(?=\s*[^;]+=)/).map((part) => part.trim().split(";")[0]).filter(Boolean).join("; ");
  if (!cookie) throw new Error("Login succeeded but no cookie was returned.");

  return { cookie, loginModel: model };
}

const state = {
  startedAt: nowIso(),
  activeWorkers: 0,
  spawnedWorkers: 0,
  stop: false,
  total: 0,
  success: 0,
  failed: 0,
  slowOverThreshold: 0,
  latencies: [],
  failures: [],
  failureResponses: [],
  scenarios: Object.fromEntries(
    scenarios.map((scenario) => [
      scenario.name,
      { total: 0, success: 0, failed: 0, latencies: [] },
    ]),
  ),
  minuteBuckets: [],
};

let cookie = "";

async function requestScenario(scenario) {
  const started = Date.now();
  let status = 0;
  let ok = false;
  let message = "";
  let responseText = "";
  let responseHeaders = {};
  let parsed = null;
  let failureKind = "";
  let requestError = null;

  try {
    const response = await fetch(`${config.baseUrl}${scenario.path}`, {
      method: scenario.method,
      headers: {
        "content-type": "application/json",
        cookie,
      },
      body: scenario.method === "GET" ? undefined : JSON.stringify(scenario.body?.() ?? {}),
    });

    status = response.status;
    responseHeaders = selectedHeaders(response.headers);
    responseText = await response.text();
    try {
      parsed = JSON.parse(responseText);
    } catch {
      message = `non-json response: ${responseText.slice(0, 120)}`;
    }

    const model = unwrapModel(parsed);
    ok = response.ok && model?.success !== false;
    if (!ok) {
      message = model?.message || model?.messageKey || `HTTP ${status}`;
      failureKind = response.ok ? "business_failure_response" : "http_failure_response";
    }
  } catch (error) {
    message = error?.message || String(error);
    failureKind = "request_exception_no_response";
    requestError = errorDetails(error);
  }

  const latencyMs = Date.now() - started;
  const scenarioStats = state.scenarios[scenario.name];
  state.total += 1;
  scenarioStats.total += 1;
  state.latencies.push(latencyMs);
  scenarioStats.latencies.push(latencyMs);

  if (latencyMs > config.p95ThresholdMs) state.slowOverThreshold += 1;

  if (ok) {
    state.success += 1;
    scenarioStats.success += 1;
  } else {
    state.failed += 1;
    scenarioStats.failed += 1;
    if (state.failures.length < 100) {
      state.failures.push({
        at: nowIso(),
        scenario: scenario.name,
        status,
        latencyMs,
        message,
      });
    }
    if (state.failureResponses.length < config.failureSampleLimit) {
      state.failureResponses.push({
        at: nowIso(),
        scenario: scenario.name,
        method: scenario.method,
        path: scenario.path,
        status,
        latencyMs,
        kind: failureKind || "unknown_failure",
        message: truncateText(message),
        response:
          status > 0
            ? {
                headers: responseHeaders,
                bodyLength: responseText.length,
                bodySnippet: truncateText(responseText),
                parsedSummary: parsedSummary(parsed),
              }
            : null,
        error: status > 0 ? null : requestError,
      });
    }
  }
}

async function worker(workerId, startedAtMs, endAtMs) {
  state.activeWorkers += 1;
  let iteration = 0;
  while (!state.stop && Date.now() < endAtMs) {
    const desired = targetVusForElapsed(Date.now() - startedAtMs);
    if (workerId > desired) {
      await sleep(500);
      continue;
    }

    const scenario = pickScenario(workerId, iteration);
    await requestScenario(scenario);
    await sleep(thinkTime(workerId, iteration));
    iteration += 1;
  }
  state.activeWorkers -= 1;
}

function buildSummary(completed = false) {
  const elapsedMs = Date.now() - startedAtMsGlobal;
  const latencySummary = summarizeLatencies(state.latencies);
  const errorRate = state.total === 0 ? 0 : state.failed / state.total;
  const thresholdPass =
    completed &&
    latencySummary.p95Ms <= config.p95ThresholdMs &&
    errorRate <= config.errorRateThreshold;

  return {
    completed,
    startedAt: state.startedAt,
    endedAt: completed ? nowIso() : null,
    elapsedSec: Math.round(elapsedMs / 1000),
    config: {
      ...config,
      account: "[REDACTED]",
      password: "[REDACTED]",
    },
    thresholds: {
      p95ThresholdMs: config.p95ThresholdMs,
      errorRateThreshold: config.errorRateThreshold,
    },
    totals: {
      requests: state.total,
      success: state.success,
      failed: state.failed,
      errorRate: Number(errorRate.toFixed(6)),
      slowOverThreshold: state.slowOverThreshold,
      slowOverThresholdRate: state.total === 0 ? 0 : Number((state.slowOverThreshold / state.total).toFixed(6)),
      rps: Number((state.total / Math.max(1, elapsedMs / 1000)).toFixed(2)),
      activeWorkers: state.activeWorkers,
      spawnedWorkers: state.spawnedWorkers,
    },
    latency: latencySummary,
    scenarioStats: Object.fromEntries(
      Object.entries(state.scenarios).map(([name, stats]) => [
        name,
        {
          total: stats.total,
          success: stats.success,
          failed: stats.failed,
          errorRate: stats.total === 0 ? 0 : Number((stats.failed / stats.total).toFixed(6)),
          latency: summarizeLatencies(stats.latencies),
        },
      ]),
    ),
    failures: state.failures,
    failureResponseEvidence: {
      file: FAILURE_RESPONSE_FILE,
      sampleCount: state.failureResponses.length,
      sampleLimit: config.failureSampleLimit,
      bodyMaxChars: config.failureBodyMaxChars,
    },
    conclusion: completed
      ? {
          passed: thresholdPass,
          reason: thresholdPass
            ? "整体 P95 与错误率均满足严格验收档默认阈值"
            : "整体 P95 或错误率未满足严格验收档默认阈值",
        }
      : null,
  };
}

function buildCleanSummary(summary) {
  return {
    ...summary,
    config: {
      ...summary.config,
      outputDir: String(summary.config.outputDir || "").replaceAll("\\", "/"),
    },
  };
}

async function writeProgress(completed = false) {
  const summary = buildSummary(completed);
  const cleanSummary = buildCleanSummary(summary);
  await writeFile(join(config.outputDir, "formal_load_latest.json"), JSON.stringify(cleanSummary, null, 2), "utf8");
  await writeFile(join(config.outputDir, FAILURE_RESPONSE_FILE), JSON.stringify(state.failureResponses, null, 2), "utf8");
  if (completed) {
    await writeFile(join(config.outputDir, "formal_load_summary.json"), JSON.stringify(cleanSummary, null, 2), "utf8");
    await writeFile(join(config.outputDir, "formal_load_clean_summary.json"), JSON.stringify(cleanSummary, null, 2), "utf8");
  }
  return cleanSummary;
}

await mkdir(config.outputDir, { recursive: true });

const auth = await login();
cookie = auth.cookie;
await writeFile(
  join(config.outputDir, "formal_load_auth_check.json"),
  JSON.stringify(
    {
      at: nowIso(),
      baseUrl: config.baseUrl,
      tenantCode: config.tenantCode,
      login: {
        success: auth.loginModel.success,
        code: auth.loginModel.code,
        nickname: auth.loginModel.nickname,
        tenantCode: auth.loginModel.tenantCode,
        expiresIn: auth.loginModel.expiresIn,
      },
      cookiePresent: true,
    },
    null,
    2,
  ),
  "utf8",
);

const startedAtMsGlobal = Date.now();
const endAtMs = startedAtMsGlobal + config.durationSec * 1000;
const workerPromises = [];

const progressTimer = setInterval(async () => {
  try {
    const summary = await writeProgress(false);
    const bucket = {
      at: nowIso(),
      elapsedSec: summary.elapsedSec,
      requests: summary.totals.requests,
      success: summary.totals.success,
      failed: summary.totals.failed,
      errorRate: summary.totals.errorRate,
      p95Ms: summary.latency.p95Ms,
      p99Ms: summary.latency.p99Ms,
      rps: summary.totals.rps,
      activeWorkers: summary.totals.activeWorkers,
    };
    state.minuteBuckets.push(bucket);
    await writeFile(join(config.outputDir, "formal_load_progress.json"), JSON.stringify(state.minuteBuckets, null, 2), "utf8");
    console.log(JSON.stringify(bucket));
  } catch (error) {
    console.error("progress write failed", error);
  }
}, config.progressIntervalSec * 1000);

while (Date.now() < endAtMs) {
  const desired = targetVusForElapsed(Date.now() - startedAtMsGlobal);
  while (state.spawnedWorkers < desired) {
    state.spawnedWorkers += 1;
    workerPromises.push(worker(state.spawnedWorkers, startedAtMsGlobal, endAtMs));
  }
  await sleep(500);
}

state.stop = true;
await Promise.all(workerPromises);
clearInterval(progressTimer);
const finalSummary = await writeProgress(true);
console.log(JSON.stringify({
  completed: true,
  requests: finalSummary.totals.requests,
  success: finalSummary.totals.success,
  failed: finalSummary.totals.failed,
  errorRate: finalSummary.totals.errorRate,
  p95Ms: finalSummary.latency.p95Ms,
  p99Ms: finalSummary.latency.p99Ms,
  maxMs: finalSummary.latency.maxMs,
  passed: finalSummary.conclusion.passed,
}));
