// ToonFlow WebView2 CDP driver (backlog #110, R2204).
// Usage: bun tools/toonflow_cdp.ts eval '<js expression>'
//        bun tools/toonflow_cdp.ts evalfile <path-to-js>
//        bun tools/toonflow_cdp.ts click '<selector>'
//        bun tools/toonflow_cdp.ts import <adapter.ts> [--dry]
//        bun tools/toonflow_cdp.ts pick-model '<model display name or substring>'
//          One-command custom provider install (tech#153): reads the adapter
//          .ts, opens the add-custom-media-provider dialog, switches to the
//          paste-code tab, fills the textarea, confirms, and validates the
//          provider list. Idempotent: if the adapter id is already installed
//          (list contains "<id>.ts") it returns "no-op" without touching the
//          dialog. --dry runs the whole mechanical chain but clicks Cancel
//          instead of the confirm button (mechanics validation, no install).
// Requires the desktop app started with CDP enabled, e.g. (PowerShell):
//   $env:WEBVIEW2_ADDITIONAL_BROWSER_ARGUMENTS='--remote-debugging-port=9222'
//   Start-Process C:\Users\sjs20\tools\ToonFlow\app\toonflow\bin\launcher.exe
// bun is NOT on PATH on this machine; use the ToonFlow-bundled binary:
//   & 'C:\Users\sjs20\tools\ToonFlow\app\toonflow\bin\bun.exe' tools/toonflow_cdp.ts ...
// (WebView2 honors WEBVIEW2_ADDITIONAL_BROWSER_ARGUMENTS, so the one-time
// provider/model UI config is automatable and auditable instead of manual.)
import { readFileSync, writeFileSync } from "bun:fs";

const OUT = "C:/Users/sjs20/Desktop/FluxGroup/media/BigStream/.c3-tmp/toonflow_cdp_result.txt";
const HTTP = "http://127.0.0.1:9222/json";

async function getPageWs(): Promise<string> {
  const res = await fetch(HTTP);
  const targets = (await res.json()) as any[];
  const page = targets.find((t) => t.type === "page");
  if (!page) throw new Error("no page target");
  return page.webSocketDebuggerUrl;
}

let mode = process.argv[2] ?? "eval";
let expr = process.argv[3] ?? "document.title";
if (mode === "evalfile") {
  expr = readFileSync(process.argv[3], "utf-8");
  mode = "eval";
}

