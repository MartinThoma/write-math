import { rasterize, SIZE } from "./raster.js";

const $ = (id) => document.getElementById(id);
const canvas = $("canvas");
const ctx = canvas.getContext("2d");
const preview = $("preview");
const pctx = preview.getContext("2d");
const status = $("status");
const resultsEl = $("results");

const TOP_K = 10;
let model = null; // {labels, metrics} once the worker has loaded the model
let requestId = 0;
const worker = new Worker(new URL("./worker.js", import.meta.url), { type: "module" });
let strokes = [];
let current = null;

// ---------------------------------------------------------------- drawing

function resizeCanvas() {
  const rect = canvas.getBoundingClientRect();
  const dpr = window.devicePixelRatio || 1;
  canvas.width = Math.round(rect.width * dpr);
  canvas.height = Math.round(rect.height * dpr);
  ctx.setTransform(dpr, 0, 0, dpr, 0, 0);
  redraw();
}

function inkColor() {
  return getComputedStyle(document.documentElement).getPropertyValue("--pad-ink").trim() || "#000";
}

function drawStroke(s) {
  if (s.length === 0) return;
  ctx.beginPath();
  if (s.length === 1) {
    ctx.arc(s[0].x, s[0].y, ctx.lineWidth / 2, 0, 2 * Math.PI);
    ctx.fill();
    return;
  }
  ctx.moveTo(s[0].x, s[0].y);
  for (let i = 1; i < s.length; i++) ctx.lineTo(s[i].x, s[i].y);
  ctx.stroke();
}

function redraw() {
  const rect = canvas.getBoundingClientRect();
  ctx.clearRect(0, 0, rect.width, rect.height);
  ctx.lineWidth = 3;
  ctx.lineCap = "round";
  ctx.lineJoin = "round";
  ctx.strokeStyle = ctx.fillStyle = inkColor();
  for (const s of strokes) drawStroke(s);
  if (current) drawStroke(current);
}

function point(e) {
  const r = canvas.getBoundingClientRect();
  return { x: e.clientX - r.left, y: e.clientY - r.top, time: Math.round(e.timeStamp) };
}

canvas.addEventListener("pointerdown", (e) => {
  if (e.button !== 0) return;
  canvas.setPointerCapture(e.pointerId);
  current = [point(e)];
  $("hint").classList.add("hidden");
  redraw();
});

canvas.addEventListener("pointermove", (e) => {
  if (!current) return;
  const events = e.getCoalescedEvents ? e.getCoalescedEvents() : [e];
  for (const ev of events.length ? events : [e]) current.push(point(ev));
  redraw();
});

function endStroke() {
  if (!current) return;
  strokes.push(current);
  current = null;
  redraw();
  update();
}

canvas.addEventListener("pointerup", endStroke);
canvas.addEventListener("pointercancel", endStroke);

$("undo").addEventListener("click", () => {
  strokes.pop();
  redraw();
  update();
});

$("clear").addEventListener("click", () => {
  strokes = [];
  redraw();
  update();
});

window.addEventListener("keydown", (e) => {
  if ((e.ctrlKey || e.metaKey) && e.key === "z") {
    e.preventDefault();
    $("undo").click();
  } else if (e.key === "Escape") {
    $("clear").click();
  }
});

new ResizeObserver(resizeCanvas).observe(canvas);
matchMedia("(prefers-color-scheme: dark)").addEventListener("change", redraw);

// ---------------------------------------------------------------- recognition

function drawPreview(img) {
  const data = pctx.createImageData(SIZE, SIZE);
  for (let i = 0; i < img.length; i++) {
    const v = Math.round(img[i] * 255);
    data.data.set([v, v, v, 255], i * 4);
  }
  pctx.putImageData(data, 0, 0);
}

function update() {
  const has = strokes.length > 0;
  $("undo").disabled = !has;
  $("clear").disabled = !has;
  $("hint").classList.toggle("hidden", has);
  $("empty").classList.toggle("hidden", has && model);
  if (!has) {
    resultsEl.replaceChildren();
    pctx.clearRect(0, 0, SIZE, SIZE);
    return;
  }
  const img = rasterize(strokes);
  drawPreview(img);
  if (!model) return;
  worker.postMessage({ id: ++requestId, image: img, k: TOP_K });
}

function renderResults(top) {
  const items = top.map((r) => {
    const li = document.createElement("li");
    const b = document.createElement("button");
    b.type = "button";
    b.title = `Copy ${r.latex}`;
    const bar = document.createElement("span");
    bar.className = "bar";
    bar.style.width = `${(r.p * 100).toFixed(1)}%`;
    const glyph = document.createElement("span");
    glyph.className = "glyph";
    glyph.textContent = r.unicode || "";
    const code = document.createElement("span");
    code.className = "code";
    code.textContent = r.latex;
    if (r.package) {
      const pkg = document.createElement("span");
      pkg.className = "pkg";
      pkg.textContent = `\\usepackage{${r.package}}`;
      code.append(pkg);
    }
    const prob = document.createElement("span");
    prob.className = "prob";
    prob.textContent = r.p >= 0.001 ? `${(r.p * 100).toFixed(1)}%` : "<0.1%";
    b.append(bar, glyph, code, prob);
    b.addEventListener("click", () => copy(r.latex));
    li.append(b);
    return li;
  });
  resultsEl.replaceChildren(...items);
}

