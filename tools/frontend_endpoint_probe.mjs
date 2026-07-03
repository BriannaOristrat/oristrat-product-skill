import { createHash } from "node:crypto";
import { mkdir, readFile, writeFile } from "node:fs/promises";
import { basename, join } from "node:path";

const baseUrl = process.env.BASE_URL || "http://103.39.67.155:8999";
const apiPrefix = process.env.API_PREFIX || "/api/service";
const tenantCode = (process.env.TENANT_CODE || "").toLowerCase();
const account = process.env.ACCOUNT || "";
const password = process.env.PASSWORD || "";
const outputDir =
  process.env.PROBE_OUTPUT_DIR ||
  join(process.cwd(), "tmp", "frontend_endpoint_probe");

if (!tenantCode || !account || !password) {
  throw new Error("Missing TENANT_CODE, ACCOUNT, or PASSWORD.");
}

const md5 = (value) => createHash("md5").update(value).digest("hex");

async function login() {
  const response = await fetch(`${baseUrl}${apiPrefix}/tenant/main/login`, {
    method: "POST",
    headers: { "content-type": "application/json" },
    body: JSON.stringify({
      loginType: "password",
      accountType: 2,
      account,
      password: md5(password),
      code: "",
      codeType: "",
      tenantCode,
    }),
  });
  const setCookie = response.headers.get("set-cookie") || "";
  const cookie = setCookie.split(";")[0];
  const body = await response.json();
  if (!response.ok || !cookie || body?.success === false) {
    throw new Error(`Login failed: ${JSON.stringify(body)}`);
  }
  return cookie;
}

function extractScriptUrls(html) {
  return [...html.matchAll(/<script[^>]+src=["']([^"']+)["']/g)].map((match) => match[1]);
}

function extractApiPaths(text) {
  return [...new Set([...text.matchAll(/\/api\/[A-Za-z0-9_-]+\/[A-Za-z0-9_/?=&:.,${}\-[\]+"'`]+/g)].map((m) => m[0]))]
    .filter((path) => /image|video|task|generate|asset|material|draw|agent|llm|skill/i.test(path))
    .sort();
}

function extractInterestingLines(text) {
  return text
    .split(/(?<=\})|(?<=;)|(?<=,)/)
    .filter((line) => /图生图|图生视频|image|video|task|generate|material|asset/i.test(line))
    .map((line) => line.trim())
    .filter(Boolean)
    .slice(0, 2000);
}

async function fetchText(url, cookie) {
  const response = await fetch(url, {
    headers: {
      cookie,
      accept: "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    },
  });
  return await response.text();
}

await mkdir(outputDir, { recursive: true });
const cookie = await login();

const pages = ["/auth/login", "/auth/main"];
const scriptUrls = new Set();
for (const page of pages) {
  const html = await fetchText(`${baseUrl}${page}`, cookie);
  const fileName = `${page.replaceAll("/", "_").replace(/^_/, "") || "root"}.html`;
  await writeFile(join(outputDir, fileName), html, "utf8");
  for (const scriptUrl of extractScriptUrls(html)) scriptUrls.add(scriptUrl);
}

const downloaded = [];
const apiPaths = new Set();
const interesting = [];
for (const scriptUrl of scriptUrls) {
  const url = new URL(scriptUrl, baseUrl).href;
  const text = await fetchText(url, cookie);
  const fileName = basename(new URL(url).pathname);
  const outPath = join(outputDir, fileName);
  await writeFile(outPath, text, "utf8");
  downloaded.push({ url, fileName, length: text.length });
  for (const apiPath of extractApiPaths(text)) apiPaths.add(apiPath);
  const lines = extractInterestingLines(text);
  if (lines.length) {
    interesting.push({ fileName, lines });
  }
}

const result = {
  at: new Date().toISOString(),
  baseUrl,
  tenantCode: "[TENANT]",
  downloaded,
  apiPaths: [...apiPaths].sort(),
  interesting,
};

const resultPath = join(outputDir, "frontend_endpoint_probe.json");
await writeFile(resultPath, JSON.stringify(result, null, 2), "utf8");
console.log(JSON.stringify({ resultPath, scripts: downloaded.length, apiPaths: result.apiPaths.length }));
