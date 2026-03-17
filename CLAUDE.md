# Claude Code Configuration

## Language
- User communicates in Chinese, respond in Chinese when appropriate

## Permissions
- Allow all file read/write/edit operations within this project
- When the user provides a web URL or需要将网页内容转成 Markdown，统一使用 Chrome MCP（navigate_page + take_snapshot），不使用 WebFetch 或 agent-browser

## Conventions
- 流程图只保存 Mermaid 源代码（.mmd 文件），不保存生成的图片