let toastTimer;
// The async clipboard API only exists on https:// and localhost; fall back to
// a hidden textarea + execCommand so copying also works over plain http on a LAN.
function legacyCopy(text) {
  const ta = document.createElement("textarea");
  ta.value = text;
  ta.setAttribute("readonly", "");
  ta.style.cssText = "position:fixed;top:0;left:0;opacity:0;font-size:16px";
  document.body.append(ta);
  ta.select();
  ta.setSelectionRange(0, text.length);
  const ok = document.execCommand("copy");
  ta.remove();
  return ok;
}

async function copy(text) {
  let ok = false;
  try {
    if (navigator.clipboard && window.isSecureContext) {
      await navigator.clipboard.writeText(text);
      ok = true;
    }
  } catch {
    // fall through to the legacy path
  }
  if (!ok) ok = legacyCopy(text);
  showToast(ok ? `Copied ${text}` : `Copy failed: ${text}`);
}

function showToast(msg, ms = 1600) {
  const t = $("toast");
  t.textContent = msg;
  t.classList.add("show");
  clearTimeout(toastTimer);
  toastTimer = setTimeout(() => t.classList.remove("show"), ms);
}

// ---------------------------------------------------------------- install / offline

const installBtn = $("install");
let installPrompt = null; // deferred `beforeinstallprompt` event (Chromium browsers)
let offlineReady = false; // service worker has cached the app and the model

// Service workers (and thus offline use and installation) need https:// or localhost.
const offlineCapable = "serviceWorker" in navigator && window.isSecureContext;

const isInstalled = () =>
  matchMedia("(display-mode: standalone)").matches || navigator.standalone === true;

// Browsers without `beforeinstallprompt` can still install the app from their
// own menus; tell the user where.
function manualInstallSteps() {
  const ua = navigator.userAgent;
  const iOS = /iPhone|iPad|iPod/.test(ua) || (/Macintosh/.test(ua) && navigator.maxTouchPoints > 1);
  if (iOS) return "Tap the Share button in the toolbar, then “Add to Home Screen”.";
  if (/Android/.test(ua) && /Firefox/.test(ua)) return "Open the browser menu (⋮) and tap “Install”.";
  const safari = /Safari/.test(ua) && !/Chrome|Chromium|CriOS|FxiOS|Edg|OPR|Firefox/.test(ua);
  if (safari && /Macintosh/.test(ua)) return "In the menu bar, choose File → “Add to Dock”.";
  return null;
}

function updateStatus() {
  if (!model) return;
  if (!navigator.onLine) status.textContent = "Offline · ready";
  else if (isInstalled()) status.textContent = "Installed · works offline";
  else if (!offlineCapable) status.textContent = "Ready · offline use needs HTTPS";
  else if (offlineReady) status.textContent = "Ready · available offline";
  else status.textContent = "Ready";
  installBtn.hidden = !(offlineCapable && !isInstalled() && (installPrompt || manualInstallSteps()));
}

window.addEventListener("beforeinstallprompt", (e) => {
  e.preventDefault(); // show our own button instead of the browser's mini-infobar
  installPrompt = e;
  updateStatus();
});

window.addEventListener("appinstalled", () => {
  installPrompt = null;
  showToast("Installed. Write Math now also works offline.", 3000);
  updateStatus();
});

installBtn.addEventListener("click", async () => {
  if (installPrompt) {
    const prompt = installPrompt;
    installPrompt = null; // a prompt can only be shown once
    prompt.prompt();
    await prompt.userChoice;
    updateStatus();
    return;
  }
  $("install-steps").textContent = manualInstallSteps();
  $("install-help").showModal();
});

matchMedia("(display-mode: standalone)").addEventListener("change", updateStatus);

worker.onmessage = ({ data }) => {
  if (data.type === "ready") {
    model = data;
    const acc = data.metrics;
    $("modelinfo").textContent = acc
      ? `The model knows ${data.labels} symbols (test accuracy ${(acc.top1 * 100).toFixed(1)}% top-1, ${(acc.top3 * 100).toFixed(1)}% top-3).`
      : `The model knows ${data.labels} symbols.`;
    updateStatus();
    update();
  } else if (data.type === "result") {
    // Ignore answers to requests that were superseded by a newer stroke.
    if (data.id === requestId && strokes.length > 0) renderResults(data.top);
  } else if (data.type === "error") {
    console.error(data.message);
    status.textContent = "Could not load the model. Reload to retry.";
  }
};

window.addEventListener("online", updateStatus);
window.addEventListener("offline", updateStatus);

if (offlineCapable) {
  navigator.serviceWorker.register(new URL("../sw.js", import.meta.url)).catch((err) => {
    console.warn("Service worker registration failed", err);
  });
  // `ready` resolves once a worker is active, i.e. its install step has
  // cached the whole app including the model.
  navigator.serviceWorker.ready.then(() => {
    offlineReady = true;
    updateStatus();
  });
}

