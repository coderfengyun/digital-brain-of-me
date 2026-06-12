const state = {
  files: [],
  currentFile: "",
  content: "",
  annotations: [],
  selection: null,
};

const els = {
  fileList: document.querySelector("#fileList"),
  fileFilter: document.querySelector("#fileFilter"),
  refreshFiles: document.querySelector("#refreshFiles"),
  currentFile: document.querySelector("#currentFile"),
  reloadFile: document.querySelector("#reloadFile"),
  showAnnotationPath: document.querySelector("#showAnnotationPath"),
  emptyState: document.querySelector("#emptyState"),
  reader: document.querySelector("#reader"),
  selectedQuote: document.querySelector("#selectedQuote"),
  commentInput: document.querySelector("#commentInput"),
  saveAnnotation: document.querySelector("#saveAnnotation"),
  annotationList: document.querySelector("#annotationList"),
  annotationCount: document.querySelector("#annotationCount"),
};

function escapeHtml(value) {
  return String(value)
    .replaceAll("&", "&amp;")
    .replaceAll("<", "&lt;")
    .replaceAll(">", "&gt;")
    .replaceAll('"', "&quot;");
}

function inlineMarkdown(value) {
  let html = escapeHtml(value);
  html = html.replace(/`([^`]+)`/g, "<code>$1</code>");
  html = html.replace(/\*\*([^*]+)\*\*/g, "<strong>$1</strong>");
  html = html.replace(/\*([^*]+)\*/g, "<em>$1</em>");
  html = html.replace(/\[([^\]]+)\]\(([^)]+)\)/g, '<a href="$2" target="_blank" rel="noreferrer">$1</a>');
  return html;
}

function splitBlocks(markdown) {
  const lines = markdown.replace(/\r\n/g, "\n").split("\n");
  const blocks = [];
  let i = 0;

  while (i < lines.length) {
    if (!lines[i].trim()) {
      i += 1;
      continue;
    }

    const start = i + 1;
    if (lines[i].startsWith("```")) {
      const fence = lines[i];
      const body = [];
      i += 1;
      while (i < lines.length && !lines[i].startsWith("```")) {
        body.push(lines[i]);
        i += 1;
      }
      if (i < lines.length) i += 1;
      blocks.push({ type: "code", start, end: i, text: body.join("\n"), fence });
      continue;
    }

    if (/^#{1,6}\s+/.test(lines[i])) {
      const match = lines[i].match(/^(#{1,6})\s+(.*)$/);
      blocks.push({ type: "heading", level: match[1].length, start, end: start, text: match[2] });
      i += 1;
      continue;
    }

    if (/^\s*[-*+]\s+/.test(lines[i]) || /^\s*\d+\.\s+/.test(lines[i])) {
      const ordered = /^\s*\d+\.\s+/.test(lines[i]);
      const items = [];
      while (i < lines.length && (/^\s*[-*+]\s+/.test(lines[i]) || /^\s*\d+\.\s+/.test(lines[i]))) {
        items.push(lines[i].replace(/^\s*(?:[-*+]|\d+\.)\s+/, ""));
        i += 1;
      }
      blocks.push({ type: ordered ? "ol" : "ul", start, end: i, items });
      continue;
    }

    if (/^\s*>\s?/.test(lines[i])) {
      const quote = [];
      while (i < lines.length && /^\s*>\s?/.test(lines[i])) {
        quote.push(lines[i].replace(/^\s*>\s?/, ""));
        i += 1;
      }
      blocks.push({ type: "quote", start, end: i, text: quote.join("\n") });
      continue;
    }

    const para = [];
    while (i < lines.length && lines[i].trim() && !/^#{1,6}\s+/.test(lines[i]) && !lines[i].startsWith("```")) {
      para.push(lines[i]);
      i += 1;
    }
    blocks.push({ type: "paragraph", start, end: i, text: para.join("\n") });
  }

  return blocks;
}

