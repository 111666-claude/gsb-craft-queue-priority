"""把计划渲染成对齐文本表。"""


def render(plan, queue):
    rows = [("slot", "job", "recipe", "start", "end")]
    for slot in plan["plan"]:
        rows.append((str(slot["slot"]), slot["job_id"], slot["recipe"],
                     str(slot["start"]), str(slot["end"])))
    widths = [max(len(row[i]) for row in rows) for i in range(5)]
    lines = []
    for row in rows:
        lines.append("  ".join(cell.ljust(widths[i]) for i, cell in enumerate(row)))
    if plan["blocked"]:
        lines.append("blocked: " + " ".join(plan["blocked"]))
    return "\n".join(lines)
