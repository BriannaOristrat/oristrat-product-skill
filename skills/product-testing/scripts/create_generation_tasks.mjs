import { createHash } from "node:crypto";
import { mkdir, writeFile } from "node:fs/promises";
import { join } from "node:path";

const config = {
  baseUrl: process.env.BASE_URL || "http://103.39.67.155:8999",
  apiPrefix: process.env.API_PREFIX || "/api/service",
  tenantCode: (process.env.TENANT_CODE || "").toLowerCase(),
  account: process.env.ACCOUNT || "",
  password: process.env.PASSWORD || "",
  imageCount: Number(process.env.IMAGE_TASK_COUNT || 30),
  videoCount: Number(process.env.VIDEO_TASK_COUNT || 30),
  delayMs: Number(process.env.TASK_DELAY_MS || 250),
  outputDir:
    process.env.TASK_OUTPUT_DIR ||
    join(process.cwd(), "evidence", "playwright_logs"),
  dryRun: process.env.TASK_DRY_RUN === "1",
};

if (!config.tenantCode || !config.account || !config.password) {
  throw new Error("Missing TENANT_CODE, ACCOUNT, or PASSWORD.");
}

const md5 = (value) => createHash("md5").update(value).digest("hex");
const sleep = (ms) => new Promise((resolve) => setTimeout(resolve, ms));

function unwrapModel(payload) {
  return payload?.model && typeof payload.model === "object" ? payload.model : payload;
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
  const payload = await response.json().catch(() => ({}));
  const model = unwrapModel(payload);
  const cookie = (response.headers.get("set-cookie") || "").split(";")[0];
  if (!response.ok || !cookie || model?.success === false) {
    throw new Error(`Login failed: ${JSON.stringify(model)}`);
  }
  return { cookie, loginModel: model };
}

async function api(cookie, path, body = {}) {
  const started = Date.now();
  const response = await fetch(`${config.baseUrl}${path}`, {
    method: "POST",
    headers: {
      "content-type": "application/json",
      cookie,
    },
    body: JSON.stringify(body),
  });
  const text = await response.text();
  let payload;
  try {
    payload = JSON.parse(text);
  } catch {
    payload = { raw: text };
  }
  const model = unwrapModel(payload);
  return {
    ok: response.ok && model?.success !== false,
    status: response.status,
    latencyMs: Date.now() - started,
    model,
  };
}

function pickOrgCode(treeModel) {
  const data = treeModel?.data ?? treeModel?.result ?? treeModel?.list ?? treeModel;
  const stack = Array.isArray(data) ? [...data] : data ? [data] : [];
  while (stack.length) {
    const node = stack.shift();
    const code = node?.orgCode || node?.code || node?.value;
    if (code) return code;
    const children = node?.children || node?.list || [];
    if (Array.isArray(children)) stack.push(...children);
  }
  return "org-root";
}

function subjectImage(seed, kind) {
  return {
    url: `https://api.dicebear.com/9.x/shapes/png?seed=item-${kind}-${seed}&size=768`,
    name: `验收主体图-${kind}-${String(seed).padStart(2, "0")}`,
  };
}

function imageTaskBody(orgCode, index) {
  return {
    tenantCode: config.tenantCode,
    orgCode,
    taskName: `验收图生图任务-${String(index).padStart(2, "0")}`,
    subjectImages: [subjectImage(index, "image")],
    motionDesc: `交付验收图生图任务 ${index}：保持主体轮廓，生成明亮产品展示背景，画面干净，细节清晰。`,
    model: "wan2.7-image",
    duration: "",
    aspect: "16:9",
    quality: "2K",
    skillCode: "",
  };
}

