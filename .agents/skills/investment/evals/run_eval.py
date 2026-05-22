#!/usr/bin/env python3
"""
Investment skill 评测脚本。

用法:
    python .claude/skills/investment/evals/run_eval.py [--runs N] [--eval-id ID]

默认跑 3 次，输出每条 assertion 的通过率。
需要 `claude` CLI 可用。
"""

import argparse
import glob as globmod
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
    # 复制最新 skill 目录到 worktree（包含 SKILL.md、evals/fixtures 等）
    skill_src = REPO_ROOT / ".claude" / "skills" / "investment"
    skill_dst = Path(worktree_path) / ".claude" / "skills" / "investment"
    if skill_dst.exists():
        shutil.rmtree(skill_dst)
    shutil.copytree(skill_src, skill_dst)
    # 复制 CLAUDE.md 到 worktree（提供路由上下文）
    claude_md = REPO_ROOT / "CLAUDE.md"
    if claude_md.exists():
        shutil.copy2(claude_md, Path(worktree_path) / "CLAUDE.md")
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
    """用 claude -p 在 worktree 中执行 prompt，返回是否成功。"""
    full_prompt = (
        f"这是离线环境，禁止访问网络（无浏览器、无 curl、无 API 调用）。"
        f"所有需要的输入数据已在本地文件中提供。"
        f"请高效完成，不要做多余的探索。\n\n{prompt}"
    )
    result = subprocess.run(
        [
            "claude", "-p", full_prompt,
            "--allowedTools", "Read,Edit,Write,Bash,Glob,Grep",
            "--effort", "low",
            "--output-format", "json",
        ],
        cwd=worktree_path,
        capture_output=True,
        text=True,
        timeout=600,
    )
    return result.returncode == 0, result.stdout


def _glob_matches(worktree_path: str, pattern: str) -> list[str]:
    """返回 worktree 下匹配 glob pattern 的文件列表。"""
    return globmod.glob(os.path.join(worktree_path, pattern), recursive=True)


def check_assertion(worktree_path: str, check: dict) -> tuple[bool, str]:
    """验证单条断言，返回 (passed, evidence)。"""
    check_type = check["type"]

    # glob 类型断言
    if check_type == "glob_exists":
        matches = _glob_matches(worktree_path, check["pattern"])
        passed = len(matches) > 0
        evidence = f"{'Matched' if passed else 'No match'}: {check['pattern']}"
        if passed:
            evidence += f" -> {[os.path.relpath(m, worktree_path) for m in matches]}"
        return passed, evidence

    if check_type == "glob_not_exists":
        matches = _glob_matches(worktree_path, check["pattern"])
        passed = len(matches) == 0
        evidence = f"{'Correctly no match' if passed else 'Unexpected match'}: {check['pattern']}"
        if not passed:
            evidence += f" -> {[os.path.relpath(m, worktree_path) for m in matches]}"
        return passed, evidence

    if check_type == "glob_file_contains":
        matches = _glob_matches(worktree_path, check["pattern"])
        if not matches:
            return False, f"No files matched: {check['pattern']}"
        for m in matches:
            with open(m, "r", errors="ignore") as f:
                if check["contains"] in f.read():
                    return True, f"Found '{check['contains']}' in {os.path.relpath(m, worktree_path)}"
        return False, f"'{check['contains']}' not found in any of {[os.path.relpath(m, worktree_path) for m in matches]}"

    if check_type == "glob_file_not_contains":
        matches = _glob_matches(worktree_path, check["pattern"])
        if not matches:
            return True, f"No files matched pattern: {check['pattern']} (vacuously true)"
        for m in matches:
            with open(m, "r", errors="ignore") as f:
                if check["contains"] in f.read():
                    return False, f"Unexpectedly found '{check['contains']}' in {os.path.relpath(m, worktree_path)}"
        return True, f"'{check['contains']}' correctly absent from all {len(matches)} files matching {check['pattern']}"

    # file 类型断言
    filepath = os.path.join(worktree_path, check["file"])

    if check_type == "file_exists":
        passed = os.path.exists(filepath)
        return passed, f"{'Exists' if passed else 'Not found'}: {check['file']}"

    if check_type == "file_not_exists":
        passed = not os.path.exists(filepath)
        return passed, f"{'Correctly absent' if passed else 'Unexpectedly exists'}: {check['file']}"

    if not os.path.exists(filepath):
        return False, f"File not found: {check['file']}"

    with open(filepath, "r") as f:
        content = f.read()

    if check_type == "file_contains":
        passed = check["contains"] in content
        evidence = f"{'Found' if passed else 'Not found'}: '{check['contains']}'"
        return passed, evidence

    elif check_type == "line_order":
        lines = content.split("\n")
        first_line = next((i for i, l in enumerate(lines) if check["first"] in l), -1)
        second_line = next((i for i, l in enumerate(lines) if check["second"] in l), -1)
        if first_line == -1 or second_line == -1:
            return False, f"first at {first_line}, second at {second_line}"
        passed = first_line < second_line
        evidence = f"'{check['first']}' at line {first_line}, '{check['second']}' at line {second_line}"
        return passed, evidence

    elif check_type == "count_max":
        count = content.count(check["pattern"])
        passed = count <= check["max_count"]
        evidence = f"'{check['pattern']}' appears {count} times (max allowed: {check['max_count']})"
        return passed, evidence

    return False, "Unknown check type"


def run_single_eval(fixture: dict, prompt: str) -> dict:
    """执行单次评测，返回结果。"""
    worktree_path = create_worktree(fixture["base_commit"])

    try:
        success, claude_output = run_claude(prompt, worktree_path)
        if not success:
            return {
                "success": False,
                "error": "claude -p failed",
                "checks": {c["name"]: (False, "claude execution failed") for c in fixture["checks"]},
                "claude_output": claude_output,
            }

        results = {}
        for check in fixture["checks"]:
            passed, evidence = check_assertion(worktree_path, check)
            results[check["name"]] = (passed, evidence)
            if not passed:
                print(f"    FAIL {check['name']}: {evidence}", file=sys.stderr)

        return {"success": True, "checks": results, "claude_output": claude_output}
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
        fixture = eval_case.get("fixture")

        if not fixture:
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
                executor.submit(run_single_eval, fixture, prompt): i
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

        check_names = [c["name"] for c in fixture["checks"]]

        for name in check_names:
            passes = sum(
                1 for r in all_results if r["success"] and r["checks"].get(name, (False,))[0]
            )
            bar = "█" * passes + "░" * (args.runs - passes)
            status = "✓" if passes == args.runs else ("△" if passes > 0 else "✗")
            print(f"  {status} {name:<35} {bar} {passes}/{args.runs}")

        overall_pass = sum(
            1
            for r in all_results
            if r["success"] and all(v[0] for v in r["checks"].values())
        )
        print(f"\n  Overall full-pass: {overall_pass}/{args.runs}")


if __name__ == "__main__":
    main()
