# cc-statusline

Claude Code status line showing model, context usage, and billing/rate limit info.

## Status line format

```
Claude Sonnet 4.6 | Ctx: 34% | 5h: 62% resets 14:30 | 7d: 41%
```

| Segment | Description |
|---|---|
| Model name | Current Claude model |
| `Ctx: N%` | Context window usage |
| `5h: N% resets HH:MM` | 5-hour session limit (Claude.ai subscribers) |
| `7d: N%` | 7-day rolling usage (Claude.ai subscribers) |

Rate limit segments only appear for Claude.ai subscribers. API key users see model + context only.

## Install

```bash
git clone git@github.com:alertform/cc-statusline.git ~/cc-statusline
cd ~/cc-statusline
bash install.sh
```

Restart Claude Code to apply.

## Files

- `statusline.py` — reads JSON from stdin, outputs formatted status string
- `statusline-command.sh` — shell wrapper invoked by Claude Code
- `install.sh` — updates `~/.claude/settings.json` to point to this repo
