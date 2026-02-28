# Digital Brain - 模块创建指南

完整的模块创建流程，确保新模块完全集成到系统中。

## ⭐ 核心命名规范

**模块主文档必须遵循以下命名规则**:

```
✅ 正确: <MODULE>.md  (模块名全大写 + .md)
   示例: PAPERS.md, KNOWLEDGE.md, MODULE-TOOLKIT.md

❌ 错误: README.md, readme.md, Papers.md, papers.md
```

**入口文件职责**: 只说明如何使用模块
- ✅ 数据格式、使用方法、目录结构、模块集成
- ❌ 不包含: 开发指南、规范文档、系统架构

**检查方法**:
```bash
python module-toolkit/check_module_integration.py <module_name> <keyword>
```

---

## 📋 6阶段创建流程

### 阶段一: 需求分析 (30分钟)

**核心任务**:
- [ ] 明确模块功能和目标用户
- [ ] 设计 JSONL 数据模型和字段
- [ ] 确定 ID 命名规则 (如 `paper-YYYYMMDD-XXX`)
- [ ] 设计标签分类体系

**输出**: 清晰的数据模型和工作流设计

---

### 阶段二: 核心文件创建 (2-3小时)

**必需文件结构**:
```bash
knowledge/<module>/
├── <module>.jsonl         # 核心数据库
└── <MODULE>.md            # 主文档 (大写命名)
```

**可选文件** (仅在必要时):
```bash
├── TEMPLATE.md            # 内容模板 (< 200行)
└── EXAMPLE.md             # 使用示例 (< 250行)
```

**⛔ 避免**:
- 多个 README 类文件
- 开发文档 (归属 module-toolkit/)
- 超过3个文档文件
- 文档总量 > 600行

**主文档标准结构** (100-150行):
```markdown
# <Module Name> - Brief Description

Brief introduction (2-3 sentences).

## Structure
Directory layout

## Data Schema
JSONL schema with all fields

## Usage
CLI commands and examples

## Integration with Other Modules
Cross-module relationships
```

**脚本文件** (在 `scripts/` 目录):
- `add_<module>.py` - 添加数据
- `search_<module>.py` - 查询数据
- `update_<module>_status.py` - 更新状态 (可选)

---

### 阶段三: 文档完善 (可选, 1-2小时)

仅在模块功能复杂时创建:
- **TEMPLATE.md**: 内容结构模板
- **EXAMPLE.md**: 完整使用示例

**质量标准**:
- TEMPLATE.md < 200行
- EXAMPLE.md < 250行
- 聚焦实用性，避免过度文档化

---

### 阶段四: 系统集成 ⭐ (1-2小时)

**必须更新 8 个文件**:

#### 核心文档 (5个)

1. **SKILL.md**
   - 添加触发短语示例
   - 添加操作流程说明
   - 更新模块列表

2. **AGENT.md**
   - 添加快速参考表
   - 添加自动化脚本列表
   - 添加模块创建章节说明

3. **ARCHITECTURE.md** (如不存在则创建)
   - 添加模块架构图
   - 说明数据流向

4. **EXAMPLES.md** (如不存在则创建)
   - 添加使用示例
   - 添加工作流说明

5. **README.md**
   - 更新目录结构图
   - 添加快速开始命令
   - 添加脚本列表

#### 模块文档 (1个)

6. **knowledge/KNOWLEDGE.md** (或对应父模块)
   - 添加新模块说明
   - 更新扩展指南

#### AI Agent Skill (2个)

7. **.claude/skills/digital-brain/skill.md**
   - 添加操作能力说明
   - 更新命令列表

8. **.claude/skills/digital-brain/instructions.xml**
   - 添加 `<operation>` 标签
   - 定义触发器和动作

**⚠️ 最容易遗漏**:
- `.claude/skills/digital-brain/` 两个文件
- EXAMPLES.md 的多个章节
- AGENT.md 的多个位置

**验证命令**:
```bash
# 检查每个文件的引用次数
for file in SKILL.md AGENT.md README.md; do
  echo "$file: $(grep -c '<keyword>' $file)"
done

# 运行自动检查
python module-toolkit/check_module_integration.py <module> <keyword>
```

---

### 阶段五: 跨模块集成 (1-2小时)

