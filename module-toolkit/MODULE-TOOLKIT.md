# Module Toolkit

Tools and guides for extending the Digital Brain system by creating new modules.

## Structure

```
module-toolkit/
├── MODULE-TOOLKIT.md           # This file
├── MODULE_CREATION_GUIDE.md    # Complete creation guide
└── check_module_integration.py # Integration checker
```

## Purpose

Module Toolkit provides:
- **Creation Guide**: Step-by-step instructions for building new modules
- **Integration Checker**: Automated verification of module completeness
- **Best Practices**: Lessons learned from existing modules

## Usage

### Creating a New Module

Follow the 6-phase process in MODULE_CREATION_GUIDE.md:

```bash
# 1. Read the guide
open module-toolkit/MODULE_CREATION_GUIDE.md

# 2. Create module files following the checklist
# 3. Update 8 system integration files
# 4. Verify integration
python module-toolkit/check_module_integration.py <module_name> <keyword>
```

**Example**:
```bash
# Check if papers module is properly integrated
python module-toolkit/check_module_integration.py papers paper
```

### Integration Requirements

Every module must update 6 files:
- **3 Core Docs**: SKILL.md, AGENT.md, README.md
- **1 Module Doc**: knowledge/KNOWLEDGE.md
- **2 Skill Files**: .claude/skills/digital-brain/skill.md, instructions.xml

### Success Criteria

Integration checker must show:
- ✅ All 6 files pass (100%)
- ✅ Module files exist (data.jsonl, scripts)
- ✅ Sufficient keyword references in each file

## Module Naming Convention

**Main Document**: `<MODULE>.md` (uppercase module name)

Examples:
- ✅ PAPERS.md, KNOWLEDGE.md, MODULE-TOOLKIT.md
- ❌ README.md, Papers.md, papers.md

## Integration with Other Modules

Module Toolkit enables system extension:
- **All modules** can be created following this toolkit
- **Check script** verifies completeness automatically
- **Creation guide** serves as authoritative reference

## Quick Reference

| Task | Command |
|------|---------|
| Create module | Follow MODULE_CREATION_GUIDE.md |
| Check integration | `python module-toolkit/check_module_integration.py <name> <keyword>` |
| View requirements | See "Integration Requirements" section in guide |

---

**For detailed instructions, see [MODULE_CREATION_GUIDE.md](MODULE_CREATION_GUIDE.md)**
