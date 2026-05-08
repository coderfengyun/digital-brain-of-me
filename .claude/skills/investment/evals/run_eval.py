#!/usr/bin/env python3
"""
Investment skill 评测脚本。

用法:
    python .claude/skills/investment/evals/run_eval.py [--runs N] [--eval-id ID]

默认跑 3 次，输出每条 assertion 的通过率。
需要 `claude` CLI 可用。
"""

import argparse
import json
import os
import subprocess
import sys
import tempfile
import shutil
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[4]  # .claude/skills/investment/evals -> repo root
SKILL_PATH = REPO_ROOT / ".claude" / "skills" / "investment" / "SKILL.md"
EVALS_PATH = REPO_ROOT / ".claude" / "skills" / "investment" / "evals" / "evals.json"

# 每个 eval 需要定义：哪个 commit 作为起始状态
EVAL_FIXTURES = {
    1: {
        "base_commit": "8e71757",  # 04-18 已添加但 04-26 还没有
        "checks": [
            {
                "name": "content_appended",
                "type": "file_contains",
                "file": "investment/卢麒元/微博VIP群发言.md",
                "contains": "## 2026-04-26",
            },
            {
                "name": "correct_order",
                "type": "line_order",
                "file": "investment/卢麒元/微博VIP群发言.md",
                "first": "2026-04-26",
                "second": "2026-04-18",
            },
            {
                "name": "index_updated",
                "type": "file_contains",
                "file": "investment/卢麒元/卢麒元.md",
                "contains": "04-26",
            },
            {
                "name": "has_strong_dollar_insight",
                "type": "file_contains",
                "file": "investment/卢麒元/卢麒元.md",
                "contains": "强美元",
            },
            {
                "name": "no_duplicate_collapse",
                "type": "count_max",
                "file": "investment/卢麒元/卢麒元.md",
                "pattern": "向心坍缩",
                "max_count": 3,  # 原有2条 + 最多1条新增（如果措辞够新）
            },
        ],
    }
}


def create_worktree(base_commit: str) -> str:
    """创建临时 worktree 并返回路径。"""
    tmpdir = tempfile.mkdtemp(prefix="investment-eval-")
    worktree_path = os.path.join(tmpdir, "worktree")
    subprocess.run(
        ["git", "worktree", "add", worktree_path, base_commit],
        cwd=REPO_ROOT,
        capture_output=True,
        check=True,
    )
    # 复制最新 SKILL.md 到 worktree
    dest = Path(worktree_path) / ".claude" / "skills" / "investment" / "SKILL.md"
    dest.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(SKILL_PATH, dest)
    return worktree_path


def cleanup_worktree(worktree_path: str):
    """清理 worktree。"""
    subprocess.run(
        ["git", "worktree", "remove", "--force", worktree_path],
        cwd=REPO_ROOT,
        capture_output=True,
    )
    parent = os.path.dirname(worktree_path)
    if os.path.exists(parent):
        shutil.rmtree(parent, ignore_errors=True)


def run_claude(prompt: str, worktree_path: str) -> bool:
    """用 claude -p --bare 在 worktree 中执行 prompt，返回是否成功。"""
    full_prompt = (
        f"你有一个 investment skill 在 .claude/skills/investment/SKILL.md，"
        f"请先读取它，然后按照其指令完成以下任务：\n\n{prompt}"
    )
    result = subprocess.run(
        [
            "claude", "-p", full_prompt,
            "--allowedTools", "Read,Edit,Write,Bash,Glob,Grep",
        ],
        cwd=worktree_path,
        capture_output=True,
        text=True,
        timeout=180,
    )
    return result.returncode == 0


