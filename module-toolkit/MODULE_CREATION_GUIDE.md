# Digital Brain - 模块创建指南

本指南记录了创建新模块时需要完成的所有步骤和检查点,基于创建papers模块的实际经验总结。

## ⭐ 核心命名规范

**模块主文档必须遵循以下命名规则**:

```
✅ 正确: <MODULE>.md  (模块名全大写 + .md)
   示例: PAPERS.md, KNOWLEDGE.md, MODULE-TOOLKIT.md

❌ 错误: README.md, readme.md, Papers.md, papers.md
```

**为什么?**
- 统一性: 所有模块遵循相同命名规范
- 可识别: 大写文件名立即表明这是模块主文档
- 避免冲突: 不与项目根目录的 README.md 混淆

**检查方法**:
```bash
python module-toolkit/check_module_integration.py <module_name> <keyword>
```

---

## 📋 创建新模块检查清单

### ✅ 阶段一:需求分析与设计 (30分钟)

#### 1. 明确需求
- [ ] 与用户讨论核心需求和期望
- [ ] 确定模块的主要功能
- [ ] 了解用户的工作流偏好
- [ ] 确定数据组织方式

**提问模板**:
```
1. 您期望这个模块解决什么问题?
2. 您希望如何组织数据? (格式、结构)
3. 您希望记录哪些信息?
4. 您希望如何与其他模块集成?
```

#### 2. 设计数据模型
- [ ] 设计JSONL元数据格式
- [ ] 设计详细内容文件格式(如果需要)
- [ ] 确定ID命名规则
- [ ] 设计标签体系

**示例 (papers模块)**:
- JSONL: `papers.jsonl` (元数据)
- MD: `paper-YYYYMMDD-XXX.md` (详细笔记)
- ID格式: `paper-YYYYMMDD-XXX`
- 三层标签: 领域/方法/应用

#### 3. 设计工作流
- [ ] 绘制数据流向图
- [ ] 确定关键操作步骤
- [ ] 设计与其他模块的集成点

---

### ✅ 阶段二:核心文件创建 (2-3小时)

#### 1. 创建模块目录和基础文件

**⚠️ 重要:遵循原repo的文档规范**

**必需文件**:
```bash
knowledge/新模块名/
├── <module>.jsonl         # 核心数据库 (REQUIRED)
└── <MODULE>.md            # 主文档,大写命名 (REQUIRED)
```

**可选文件**(仅在确实需要时添加):
```bash
knowledge/新模块名/
├── TEMPLATE.md            # 仅当内容结构复杂时
└── EXAMPLE.md             # 仅当示例能显著帮助理解时
```

**⛔ 避免创建**:
- ❌ 多个README类文件 (README.md + QUICKSTART.md + OVERVIEW.md)
- ❌ 开发文档 (COMPLETION_REPORT.md, SUMMARY.md) - 这些属于 module-toolkit/
- ❌ 超过3个文档文件

**文档大小规范**:
- **<MODULE>.md**: 100-150行 (~500-700词) - 聚焦数据格式和工作流
- **TEMPLATE.md**: < 200行
- **EXAMPLE.md**: < 250行
- **总文档量**: < 600行/模块

**检查点**:
- [ ] 目录创建在正确位置
- [ ] JSONL文件初始化(空文件或示例数据)
- [ ] ⭐ **主文档命名正确**: `<MODULE>.md` (全大写,不是README.md)
- [ ] 文档总量 < 600行
- [ ] 没有重复/冗余文档
- [ ] 检查脚本可以通过命名规范验证

#### 2. 编写主文档 (<MODULE>.md)

**⭐ 命名规则 (必须遵守)**:
- 使用**大写模块名**作为主文档名: `<MODULE>.md`
- 示例: `PAPERS.md`, `KNOWLEDGE.md`, `CONTACTS.md`, `MODULE-TOOLKIT.md`
- ❌ 不要使用: `README.md`, `readme.md`, `Papers.md`
- ✅ 正确格式: 模块名全大写 + `.md` 扩展名

**⭐ 文档职责 (入口文件标准)**:

模块入口文件的**唯一职责**是说明**如何使用这个模块**:
- ✅ 数据格式 (JSONL schema)
- ✅ 使用方法 (CLI命令、工作流)
- ✅ 目录结构
- ✅ 与其他模块的集成
- ❌ 不包含: 开发指南、规范文档、系统架构

