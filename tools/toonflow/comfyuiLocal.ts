// Toonflow custom provider adapter: local ComfyUI (Qwen-Image-2.1 text-to-image).
// Contract source: addCustomProviderDialog embedded types.d.ts (docs/research/R-20261014-bigstream-01 §三).
// Server-side Bun: no imports; host injects this.tool.fetch / this.tool.errorMessage / this.config / this.signal.
// Local no-auth ComfyUI -> rules: [] (no apiKey field). Address = public local info (single-machine deploy:
// Toonflow server and ComfyUI on the same machine, so 127.0.0.1 is reachable from the Toonflow server side).
// Workflow: Comfy-Org 0.37.0 qwen_image_2.1 t2i template lineage (runner_r1792 canon):
//   UNETLoader(qwen_image_2.1_int8_convrot) -> QwenImage21Cache -> KSampler(euler/simple, cfg 1.0)
//   CLIPLoader(qwen3vl_8b_w4a8, qwen_image) -> TextEncodeQwenImage21(prompt, negative_prompt, resolution 1024)
//   EmptyLatentImage(multiples of 16) -> VAEDecode(qwen_image_2.1_vae_bf16) -> SaveImage(unique prefix)
// Safe cancellation: never calls /interrupt and never clears the whole queue; on abort only removes
// this adapter's own pending prompt via POST /queue {"delete":[prompt_id]}.

type ImageRequestLocal = {
  model: string;
  prompt: string;
  images?: unknown[];
  mask?: unknown;
  n?: number;
  ratio?: string;
  size?: string;
  quality?: string;
  outputFormat?: string;
  other?: Record<string, unknown>;
};

type ContextLocal = {
  config: Record<string, unknown>;
  signal?: AbortSignal;
  tool: {
    fetch: typeof globalThis.fetch;
    errorMessage: (value: unknown) => string;
  };
};

type MediaAssetLocal = { mediaType: "image"; type: "url"; url: string; mimeType?: string };

