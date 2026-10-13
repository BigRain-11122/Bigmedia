// ToonFlow WebView2 CDP driver (backlog #110, R2204).
// Usage: bun tools/toonflow_cdp.ts eval '<js expression>'
//        bun tools/toonflow_cdp.ts evalfile <path-to-js>
//        bun tools/toonflow_cdp.ts click '<selector>'
// Requires the desktop app started with CDP enabled, e.g. (PowerShell):
//   $env:WEBVIEW2_ADDITIONAL_BROWSER_ARGUMENTS='--remote-debugging-port=9222'
//   Start-Process C:\Users\sjs20\tools\ToonFlow\app\toonflow\bin\launcher.exe
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

const js =
  mode === "eval"
    ? `(function(){ try { return String(eval(${JSON.stringify(expr)})); } catch(e){ return "ERR:"+e; } })()`
    : mode === "click"
      ? `(function(){ const els=[...document.querySelectorAll(${JSON.stringify(expr)})]; els.forEach(e=>e.click()); return "clicked "+els.length; })()`
      : "unknown-mode";

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
