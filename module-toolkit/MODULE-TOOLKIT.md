# Module Toolkit

This directory contains tools and guides for creating and managing Digital Brain modules.

## 📁 Contents

### MODULE_CREATION_GUIDE.md
Complete step-by-step guide for creating new modules in the Digital Brain system.

**Includes:**
- 6-phase creation process (Requirements → Core Files → Documentation → Integration → Cross-Module → QA)
- Detailed checklists for each phase
- File templates and examples
- Common pitfalls and how to avoid them (especially the 8-file integration requirement)

**Key requirements:**
- Keep documentation lean (~100-150 lines for main doc)
- Follow naming: `<MODULE>.md` (uppercase)
- Total docs < 600 lines per module
- Focus on data schema + workflows

**When to use:** Creating any new module (projects, contacts, courses, etc.)

### check_module_integration.py
Automated checker that verifies module integration completeness.

**Usage:**
```bash
python module-toolkit/check_module_integration.py <module_name> <keyword>
```

**Examples:**
```bash
# Check papers module
python module-toolkit/check_module_integration.py papers paper

# Check a hypothetical contacts module
python module-toolkit/check_module_integration.py contacts contact
```

**What it checks:**
- ✅ All 8 system files have sufficient keyword references:
  - 5 core docs: SKILL.md, AGENT.md, ARCHITECTURE.md, EXAMPLES.md, README.md
  - 1 module doc: knowledge/KNOWLEDGE.md
  - 2 Claude Code Skill files: .claude/skills/digital-brain/skill.md, instructions.xml
- ✅ Module files exist (README.md, data.jsonl, scripts)
- ✅ Generates detailed pass/fail report

## 🎯 Quick Start

### Creating a New Module

1. **Read the guide:**
   ```bash
   open module-toolkit/MODULE_CREATION_GUIDE.md
   ```

2. **Follow the 6 phases:**
   - Phase 1: Requirements Analysis (30 min)
   - Phase 2: Core Files Creation (2-3 hours)
   - Phase 3: Documentation (2-3 hours)
   - Phase 4: **System Integration** (1-2 hours) ⭐ Most important!
   - Phase 5: Cross-Module Integration (1-2 hours)
   - Phase 6: Quality Assurance (1 hour)

3. **Verify integration:**
   ```bash
   python module-toolkit/check_module_integration.py <your_module> <keyword>
   ```

4. **Success criteria:**
   - ✅ All 8 files pass integration check (100%)
   - ✅ Module files exist and are functional
   - ✅ Scripts tested and working

## 🔍 Integration Requirements

Every new module **MUST** update these 8 files:

### Core Documentation (5 files)
1. **SKILL.md** - Add trigger phrases and examples
2. **AGENT.md** - Add operations and data formats
3. **ARCHITECTURE.md** - Update system architecture
4. **EXAMPLES.md** - Add usage examples
5. **README.md** - Update structure and quick commands

### Module Documentation (1 file)
6. **knowledge/KNOWLEDGE.md** - Add module description

### Claude Code Skill (2 files)
7. **.claude/skills/digital-brain/skill.md** - Add capabilities
8. **.claude/skills/digital-brain/instructions.xml** - Add operations

⚠️ **Most commonly missed:**
- `.claude/skills/digital-brain/` files (both of them!)
- Multiple sections in EXAMPLES.md and AGENT.md

## 📊 Success Examples

### Papers Module
- **Created:** 2026-02-27
- **Total files:** 20 (12 new + 8 updated)
- **Integration check:** ✅ 100% (8/8 files pass)
- **Status:** Production ready ⭐⭐⭐⭐⭐

See [knowledge/papers/COMPLETION_REPORT.md](../knowledge/papers/COMPLETION_REPORT.md) for details.

## 💡 Tips

1. **Use the checklist** - Print the guide and mark items as you complete them
2. **Don't skip Phase 4** - System integration is CRITICAL
3. **Run the checker early** - Don't wait until the end to verify
4. **Reference papers module** - It's a complete, working example
5. **Ask Claude for help** - The system can guide you through module creation

## 🚀 Self-Hosting

The Digital Brain system can now extend itself! Just say to Claude:

> "I want to create a projects module to track my side projects"

Claude will:
1. Open MODULE_CREATION_GUIDE.md
2. Guide you through all 6 phases
3. Create necessary files
4. Update all 8 system files
5. Run the integration checker
6. Ensure 100% completeness

**The system builds itself!** 🎉

---

**Last Updated:** 2026-02-27
**Version:** 1.0.0
