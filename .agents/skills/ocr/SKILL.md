---
name: ocr
description: "OCR tool for extracting text from images. Use when: user wants to recognize text in images, convert screenshots/photos to text, or extract content from long-form image posts. Trigger on phrases like 'OCR', '识别这张图', '读一下这张图', '图片识别', '图片转文字', '提取文字', 'recognize text', 'extract text from image'."
---

# OCR — 图片文字识别

通用图片 OCR 工具：将图片中的文字识别为 Markdown 文本。

## 环境

`~/ocr-env` 虚拟环境（已安装 easyocr）

## 流程

```bash
# 1. 激活环境并运行 OCR
source ~/ocr-env/bin/activate && python3 -c "
import easyocr
reader = easyocr.Reader(['ch_sim', 'en'], gpu=False)
results = reader.readtext('<图片路径>', detail=0, paragraph=True)
for p in results:
    print(p)
    print()
"
```

```bash
# 2. 将识别结果整理后保存为 Markdown
# 命名规则：与原图同名 + _OCR 后缀
# 例如：史诗级TACO.jpg → 史诗级TACO_OCR.md
# 保存位置：与原图同目录
```

## 整理要求

- OCR 原始输出有断行和识别误差，需人工修正断句、补全缺字
- 保留原文结构（标题、段落、列表）
- 不添加额外分析或总结，忠于原文
- 文件开头注明来源和日期