def check_assertion(worktree_path: str, check: dict) -> tuple[bool, str]:
    """验证单条断言，返回 (passed, evidence)。"""
    filepath = os.path.join(worktree_path, check["file"])

    if not os.path.exists(filepath):
        return False, f"File not found: {check['file']}"

    with open(filepath, "r") as f:
        content = f.read()

    if check["type"] == "file_contains":
        passed = check["contains"] in content
        evidence = f"{'Found' if passed else 'Not found'}: '{check['contains']}'"
        return passed, evidence

    elif check["type"] == "line_order":
        lines = content.split("\n")
        first_line = next((i for i, l in enumerate(lines) if check["first"] in l), -1)
        second_line = next((i for i, l in enumerate(lines) if check["second"] in l), -1)
        if first_line == -1 or second_line == -1:
            return False, f"first at {first_line}, second at {second_line}"
        passed = first_line < second_line
        evidence = f"'{check['first']}' at line {first_line}, '{check['second']}' at line {second_line}"
        return passed, evidence

    elif check["type"] == "count_max":
        count = content.count(check["pattern"])
        passed = count <= check["max_count"]
        evidence = f"'{check['pattern']}' appears {count} times (max allowed: {check['max_count']})"
        return passed, evidence

    return False, "Unknown check type"


def run_single_eval(eval_id: int, prompt: str) -> dict:
    """执行单次评测，返回结果。"""
    fixture = EVAL_FIXTURES[eval_id]
    worktree_path = create_worktree(fixture["base_commit"])

    try:
        success = run_claude(prompt, worktree_path)
        if not success:
            return {
                "success": False,
                "error": "claude -p failed",
                "checks": {c["name"]: (False, "claude execution failed") for c in fixture["checks"]},
            }

        results = {}
        for check in fixture["checks"]:
            passed, evidence = check_assertion(worktree_path, check)
            results[check["name"]] = (passed, evidence)

        return {"success": True, "checks": results}
    finally:
        cleanup_worktree(worktree_path)


def main():
    parser = argparse.ArgumentParser(description="Run investment skill evals")
    parser.add_argument("--runs", type=int, default=3, help="每个 case 跑几次 (default: 3)")
    parser.add_argument("--eval-id", type=int, default=None, help="只跑指定 ID 的 eval")
    args = parser.parse_args()

    with open(EVALS_PATH) as f:
        evals_data = json.load(f)

    evals = evals_data["evals"]
    if args.eval_id is not None:
        evals = [e for e in evals if e["id"] == args.eval_id]

    if not evals:
        print("No matching evals found.")
        sys.exit(1)

    for eval_case in evals:
        eval_id = eval_case["id"]
        prompt = eval_case["prompt"]

        if eval_id not in EVAL_FIXTURES:
            print(f"⚠️  Eval {eval_id}: no fixture defined, skipping")
            continue

        print(f"\n{'='*60}")
        print(f"Eval {eval_id}: {eval_case.get('expected_output', '')[:60]}...")
        print(f"Running {args.runs} times (parallel)...")
        print(f"{'='*60}")

        t0 = time.time()
        all_results = [None] * args.runs

        with ThreadPoolExecutor(max_workers=args.runs) as executor:
            futures = {
                executor.submit(run_single_eval, eval_id, prompt): i
                for i in range(args.runs)
            }
            for future in as_completed(futures):
                run_idx = futures[future]
                result = future.result()
                all_results[run_idx] = result
                run_num = run_idx + 1
                if result["success"]:
                    passed = sum(1 for v in result["checks"].values() if v[0])
                    total = len(result["checks"])
                    print(f"  Run {run_num}/{args.runs} ✓ ({passed}/{total} checks passed)")
                else:
                    print(f"  Run {run_num}/{args.runs} ✗ ({result.get('error', 'unknown')})")

        elapsed = time.time() - t0

        # 汇总
        print(f"\n{'─'*60}")
        print(f"Results summary (total {elapsed:.0f}s):")
        print(f"{'─'*60}")

        check_names = [c["name"] for c in EVAL_FIXTURES[eval_id]["checks"]]

        for name in check_names:
            passes = sum(
                1 for r in all_results if r["success"] and r["checks"].get(name, (False,))[0]
            )
            rate = passes / args.runs
            bar = "█" * passes + "░" * (args.runs - passes)
            status = "✓" if rate == 1.0 else ("△" if rate > 0 else "✗")
            print(f"  {status} {name:<35} {bar} {passes}/{args.runs}")

        overall_pass = sum(
            1
            for r in all_results
            if r["success"] and all(v[0] for v in r["checks"].values())
        )
        print(f"\n  Overall full-pass: {overall_pass}/{args.runs}")


if __name__ == "__main__":
    main()
