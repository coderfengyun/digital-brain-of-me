#!/usr/bin/env node

const fs = require("fs");
const path = require("path");
const http = require("http");
const crypto = require("crypto");

const repoRoot = path.resolve(__dirname, "../..");
const publicDir = __dirname;
const port = Number(process.env.PORT || 4177);

function sendJson(res, status, data) {
  res.writeHead(status, {
    "content-type": "application/json; charset=utf-8",
    "cache-control": "no-store",
  });
  res.end(JSON.stringify(data, null, 2));
}

function sendText(res, status, text, contentType = "text/plain; charset=utf-8") {
  res.writeHead(status, {
    "content-type": contentType,
    "cache-control": "no-store",
  });
  res.end(text);
}

function safeRepoPath(inputPath) {
  const clean = String(inputPath || "").replace(/^\/+/, "");
  const absolute = path.resolve(repoRoot, clean);
  if (absolute !== repoRoot && !absolute.startsWith(repoRoot + path.sep)) {
    throw new Error("Path is outside the repository");
  }
  return absolute;
}

function toRepoRelative(absolutePath) {
  return path.relative(repoRoot, absolutePath).split(path.sep).join("/");
}

function annotationPathFor(markdownPath) {
  return markdownPath.replace(/\.md$/i, "") + ".annotations.json";
}

function readBody(req) {
  return new Promise((resolve, reject) => {
    let body = "";
    req.on("data", (chunk) => {
      body += chunk;
      if (body.length > 2_000_000) {
        reject(new Error("Request body is too large"));
        req.destroy();
      }
    });
    req.on("end", () => resolve(body));
    req.on("error", reject);
  });
}

function walkMarkdownFiles(dir, results = []) {
  const ignored = new Set([".git", "node_modules", ".DS_Store"]);
  for (const entry of fs.readdirSync(dir, { withFileTypes: true })) {
    if (ignored.has(entry.name)) continue;
    const absolute = path.join(dir, entry.name);
    if (entry.isDirectory()) {
      walkMarkdownFiles(absolute, results);
    } else if (entry.isFile() && entry.name.endsWith(".md")) {
      results.push(toRepoRelative(absolute));
    }
  }
  return results;
}

function readAnnotations(markdownAbsolutePath) {
  const annotationsPath = annotationPathFor(markdownAbsolutePath);
  if (!fs.existsSync(annotationsPath)) {
    return {
      file: toRepoRelative(markdownAbsolutePath),
      version: 1,
      annotations: [],
    };
  }
  return JSON.parse(fs.readFileSync(annotationsPath, "utf8"));
}

function writeAnnotations(markdownAbsolutePath, payload) {
  const annotationsPath = annotationPathFor(markdownAbsolutePath);
  const normalized = {
    file: toRepoRelative(markdownAbsolutePath),
    version: 1,
    updated_at: new Date().toISOString(),
    annotations: Array.isArray(payload.annotations) ? payload.annotations : [],
  };
  fs.writeFileSync(annotationsPath, JSON.stringify(normalized, null, 2) + "\n");
  return normalized;
}

function createAnnotation(markdownAbsolutePath, input) {
  const current = readAnnotations(markdownAbsolutePath);
  const now = new Date().toISOString();
  const annotation = {
    id: "ann-" + now.slice(0, 10).replace(/-/g, "") + "-" + crypto.randomUUID().slice(0, 8),
    status: "open",
    created_at: now,
    updated_at: now,
    quote: String(input.quote || "").trim(),
    comment: String(input.comment || "").trim(),
    line_start: Number(input.line_start || 0),
    line_end: Number(input.line_end || input.line_start || 0),
    context_before: String(input.context_before || ""),
    context_after: String(input.context_after || ""),
  };
  current.annotations.push(annotation);
  return writeAnnotations(markdownAbsolutePath, current);
}

function updateAnnotation(markdownAbsolutePath, id, patch) {
  const current = readAnnotations(markdownAbsolutePath);
  const index = current.annotations.findIndex((item) => item.id === id);
  if (index === -1) throw new Error("Annotation not found");
  current.annotations[index] = {
    ...current.annotations[index],
    ...patch,
    updated_at: new Date().toISOString(),
  };
  return writeAnnotations(markdownAbsolutePath, current);
}

function serveStatic(req, res, pathname) {
  const filePath = pathname === "/" ? path.join(publicDir, "index.html") : path.join(publicDir, pathname);
  const absolute = path.resolve(filePath);
  if (!absolute.startsWith(publicDir + path.sep) && absolute !== path.join(publicDir, "index.html")) {
    sendText(res, 403, "Forbidden");
    return;
  }
  if (!fs.existsSync(absolute) || !fs.statSync(absolute).isFile()) {
    sendText(res, 404, "Not found");
    return;
  }
  const ext = path.extname(absolute);
  const types = {
    ".html": "text/html; charset=utf-8",
    ".css": "text/css; charset=utf-8",
    ".js": "application/javascript; charset=utf-8",
  };
  sendText(res, 200, fs.readFileSync(absolute, "utf8"), types[ext] || "text/plain; charset=utf-8");
}

const server = http.createServer(async (req, res) => {
  try {
    const url = new URL(req.url, `http://${req.headers.host}`);
    if (url.pathname === "/api/files" && req.method === "GET") {
      sendJson(res, 200, { files: walkMarkdownFiles(repoRoot).sort() });
      return;
    }

    if (url.pathname === "/api/file" && req.method === "GET") {
      const markdownPath = safeRepoPath(url.searchParams.get("path"));
      if (!markdownPath.endsWith(".md")) throw new Error("Only Markdown files are supported");
      sendJson(res, 200, {
        file: toRepoRelative(markdownPath),
        content: fs.readFileSync(markdownPath, "utf8"),
        annotations: readAnnotations(markdownPath),
      });
      return;
    }

    if (url.pathname === "/api/annotations" && req.method === "POST") {
      const body = JSON.parse(await readBody(req));
      const markdownPath = safeRepoPath(body.file);
      if (!markdownPath.endsWith(".md")) throw new Error("Only Markdown files are supported");
      sendJson(res, 200, createAnnotation(markdownPath, body.annotation || {}));
      return;
    }

    if (url.pathname === "/api/annotations" && req.method === "PUT") {
      const body = JSON.parse(await readBody(req));
      const markdownPath = safeRepoPath(body.file);
      if (!markdownPath.endsWith(".md")) throw new Error("Only Markdown files are supported");
      sendJson(res, 200, updateAnnotation(markdownPath, body.id, body.patch || {}));
      return;
    }

    serveStatic(req, res, url.pathname);
  } catch (error) {
    sendJson(res, 400, { error: error.message });
  }
});

server.listen(port, "127.0.0.1", () => {
  console.log(`Markdown annotator: http://127.0.0.1:${port}`);
  console.log(`Repository: ${repoRoot}`);
});
