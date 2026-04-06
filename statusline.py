import json, sys, datetime, subprocess, os, io

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

def get_git_branch():
    try:
        result = subprocess.run(
            ['git', 'branch', '--show-current'],
            capture_output=True, text=True, timeout=2,
            cwd=os.getcwd()
        )
        branch = result.stdout.strip()
        return f"⎇ {branch}" if branch else None
    except Exception:
        return None

def get_battery():
    try:
        import platform
        system = platform.system()
        if system == 'Windows':
            result = subprocess.run(
                ['WMIC', 'Path', 'Win32_Battery', 'Get', 'EstimatedChargeRemaining,BatteryStatus', '/Format:List'],
                capture_output=True, text=True, timeout=2
            )
            lines = {l.split('=')[0].strip(): l.split('=')[1].strip()
                     for l in result.stdout.strip().splitlines() if '=' in l}
            pct = int(lines.get('EstimatedChargeRemaining', ''))
            # BatteryStatus: 1=discharging, 2=AC
            charging = lines.get('BatteryStatus', '') != '1'
        elif system == 'Darwin':
            result = subprocess.run(
                ['pmset', '-g', 'batt'],
                capture_output=True, text=True, timeout=2
            )
            import re
            m = re.search(r'(\d+)%;\s*(\w+)', result.stdout)
            if not m:
                return None
            pct = int(m.group(1))
            charging = m.group(2) != 'discharging'
        else:
            return None
        icon = '⚡' if charging else '🔋'
        return f"{icon}{pct}%"
    except Exception:
        return None

def get_cwd_short():
    cwd = os.getcwd()
    home = os.path.expanduser('~')
    if cwd.startswith(home):
        cwd = '~' + cwd[len(home):]
    parts = cwd.split('/')
    if len(parts) > 3:
        cwd = '/'.join(['…'] + parts[-2:])
    return cwd

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

    line2 = []
    # Cost
    cost = data.get('cost', {})
    total_cost = cost.get('total_cost_usd')
    if total_cost is not None:
        parts.append(f"${total_cost:.2f}")

    # Code changes
    added = cost.get('total_lines_added')
    removed = cost.get('total_lines_removed')
    if added is not None and removed is not None:
        parts.append(f"+{added}/-{removed}")

    # Total tokens
    ctx = data.get('context_window', {})
    in_tok = ctx.get('total_input_tokens', 0)
    out_tok = ctx.get('total_output_tokens', 0)
    total_tok = in_tok + out_tok
    if total_tok > 0:
        parts.append(f"{total_tok/1000:.0f}k tokens")

    line2 = []
    branch = get_git_branch()
    if branch:
        line2.append(branch)
    line2.append(get_cwd_short())
    line2.append(datetime.datetime.now().strftime('%H:%M'))
    battery = get_battery()
    if battery:
        line2.append(battery)

    print(" | ".join(parts) + "\n" + " | ".join(line2), end='')
except Exception:
    print("Claude Code | Ctx: --", end='')
