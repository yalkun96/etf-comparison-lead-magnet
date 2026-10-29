# AI Conversation Exports

This directory contains the AI work summary and sanitized transcripts derived from
the local Codex session history.

## Codex transcripts

Each `codex-*.md` file was extracted from the corresponding local Codex JSONL
session listed in its header. These are derived transcripts, not byte-for-byte
native `/export` files. They include visible user and assistant messages while
excluding internal analysis-channel messages, tool calls, and tool outputs.
Common secrets and email addresses were masked automatically.

The original JSONL files remain in the local Codex history directory and have
not been copied into this repository. Automatic masking is not guaranteed to
catch every secret: manually review each transcript before committing it.

## ChatGPT and Claude Code

This export operation covers Codex sessions only. It does not export the current
ChatGPT conversation or create a Claude Code transcript. Do not invent exports
or label summaries as original conversations. If another genuine source
conversation is required by the assignment, export it separately and review it
before adding it to Git.

## Security

Never commit API keys, credentials, `.env` contents, database passwords, personal
contact details, or unrelated conversations. Review the generated files and
`git diff` before staging them.
