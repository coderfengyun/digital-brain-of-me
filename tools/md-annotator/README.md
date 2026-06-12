# Markdown Annotator

一个给本仓库 Markdown 文件做可视化批注的小工具。它把 `.md` 渲染成网页，你可以选中文本、写修改意见，批注会保存到同目录的 sidecar 文件。

## 使用

```bash
npm run annotate:md
```

打开终端输出里的本地地址，默认是：

```text
http://127.0.0.1:4177
```

## 批注文件

如果原文件是：

```text
content/drafts/example.md
```

批注会保存为：

```text
content/drafts/example.annotations.json
```

之后可以对 Codex 说：

```text
处理 content/drafts/example.annotations.json 里的 open 批注
```

Codex 会根据 `quote`、`comment`、`line_start` 和 `line_end` 修改原 Markdown。

## 数据格式

```json
{
  "file": "content/drafts/example.md",
  "version": 1,
  "updated_at": "2026-06-12T00:00:00.000Z",
  "annotations": [
    {
      "id": "ann-20260612-xxxxxxxx",
      "status": "open",
      "created_at": "2026-06-12T00:00:00.000Z",
      "updated_at": "2026-06-12T00:00:00.000Z",
      "quote": "被选中的原文",
      "comment": "这里改得更口语一点",
      "line_start": 12,
      "line_end": 14,
      "context_before": "...",
      "context_after": "..."
    }
  ]
}
```
