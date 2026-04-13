#!/usr/bin/env python3
"""
Automated module creation script for Digital Brain system.

Usage:
    python module-toolkit/create_module.py <module_name> <keyword> [--top-level]

Example:
    python module-toolkit/create_module.py tasks task                # Creates knowledge/tasks/
    python module-toolkit/create_module.py projects project --top-level  # Creates projects/

Creates:
    - <module>/<MODULE>.md (top-level or under knowledge/)
    - Updates 6 system integration files automatically
"""

import os
import sys
import re
from pathlib import Path
from datetime import datetime

# Paths
ROOT = Path(__file__).parent.parent
MODULE_TEMPLATE_PATH = Path(__file__).parent / "templates" / "MODULE_TEMPLATE.md"


def create_module_directory(module_name, top_level=False):
    """Create module directory structure"""
    if top_level:
        module_dir = ROOT / module_name
    else:
        module_dir = ROOT / "knowledge" / module_name
    module_dir.mkdir(parents=True, exist_ok=True)
    return module_dir


def generate_module_doc(module_name, keyword, top_level=False):
    """Generate MODULE.md from template"""
    module_upper = module_name.upper()
    module_title = module_name.capitalize()
    module_path = module_name if top_level else f"knowledge/{module_name}"

    template = f"""# {module_title} - Brief Description

Brief introduction to the {module_name} module (2-3 sentences).

## Structure

```
{module_path}/
└── {module_upper}.md            # This file
```

## Data Schema

(Optional) If using JSONL, define the schema here:

```json
{{
  "id": "{module_name[:4]}-XXX",
  "title": "Entry title",
  "tags": ["tag1", "tag2"],
  "created_at": "YYYY-MM-DD",
  "status": "active"
}}
```

## Usage

### Adding Entries

```bash
# Manual method
echo '{{"id": "{module_name[:4]}-001", "title": "Example"}}' >> {module_path}/{module_name}.jsonl
```

### Searching Entries

```bash
# Using grep
grep "{keyword}" {module_path}/{module_name}.jsonl

# Using jq
jq 'select(.tags[] == "tag1")' {module_path}/{module_name}.jsonl
```

## Integration with Other Modules

Describe how this module relates to other parts of the system:
- **knowledge → {module_name}**: Example integration
- **{module_name} → operations**: Example integration

## Further Reading

Add links to additional documentation if needed.
"""
    return template


def update_skill_md(module_name, keyword):
    """Update .claude/skills/digital-brain/skill.md with new module references"""
    skill_path = ROOT / ".claude" / "skills" / "digital-brain" / "skill.md"
    content = skill_path.read_text(encoding='utf-8')

    # Add to trigger phrases (line ~28)
    trigger_pattern = r'(\*\*Trigger phrases\*\*:.*?)"'
    replacement = r'\1, "add ' + keyword + r'", "search ' + keyword + r's"'
    content = re.sub(trigger_pattern, replacement, content, count=1)

    # Add to module overview (after operations module, line ~68)
    module_section = f"""├── knowledge/    → Bookmarks, research, learning, {module_name}"""
    content = content.replace(
        "├── knowledge/    → Bookmarks, research, learning",
        module_section
    )

    skill_path.write_text(content, encoding='utf-8')
    return True


def update_agent_md(module_name, keyword):
    """Update CLAUDE.md with new module references"""
    agent_path = ROOT / "CLAUDE.md"
    content = agent_path.read_text(encoding='utf-8')

    # Add to Quick Reference table (around line ~30)
    new_row = f'| "Add {keyword}" | Append to `{module_name}/{module_name}.jsonl` |\n'

    # Find the table and add before the automation scripts section
    table_pattern = r'(\| "Track a goal" \| Update `goals/goals\.yaml` with progress \|)'
    content = re.sub(table_pattern, r'\1\n' + new_row.rstrip(), content, count=1)

    agent_path.write_text(content, encoding='utf-8')
    return True


def update_readme_md(module_name, keyword):
    """Update README.md with new module references"""
    readme_path = ROOT / "README.md"
    content = readme_path.read_text(encoding='utf-8')

    # Update structure diagram (around line ~31)
    papers_line = "├── papers/           # Academic paper reading"
    new_structure = f"""├── papers/           # Academic paper reading
│   └── paper-*.md    # Reading notes
├── knowledge/{module_name}/    # {module_name.capitalize()} management
│   └── {module_name.upper()}.md        # Module documentation"""

    content = content.replace(papers_line + "\n│   └── paper-*.md    # Reading notes", new_structure)

    readme_path.write_text(content, encoding='utf-8')
    return True


