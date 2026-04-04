import json, sys, datetime

try:
    data = json.load(sys.stdin)
    model = data.get('model', {}).get('display_name', 'Unknown Model')

    # Context window usage
    ctx = data.get('context_window', {})
    used = ctx.get('used_percentage')
    remaining = ctx.get('remaining_percentage')
    if used is not None and remaining is not None:
        ctx_str = f"Ctx: {used:.0f}%"
    else:
        ctx_str = "Ctx: --"

    # Rate limit / billing usage
    rate = data.get('rate_limits', {})
    parts = [model, ctx_str]

    five_hour = rate.get('five_hour')
    if five_hour:
        pct = five_hour.get('used_percentage')
        resets_at = five_hour.get('resets_at')
        if pct is not None:
            reset_str = ""
            if resets_at:
                reset_dt = datetime.datetime.fromtimestamp(resets_at)
                reset_str = f" resets {reset_dt.strftime('%H:%M')}"
            parts.append(f"5h: {pct:.0f}%{reset_str}")

    seven_day = rate.get('seven_day')
    if seven_day:
        pct = seven_day.get('used_percentage')
        resets_at = seven_day.get('resets_at')
        if pct is not None:
            reset_str = ""
            if resets_at:
                reset_dt = datetime.datetime.fromtimestamp(resets_at)
                reset_str = f" resets {reset_dt.strftime('%m/%d %H:%M')}"
            parts.append(f"7d: {pct:.0f}%{reset_str}")

    print(" | ".join(parts), end='')
except Exception:
    print("Claude Code | Ctx: --", end='')
