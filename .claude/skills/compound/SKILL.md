---
name: compound
description: Capture business rules and tacit knowledge from the current session
---

Before anything else, read `.claude/KNOWLEDGE.md`. It defines what project knowledge is, the four types it can take, and where each type lives. Apply it when proposing where to write.

Review the diff (`git diff main...HEAD`) and the conversation history.

Extract **business rules and tacit knowledge** that influenced the code — the why behind decisions that code alone doesn't capture.

Before proposing changes to project knowledge, ask me everything you need to understand the _why_ behind the decisions. Don't assume — ask.

Only capture what isn't already in project knowledge. When the diff or conversation exposes stale or incorrect project knowledge, propose fixes alongside the additions. Show me the proposed changes and wait for approval before writing.
