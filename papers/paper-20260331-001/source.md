# How Noah Keeps Generative UI and LLM Conversations in Sync

**Author**: Eric Xu (e/Mettā) @xleaps
**Date**: Mar 15, 2026
**Source**: https://x.com/xleaps/status/2032983609947131946

---

Noah's chat thread combines text and generative UI. We've developed a pattern for users to interact with on-screen UI components as part of the chat thread — and for the LLM to stay aware of every interaction.

## The Problem

A common pitfall in text + generative UI apps is that the UI and LLM conversation become two separate systems. The user clicks a button, selects an option, or changes a form — but the LLM has no idea it happened. This leads to disjointed experiences where the AI responds as if nothing changed.

> Claude cannot tell what UI state you are in within its generated UI widget.

## Why Existing Patterns Fall Short

**TUI approach (Claude Code):** The [AskUserQuestion](https://platform.claude.com/docs/en/agent-sdk/user-input#handle-clarifying-questions) tool inserts the user's answer directly into the conversation as a tool call result. It works well in a terminal, but the pattern doesn't translate to GUI — you can't lock the chat box every time the UI needs input. The chat box should always be available.

**Prompt injection approach (Pi, Claude):** Some apps use `sentPrompt(text)` to pass UI state back to the LLM when the user types something. This solves half the problem — the LLM receives the state — but it doesn't solve persistence. When you reload the thread, the UI has no way to reconstruct what the user previously selected.

## What We Did in Noah

We pack every UI state change as a structured segment and send it to the LLM as a complete user message. The segment is a tagged union:

```json
{ "state": "clicked|selected...", "message": "Review AI model" }
```

This does two things at once:

- **The LLM stays in sync.** It receives the state change as context and continues its agentic loop with full awareness of what the user did.
- **The UI stays in sync.** Noah's UI harness recognizes the state field in the conversation history. When you reload the session, it reconstructs the exact UI state the user left off with.

The conversation history becomes the single source of truth for both the LLM and the UI.

## Why It Matters

Most of the time when you change UI state in ChatGPT or Claude — the LLM is unaware of the change. That may be acceptable for many applications — but not for one where the AI is generating interactive UI that the user acts on, and where those actions should inform what the AI does next.

If you're building in this space, the core insight is simple: don't treat the UI and the conversation as separate channels. Make every user interaction part of the conversation itself.