**标准文档结构** (100-150行):
```markdown
# <Module Name> - Brief Description

Brief introduction (2-3 sentences) - What this module does.

## Structure
File organization diagram - Show directory layout

## Data Schema
Complete JSONL schema - Document all fields with types and descriptions

## Workflows (optional)
Step-by-step usage workflows - How users interact with this module

## Usage
CLI commands and examples - Concrete usage instructions

## Integration with Other Modules (optional)
Cross-module relationships - How this connects to other parts

## Integration with Other Modules
How this module connects to others

## Further Reading (optional)
Links to TEMPLATE.md, EXAMPLE.md if they exist
```

**内容原则**:
- **聚焦**: 数据格式 + 工作流 + 使用命令
- **简洁**: 避免冗长说明,用示例代替解释
- **实用**: 提供可执行的命令,而非理论讨论
- **精确**: 100-150行,~500-700词

**检查点**:
- [ ] ⭐ **文件名使用大写模块名**: `<MODULE>.md` (例: PAPERS.md, CONTACTS.md)
- [ ] 长度在100-150行之间
- [ ] 所有JSONL字段都有说明
- [ ] 包含完整工作流程
- [ ] 提供CLI使用示例
- [ ] 没有哲学性/理论性长篇内容

#### 3. 创建自动化脚本

**至少需要**:
- [ ] 添加操作脚本 (如 `add_*.py`)
- [ ] 查询操作脚本 (如 `search_*.py`)
- [ ] (可选)更新操作脚本 (如 `update_*.py`)

**脚本规范**:
```python
#!/usr/bin/env python3
"""
脚本说明

Usage:
    ./scripts/script_name.py [options]
"""

# 标准库导入
# 项目路径定义
# 功能函数
# 主函数
# if __name__ == "__main__":
```

**检查点**:
- [ ] 脚本有执行权限 (`chmod +x`)
- [ ] 支持 `--help` 参数
- [ ] 错误处理完善
- [ ] 输出信息清晰友好

---

### ✅ 阶段三:文档体系完善 (2-3小时)

#### 1. 创建扩展文档

**推荐文档**:
- [ ] `QUICKSTART.md` - 5分钟快速入门
- [ ] `EXAMPLE.md` - 完整使用示例
- [ ] `OVERVIEW.md` - 系统架构说明
- [ ] `INTEGRATION.md` - 跨模块集成指南

**QUICKSTART.md 结构**:
```markdown
# 快速入门

## 🚀 5分钟开始
### 添加第一条记录
### 查询数据
### 更新状态

## 📋 完整工作流

## 💡 使用技巧

## 📚 参考资料
```

#### 2. 创建示例文件

**检查点**:
- [ ] 示例数据真实可用
- [ ] 示例覆盖主要功能
- [ ] 示例展示最佳实践

---

### ✅ 阶段四:系统集成 (1-2小时)

**⚠️ 这是最容易遗漏的部分!**

#### 1. 更新根目录文档 (6个文件)

##### ✅ SKILL.md
- [ ] `description` 添加新模块触发词
- [ ] `When to Activate` 添加使用场景
- [ ] `Trigger phrases` 添加触发短语
- [ ] `Module Overview` 更新目录结构
- [ ] `Examples` 添加使用示例
- [ ] `Guidelines` 添加相关原则
- [ ] `References` 添加内部链接

**位置**:
```yaml
description: "...旧模块..., 新模块关键词, ..."
触发短语: "..., 新模块动作, ..."
```

##### ✅ AGENT.md
- [ ] `When User Asks To` 表格添加新命令
- [ ] `Module Loading Strategy` 添加数据加载
- [ ] `Load on Demand` 添加详细文件
- [ ] `Data Entry Best Practices` 添加数据格式
- [ ] `Automation Scripts` 列出新脚本

**关键位置**:
```markdown
| "新操作" | 处理流程 |

2. **Load on Content Tasks** (L2):
   - 新模块的.jsonl文件

### Adding 新数据类型
[数据格式示例]

- `python scripts/新脚本.py` - 说明
```

##### ✅ ARCHITECTURE.md
- [ ] 对应模块的目录结构更新
- [ ] 添加数据流程图
- [ ] 更新 Key Features

**位置**:
```markdown
### X. 模块名 Module

**Purpose**: ...

```
模块目录/
├── 新子目录/
```

**数据流程图**
```

