# Prompt 设计文章写作规范

写 Prompt 设计相关的文章时，示例应基于 AITutor 的实际规范。

## 示例格式

- **发言**: 以 `发言开始:` 为前缀
- **板书操作**: 使用 `<document-opt>` XML 标签
  - 添加: `<document-opt method="add" id="T1" type="text" belong="C1" content="..." />`
  - 高亮: `<document-opt method="highlight" id="T1" />`
  - 修改: `<call-text id="T1" action="rewrite" content="..." />`
- **教具/情感**: 使用 XML 标签
  - 情感: `<emotion type="super-affirm" />`
  - 等待: `<wait />`
- **混合输出**: 发言、板书、教具指令可混合在同一段中

## 参考文件

- 完整对话示例: `work-standard/AITutor对话示例.md`

## 示例

```
发言开始:同学们，我们来看这个公式。<document-opt method="add" id="T1" type="text" belong="C1" content="勾股定理：a² + b² = c²" />这就是著名的勾股定理。<document-opt method="highlight" id="T1" />
```