**设计数据流向**:
- 定义与其他模块的集成点
- 在相关模块文档中添加引用
- 确保 ID 格式一致

**检查点**:
- [ ] 在相关模块的主文档中提及新模块
- [ ] 跨模块引用使用一致的 ID 格式
- [ ] 标签命名与系统其他部分一致

---

### 阶段六: 质量保证 (1小时)

**功能测试**:
```bash
# 测试添加
python scripts/add_<module>.py <test_data>

# 测试查询
python scripts/search_<module>.py --status all

# 测试更新
python scripts/update_<module>_status.py <id> --status updated
```

**数据一致性**:
- [ ] ID 格式统一
- [ ] 日期格式统一 (`YYYY-MM-DD`)
- [ ] 标签命名一致
- [ ] JSONL 格式正确 (每行一个 JSON 对象)

**文档链接**:
```bash
# 检查死链接
find . -name "*.md" -exec grep -H "\[.*\](.*/.*)" {} \; | \
  while read line; do
    # 验证链接有效性
  done
```

**集成检查**:
```bash
python module-toolkit/check_module_integration.py <module> <keyword>
```

**期望结果**: ✅ 100% (8/8 files pass)

---

## 🔍 最容易遗漏的检查项

### 1. AI Skill 文件 (⭐⭐⭐ 最重要)
- `.claude/skills/digital-brain/skill.md`
- `.claude/skills/digital-brain/instructions.xml`

### 2. 多个位置的引用
- EXAMPLES.md 的不同章节
- AGENT.md 的多个部分
- README.md 的不同区块

### 3. 命名规范
- 主文档使用大写: `<MODULE>.md`
- 数据文件使用小写: `<module>.jsonl`

### 4. 文档职责
- 入口文件只说明使用方法
- 不包含开发指南内容

---

## 📊 文件清单

### 模块内文件 (最少3个)
- ✅ `<module>.jsonl` - 数据文件
- ✅ `<MODULE>.md` - 主文档
- ⚪ `TEMPLATE.md` - 可选
- ⚪ `EXAMPLE.md` - 可选

### 脚本文件 (最少2个)
- ✅ `scripts/add_<module>.py`
- ✅ `scripts/search_<module>.py`
- ⚪ `scripts/update_<module>_status.py` - 可选

### 系统文档更新 (8个)
- ✅ 5个核心文档
- ✅ 1个模块文档
- ✅ 2个 AI Skill 文件

---

## 💡 最佳实践

### 1. 分阶段推进
- Day 1: 阶段 1-2 (需求 + 核心文件)
- Day 2: 阶段 3-4 (文档 + 系统集成)
- Day 3: 阶段 5-6 (跨模块 + 质量检查)

### 2. 先 MVP 后完善
**MVP 包含**:
- 1个 JSONL 文件
- 1个主文档
- 2个脚本 (add + search)

**后续扩展**:
- 添加 TEMPLATE.md
- 添加更多脚本
- 完善文档

### 3. 对比现有模块
```bash
# 对比文档结构
diff <(grep "^##" papers/PAPERS.md) \
     <(grep "^##" knowledge/KNOWLEDGE.md)
```

### 4. 及时验证
每完成一个阶段就运行检查脚本，不要等到最后。

---

## 🎯 成功标准

### 集成检查: ✅ 100%
```bash
python module-toolkit/check_module_integration.py <module> <keyword>
```

### 功能测试: ✅ 全部通过
- 数据添加正常
- 查询返回正确
- 状态更新有效

### 文档完整: ✅ 无死链接
- 所有内部链接有效
- 引用的文件存在
- 命令可执行

---

## 📚 参考资料

### 成功案例: Papers 模块
- **位置**: `papers/`
- **特点**: 完整的两阶段读取流程
- **文件数**: 20个 (12新增 + 8更新)
- **集成度**: 100%

**可参考**:
- 数据模型设计
- 文档组织方式
- 脚本实现模式
- 系统集成方法

### 其他模块
- **knowledge/** - 简洁的父模块设计
- **module-toolkit/** - 工具模块模式

---

## 🔄 持续改进

模块创建后:
- 根据使用反馈优化工作流
- 补充缺失的文档
- 改进脚本功能
- 更新本指南

**记录问题**: 在 module-toolkit/ 中记录遇到的问题和解决方案，帮助改进未来的模块创建过程。