##### ✅ EXAMPLES.md
- [ ] 在相关示例中使用新模块
- [ ] 添加完整的使用示例
- [ ] 展示跨模块集成

**示例位置**:
- Example 4: Researcher Managing Projects
- Pro Tips
- Advanced Workflows

##### ✅ README.md
- [ ] 目录结构图添加新模块
- [ ] Quick Start 添加使用示例
- [ ] 自动化脚本列表更新
- [ ] Claude Code 示例添加

**关键位置**:
```
digital-brain-of-me/
├── knowledge/
│   ├── 新模块/

#### Add New Thing
```bash
python scripts/new_script.py
```

"新操作示例"
```

##### ✅ knowledge/KNOWLEDGE.md (或对应父模块)
- [ ] 添加新子模块说明
- [ ] 更新数据格式描述
- [ ] 添加使用提示

#### 2. 更新Claude Code Skill (2个文件)

**⚠️ 经常被遗忘!**

##### ✅ .claude/skills/digital-brain/skill.md
- [ ] `Core Capabilities` 更新模块列表
- [ ] `Commands` 添加新操作
- [ ] `Automation Scripts` 更新数量和列表
- [ ] `Usage Examples` 添加示例

**位置**:
```markdown
3. **Knowledge** - ..., 新模块内容

- 新操作描述

Seven Python scripts in `scripts/`:
5. `新脚本.py` - 说明

### 新操作示例
"示例命令"
```

##### ✅ .claude/skills/digital-brain/instructions.xml
- [ ] 对应 `<module>` 添加文件列表
- [ ] `<operations>` 添加新操作定义
- [ ] `<behavior-guidelines>` 添加相关原则
- [ ] `<context-loading>` 添加加载策略

**位置**:
```xml
<module name="knowledge">
  <files>
    <file>新模块/数据文件</file>
  </files>
  <purpose>...新模块...</purpose>
</module>

<operation name="新操作">
  <trigger>触发条件</trigger>
  <action>执行动作</action>
  <fields>字段列表</fields>
</operation>

<guideline>新模块相关原则</guideline>

<on-新模块-task>
  <load>新模块数据</load>
  <reason>加载原因</reason>
</on-新模块-task>
```

#### 3. 验证系统文档完整性

**检查脚本**:
```bash
# 检查所有文档中的新模块引用
echo "=== 检查 SKILL.md ===" && grep -c "新模块关键词" SKILL.md
echo "=== 检查 AGENT.md ===" && grep -c "新模块关键词" AGENT.md
echo "=== 检查 ARCHITECTURE.md ===" && grep -c "新模块关键词" ARCHITECTURE.md
echo "=== 检查 EXAMPLES.md ===" && grep -c "新模块关键词" EXAMPLES.md
echo "=== 检查 README.md ===" && grep -c "新模块关键词" README.md
echo "=== 检查 Skill ===" && grep -c "新模块关键词" .claude/skills/digital-brain/skill.md
```

**期望结果**: 每个文件都应该有至少5-10处引用

---

### ✅ 阶段五:跨模块集成 (1-2小时)

#### 1. 设计数据流向

**从其他模块到新模块**:
```
bookmarks → papers (发现)
papers → research (综合)
papers → ideas (启发)
papers → tasks (行动)
papers → contacts (交流)
```

#### 2. 创建INTEGRATION.md

**必需内容**:
```markdown
# 新模块集成指南

## 🔗 模块间联动

### 模块A → 新模块
**场景**: ...
**数据流**: ...
**示例**: ...

### 新模块 → 模块B
[类似格式]

## 🔄 完整工作流示例
[Mermaid流程图]

## 📋 跨模块查询示例
[具体脚本]

## 🎯 最佳实践
[引用一致性、标签管理等]
```

#### 3. 更新其他模块文档

**检查点**:
- [ ] 在相关模块的README中提及新模块
- [ ] 在research/notes中使用新模块ID格式

---

### ✅ 阶段六:质量保证 (1小时)

#### 1. 功能测试

**测试清单**:
```bash
# 1. 添加功能
python scripts/add_新模块.py [测试参数]

# 2. 查询功能
python scripts/search_新模块.py --各种参数

# 3. 更新功能
python scripts/update_新模块.py [测试参数]

# 4. 边界情况
# - 空输入
# - 重复ID
# - 无效参数
```

#### 2. 数据一致性检查