function renderMarkdown(markdown) {
  const blocks = splitBlocks(markdown);
  return blocks
    .map((block) => {
      const attrs = `class="block" data-line-start="${block.start}" data-line-end="${block.end}"`;
      if (block.type === "heading") {
        return `<h${block.level} ${attrs}>${inlineMarkdown(block.text)}</h${block.level}>`;
      }
      if (block.type === "code") {
        return `<pre ${attrs}><code>${escapeHtml(block.text)}</code></pre>`;
      }
      if (block.type === "ul" || block.type === "ol") {
        const items = block.items.map((item) => `<li>${inlineMarkdown(item)}</li>`).join("");
        return `<${block.type} ${attrs}>${items}</${block.type}>`;
      }
      if (block.type === "quote") {
        return `<blockquote ${attrs}>${inlineMarkdown(block.text).replaceAll("\n", "<br>")}</blockquote>`;
      }
      return `<p ${attrs}>${inlineMarkdown(block.text).replaceAll("\n", "<br>")}</p>`;
    })
    .join("\n");
}

function renderFileList() {
  const filter = els.fileFilter.value.trim().toLowerCase();
  const files = state.files.filter((file) => file.toLowerCase().includes(filter));
  els.fileList.innerHTML = files
    .map((file) => {
      const active = file === state.currentFile ? " active" : "";
      return `<button class="file-item${active}" data-file="${escapeHtml(file)}">${escapeHtml(file)}</button>`;
    })
    .join("");
}

function renderAnnotations() {
  const openCount = state.annotations.filter((item) => item.status !== "resolved").length;
  els.annotationCount.textContent = `${openCount} open / ${state.annotations.length} total`;
  els.annotationList.innerHTML = state.annotations.length
    ? state.annotations
        .map((item) => {
          const resolved = item.status === "resolved";
          return `
            <article class="annotation-card ${resolved ? "resolved" : ""}" data-id="${escapeHtml(item.id)}">
              <div class="annotation-meta">
                <span>${escapeHtml(item.id)}</span>
                <span>line ${escapeHtml(item.line_start)}-${escapeHtml(item.line_end)}</span>
              </div>
              <p class="annotation-quote">“${escapeHtml(item.quote)}”</p>
              <p class="annotation-comment">${escapeHtml(item.comment)}</p>
              <div class="card-actions">
                <button data-action="jump">定位</button>
                <button data-action="toggle">${resolved ? "重新打开" : "标记完成"}</button>
              </div>
            </article>
          `;
        })
        .join("")
    : `<p class="label">还没有批注。</p>`;

  document.querySelectorAll(".reader .block").forEach((block) => {
    const start = Number(block.dataset.lineStart);
    const end = Number(block.dataset.lineEnd);
    const hasAnnotation = state.annotations.some((item) => {
      if (item.status === "resolved") return false;
      return Number(item.line_start) <= end && Number(item.line_end) >= start;
    });
    block.classList.toggle("has-annotation", hasAnnotation);
  });
}

function setSelectionFromDocument() {
  const selection = window.getSelection();
  const quote = selection ? selection.toString().trim() : "";
  if (!quote || !els.reader.contains(selection.anchorNode) || !els.reader.contains(selection.focusNode)) {
    state.selection = null;
    els.selectedQuote.textContent = "还没有选中文本";
    els.saveAnnotation.disabled = true;
    return;
  }

  const range = selection.getRangeAt(0);
  const startBlock = range.startContainer.parentElement.closest(".block");
  const endBlock = range.endContainer.parentElement.closest(".block");
  if (!startBlock || !endBlock) return;

  const lineStart = Math.min(Number(startBlock.dataset.lineStart), Number(endBlock.dataset.lineStart));
  const lineEnd = Math.max(Number(startBlock.dataset.lineEnd), Number(endBlock.dataset.lineEnd));
  state.selection = {
    quote,
    line_start: lineStart,
    line_end: lineEnd,
    context_before: startBlock.innerText.slice(0, 240),
    context_after: endBlock.innerText.slice(-240),
  };
  els.selectedQuote.textContent = quote;
  els.saveAnnotation.disabled = !els.commentInput.value.trim();
}

async function loadFiles() {
  const response = await fetch("/api/files");
  const data = await response.json();
  state.files = data.files;
  renderFileList();
}