def update_knowledge_md(module_name, keyword):
    """Update knowledge/KNOWLEDGE.md with new module reference"""
    knowledge_path = ROOT / "knowledge" / "KNOWLEDGE.md"
    content = knowledge_path.read_text(encoding='utf-8')

    # Add to Extending section (around line ~48)
    extension_text = f"""- **{module_name}/**: {module_name.capitalize()} management and tracking
"""

    # Find the examples section and add before it
    examples_pattern = r'(Examples of modules you could add:)'
    content = re.sub(examples_pattern, extension_text + r'\1', content, count=1)

    knowledge_path.write_text(content, encoding='utf-8')
    return True


def update_claude_skill_md(module_name, keyword):
    """Update .claude/skills/digital-brain/skill.md"""
    skill_path = ROOT / ".claude" / "skills" / "digital-brain" / "skill.md"
    content = skill_path.read_text(encoding='utf-8')

    # Add to capabilities list (line ~10)
    knowledge_line = "3. **Knowledge** - Bookmarks, research, and learning materials"
    new_line = f"3. **Knowledge** - Bookmarks, research, learning materials, and {module_name}"
    content = content.replace(knowledge_line, new_line)

    # Add to commands list (around line ~24)
    commands_addition = f"- Add and manage {keyword}s\n"
    pattern = r'(- Add and read academic papers with narrative-driven approach)'
    content = re.sub(pattern, r'\1\n' + commands_addition.rstrip(), content, count=1)

    skill_path.write_text(content, encoding='utf-8')
    return True


def create_module(module_name, keyword, top_level=False):
    """Main function to create module and update system files"""

    print(f"🚀 Creating module: {module_name}")
    print(f"   Keyword: {keyword}")
    print(f"   Location: {'Top-level' if top_level else 'knowledge/'}")
    print()

    # Validate inputs
    if not re.match(r'^[a-z][a-z0-9-]*$', module_name):
        print("❌ Error: Module name must be lowercase, start with letter, use hyphens for spaces")
        return False

    if not re.match(r'^[a-z][a-z0-9-]*$', keyword):
        print("❌ Error: Keyword must be lowercase, start with letter")
        return False

    # Step 1: Create module directory
    print("📁 Creating module directory...")
    module_dir = create_module_directory(module_name, top_level)
    print(f"   ✅ Created {module_dir}")

    # Step 2: Generate MODULE.md
    print("\n📝 Generating module documentation...")
    module_doc = generate_module_doc(module_name, keyword, top_level)
    module_doc_path = module_dir / f"{module_name.upper()}.md"
    module_doc_path.write_text(module_doc, encoding='utf-8')
    print(f"   ✅ Created {module_doc_path}")

    # Step 3: Update 6 system files
    print("\n🔗 Integrating into system...")

    files_to_update = [
        (".claude/skills/digital-brain/skill.md", lambda m, k: update_skill_md(m, k)),
        ("CLAUDE.md", lambda m, k: update_agent_md(m, k)),
        ("README.md", lambda m, k: update_readme_md(m, k)),
        ("knowledge/KNOWLEDGE.md", lambda m, k: update_knowledge_md(m, k)),
    ]

    for file_name, update_func in files_to_update:
        try:
            update_func(module_name, keyword)
            print(f"   ✅ Updated {file_name}")
        except Exception as e:
            print(f"   ⚠️  Warning: Could not update {file_name}: {e}")

    # Step 4: Success message
    module_path = module_name if top_level else f"knowledge/{module_name}"
    print("\n" + "="*60)
    print("✅ Module created successfully!")
    print("="*60)
    print()
    print("📋 Next steps:")
    print(f"   1. Edit {module_doc_path} to define your data schema")
    print(f"   2. Create {module_name}.jsonl if needed:")
    print(f"      touch {module_path}/{module_name}.jsonl")
    print(f"   3. Verify integration:")
    print(f"      python module-toolkit/check_module_integration.py {module_name} {keyword}")
    print()
    print("📚 For more details, see:")
    print("   - module-toolkit/MODULE_CREATION_GUIDE.md")
    print()

    return True


def main():
    if len(sys.argv) < 3:
        print("Usage: python module-toolkit/create_module.py <module_name> <keyword> [--top-level]")
        print()
        print("Examples:")
        print("  python module-toolkit/create_module.py tasks task")
        print("  # Creates: knowledge/tasks/TASKS.md")
        print()
        print("  python module-toolkit/create_module.py projects project --top-level")
        print("  # Creates: projects/PROJECTS.md")
        print()
        print("Options:")
        print("  --top-level    Create module in top-level directory (default: knowledge/)")
        print()
        print("This will:")
        print("  - Create module directory with MODULE.md")
        print("  - Update 6 system integration files")
        print()
        sys.exit(1)

    module_name = sys.argv[1].lower()
    keyword = sys.argv[2].lower()
    top_level = "--top-level" in sys.argv

    success = create_module(module_name, keyword, top_level)
    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()
