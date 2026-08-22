---
name: investment
description: "投资交易日志、盈亏计算、券商导入、投研作者管理。触发场景：交易记录（'交易记录', '更新交易', '导入交易'）；盈亏与持仓（'盈亏', '算算收益', '持仓', '仓位', 'P&L'）；券商（'币安', '富途', '招商证券', 'Binance', 'Futu'）；投研作者——提到 '洪灏'/'洪浩'/'卢麒元' 任何上下文都触发（读文章、讨论观点、更新索引、增加/追加发言或内容——即使操作看似简单也必须触发，因为有索引更新步骤）；研报（'研报', '微博研报', '下载微博', '最新文章'）；微博VIP群发言记录。Note: image OCR is handled by the standalone 'ocr' skill."
---

# Investment

交易日志管理 + 投研内容管理。

## Data Location

- 交易日志：`investment/投资日志整理/交易日志汇总表.csv`
- CSV Schema：`investment/投资日志整理/交易日志汇总表.schema.json`
- 投研作者索引：`investment/{作者名}/{作者名}.md`
- 设计文档：`investment/投资日志整理/DESIGN_盈亏统计系统设计.md`

## Scripts

All scripts live in `.codex/skills/investment/scripts/`:

- `write_trade_journal.py` — 交易日志写入工具（添加/导入/迁移/校验）
- `fetch_binance_trades.py` — 币安现货交易记录获取
- `fetch_binance_futures.py` — 币安合约（USDT-M）交易记录获取（自动分段查询，绕过7天限制）
- `fetch_binance_balances.py` — 币安账户全部资产余额及 USD 估值
- `fetch_futu_trades.py` — 富途交易记录获取
- `fetch_futu_positions.py` — 富途账户持仓及资金概览
- `fetch_cms_trades.py` — 招商证券交易记录获取（Chrome MCP）
- `calc_pnl.py` — 盈亏计算（FIFO 匹配）

---

## 交易日志操作

### 添加单条记录

```bash
python .codex/skills/investment/scripts/write_trade_journal.py add \
  --品种 BTC --代码 BTCUSDT --操作 买入 --价格 76653 --数量 0.00391 --金额 299.71 \
  --币种 USD --日期 2025-04-07 --交易平台 币安
```

必填：`--品种`、`--操作`、`--价格`、`--数量`、`--金额`、`--币种`、`--日期`。可选：`--代码`（资产唯一标识，如 US.SLV, HK.00883, 512400, BTCUSDT）、`--交易平台`（注意不是 `--平台`）、`--日期精确度`、`--备注`。完整参数见 `add --help`。

### 批量更新交易记录

当用户说"更新交易记录"时，按顺序拉取三个平台（币安 → 富途 → 招商证券）。详细步骤见 [`references/trade-import.md`](references/trade-import.md)。

### 工具命令

| 操作 | 命令 |
|------|------|
| 校验数据 | `python3 .codex/skills/investment/scripts/write_trade_journal.py validate` |
| 盈亏计算 | `python3 .codex/skills/investment/scripts/calc_pnl.py` |
| 运行测试 | `cd .codex/skills/investment/scripts && python3 -m pytest -v` |

---

## 投研内容管理

每位长期跟踪的作者在 `investment/` 下有独立目录，以 `{作者名}.md` 为索引。索引文件汇聚该作者在整个 repo 中的全部内容（研究文章、OCR 转换、podcast 转录、原始发言等），是查找某位作者观点的唯一入口。

**现有作者索引**：
- [`洪灏/洪灏.md`](../../../investment/洪灏/洪灏.md) — 宏观分析、地缘-能源-通胀传导、黄金/美元结构性分析
- [`卢麒元/卢麒元.md`](../../../investment/卢麒元/卢麒元.md) — 马克思资本论框架、货币体系、资产配置三三四原则
- [`Medi_and_莎姐/Medi_and_莎姐.md`](../../../investment/Medi_and_莎姐/Medi_and_莎姐.md) — 加密资产市场结构、流动性计算、多时间框架与仓位管理

**新建作者索引时**：
1. 在 `investment/{作者名}/` 下创建 `{作者名}.md`
2. 开头用 blockquote 简述身份、分析风格、核心关注领域
3. 按内容类型分节（Podcast 转录 / 研究文章 / 投资研究 / 一手发言等），用相对路径链接到实际文件
4. 附"关键观点速查"表格（主题 / 观点 / 出处）
5. 更新本 skill 的"现有作者索引"列表

**内容文件夹命名规则**：`YYYYMMDD-标题`（发布日期前缀），例如 `20260606-港股指数开始AI化`。同一天多篇追加字母：`20260519a-全球债券收益率飙升`、`20260519b-香港劲揪`。这样文件系统按字母排序即为时间线，且插入历史内容不影响已有文件夹名。