let js: string;
if (mode === "import") {
  // tech#153: mechanized install of a custom media provider adapter.
  const adapterPath = process.argv[3];
  // CRLF->LF: the browser textarea normalizes newlines anyway, so compare and
  // fill with the normalized form (matches what actually gets installed).
  const content = readFileSync(adapterPath, "utf-8").replace(/\r\n/g, "\n");
  const dry = process.argv.includes("--dry");
  const idm = content.match(/id\s*:\s*["'`]([^"'`]+)["'`]/);
  const adapterId = idm ? idm[1] : "unknownAdapter";
  const sleepFn = "const sleep=(ms)=>new Promise(r=>setTimeout(r,ms));";
  const dlgFind =
    "const dlgAll=()=>[...document.querySelectorAll('.el-overlay')].filter(o=>o.innerHTML.includes('粘贴代码'));";
  js = `(async function(){
  const CONTENT=${JSON.stringify(content)};
  const ID=${JSON.stringify(adapterId)};
  const DRY=${dry ? "true" : "false"};
  ${sleepFn}
  ${dlgFind}
  try {
    // 0) close any stale add-custom-provider dialog left open by a prior run
    const stale = dlgAll()[0];
    if (stale) {
      const c = [...stale.querySelectorAll("button")].find(b => b.innerText.trim() === "取消");
      if (c) { c.click(); await sleep(400); }
    }
    // 1) idempotency: provider list already contains <id>.ts -> no-op
    await sleep(200);
    if (document.body.innerText.includes(ID + ".ts")) return "no-op: " + ID + " already installed";
    // 2) ensure the media-model settings page shows the entry button
    let addBtn = [...document.querySelectorAll("button")].find(b => b.innerText.trim().includes("添加自定义供应商"));
    if (!addBtn) {
      const nav = [...document.querySelectorAll("span,div,li,button")].filter(e => e.innerText && e.innerText.trim() === "媒体模型");
      if (nav.length) { nav[nav.length - 1].click(); await sleep(600); }
      addBtn = [...document.querySelectorAll("button")].find(b => b.innerText.trim().includes("添加自定义供应商"));
    }
    if (!addBtn) return "ERR:no-add-custom-provider-button (open 设置→媒体模型 first)";
    addBtn.click(); await sleep(500);
    // 3) switch to the paste-code tab
    const dlg = dlgAll().pop();
    if (!dlg) return "ERR:dialog-not-open";
    const pasteLbl = [...dlg.querySelectorAll("label,.el-radio-button")].find(l => l.innerText.trim().includes("粘贴代码"));
    if (!pasteLbl) return "ERR:no-paste-mode-label";
    pasteLbl.click(); await sleep(300);
    // 4) fill the provider code textarea (native setter + input event for v-model)
    const d2 = dlgAll().pop();
    const ta = d2.querySelector("textarea.el-textarea__inner");
    if (!ta) return "ERR:no-textarea";
    const setter = Object.getOwnPropertyDescriptor(window.HTMLTextAreaElement.prototype, "value").set;
    setter.call(ta, CONTENT);
    ta.dispatchEvent(new Event("input", { bubbles: true }));
    await sleep(300);
    if (ta.value.length !== CONTENT.length) return "ERR:textarea-fill-mismatch got=" + ta.value.length + " want=" + CONTENT.length;
    // 5) confirm (or cancel in dry mode)
    if (DRY) {
      const c = [...d2.querySelectorAll("button")].find(b => b.innerText.trim() === "取消");
      if (c) c.click();
      return "DRY-OK: filled " + CONTENT.length + " chars, canceled before confirm (id=" + ID + ")";
    }
    const ok = [...d2.querySelectorAll("button")].find(b => b.innerText.trim() === "确定添加供应商");
    if (!ok) return "ERR:no-confirm-button";
    ok.click();
    // 6) validate the install persisted in the provider list
    for (let i = 0; i < 12 && !document.body.innerText.includes(ID + ".ts"); i++) await sleep(500);
    return document.body.innerText.includes(ID + ".ts")
      ? "INSTALLED: " + ID + " (" + CONTENT.length + " chars)"
      : "WARN:install-not-confirmed-in-list id=" + ID;
  } catch (e) { return "ERR:" + e; }
})()`;
} else if (mode === "pick-model") {
  // tech#154: mechanize the main-interface model selector (composer footer
  // modelButton -> agentModelPopover -> el-select). Scope note (R2214 live
  // probe): this selector lists LANGUAGE models only (agent LLM); media
  // models installed as custom providers do NOT appear here - their
  // consumption point is the image-generation node inside a project
  // workspace (LEG-3 ③ probe, VRAM-gated). This command serves the
  // language-model domain and any future selector entry.
  const want = process.argv[3] ?? "";
  js = `(async function(){
  const sleep=(ms)=>new Promise(r=>setTimeout(r,ms));
  const WANT=${JSON.stringify(want)};
  const fire=(el)=>["mousedown","mouseup","click"].forEach(t=>el.dispatchEvent(new MouseEvent(t,{bubbles:true,cancelable:true,view:window})));
  const esc=()=>document.dispatchEvent(new KeyboardEvent("keydown",{key:"Escape",bubbles:true}));
  try {
    if (!WANT) return "ERR:no-model-name-arg";
    // 1) fresh popover: close any stale one (Escape, then outside-click),
    // reopen via the composer model button
    if (document.querySelector(".agentModelPopover")) { esc(); await sleep(250); }
    if (document.querySelector(".agentModelPopover")) { document.body.click(); await sleep(250); }
    const btn0 = document.querySelector("button.modelButton");
    if (!btn0) return "ERR:no-model-button";
    if (btn0.innerText.includes(WANT) && !document.querySelector(".agentModelPopover")) return "no-op: already on " + WANT;
    btn0.click(); await sleep(500);
    const pop = document.querySelector(".agentModelPopover");
    if (!pop) return "ERR:popover-did-not-open";
    // 2) open the el-select dropdown (full mouse sequence; retry loop in
    // case a toggle lands on an already-open menu)
    const sel = pop.querySelector(".el-select__wrapper");
    if (!sel) return "ERR:no-select-wrapper";
    let dd = null;
    for (let i = 0; i < 3 && !dd; i++) {
      fire(sel); await sleep(400);
      const dds = [...document.querySelectorAll(".el-select-dropdown")].filter(d => d.offsetParent && d.querySelector(".el-select-dropdown__item"));
      if (dds.length) dd = dds[dds.length - 1];
    }
    if (!dd) return "ERR:dropdown-not-open";
    const items = [...dd.querySelectorAll(".el-select-dropdown__item")];
    const target = items.find(li => (li.innerText || "").trim().includes(WANT));
    if (!target) return "ERR:not-in-list available=" + items.map(li => (li.innerText || "").trim()).join(",");
    fire(target); await sleep(600);
    // 3) verify the model button shows the target name, then close popover
    const btn = document.querySelector("button.modelButton");
    const now = btn ? (btn.innerText || "").replace(/\\n/g, "|").trim() : "";
    const ok = btn && btn.innerText.includes(WANT);
    esc(); await sleep(250);
    if (document.querySelector(".agentModelPopover")) { document.body.click(); await sleep(250); }
    const left = document.querySelector(".agentModelPopover") ? " (popover-still-open)" : "";
    return (ok ? "PICKED: " : "WARN:button-not-updated ") + "button=[" + now + "] want=" + WANT + left;
  } catch (e) { return "ERR:" + e; }
})()`;
} else if (mode === "eval") {
  js = `(function(){ try { return String(eval(${JSON.stringify(expr)})); } catch(e){ return "ERR:"+e; } })()`;
} else if (mode === "click") {
  js = `(function(){ const els=[...document.querySelectorAll(${JSON.stringify(expr)})]; els.forEach(e=>e.click()); return "clicked "+els.length; })()`;
} else {
  js = "unknown-mode";
}

const ws = new WebSocket(await getPageWs());
let id = 0;
const pending = new Map<number, (v: any) => void>();
function send(method: string, params: any = {}): Promise<any> {
  return new Promise((resolve) => {
    const mid = ++id;
    pending.set(mid, resolve);
    ws.send(JSON.stringify({ id: mid, method, params }));
  });
}
ws.onmessage = (ev) => {
  const msg = JSON.parse(String(ev.data));
  if (msg.id && pending.has(msg.id)) {
    pending.get(msg.id)!(msg);
    pending.delete(msg.id);
  }
};
await new Promise((r) => (ws.onopen = r));
await send("Runtime.enable");
const r = await send("Runtime.evaluate", {
  expression: js,
  awaitPromise: true,
  returnByValue: true,
});
const val = r?.result?.value ?? JSON.stringify(r);
writeFileSync(OUT, String(val));
console.log(String(val).slice(0, 1500));
ws.close();
