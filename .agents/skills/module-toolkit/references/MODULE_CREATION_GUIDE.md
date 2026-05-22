# Digital Brain - 模块创建指南

完整的模块创建流程，确保新模块完全集成到系统中。

## 🚀 快速开始 (自动化创建)

**推荐方式**: 使用自动化脚本

```bash
# 默认: 在 knowledge/ 子目录下创建
python .claude/skills/module-toolkit/scripts/create_module.py <module_name> <keyword>

# 例如:
python .claude/skills/module-toolkit/scripts/create_module.py tasks task
# 创建: knowledge/tasks/TASKS.md

# 顶级目录: 使用 --top-level 标志
python .claude/skills/module-toolkit/scripts/create_module.py <module_name> <keyword> --top-level

# 例如:
python .claude/skills/module-toolkit/scripts/create_module.py projects project --top-level
# 创建: projects/PROJECTS.md
```

**自动完成**:
- ✅ 创建 `<module>/<MODULE>.md` (顶级) 或 `knowledge/<module>/<MODULE>.md` (子目录)
- ✅ 更新 6 个系统集成文件
- ✅ 提供下一步指导

**后续步骤**:
1. 编辑 `<MODULE>.md` 定义数据模型
2. 如需要,创建 `<module>.jsonl`: `touch <module_path>/<module>.jsonl`
3. 验证集成: `python .claude/skills/module-toolkit/scripts/check_module_integration.py <module> <keyword>`

**选择目录的建议**:
- 📁 **knowledge/** - 适合知识管理类模块 (bookmarks, research, learning)
- 📁 **顶级目录** - 适合独立功能模块 (operations, network, identity, content, investment)

---

## ⭐ 核心命名规范

**模块主文档必须遵循以下命名规则**:

```
✅ 正确: <MODULE>.md  (模块名全大写 + .md)
   示例: AI.md, KNOWLEDGE.md, MODULE-TOOLKIT.md

❌ 错误: README.md, readme.md, Papers.md, papers.md
```

**入口文件职责**: 只说明如何使用模块
- ✅ 数据格式、使用方法、目录结构、模块集成
- ❌ 不包含: 开发指南、规范文档、系统架构

**检查方法**:
```bash
python .claude/skills/module-toolkit/scripts/check_module_integration.py <module_name> <keyword>
```

---

## 📖 手动创建流程 (高级自定义)

如果自动化脚本不满足需求,按以下流程手动创建:

## 📋 5阶段创建流程

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

**⛔ 避免**:
- 多个 README 类文件
- 开发文档 (归属 module-toolkit skill)
- 超过2个文档文件

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

### 阶段三: 系统集成 ⭐ (1-2小时)

**必须更新 3 个文件**:

#### 核心文档 (2个)

1. **CLAUDE.md**
   - Module Navigation 表添加新模块入口
   - Data Entry Schemas 添加数据格式（如有 JSONL）
   - 添加自动化脚本列表

2. **README.md**
   - 更新目录结构图
   - 添加脚本列表

#### 模块文档 (1个)

3. **knowledge/KNOWLEDGE.md** (或对应父模块)
   - 添加新模块说明
   - 更新扩展指南

**⚠️ 最容易遗漏**:
- CLAUDE.md 的多个位置（Module Navigation + Schemas）

**验证命令**:
```bash
# 检查每个文件的引用次数
for file in CLAUDE.md README.md; do
  echo "$file: $(grep -c '<keyword>' $file)"
done

# 运行自动检查
python .claude/skills/module-toolkit/scripts/check_module_integration.py <module> <keyword>
```

---

### 阶段四: 跨模块集成 (1-2小时)

**设计数据流向**:
- 定义与其他模块的集成点
- 在相关模块文档中添加引用
- 确保 ID 格式一致

**检查点**:
- [ ] 在相关模块的主文档中提及新模块
- [ ] 跨模块引用使用一致的 ID 格式
- [ ] 标签命名与系统其他部分一致

---

### 阶段五: 质量保证 (1小时)

**数据一致性**:
- [ ] ID 格式统一
- [ ] 日期格式统一 (`YYYY-MM-DD`)
- [ ] 标签命名一致
- [ ] JSONL 格式正确 (每行一个 JSON 对象)

**集成检查**:
```bash
python .claude/skills/module-toolkit/scripts/check_module_integration.py <module> <keyword>
```

**期望结果**: ✅ 100% (all files pass)

---

## 🔍 最容易遗漏的检查项

### 1. CLAUDE.md 多个位置 (⭐⭐⭐ 最重要)
- Module Navigation 表
- Data Entry Schemas（如有新数据格式）

### 2. README.md 的不同区块
- 目录结构图
- 脚本列表

### 3. 命名规范
- 主文档使用大写: `<MODULE>.md`
- 数据文件使用小写: `<module>.jsonl`

### 4. 文档职责
- 入口文件只说明使用方法
- 不包含开发指南内容

---

## 📊 文件清单

### 模块内文件 (最少2个)
- ✅ `<module>.jsonl` - 数据文件
- ✅ `<MODULE>.md` - 主文档

### 脚本文件 (最少2个)
- ✅ `scripts/add_<module>.py`
- ✅ `scripts/search_<module>.py`
- ⚪ `scripts/update_<module>_status.py` - 可选

### 系统文档更新 (4个)
- ✅ 3个核心文档 (skill.md, CLAUDE.md, README.md)
- ✅ 1个模块文档

---

## 💡 最佳实践

### 1. 先 MVP 后完善
**MVP 包含**:
- 1个 JSONL 文件
- 1个主文档
- 2个脚本 (add + search)

### 2. 对比现有模块
```bash
# 对比文档结构
diff <(grep "^##" knowledge/ai/AI.md) \
     <(grep "^##" knowledge/KNOWLEDGE.md)
```

### 3. 及时验证
每完成一个阶段就运行检查脚本，不要等到最后。

---

## 🎯 成功标准

### 集成检查: ✅ 100%
```bash
python .claude/skills/module-toolkit/scripts/check_module_integration.py <module> <keyword>
```


---

## 📚 参考资料

### 成功案例: AI 模块
- **位置**: `knowledge/ai/`
- **特点**: 领域归属清晰，长文处理结果由 `sources/sources.jsonl` 索引
- **文件数**: 按主题目录增长
- **集成度**: 由 `sources` 账本和 `knowledge/KNOWLEDGE.md` 共同保证

**可参考**:
- 数据模型设计
- 文档组织方式
- 脚本实现模式
- 系统集成方法

### 其他模块
- **knowledge/** - 简洁的父模块设计
- **module-toolkit skill** - 工具模块模式

---

## 🔄 持续改进

模块创建后:
- 根据使用反馈优化工作流
- 补充缺失的文档
- 改进脚本功能
- 更新本指南

**记录问题**: 记录遇到的问题和解决方案，帮助改进未来的模块创建过程。