function videoTaskBody(orgCode, index) {
  return {
    tenantCode: config.tenantCode,
    orgCode,
    taskName: `验收图生视频任务-${String(index).padStart(2, "0")}`,
    subjectImages: [subjectImage(index, "video")],
    motionDesc: `交付验收图生视频任务 ${index}：镜头缓慢推进，主体稳定居中，光线自然，产品质感清晰。`,
    model: "happyhorse-1.1-i2v",
    duration: "5s",
    aspect: "16:9",
    quality: "1080P",
    resolution: "1080P",
    skillCode: "",
  };
}

async function createTasks(cookie, type, count, orgCode) {
  const path =
    type === "image" ? `${config.apiPrefix}/agent/img/2/img/generate` : `${config.apiPrefix}/agent/img/2/video/generate`;
  const bodyFactory = type === "image" ? imageTaskBody : videoTaskBody;
  const rows = [];
  for (let index = 1; index <= count; index += 1) {
    const body = bodyFactory(orgCode, index);
    if (config.dryRun) {
      rows.push({ type, index, ok: true, dryRun: true, request: body });
      continue;
    }
    const result = await api(cookie, path, body);
    rows.push({
      type,
      index,
      ok: result.ok,
      status: result.status,
      latencyMs: result.latencyMs,
      code: result.model?.code,
      message: result.model?.message || result.model?.msg || "",
      materialCode: result.model?.data?.materialCode || result.model?.data?.material_code || result.model?.data?.code || "",
      traceCode: result.model?.data?.traceCode || result.model?.data?.trace_code || "",
      taskName: body.taskName,
    });
    await sleep(config.delayMs);
  }
  return rows;
}

async function verify(cookie) {
  const [imageList, videoList, history] = await Promise.all([
    api(cookie, `${config.apiPrefix}/agent/assets/material/list`, {
      tenantCode: config.tenantCode,
      sourceType: "image",
      status: "",
      orgCode: "",
      keyword: "验收图生图任务",
      page: 1,
      pageSize: 100,
    }),
    api(cookie, `${config.apiPrefix}/agent/assets/material/list`, {
      tenantCode: config.tenantCode,
      sourceType: "video",
      status: "",
      orgCode: "",
      keyword: "验收图生视频任务",
      page: 1,
      pageSize: 100,
    }),
    api(cookie, `${config.apiPrefix}/agent/assets/history/list`, {
      tenantCode: config.tenantCode,
      status: "",
      duration: "",
      aspect: "",
      keyword: "验收",
      page: 1,
      pageSize: 100,
    }),
  ]);
  return { imageList, videoList, history };
}

await mkdir(config.outputDir, { recursive: true });
const { cookie, loginModel } = await login();
const orgTree = await api(cookie, `${config.apiPrefix}/tenant/org/tree`, { tenantCode: config.tenantCode });
const orgCode = pickOrgCode(orgTree.model);

const startedAt = new Date().toISOString();
const imageTasks = await createTasks(cookie, "image", config.imageCount, orgCode);
const videoTasks = await createTasks(cookie, "video", config.videoCount, orgCode);
const verification = config.dryRun ? null : await verify(cookie);
const endedAt = new Date().toISOString();

const summary = {
  startedAt,
  endedAt,
  dryRun: config.dryRun,
  tenantCode: "[TENANT]",
  account: "[ACCOUNT]",
  orgCode,
  requested: {
    image: config.imageCount,
    video: config.videoCount,
  },
  created: {
    image: imageTasks.filter((row) => row.ok).length,
    video: videoTasks.filter((row) => row.ok).length,
  },
  failed: {
    image: imageTasks.filter((row) => !row.ok).length,
    video: videoTasks.filter((row) => !row.ok).length,
  },
  login: {
    success: loginModel?.success,
    code: loginModel?.code,
    nickname: loginModel?.nickname,
  },
  tasks: [...imageTasks, ...videoTasks],
  verification,
};

const outputPath = join(config.outputDir, "generation_task_creation.json");
await writeFile(outputPath, JSON.stringify(summary, null, 2), "utf8");
console.log(JSON.stringify({ outputPath, created: summary.created, failed: summary.failed, dryRun: summary.dryRun }));
