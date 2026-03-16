# Claude Code Configuration

## Language
- User communicates in Chinese, respond in Chinese when appropriate

## Permissions
- Allow all WebFetch calls
- Allow all file read/write/edit operations within this project
- When the user provides a web URL, always use agent-browser first to open it (not WebFetch)
- Only fall back to WebFetch if agent-browser is unavailable or fails

## Conventions
- 流程图只保存 Mermaid 源代码（.mmd 文件），不保存生成的图片