**检查点**:
- [ ] ID格式统一 (如 `paper-YYYYMMDD-XXX`)
- [ ] 日期格式统一 (`YYYY-MM-DD`)
- [ ] 标签命名与其他模块一致
- [ ] JSONL格式正确(每行一个完整JSON对象)

#### 3. 文档链接验证

**检查清单**:
```bash
# 检查所有内部链接
grep -r "\[.*\](.*.md)" knowledge/新模块/

# 检查所有脚本引用
grep -r "scripts/" knowledge/新模块/

# 检查所有模块引用
grep -r "\[.*-XXX\]" knowledge/新模块/
```

#### 4. 创建对比报告

**创建 `SUMMARY.md`**:
```markdown
# 新模块完整性检查

## 与其他模块对比
[对比表格]

## 功能测试结果
[测试清单]

## 质量检查
[一致性验证]
```

---

## 📊 文件创建总览

### 模块内文件 (最少5个,推荐8-10个)

**必需**:
1. ✅ `数据.jsonl` - 核心数据库
2. ✅ `README.md` - 模块文档
3. ✅ `TEMPLATE.md` - 内容模板

**推荐**:
4. ✅ `QUICKSTART.md` - 快速入门
5. ✅ `EXAMPLE.md` - 完整示例
6. ✅ `OVERVIEW.md` - 系统架构
7. ✅ `INTEGRATION.md` - 集成指南
8. ✅ `SUMMARY.md` - 对比总结

### 脚本文件 (最少2个,推荐3个)

1. ✅ `add_新模块.py` - 添加功能
2. ✅ `search_新模块.py` - 查询功能
3. ✅ `update_新模块_status.py` - 更新功能(可选)

### 系统文档更新 (8个文件)

**根目录** (6个):
1. ✅ `SKILL.md`
2. ✅ `AGENT.md`
3. ✅ `ARCHITECTURE.md`
4. ✅ `EXAMPLES.md`
5. ✅ `README.md`
6. ✅ `父模块/README.md`

**Claude Code Skill** (2个):
7. ✅ `.claude/skills/digital-brain/skill.md`
8. ✅ `.claude/skills/digital-brain/instructions.xml`

---

## 🔍 常见遗漏检查

### ⚠️ 最容易遗漏的地方

1. **Claude Code Skill 文件** ⭐⭐⭐
   - `.claude/skills/digital-brain/skill.md`
   - `.claude/skills/digital-brain/instructions.xml`
   - 这两个文件经常被忘记!

2. **EXAMPLES.md 的示例更新** ⭐⭐
   - 不仅要添加新示例
   - 还要在现有示例中使用新模块

3. **跨模块引用** ⭐⭐
   - 在其他模块文档中提及新模块
   - 确保ID引用格式统一

4. **AGENT.md 的多个位置** ⭐
   - "When User Asks To" 表格
   - Module Loading Strategy
   - Data Entry Best Practices
   - Automation Scripts

### ✅ 遗漏检查脚本

创建 `scripts/check_module_integration.py`:

```python
#!/usr/bin/env python3
"""检查新模块是否完全集成到系统中"""

import sys

MODULE_NAME = sys.argv[1] if len(sys.argv) > 1 else "new_module"
KEYWORD = sys.argv[2] if len(sys.argv) > 2 else MODULE_NAME

files_to_check = {
    "SKILL.md": 5,
    "AGENT.md": 5,
    "ARCHITECTURE.md": 3,
    "EXAMPLES.md": 5,
    "README.md": 5,
    ".claude/skills/digital-brain/skill.md": 3,
    ".claude/skills/digital-brain/instructions.xml": 3,
}

print(f"检查模块 '{MODULE_NAME}' 的集成完整性")
print(f"搜索关键词: '{KEYWORD}'\n")

all_passed = True
for filepath, min_count in files_to_check.items():
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
            count = content.lower().count(KEYWORD.lower())
            status = "✅" if count >= min_count else "❌"
            print(f"{status} {filepath}: {count} 次 (期望 >= {min_count})")
            if count < min_count:
                all_passed = False
    except FileNotFoundError:
        print(f"❌ {filepath}: 文件不存在")
        all_passed = False

print("\n" + "="*60)
if all_passed:
    print("✅ 所有检查通过! 模块已完全集成")
else:
    print("❌ 有文件未正确更新,请检查上述标记")

sys.exit(0 if all_passed else 1)
```

