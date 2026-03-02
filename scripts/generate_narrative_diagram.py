#!/usr/bin/env python3
"""
Generate narrative structure diagram for a paper.

Usage:
    python scripts/generate_narrative_diagram.py paper-20260302-001 \
        "问题: GenAI上下文管理碎片化、不可追溯" \
        "观察: 现有方法缺乏统一架构基础" \
        "假设: 文件系统抽象可提供统一、持久、可治理的上下文基础设施" \
        "方法: 提出file-system abstraction + context engineering pipeline" \
        "约束识别: token window、statelessness、non-determinism" \
        "架构设计: History/Memory/Scratchpad生命周期 + Constructor/Updater/Evaluator流水线" \
        "实现: AIGNE框架 + AFS模块" \
        "验证: 两个exemplars展示可行性和可扩展性" \
        "结论: 方法有效,将LLM-as-OS从比喻转为具体架构"
"""

import argparse
import subprocess
import sys
from pathlib import Path


def generate_dot_content(nodes):
    """Generate Graphviz DOT content from nodes."""
    if len(nodes) < 2:
        raise ValueError("Need at least 2 nodes")

    # Start of DOT file
    dot_lines = [
        "digraph narrative {",
        "    // Graph settings",
        "    rankdir=TB;",
        '    node [shape=box, style="rounded,filled", fontname="Arial", fontsize=11, margin=0.3];',
        "    edge [arrowsize=0.8, penwidth=2];",
        '    bgcolor="white";',
        "",
        "    // Nodes",
    ]

    # Generate node definitions
    node_ids = []
    for i, node_text in enumerate(nodes):
        node_id = chr(65 + i)  # A, B, C, ...
        node_ids.append(node_id)

        # Format text with proper escaping
        escaped_text = node_text.replace('"', '\\"').replace('\n', '\\n')

        # First node is red, last node is green, others are white
        if i == 0:
            color = "#ffcccc"
        elif i == len(nodes) - 1:
            color = "#ccffcc"
        else:
            color = "white"

        dot_lines.append(f'    {node_id} [label="{escaped_text}", fillcolor="{color}"];')

    # Generate edges
    dot_lines.append("")
    dot_lines.append("    // Edges")
    edge_chain = " -> ".join(node_ids)
    dot_lines.append(f"    {edge_chain};")

    # Close the graph
    dot_lines.append("}")

    return "\n".join(dot_lines)


def generate_diagram(paper_id, nodes, papers_dir="papers"):
    """Generate narrative diagram for a paper."""
    papers_path = Path(papers_dir)
    paper_path = papers_path / paper_id

    if not paper_path.exists():
        raise FileNotFoundError(f"Paper folder not found: {paper_path}")

    # Generate DOT content
    dot_content = generate_dot_content(nodes)

    # Write DOT file to temporary location
    dot_file = Path("/tmp") / f"{paper_id}_narrative.dot"
    with open(dot_file, "w", encoding="utf-8") as f:
        f.write(dot_content)

    # Generate PNG using Graphviz
    output_file = paper_path / "narrative_diagram.png"
    try:
        subprocess.run(
            ["dot", "-Tpng", str(dot_file), "-o", str(output_file)],
            check=True,
            capture_output=True,
            text=True
        )
        print(f"✓ Diagram generated: {output_file}")
        return True
    except subprocess.CalledProcessError as e:
        print(f"✗ Failed to generate diagram: {e.stderr}", file=sys.stderr)
        return False
    except FileNotFoundError:
        print("✗ Graphviz not found. Install with: brew install graphviz", file=sys.stderr)
        return False


def main():
    parser = argparse.ArgumentParser(
        description="Generate narrative structure diagram for a paper",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Example:
  python scripts/generate_narrative_diagram.py paper-20260302-001 \\
      "问题: GenAI上下文管理碎片化" \\
      "观察: 现有方法缺乏统一架构" \\
      "假设: 文件系统抽象可提供统一基础设施" \\
      "方法: 提出file-system abstraction" \\
      "验证: 两个exemplars展示可行性" \\
      "结论: 方法有效"
        """
    )
    parser.add_argument("paper_id", help="Paper ID (e.g., paper-20260302-001)")
    parser.add_argument("nodes", nargs="+", help="Node labels for the diagram")
    parser.add_argument("--papers-dir", default="papers", help="Papers directory (default: papers)")

    args = parser.parse_args()

    if len(args.nodes) < 2:
        parser.error("Need at least 2 nodes")

    success = generate_diagram(args.paper_id, args.nodes, args.papers_dir)
    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()
