#!/usr/bin/env python3
"""
检查新模块是否完全集成到Digital Brain系统中

Usage:
    python scripts/check_module_integration.py <module_name> [keyword]

Example:
    python scripts/check_module_integration.py papers paper
    python scripts/check_module_integration.py contacts contact
"""

import sys
from pathlib import Path
from collections import defaultdict

# Paths
ROOT = Path(__file__).parent.parent


def count_occurrences(filepath, keyword):
    """统计关键词在文件中出现的次数"""
    try:
        with open(ROOT / filepath, 'r', encoding='utf-8') as f:
            content = f.read().lower()
            return content.count(keyword.lower())
    except FileNotFoundError:
        return -1
    except Exception as e:
        print(f"⚠️  读取 {filepath} 时出错: {e}")
        return -1


def check_file_exists(filepath):
    """检查文件是否存在"""
    return (ROOT / filepath).exists()


def main():
    if len(sys.argv) < 2:
        print("Usage: python scripts/check_module_integration.py <module_name> [keyword]")
        print("\nExample:")
        print("  python scripts/check_module_integration.py papers paper")
        sys.exit(1)

    module_name = sys.argv[1]
    keyword = sys.argv[2] if len(sys.argv) > 2 else module_name

    print("╔═══════════════════════════════════════════════════════════╗")
    print(f"║  模块集成完整性检查: {module_name:^30}  ║")
    print("╚═══════════════════════════════════════════════════════════╝")
    print(f"\n搜索关键词: '{keyword}'")
    print("="*70)

    # 定义需要检查的文件和最低出现次数
    files_to_check = {
        "系统核心文档": {
            "SKILL.md": 5,
            "AGENT.md": 5,
            "ARCHITECTURE.md": 3,
            "EXAMPLES.md": 5,
            "README.md": 5,
        },
        "模块文档": {
            f"knowledge/KNOWLEDGE.md": 3,
        },
        "Claude Code Skill": {
            ".claude/skills/digital-brain/skill.md": 3,
            ".claude/skills/digital-brain/instructions.xml": 3,
        }
    }

    # 检查模块自身文件
    # 尝试单数和复数形式
    module_singular = module_name.rstrip('s')  # papers -> paper
    module_upper = module_name.upper()  # papers -> PAPERS

    # 优先检查大写命名(新规范),降级到README.md(旧规范)
    # 支持顶层模块(如papers/)和knowledge子模块(如knowledge/bookmarks/)
    main_doc_path = f"{module_name}/{module_upper}.md"
    data_file_path = f"{module_name}/{module_name}.jsonl"

    if not check_file_exists(main_doc_path):
        main_doc_path = f"knowledge/{module_name}/{module_upper}.md"
        data_file_path = f"knowledge/{module_name}/{module_name}.jsonl"
        if not check_file_exists(main_doc_path):
            main_doc_path = f"knowledge/{module_name}/README.md"

    module_files = {
        main_doc_path: "模块主文档",
        data_file_path: "数据文件",
    }

    # 检查脚本(支持单复数变化)
    for script_prefix in ['add', 'search', 'update']:
        for name_variant in [module_name, module_singular]:
            script_path = f"scripts/{script_prefix}_{name_variant}.py"
            if check_file_exists(script_path):
                module_files[script_path] = f"{script_prefix}脚本"
                break

    results = defaultdict(dict)
    all_passed = True

    # 检查系统文档中的引用
    print("\n📋 系统文档引用检查")
    print("-"*70)

    for category, files in files_to_check.items():
        print(f"\n{category}:")
        for filepath, min_count in files.items():
            count = count_occurrences(filepath, keyword)

            if count == -1:
                status = "❌"
                message = "文件不存在"
                all_passed = False
            elif count >= min_count:
                status = "✅"
                message = f"{count:2d} 次引用"
            else:
                status = "⚠️ "
                message = f"{count:2d} 次引用 (期望 >= {min_count})"
                all_passed = False

            print(f"  {status} {filepath:45s} {message}")
            results[category][filepath] = (count, min_count, count >= min_count)

    # 检查模块自身文件
    print(f"\n📦 模块文件存在性检查")
    print("-"*70)

    for filepath, description in module_files.items():
        exists = check_file_exists(filepath)
        status = "✅" if exists else "❌"
        print(f"  {status} {filepath:45s} {description}")
        if not exists:
            all_passed = False

    # 统计总结
    print("\n" + "="*70)
    print("📊 检查统计")
    print("-"*70)

    total_checks = 0
    passed_checks = 0

    for category, files in results.items():
        category_total = len(files)
        category_passed = sum(1 for _, _, passed in files.values() if passed)
        total_checks += category_total
        passed_checks += category_passed

        percentage = (category_passed / category_total * 100) if category_total > 0 else 0
        status = "✅" if category_passed == category_total else "⚠️"

        print(f"{status} {category:30s} {category_passed}/{category_total} ({percentage:.0f}%)")

    print("-"*70)
    total_percentage = (passed_checks / total_checks * 100) if total_checks > 0 else 0
    print(f"   {'总计':30s} {passed_checks}/{total_checks} ({total_percentage:.0f}%)")

    # 最终结果
    print("\n" + "="*70)
    if all_passed:
        print("✅ 所有检查通过! 模块已完全集成到系统中")
        print("\n🎉 恭喜!新模块创建完成并已完美集成!")
    else:
        print("❌ 部分检查未通过,请检查上述标记的项目")
        print("\n💡 建议:")
        print("   1. 查看 MODULE_CREATION_GUIDE.md 了解完整步骤")
        print("   2. 使用检查清单逐项完成")
        print("   3. 参考 knowledge/papers/ 作为完整示例")

    print("="*70)

    # 详细建议
    if not all_passed:
        print("\n📝 需要更新的文件:")
        for category, files in results.items():
            for filepath, (count, min_count, passed) in files.items():
                if not passed and count >= 0:
                    print(f"   • {filepath} (当前 {count} 次,需要至少 {min_count} 次)")

    sys.exit(0 if all_passed else 1)


if __name__ == "__main__":
    main()
