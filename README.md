# cc-statusline

A two-line status bar for [Claude Code](https://claude.ai/code) showing model, context usage, cost, git branch, and more.

## Preview

```
Claude Sonnet 4.6 | Ctx: 34% | 5h: 62% resets 14:30 | 7d: 41%
$0.42 | +120/-35 | 18k tok | ⎇ main | ~/my-project | 09:15 | 🔋87%
```

**Line 1** — session limits and context:

| Segment | Description |
|---|---|
| Model name | Current Claude model |
| `Ctx: N%` | Context window usage |
| `5h: N% resets HH:MM` | 5-hour rolling limit (Claude.ai subscribers) |
| `7d: N%` | 7-day rolling usage (Claude.ai subscribers) |

Rate limit segments only appear for Claude.ai subscribers. API key users see model + context only.

**Line 2** — session stats and environment:

| Segment | Description |
|---|---|
| `$N.NN` | Session cost in USD |
| `+N/-N` | Lines added / removed this session |
| `Nk tok` | Total tokens used (input + output) |
| `⎇ branch` | Current git branch |
| `~/path` | Shortened working directory |
| `HH:MM` | Local time |
| `⚡N%` / `🔋N%` | Battery level (charging / discharging) |

## Install

```bash
git clone git@github.com:alertform/cc-statusline.git ~/cc-statusline
cd ~/cc-statusline
bash install.sh
```

Restart Claude Code to apply.

## Requirements

- Python 3 (or Python 2 as fallback)
- Claude Code with `statusLine` support

## Files

| File | Description |
|---|---|
| `statusline.py` | Reads JSON from stdin, outputs formatted status string |
| `statusline-command.sh` | Shell wrapper invoked by Claude Code on each update |
| `install.sh` | Writes the `statusLine` config into `~/.claude/settings.json` |

## Platform support

| Feature | macOS | Windows | Linux |
|---|---|---|---|
| Model / context / rate limits | ✅ | ✅ | ✅ |
| Cost / tokens / code changes | ✅ | ✅ | ✅ |
| Git branch | ✅ | ✅ | ✅ |
| Battery | ✅ | ✅ | — |

## Manual config

If `install.sh` doesn't work, add this to `~/.claude/settings.json`:

```json
{
  "statusLine": {
    "type": "command",
    "command": "bash ~/cc-statusline/statusline-command.sh"
  }
}
```
