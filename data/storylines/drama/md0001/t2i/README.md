# MD-0001 T2I 桥腿（#108·R1788 起链）

> 桥=**PACK-v1.json**（机读正典件·双消费端）：bm-a ComfyUI 本地草稿路（现役位）与 bm-c ComfyUI 正座（plan 正典位）同包可消费——bm-c 被 CEO 直令 MV 线占用期间，草稿档按 O-2126 科学决策授权走本地路，判据窗（72h 至 ~10-11）不受座位置换阻塞。

## 本腿产物

- `PACK-v1.json`：12 镜 T2I 正典提示词包（13 号镜=程序层黑屏文字·零 T2I）——逐镜 prompt/negative（风格锁+角色锁双前缀）/seed（角色锚定固定）/尺寸 1216×683（16:9 草稿档）/Ken Burns 动效参数（camera 字段→装配腿消费）。
- 角色一致性锚：C-00028 十四号路灯→census v19 卡 / C-00027 邓建国→v18 卡 / C-00029 咪喱→v20 卡（参照卡制=画风+特征锚·灯罩歪补丁/老兵侧脸工装/猫左耳缺口+尾天线）。
- 模型件：`sd_xl_base_1.0.safetensors`（官方 all-in-one XL checkpoint·期望字节 6,938,078,334）——三闸全过（能用=官方正主仓/速度=hf-mirror 夜窗快车道/档位=plan 批准的 SDXL 现役起步档）；下载在飞（断点续传+字节校验·日志 `data/assets/model-pulls/sdxl-base-pull.log`·R1776 工艺复用）。

## 消费契约（runner 位·下轮领）

1. 起 ComfyUI：`C:/Agent/ComfyUI/.venv/Scripts/python.exe main.py --listen 127.0.0.1 --port 8188 --lowvram`（共卡让路纪律：起前 nvidia-smi 实测·AIHOT 模型在载时等待波动窗〔R1786 先例〕）。
2. 逐镜 POST /prompt（标准 SDXL text2img API workflow：CheckpointLoaderSimple→CLIPTextEncode×2→EmptyLatentImage(1216×683)→KSampler(30 步·cfg 6.5·dpmpp_2m/karras)→VAEDecode→SaveImage）——prompt=style_lock+char.tokens+shot.prompt·negative=negative_lock。
3. 落盘 `frames/shotNN.png` → 一致抽验（多模态并排 vs 参照卡·判据 ≥8/10）→ 合成腿（音轨=R1787 13 段全集·KB 参数入 Ken Burns）。

## 风格口径（世界原生·三律预对位）

- 硅基城市世界原生质感：扁平风格化 2D 插画+降饱和+夜雨氛围（SC-002 漫画线同世界「2D 像素+降饱和」承继）；像素灵（灯/猫）=soft square pixel 质感·碳基市民（邓建国）=常人风格化——物种差异即画风分层。
- 画面内零文字承载（文字层分离律·SC-002 定谳）：shot7 琥珀屏=氛围元素·中文一律程序层烧录。
- 草稿档 = NC 分级草稿期合法（480P/720P 装配消费）；升档 A/B 位=Qwen-Image-2.0 GGUF（#109 位·并行评估）。