**向已有作者添加新内容时**：
1. 按命名规则创建文件夹，获取/保存原文为 `article.md`
2. **触发 paper-reading 全流程**：
   - 非中文文章 → 生成中文翻译 `article-zh.md`
   - 按 paper-reading skill Phase 1-3 生成精读笔记 `notes.md`
   - 注册到 `sources/sources.jsonl`（分配 ID、填写 output 路径）
3. 更新该作者的索引文件，添加链接（含翻译和笔记链接）
4. 判断是否更新"关键观点速查"表：只有**新的分析框架、新指标、或与已有观点矛盾/显著升级的判断**才追加；已有观点的重复验证或应用实例不追加

### 获取微博研报（端到端 pipeline）

当用户说"帮我获取一下XX最新研报"时，执行完整流程：下载 → OCR转录 → 生成结构化笔记。

**前置知识**：微博图片带签名认证（ssig），外部 curl 无法下载。必须通过 Chrome DevTools MCP 的 `get_network_request` 从浏览器网络请求缓存中提取图片响应体。

**常见作者微博主页**：
- 洪灏：`https://weibo.com/u/7799274131`

---

#### Phase 1：下载文本和图片

1. **导航到作者主页**：`navigate_page` → 作者微博主页 URL
2. **找到目标帖**：
   - 在"微博"tab（不是"文章"tab）的搜索框搜关键词
   - 如果用户没指定具体文章，浏览最新帖子，选择长文分析类研报（跳过转发、短评）
   - 点击进入目标帖
3. **获取全文**：
   - 长帖先点"展开"
   - `take_snapshot` 获取正文
4. **下载配图**（关键步骤，不能用 curl）：
   - 点击任一配图 → 点"查看大图" → 让浏览器加载 `mw2000` 分辨率图片
   - `list_network_requests(resourceTypes=["image"])` → 找 URL 含 `mw2000` 的请求 reqid
   - 逐个 `get_network_request(reqid=xxx, responseFilePath=本地路径)` 保存
   - 保存目录：`investment/{作者名}/{文章简短标题}/`
5. **写 article.md**：在同一子目录创建，包含：
   - 元信息 blockquote（来源、日期、链接）
   - 正文
   - 配图引用（`![image_N](image_N.jpg)`）

#### Phase 2：OCR 图片转录

对每张配图，使用 `ocr` skill 转录为纯文本：

```bash
source ~/ocr-env/bin/activate && python3 -c "
import easyocr, sys
reader = easyocr.Reader(['ch_sim', 'en'], gpu=False)
results = reader.readtext('IMAGE_PATH', paragraph=True)
print('\n\n'.join([r[1] for r in results]))
" > IMAGE_OCR_PATH
```

- 输出文件命名：`image_N_OCR.md`，与图片同目录
- 人工校对 OCR 结果，修正识别错误
- 将所有 OCR 文本按图片顺序合并，得到图片中的完整文字内容

#### Phase 3：合成完整文本 + 生成笔记

1. **合成研报全文**：将 article.md 正文 + 所有 OCR 转录文本合并为一份完整的研报文本
2. **更新作者索引**：在 `investment/{作者名}/{作者名}.md` 中添加新文章链接
3. **调用 paper-reading skill 生成笔记**：
   - 为研报分配 ID（`paper-YYYYMMDD-XXX`）
   - 将合成全文保存在 `investment/{作者名}/{文章简短标题}/article.md` 或 `source.md`
   - 更新 `sources/sources.jsonl`
   - 按 paper-reading skill 的三阶段流程（全局扫描 → 叙事提取 + 证据验证 → 批判思考）在同一目录生成 `notes.md`
   - `sources.jsonl` 的 `output` 指向 `investment/{作者名}/{文章简短标题}/notes.md`
   - 模板选择：洪灏的研报通常用 **Narrative**（叙事型，时间/事件驱动分析）

> **注意**：如果用户只要求下载不需要笔记，执行到 Phase 1 即可。如果图片中没有文字内容（纯图表），Phase 2 可跳过。向用户确认是否需要完整 pipeline。

### 微博视频投研内容

当用户分享微博视频链接，或 `take_snapshot` 发现帖子是视频（有"播放视频"按钮）而非图文时：

1. 点击"播放视频" → `list_network_requests(resourceTypes=["media"])` 获取 `.mp4` URL → `curl -L -H "Referer: https://weibo.com/"` 下载到 `investment/{作者名}/{主题}/video.mp4`
2. 触发 `transcribe` skill 对 `video.mp4` 进行转录（输出到同一目录）
3. 基于转录内容直接生成精读笔记 `notes-YYYYMMDD.md`（不询问用户）
4. 更新作者索引，按规则判断是否更新"关键观点速查"表
5. 清理 `video.mp4`
