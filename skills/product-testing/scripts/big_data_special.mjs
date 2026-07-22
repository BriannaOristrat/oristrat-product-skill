import { createHash } from "node:crypto";
import { mkdir, writeFile } from "node:fs/promises";
import { join } from "node:path";

const config = {
  baseUrl: process.env.BASE_URL || "http://103.39.67.155:8999",
  apiPrefix: process.env.API_PREFIX || "/api/service",
  tenantCode: (process.env.TENANT_CODE || "").toLowerCase(),
  account: process.env.ACCOUNT || "",
  password: process.env.PASSWORD || "",
  roleCount: Number(process.env.BIGDATA_ROLE_COUNT || 120),
  orgCount: Number(process.env.BIGDATA_ORG_COUNT || 120),
  batchSize: Number(process.env.BIGDATA_BATCH_SIZE || 12),
  prefix: process.env.BIGDATA_PREFIX || `验收大数据-${new Date().toISOString().replace(/[-:.TZ]/g, "").slice(0, 14)}`,
  outputDir:
    process.env.BIGDATA_OUTPUT_DIR ||
    join(process.cwd(), "evidence", "playwright_logs"),
  probeOnly: process.env.BIGDATA_PROBE_ONLY === "1",
};

if (!config.tenantCode || !config.account || !config.password) {
  throw new Error("Missing TENANT_CODE, ACCOUNT, or PASSWORD.");
}

const md5 = (value) => createHash("md5").update(value).digest("hex");
const sleep = (ms) => new Promise((resolve) => setTimeout(resolve, ms));

function unwrapModel(payload) {
  return payload?.model && typeof payload.model === "object" ? payload.model : payload;
}

function sanitizeModel(model) {
  if (!model || typeof model !== "object") return model;
  const text = JSON.stringify(model)
    .replaceAll(config.account, "[ACCOUNT]")
    .replaceAll(config.password, "[PASSWORD]")
    .replaceAll(config.tenantCode, "[TENANT]");
  return JSON.parse(text);
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
    throw new Error(`Login failed: ${JSON.stringify(sanitizeModel(model))}`);
  }
  return { cookie, model };
}

async function api(cookie, path, body = {}, method = "POST") {
  const started = Date.now();
  const response = await fetch(`${config.baseUrl}${path}`, {
    method,
    headers: {
      "content-type": "application/json",
      cookie,
    },
    body: method === "GET" ? undefined : JSON.stringify(body),
  });
  const text = await response.text();
  let parsed;
  try {
    parsed = JSON.parse(text);
  } catch {
    parsed = { raw: text.slice(0, 500) };
  }
  const model = unwrapModel(parsed);
  return {
    ok: response.ok && model?.success !== false,
    status: response.status,
    latencyMs: Date.now() - started,
    model,
  };
}

function getRows(model) {
  const data = model?.data ?? model?.result ?? model;
  if (Array.isArray(data)) return data;
  if (Array.isArray(data?.roles)) return data.roles;
  if (Array.isArray(data?.users)) return data.users;
  if (Array.isArray(data?.list)) return data.list;
  if (Array.isArray(data?.rows)) return data.rows;
  if (Array.isArray(data?.records)) return data.records;
  return [];
}

function getTotal(model) {
  const data = model?.data ?? model?.result ?? model;
  return Number(data?.total ?? data?.count ?? getRows(model).length ?? 0);
}

function flattenOrgTree(model) {
  const data = model?.data ?? model?.result ?? model;
  const roots = Array.isArray(data?.tree)
    ? data.tree
    : Array.isArray(data?.list)
      ? data.list
      : Array.isArray(data)
        ? data
        : data?.tree
          ? [data.tree]
          : [];
  const rows = [];
  const stack = [...roots];
  while (stack.length) {
    const node = stack.shift();
    rows.push(node);
    const children = node?.children || node?.list || [];
    if (Array.isArray(children)) stack.push(...children);
  }
  return rows;
}

function pickRootOrgCode(model) {
  const nodes = flattenOrgTree(model);
  return nodes[0]?.orgCode || nodes[0]?.code || "org-root";
}

function roleCode(index) {
  return `${config.prefix}-角色-${String(index).padStart(4, "0")}`;
}

