# Improving Skill-Creator: Test, Measure, and Refine Agent Skills

Source: https://claude.com/blog/improving-skill-creator-test-measure-and-refine-agent-skills

## Overview

Anthropic has announced enhancements to skill-creator that enable authors to verify skills work properly, catch performance regressions, and improve skill descriptions without requiring coding expertise. These updates are available in Claude.ai, Cowork, and as a plugin for Claude Code.

## Key Problem Addressed

The company observed that most skill authors are subject matter experts rather than engineers. They understand their workflows but lack tools to determine whether skills still function with new models, trigger appropriately, or actually improve after modifications.

## Two Types of Skills

**Capability uplift skills** help Claude perform tasks the base model cannot do consistently or at all—like document creation skills that encode specific techniques and patterns.

**Encoded preference skills** document workflows where Claude can already handle individual components but the skill sequences them according to team processes—such as NDA review workflows or weekly update generation.

## New Testing Features

### Evaluation Framework
Skill-creator now enables authors to write evals—tests checking whether Claude produces expected outputs for given prompts. The PDF skill example illustrates how evals identified failures with non-fillable forms, leading to fixes using improved text coordinate anchoring.

### Benchmark Mode
A standardized assessment tool tracks eval pass rates, elapsed time, and token usage, helping authors identify when model improvements render skills unnecessary or when quality regressions occur.

### Multi-Agent Support
Independent agents run evals in parallel with clean contexts, eliminating cross-contamination between test runs and providing faster results with separate token and timing metrics.

### A/B Comparison
Comparator agents conduct blind evaluations between two skill versions or skill versus baseline, determining whether changes genuinely improve performance.

## Skill Description Optimization

Skill-creator analyzes current descriptions against sample prompts and suggests refinements to reduce false positives and negatives. Testing across six document-creation skills showed improved triggering on five of them.

## Future Direction

As models advance, the distinction between "skill" and "specification" may blur. Currently, SKILL.md files function as implementation plans providing detailed instructions. Eventually, natural-language descriptions of desired outcomes may suffice, with models determining execution independently.