async function loadFile(file) {
  const response = await fetch(`/api/file?path=${encodeURIComponent(file)}`);
  const data = await response.json();
  if (!response.ok) throw new Error(data.error || "Failed to load file");
  state.currentFile = data.file;
  state.content = data.content;
  state.annotations = data.annotations.annotations || [];
  state.selection = null;
  els.currentFile.textContent = state.currentFile;
  els.reader.innerHTML = renderMarkdown(state.content);
  els.reader.hidden = false;
  els.emptyState.hidden = true;
  els.reloadFile.disabled = false;
  els.showAnnotationPath.disabled = false;
  els.selectedQuote.textContent = "还没有选中文本";
  els.commentInput.value = "";
  els.saveAnnotation.disabled = true;
  renderFileList();
  renderAnnotations();
}

async function saveAnnotation() {
  if (!state.currentFile || !state.selection) return;
  const comment = els.commentInput.value.trim();
  if (!comment) return;

  const response = await fetch("/api/annotations", {
    method: "POST",
    headers: { "content-type": "application/json" },
    body: JSON.stringify({
      file: state.currentFile,
      annotation: {
        ...state.selection,
        comment,
      },
    }),
  });
  const data = await response.json();
  if (!response.ok) throw new Error(data.error || "Failed to save annotation");
  state.annotations = data.annotations || [];
  els.commentInput.value = "";
  window.getSelection().removeAllRanges();
  state.selection = null;
  els.selectedQuote.textContent = "还没有选中文本";
  els.saveAnnotation.disabled = true;
  renderAnnotations();
}

async function updateAnnotation(id, patch) {
  const response = await fetch("/api/annotations", {
    method: "PUT",
    headers: { "content-type": "application/json" },
    body: JSON.stringify({ file: state.currentFile, id, patch }),
  });
  const data = await response.json();
  if (!response.ok) throw new Error(data.error || "Failed to update annotation");
  state.annotations = data.annotations || [];
  renderAnnotations();
}

function jumpToAnnotation(id) {
  const annotation = state.annotations.find((item) => item.id === id);
  if (!annotation) return;
  const block = document.querySelector(`.reader .block[data-line-start="${annotation.line_start}"]`);
  if (block) {
    block.scrollIntoView({ behavior: "smooth", block: "center" });
    block.animate(
      [
        { outlineColor: "#16786f", backgroundColor: "#dff3ef" },
        { outlineColor: "#ffd879", backgroundColor: "#fff0cf" },
      ],
      { duration: 900 }
    );
  }
}

els.fileList.addEventListener("click", (event) => {
  const button = event.target.closest(".file-item");
  if (button) loadFile(button.dataset.file).catch((error) => alert(error.message));
});

els.fileFilter.addEventListener("input", renderFileList);
els.refreshFiles.addEventListener("click", () => loadFiles().catch((error) => alert(error.message)));
els.reloadFile.addEventListener("click", () => state.currentFile && loadFile(state.currentFile));
els.reader.addEventListener("mouseup", setSelectionFromDocument);
els.reader.addEventListener("keyup", setSelectionFromDocument);
els.commentInput.addEventListener("input", () => {
  els.saveAnnotation.disabled = !(state.selection && els.commentInput.value.trim());
});
els.saveAnnotation.addEventListener("click", () => saveAnnotation().catch((error) => alert(error.message)));
els.showAnnotationPath.addEventListener("click", () => {
  if (!state.currentFile) return;
  const annotationFile = state.currentFile.replace(/\.md$/i, ".annotations.json");
  alert(`批注会保存到：${annotationFile}`);
});

els.annotationList.addEventListener("click", (event) => {
  const card = event.target.closest(".annotation-card");
  const action = event.target.dataset.action;
  if (!card || !action) return;
  if (action === "jump") jumpToAnnotation(card.dataset.id);
  if (action === "toggle") {
    const annotation = state.annotations.find((item) => item.id === card.dataset.id);
    const nextStatus = annotation.status === "resolved" ? "open" : "resolved";
    updateAnnotation(card.dataset.id, { status: nextStatus }).catch((error) => alert(error.message));
  }
});

loadFiles().catch((error) => alert(error.message));