function orgName(index) {
  return `${config.prefix}-组织-${String(index).padStart(4, "0")}`;
}

async function runLimited(items, limit, worker) {
  const results = [];
  let cursor = 0;
  async function next() {
    while (cursor < items.length) {
      const index = cursor;
      cursor += 1;
      results[index] = await worker(items[index], index);
    }
  }
  await Promise.all(Array.from({ length: Math.min(limit, items.length) }, next));
  return results;
}

function compactResult(action, name, result) {
  return {
    action,
    name,
    ok: result.ok,
    status: result.status,
    latencyMs: result.latencyMs,
    code: result.model?.code,
    message: result.model?.message || result.model?.msg || "",
    data: sanitizeModel(result.model?.data ?? result.model ?? null),
  };
}

async function createRoles(cookie, count) {
  const indexes = Array.from({ length: count }, (_, index) => index + 1);
  return runLimited(indexes, config.batchSize, async (index) => {
    const code = roleCode(index);
    const result = await api(cookie, `${config.apiPrefix}/tenant/role/operation`, {
      tenantCode: config.tenantCode,
      op: "create",
      code,
      name: code,
      status: 1,
      permissionIds: [],
      orgCodes: [],
      userIds: [],
    });
    return compactResult("create_role", code, result);
  });
}

async function deleteRole(cookie, role) {
  const result = await api(cookie, `${config.apiPrefix}/tenant/role/operation`, {
    tenantCode: config.tenantCode,
    op: "delete",
    code: role.code || role.roleCode || role.name,
    roleId: role.id || role.roleId,
    id: role.id || role.roleId,
  });
  return compactResult("delete_role", role.code || role.roleCode || role.name || String(role.id || ""), result);
}

async function listRoles(cookie, keyword = "", page = 1, pageSize = 50) {
  return api(cookie, `${config.apiPrefix}/tenant/role/list`, {
    tenantCode: config.tenantCode,
    keyword,
    status: 0,
    page,
    pageSize,
  });
}

async function createOrgParent(cookie, rootOrgCode) {
  const result = await api(cookie, `${config.apiPrefix}/tenant/org/operation`, {
    tenantCode: config.tenantCode,
    op: "create",
    parentOrgCode: rootOrgCode,
    orgName: `${config.prefix}-组织父级`,
    orgCode: `${config.prefix}-org-parent`,
    levelName: "验收父级",
    managerName: "验收",
    status: 1,
  });
  return compactResult("create_org_parent", `${config.prefix}-组织父级`, result);
}

async function createOrgs(cookie, parentOrgCode, count) {
  const indexes = Array.from({ length: count }, (_, index) => index + 1);
  return runLimited(indexes, 1, async (index) => {
    const name = orgName(index);
    const result = await api(cookie, `${config.apiPrefix}/tenant/org/operation`, {
      tenantCode: config.tenantCode,
      op: "create",
      parentOrgCode,
      orgName: name,
      orgCode: `${config.prefix}-org-${String(index).padStart(4, "0")}`,
      levelName: "验收组织",
      managerName: "验收",
      status: 1,
    });
    return compactResult("create_org", name, result);
  });
}

async function deleteOrg(cookie, orgCode, name) {
  const result = await api(cookie, `${config.apiPrefix}/tenant/org/operation`, {
    tenantCode: config.tenantCode,
    op: "delete",
    orgCode,
  });
  return compactResult("delete_org", name || orgCode, result);
}

async function tree(cookie) {
  return api(cookie, `${config.apiPrefix}/tenant/org/tree`, { tenantCode: config.tenantCode });
}

function summarizeTimings(rows) {
  const latencies = rows.filter((row) => Number.isFinite(row.latencyMs)).map((row) => row.latencyMs).sort((a, b) => a - b);
  if (!latencies.length) return { count: 0, avgMs: 0, p95Ms: 0, maxMs: 0 };
  const sum = latencies.reduce((acc, value) => acc + value, 0);
  const pick = (p) => latencies[Math.min(latencies.length - 1, Math.ceil(latencies.length * p) - 1)];
  return {
    count: latencies.length,
    avgMs: Math.round(sum / latencies.length),
    p95Ms: pick(0.95),
    maxMs: latencies[latencies.length - 1],
  };
}