**使用方法**:
```bash
python scripts/check_module_integration.py papers paper
```

---

## 💡 创建新模块的最佳实践

### 1. 分阶段进行,不要一次完成所有

**推荐顺序**:
```
Day 1: 需求分析 + 核心文件
Day 2: 脚本开发 + 基础测试
Day 3: 文档完善 + 系统集成
Day 4: 质量检查 + 最终验证
```

### 2. 使用检查清单

- 打印本指南作为检查清单
- 逐项完成并标记
- 不要跳过任何步骤

### 3. 先完成MVP,再扩展功能

**MVP (最小可用产品)**:
- 1个JSONL文件
- 1个README
- 1个添加脚本
- 1个查询脚本
- 更新6个系统文档

**扩展功能**:
- 更多文档
- 更多脚本
- 高级功能

### 4. 对比现有模块

参考已有模块的文件结构:
```bash
# 对比文件数量
ls -1 knowledge/papers/ | wc -l
ls -1 knowledge/bookmarks/ | wc -l

# 对比文档章节
diff <(grep "^##" knowledge/papers/README.md) \
     <(grep "^##" knowledge/bookmarks/README.md)
```

### 5. 及时记录遇到的问题

在本指南中补充:
```markdown
## 🐛 已知问题和解决方案

### 问题: [描述]
**解决**: [方案]
```

---

## 📝 模板文件

### README.md 模板

```markdown
# [模块名] Module

[简短描述模块的作用]

## 核心理念

[设计思想]

## 文件结构

```
模块名/
├── 文件1
└── 文件2
```

## 数据格式

### 元数据.jsonl

```json
{
  "id": "type-XXX",
  "field1": "...",
  "field2": "..."
}
```

## 工作流程

### 步骤1
### 步骤2

## 模块集成

- **模块A → 本模块**: ...
- **本模块 → 模块B**: ...

## 快速命令

```bash
# 命令示例
```

## 相关文档

- [链接1]
- [链接2]
```

### 脚本模板

```python
#!/usr/bin/env python3
"""
[脚本说明]

Usage:
    ./scripts/script_name.py [options]
"""

import json
import argparse
from datetime import datetime
from pathlib import Path

# Paths
ROOT = Path(__file__).parent.parent
MODULE_DIR = ROOT / "knowledge" / "module_name"
DATA_JSONL = MODULE_DIR / "data.jsonl"


def main():
    parser = argparse.ArgumentParser(
        description="[描述]",
        formatter_class=argparse.RawDescriptionHelpFormatter
    )

    # 添加参数
    parser.add_argument("arg1", help="说明")
    parser.add_argument("--option", help="可选参数")

    args = parser.parse_args()

    # 执行逻辑
    print("✅ 操作完成")


if __name__ == "__main__":
    main()
```

---

## 🎯 成功标准

一个完整的模块应该满足:

### 功能完整性 ✅
- [ ] 核心功能全部实现
- [ ] 脚本测试通过
- [ ] 数据格式统一

### 文档完整性 ✅
- [ ] 所有必需文档存在
- [ ] 文档内容详尽清晰
- [ ] 示例真实可用

### 系统集成 ✅
- [ ] 8个系统文件全部更新
- [ ] 每个文件有5+处引用
- [ ] Claude Code Skill已配置

### 质量保证 ✅
- [ ] 所有测试通过
- [ ] 数据格式一致
- [ ] 文档链接有效

---

## 📚 参考资料

### 成功案例: Papers 模块

- 创建文件: 12个
- 更新文件: 8个
- 总时长: ~8小时
- 最终评分: ⭐⭐⭐⭐⭐

**关键文档**:
- [knowledge/papers/COMPLETION_REPORT.md](knowledge/papers/COMPLETION_REPORT.md)
- [knowledge/papers/SUMMARY.md](knowledge/papers/SUMMARY.md)

### 其他模块参考

- `content/` - 内容创作模块
- `network/` - 关系管理模块
- `operations/` - 任务管理模块

---

## 🔄 持续改进

本指南应该随着每次创建新模块而更新:

1. 记录遇到的新问题
2. 补充新的检查点
3. 优化工作流程
4. 更新模板文件

**版本历史**:
- v1.0 (2026-02-27): 基于papers模块创建经验初版

---

**使用本指南创建新模块,可以确保质量一致性和完整性! ✨**
