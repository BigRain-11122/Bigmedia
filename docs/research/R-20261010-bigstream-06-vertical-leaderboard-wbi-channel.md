# R-20261010-bigstream-06 · B站分区垂直榜通道工程候选评估（wbi 签名 vs legacy 路由）

> OS 循环 R1857 · explore#6（B5 段子·幽默工艺对标「垂直榜 wbi 签名通道工程候选」挂账位承接）
> 缺口锚=R1362 B 面 slice 三刀 -352 风控墙判负留痕（ranking/v2 rid=0/5/24 零 key 不可达·wbi 签名=工程候选挂账）
> 纪律=research-protocol（源分级/零断言/限时律）·窗读数=外锚 ~10 min ≤15 min 限时律·17 请求全匿名只读零 key
> 证据件=`.c3-tmp/r1857_wbi_evidence.json`（原始响应读数留档）+ 探针 `.c3-tmp/r1857_wbi_probe.py`

## 1. 判据预注册（执行前立）

- **J1**：匿名 GET `/x/web-interface/nav` 可取 wbi keys（img_key+sub_key）→ mixin key 可派生
- **J2**：wbi 签名请求 `ranking/v2?rid=138&type=all` 返回 code==0 且列表 ≥1 条
- FAIL=判负留痕（P-2026-09-28-02 ①）·目标级判据（B5 立场）=「搞笑分区垂直榜通道可达」

## 2. 实测读数（2026-10-10 03:03-03:10·全部 UA+Referer 标准头·零 cookie 零 key）

| # | 探针 | 读数 | 判 |
|---|---|---|---|
| R0 | ranking/v2 rid=138 unsigned | code=**-352** | 复现 R1362 风控墙 ✓ |
| J1 | nav 匿名 | code=-101（未登录预期态）+ `wbi_img.img_url/sub_url` 双 key 取得（img_key `7cd0849…77c` + sub_key `4932ca…c45`）→ mixin key 32 字符派生成功 | **PASS** |
| J2a | wbi 签名（wts+w_rid MD5·mixin 置换表 64→32）| code=**-352**（签名后仍风控墙） | **FAIL** |
| J2b | wbi 签名 + buvid3/buvid4（finger/spi 匿名指纹端点=浏览器首访标准件）| code=**-352** | **FAIL** |
| J3 | **legacy `ranking/region?rid=138&day=3`（无签名无 cookie）** | code=**0**·9 条真条目（top1 播放 3,229,616）| **PASS（主发现）** |
| J3b | 泛化：rid=138 day=7 / rid=5 day=3 | 双双 code=0（10 条·top1 播放 4,685,697 / 11 条·top1 播放 5,217,309）| 泛化成立 |

**legacy 条目 schema 全字段**（零断言直录）：`aid/bvid/title/author/mid/play/video_review/coins/favorites/pts/duration/create/typename/pic/description` —— bvid+aid 自带源锚（无来源不发布红线消费位天然在位）；duration/play/create 字段=B 面密度结构读数可承载面。

top1 样例（rid=138 day=3）：《每天一遍，天天开心》·小小潮爱生活·播放 3,229,616·0:58·bvid `BV1dFdpYqEcq`。

## 3. 定谳

1. **目标级判据=PASS via legacy route**：搞笑分区垂直榜通道零 key 匿名可达（`ranking/region?rid=N&day=D` 族·rid 与 day 双参数泛化实证）——R1362「B 面不可达」结论由「v2 端点不可达」修正为「v2 不可达但 legacy 路由可达」。
2. **wbi 工程候选=判负留痕（双面）**：对 v2 端点**不充分**（签名+匿名 buvid 后仍 -352·墙在完整浏览器指纹链域=猫鼠工程非零 key 域）；对 legacy 端点**不必要**（无签名即通）。候选关闭，重开条件=legacy 路由失效且 B 面消费面确有 v2 独有字段需求。
3. 操作红一笔（如实）：nav 的 sub key 字段名=`sub_url`（非社区文档面 `img_sub_url`）——首跑 sub_key 空读数即此，原始响应直读勘正。

## 4. 消费位

- **B5 B 面 slice 升级解锁**：「top 段子主阵地=搞笑分区垂直面」假设（R1358 A 面 6.9% 标题带推断+R1362 popular 12.0% 标签侧佐证）现可用**真垂直榜数据**直接核验——B 面结构腿（标题/播放/时长带）零 key 可执行；**C 面单件密度采样（≥3 笑点/分钟判据）仍挂账号期不变·段子库提案维持不触发**（判据未全判 pending 留痕照旧）。
- **B 面真榜单读数已交付（explore#20 · R1858 收口）**：user-research v1.9.2 §9.3（rid=138 day=3/7 双窗 18 件·播放 1.27M-10.9M·梗位标题面 18/18 构式对照落位表·主阵地假设三态判=**支持〔观察级·单窗〕**·采样框互证）——「B 面结构腿」消费位就此闭合；余强判位=30 日窗+通用热榜同窗对照（explore 后继）+C 面密度（账号期）。
- 后继队列项=explore#20 已 done（读数落 §9.3）；explore#21=主阵地假设双窗强判位（30 日窗读数+通用热榜同窗对照）零 key 可领。
- daily_brief/radar 接线位：不在本件射程（反重复律·现有 18 源架构改造=独立评估件）；potential 消费=搞笑区垂直榜作为标题面扫描源的增量源候选。

## 5. 红线与纪律对位

- 无来源不发布：条目自带 bvid/aid 源锚 ✓（本件=纯调研不发布·无 AIGC 标识涉面）
- 脱敏律：公开平台榜单数据·无涉 ✓
- 源分级：A=官方公开 API 直读（nav/ranking 族）·零断言=只录实测响应·限外锚窗 ≤15 min ✓（实耗 ~10 min·17 请求）

## 变更记录

- 2026-10-10 v1.1 R1858（explore#20 消费位收口注记：B 面真榜单读数落 user-research v1.9.2 §9.3·主阵地假设三态判=支持〔观察级·单窗〕·后继=explore#21 双窗强判位）
- 2026-10-10 v1.0 R1857 初版（explore#6 承接·B5 挂账位收口·legacy 路由主发现）