await mkdir(config.outputDir, { recursive: true });

const startedAt = new Date().toISOString();
const { cookie, model: loginModel } = await login();

const baselineRoleList = await listRoles(cookie, "", 1, 50);
const baselineTree = await tree(cookie);
const rootOrgCode = pickRootOrgCode(baselineTree.model);

const probeRoleCode = roleCode(0);
const probeRoleCreate = compactResult(
  "probe_create_role",
  probeRoleCode,
  await api(cookie, `${config.apiPrefix}/tenant/role/operation`, {
    tenantCode: config.tenantCode,
    op: "create",
    code: probeRoleCode,
    name: probeRoleCode,
    status: 1,
    permissionIds: [],
    orgCodes: [],
    userIds: [],
  }),
);
const probeRoleList = await listRoles(cookie, probeRoleCode, 1, 10);
const probeRoleRows = getRows(probeRoleList.model);
const probeRole = probeRoleRows.find((row) => [row?.code, row?.roleCode, row?.name].includes(probeRoleCode)) || probeRoleRows[0];
const probeRoleDelete = probeRole ? await deleteRole(cookie, probeRole) : { action: "delete_role", name: probeRoleCode, ok: false, message: "probe role not found after create" };

let createdRoleOps = [];
let createOrgParentResult = null;
let createdOrgOps = [];
let checks = {};
let cleanup = { roles: [], orgParent: null };

if (!config.probeOnly && probeRoleCreate.ok && probeRoleDelete.ok) {
  createdRoleOps = await createRoles(cookie, config.roleCount);
  createOrgParentResult = await createOrgParent(cookie, rootOrgCode);
  const orgParentCode =
    createOrgParentResult?.data?.orgCode ||
    createOrgParentResult?.data?.code ||
    `${config.prefix}-org-parent`;
  if (createOrgParentResult.ok) {
    createdOrgOps = await createOrgs(cookie, orgParentCode, config.orgCount);
  }

  const [rolePage1, rolePage2, roleSearch, roleStatistic, orgTreeAfter, orgExport] = await Promise.all([
    listRoles(cookie, "", 1, 50),
    listRoles(cookie, "", 2, 50),
    listRoles(cookie, config.prefix, 1, Math.min(200, config.roleCount + 20)),
    api(cookie, `${config.apiPrefix}/tenant/role/statistic`, { tenantCode: config.tenantCode }),
    tree(cookie),
    api(cookie, `${config.apiPrefix}/tenant/org/export`, { tenantCode: config.tenantCode }),
  ]);

  const roleSearchRows = getRows(roleSearch.model);
  const orgRows = flattenOrgTree(orgTreeAfter.model);
  const orgExportRows = getRows(orgExport.model);

  checks = {
    roleListPage1: {
      ok: rolePage1.ok,
      latencyMs: rolePage1.latencyMs,
      total: getTotal(rolePage1.model),
      rowCount: getRows(rolePage1.model).length,
    },
    roleListPage2: {
      ok: rolePage2.ok,
      latencyMs: rolePage2.latencyMs,
      total: getTotal(rolePage2.model),
      rowCount: getRows(rolePage2.model).length,
    },
    roleSearch: {
      ok: roleSearch.ok,
      latencyMs: roleSearch.latencyMs,
      total: getTotal(roleSearch.model),
      matchedPrefixRows: roleSearchRows.filter((row) => [row?.code, row?.roleCode, row?.name].some((value) => String(value || "").includes(config.prefix))).length,
    },
    roleStatistic: {
      ok: roleStatistic.ok,
      latencyMs: roleStatistic.latencyMs,
      data: sanitizeModel(roleStatistic.model?.data ?? roleStatistic.model),
    },
    orgTree: {
      ok: orgTreeAfter.ok,
      latencyMs: orgTreeAfter.latencyMs,
      totalNodes: orgRows.length,
      matchedPrefixNodes: orgRows.filter((row) => String(row?.orgName || row?.name || row?.orgCode || "").includes(config.prefix)).length,
    },
    orgExport: {
      ok: orgExport.ok,
      latencyMs: orgExport.latencyMs,
      exportedRows: orgExportRows.length,
      matchedPrefixRows: orgExportRows.filter((row) => String(row?.orgName || row?.name || row?.orgCode || "").includes(config.prefix)).length,
    },
  };

  const createdRoleRows = getRows((await listRoles(cookie, config.prefix, 1, Math.min(500, config.roleCount + 50))).model);
  cleanup.roles = await runLimited(
    createdRoleRows.filter((row) => [row?.code, row?.roleCode, row?.name].some((value) => String(value || "").includes(config.prefix))),
    config.batchSize,
    (role) => deleteRole(cookie, role),
  );
  cleanup.orgParent = createOrgParentResult.ok ? await deleteOrg(cookie, orgParentCode, `${config.prefix}-组织父级`) : null;
}

