# Module Toolkit

Tools and guides for extending the Digital Brain system by creating new modules.

## Structure

```
module-toolkit/
├── MODULE-TOOLKIT.md            # This file
├── MODULE_CREATION_GUIDE.md     # Complete creation guide
├── create_module.py             # Automated module creator
└── check_module_integration.py  # Integration checker
```

## Purpose

Module Toolkit provides:
- **Automated Creator**: Script to generate new modules with system integration
- **Creation Guide**: Step-by-step instructions for building new modules
- **Integration Checker**: Automated verification of module completeness

## Usage

### Creating a New Module

**Automated creation** (recommended):

```bash
# Create module and auto-integrate into system
python module-toolkit/create_module.py <module_name> <keyword>

# Example:
python module-toolkit/create_module.py tasks task
```

This automatically:
- ✅ Creates `knowledge/<module>/<MODULE>.md`
- ✅ Updates 6 system integration files
- ✅ Provides template with standard structure

**Manual creation**:

Follow the 5-phase process in MODULE_CREATION_GUIDE.md for custom requirements.

**Verification**:

```bash
# Check integration completeness
python module-toolkit/check_module_integration.py <module_name> <keyword>
```

### Integration Requirements

Every module must update 5 files:
- **3 Core Docs**: SKILL.md, CLAUDE.md, README.md
- **1 Module Doc**: knowledge/KNOWLEDGE.md
- **1 Skill File**: .claude/skills/digital-brain/skill.md

### Success Criteria

Integration checker must show:
- ✅ All 5 files pass (100%)
- ✅ Module files exist (data.jsonl, scripts)
- ✅ Sufficient keyword references in each file

## Integration with Other Modules

Module Toolkit enables system extension:
- **All modules** can be created following this toolkit
- **Check script** verifies completeness automatically
- **Creation guide** serves as authoritative reference

## Quick Reference

| Task | Command |
|------|---------|
| Create module (auto) | `python module-toolkit/create_module.py <name> <keyword>` |
| Create module (manual) | Follow MODULE_CREATION_GUIDE.md |
| Check integration | `python module-toolkit/check_module_integration.py <name> <keyword>` |
| View requirements | See "Integration Requirements" section above |

---

**For detailed instructions, see [MODULE_CREATION_GUIDE.md](MODULE_CREATION_GUIDE.md)**