export default {
  id: "comfyuiLocal",
  label: "ComfyUI 本地（Qwen-Image-2.1）",
  version: "2.0.0",
  readme: "本地 ComfyUI 供应商（单机部署，无需 API Key）。\n\n- 地址：http://127.0.0.1:8188（Toonflow 服务端与 ComfyUI 同机时可达；跨机部署请先修改适配器内地址）\n- 模型：Qwen-Image-2.1 文生图；需 ComfyUI 内已放置 qwen_image_2.1_int8_convrot.safetensors、qwen3vl_8b_w4a8.safetensors、qwen_image_2.1_vae_bf16.safetensors 三个模型文件\n- 画幅：16:9（默认，1216×688）/ 9:16 / 1:1 / 4:3 / 3:4\n- 生成数量：1-4 张\n- 高级参数（other）：seed（整数，缺省随机）、steps（4-50，缺省 25）、negative_prompt（字符串，缺省空）\n- 输出：PNG（ComfyUI /view 直链）\n- 超时：单次生成上限 20 分钟，超时自动从队列移除本任务\n- 取消安全：不会调用 /interrupt，不会清空队列，仅移除本适配器自己的排队任务",
  rules: [],
  models: [
    {
      id: "qwen-image-2.1-t2i",
      label: "Qwen-Image-2.1 文生图（本地 ComfyUI）",
      type: "image",
      mode: ["text"],
      imageRatios: ["16:9", "9:16", "1:1", "4:3", "3:4"],
    },
  ],
  async generateImage(this: ContextLocal, request: ImageRequestLocal): Promise<MediaAssetLocal[]> {
    const COMFY_BASE = "http://127.0.0.1:8188";
    const POLL_MS = 3000;
    const TOTAL_MS = 1200000;
    const RATIO_DIMS: Record<string, { width: number; height: number }> = {
      "16:9": { width: 1216, height: 688 },
      "9:16": { width: 688, height: 1216 },
      "1:1": { width: 1024, height: 1024 },
      "4:3": { width: 1024, height: 768 },
      "3:4": { width: 768, height: 1024 },
    };

    // ---- 输入校验：不支持的字段显式报错，绝不静默丢弃 ----
    if (request.model !== "qwen-image-2.1-t2i") {
      throw new Error("不支持的模型：" + request.model + "（本适配器仅支持 qwen-image-2.1-t2i 文生图）");
    }
    if (!request.prompt || !String(request.prompt).trim()) {
      throw new Error("提示词为空，无法生成");
    }
    if (request.images && request.images.length > 0) {
      throw new Error("当前仅支持纯文生图，不支持参考图输入");
    }
    if (request.mask) {
      throw new Error("当前不支持蒙版（mask）输入");
    }
    if (request.size !== undefined) {
      throw new Error("不支持自定义尺寸参数 size；请通过 ratio 选择画幅（16:9/9:16/1:1/4:3/3:4）");
    }
    if (request.quality !== undefined) {
      throw new Error("不支持画质档位 quality；本地工作流固定采样参数");
    }
    if (request.outputFormat !== undefined && request.outputFormat !== "png") {
      throw new Error("仅支持 png 输出格式（ComfyUI SaveImage 原生输出）");
    }
    let n = 1;
    if (request.n !== undefined) {
      n = Number(request.n);
      if (!Number.isInteger(n) || n < 1 || n > 4) {
        throw new Error("生成数量 n 仅支持 1-4");
      }
    }
    let dims = RATIO_DIMS["16:9"];
    if (request.ratio !== undefined) {
      const d = RATIO_DIMS[String(request.ratio)];
      if (!d) {
        throw new Error("不支持的画幅 ratio：" + request.ratio + "（支持 16:9/9:16/1:1/4:3/3:4）");
      }
      dims = d;
    }
    let seed = Math.floor(Math.random() * 2147483647) + 1;
    let steps = 25;
    let negative = "";
    const other = request.other ?? {};
    for (const key of Object.keys(other)) {
      if (key === "seed") {
        const v = Number(other.seed);
        if (!Number.isInteger(v) || v < 0 || v > 9007199254740991) {
          throw new Error("other.seed 须为 0 起的整数");
        }
        seed = v;
      } else if (key === "steps") {
        const v = Number(other.steps);
        if (!Number.isInteger(v) || v < 4 || v > 50) {
          throw new Error("other.steps 须为 4-50 的整数");
        }
        steps = v;
      } else if (key === "negative_prompt") {
        if (typeof other.negative_prompt !== "string") {
          throw new Error("other.negative_prompt 须为字符串");
        }
        negative = other.negative_prompt;
      } else {
        throw new Error("不支持的供应商参数 other." + key + "（仅支持 seed / steps / negative_prompt）");
      }
    }

    // ---- 组装 ComfyUI API 工作流（Qwen-Image-2.1 t2i 模板谱系）----
    const prefix = "toonflow_qwen21_" + Date.now().toString(36) + "_" + seed;
    const workflow: Record<string, unknown> = {
      "1": { class_type: "UNETLoader", inputs: { unet_name: "qwen_image_2.1_int8_convrot.safetensors", weight_dtype: "default" } },
      "2": { class_type: "CLIPLoader", inputs: { clip_name: "qwen3vl_8b_w4a8.safetensors", type: "qwen_image", device: "default" } },
      "3": { class_type: "VAELoader", inputs: { vae_name: "qwen_image_2.1_vae_bf16.safetensors" } },
      "4": { class_type: "QwenImage21Cache", inputs: { model: ["1", 0], device: "auto", dtype: "default" } },
      "5": { class_type: "TextEncodeQwenImage21", inputs: { clip: ["2", 0], prompt: request.prompt, negative_prompt: negative, resolution: 1024 } },
      "6": { class_type: "EmptyLatentImage", inputs: { width: dims.width, height: dims.height, batch_size: n } },
      "7": { class_type: "KSampler", inputs: { seed: seed, steps: steps, cfg: 1.0, sampler_name: "euler", scheduler: "simple", denoise: 1.0, model: ["4", 0], positive: ["5", 0], negative: ["5", 1], latent_image: ["6", 0] } },
      "8": { class_type: "VAEDecode", inputs: { samples: ["7", 0], vae: ["3", 0] } },
      "9": { class_type: "SaveImage", inputs: { filename_prefix: prefix, images: ["8", 0] } },
    };

    // ---- 提交（外层总超时 + 响应取消）----
    this.signal?.throwIfAborted();
    const outerSignal = AbortSignal.any([AbortSignal.timeout(TOTAL_MS), ...(this.signal ? [this.signal] : [])]);
    let promptId = "";
    let res: any;
    try {
      res = await this.tool.fetch(COMFY_BASE + "/prompt", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ prompt: workflow, client_id: "toonflow-comfyui-local" }),
        signal: outerSignal,
      });
    } catch (e: any) {
      if (this.signal?.aborted) throw new Error("任务已取消");
      throw new Error("无法连接本地 ComfyUI（127.0.0.1:8188）：请确认本机 ComfyUI 已启动。原因：" + this.tool.errorMessage(e));
    }
    if (!res.ok) {
      const text = await res.text();
      throw new Error("ComfyUI 提交失败（HTTP " + res.status + "）：" + this.tool.errorMessage(text));
    }
    const data: any = await res.json();
    promptId = String(data?.prompt_id ?? "");
    if (!promptId) {
      throw new Error("ComfyUI 未返回 prompt_id：请检查三个模型文件是否已放入 ComfyUI 对应目录");
    }

    // ---- 轮询 /history：响应取消 + 有限超时；取消仅移除自己的排队任务 ----
    const cancelPending = async (): Promise<void> => {
      try {
        await this.tool.fetch(COMFY_BASE + "/queue", {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({ delete: [promptId] }),
          signal: AbortSignal.timeout(10000),
        });
      } catch {
        // 尽力清理，失败不掩盖原始错误
      }
    };
    const startedAt = Date.now();
    while (true) {
      if (this.signal?.aborted) {
        await cancelPending();
        throw new Error("任务已取消（已尝试从 ComfyUI 队列移除本任务）");
      }
      if (Date.now() - startedAt > TOTAL_MS) {
        await cancelPending();
        throw new Error("生成超时（20 分钟）：本机 ComfyUI 负载过高或队列拥堵，请稍后重试");
      }
      let entry: any = null;
      try {
        const h = await this.tool.fetch(COMFY_BASE + "/history/" + promptId, { signal: AbortSignal.timeout(15000) });
        if (h.ok) {
          const hist: any = await h.json();
          entry = hist?.[promptId] ?? null;
        }
      } catch {
        // 单次轮询失败不致命，进入下一轮
      }
      if (entry && entry.status && entry.status.completed) {
        if (entry.status.status_str === "error") {
          let detail = "";
          try {
            const msgs: any[] = entry.status.messages ?? [];
            for (const m of msgs) {
              if (m && m[0] === "execution_error" && m[1]) {
                detail = String(m[1].exception_message ?? m[1].exception_type ?? "") || detail;
              }
            }
          } catch {
            // 细节提取失败不影响主错误
          }
          throw new Error("ComfyUI 执行出错" + (detail ? "：" + detail : "（详见 ComfyUI 控制台日志）"));
        }
        const assets: MediaAssetLocal[] = [];
        const outputs: any = entry.outputs ?? {};
        for (const nodeKey of Object.keys(outputs)) {
          const imgs: any[] = outputs[nodeKey]?.images ?? [];
          for (const img of imgs) {
            const qs = new URLSearchParams({
              filename: String(img.filename ?? ""),
              subfolder: String(img.subfolder ?? ""),
              type: String(img.type ?? "output"),
            });
            assets.push({ mediaType: "image", type: "url", url: COMFY_BASE + "/view?" + qs.toString(), mimeType: "image/png" });
          }
        }
        if (assets.length === 0) {
          throw new Error("ComfyUI 任务已完成但没有输出图像（请检查 SaveImage 节点与磁盘空间）");
        }
        return assets;
      }
      await new Promise<void>((resolve) => setTimeout(resolve, POLL_MS));
    }
  },
};