const finalRoleSearch = await listRoles(cookie, config.prefix, 1, 50);
const finalTree = await tree(cookie);
const finalOrgRows = flattenOrgTree(finalTree.model);

const endedAt = new Date().toISOString();
const summary = {
  startedAt,
  endedAt,
  tenantCode: "[TENANT]",
  account: "[ACCOUNT]",
  prefix: config.prefix,
  probeOnly: config.probeOnly,
  requested: {
    roles: config.roleCount,
    orgs: config.orgCount,
  },
  baseline: {
    roles: {
      ok: baselineRoleList.ok,
      total: getTotal(baselineRoleList.model),
      rowCount: getRows(baselineRoleList.model).length,
      latencyMs: baselineRoleList.latencyMs,
    },
    orgs: {
      ok: baselineTree.ok,
      totalNodes: flattenOrgTree(baselineTree.model).length,
      rootOrgCode,
      latencyMs: baselineTree.latencyMs,
    },
  },
  probe: {
    createRole: probeRoleCreate,
    listRole: {
      ok: probeRoleList.ok,
      latencyMs: probeRoleList.latencyMs,
      total: getTotal(probeRoleList.model),
      rowCount: probeRoleRows.length,
    },
    deleteRole: probeRoleDelete,
  },
  created: {
    roles: createdRoleOps.filter((row) => row.ok).length,
    orgs: createdOrgOps.filter((row) => row.ok).length + (createOrgParentResult?.ok ? 1 : 0),
  },
  failed: {
    roles: createdRoleOps.filter((row) => !row.ok).length,
    orgs: createdOrgOps.filter((row) => !row.ok).length + (createOrgParentResult && !createOrgParentResult.ok ? 1 : 0),
  },
  checks,
  cleanup: {
    rolesDeleted: cleanup.roles.filter((row) => row.ok).length,
    roleDeleteFailed: cleanup.roles.filter((row) => !row.ok).length,
    orgParentDeleted: cleanup.orgParent?.ok ?? null,
    orgParentCleanup: cleanup.orgParent,
  },
  final: {
    rolePrefixRemaining: getTotal(finalRoleSearch.model),
    orgPrefixRemaining: finalOrgRows.filter((row) => String(row?.orgName || row?.name || row?.orgCode || "").includes(config.prefix)).length,
  },
  timings: {
    createRoles: summarizeTimings(createdRoleOps),
    createOrgs: summarizeTimings(createdOrgOps),
    cleanupRoles: summarizeTimings(cleanup.roles),
  },
  samples: {
    createRoles: createdRoleOps.slice(0, 5),
    createOrgs: createdOrgOps.slice(0, 5),
    cleanupRoles: cleanup.roles.slice(0, 5),
  },
  operations: {
    createRoles: createdRoleOps,
    createOrgs: createdOrgOps,
    cleanupRoles: cleanup.roles,
  },
  login: {
    success: loginModel?.success,
    code: loginModel?.code,
    nickname: loginModel?.nickname,
  },
};

const outputPath = join(config.outputDir, "big_data_special.json");
await writeFile(outputPath, JSON.stringify(summary, null, 2), "utf8");
console.log(JSON.stringify({
  outputPath,
  prefix: summary.prefix,
  probeOnly: summary.probeOnly,
  created: summary.created,
  failed: summary.failed,
  cleanup: summary.cleanup,
  final: summary.final,
}));
