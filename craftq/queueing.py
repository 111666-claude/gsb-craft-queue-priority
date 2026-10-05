"""队列与排产核心。"""


class Counter:
    """记录本轮检查过的作业条数。"""

    def __init__(self):
        self.scanned = 0


def new_queue():
    return {"jobs": [], "next_seq": 0, "seen": []}


def add(queue, job, req_id):
    entry = dict(job)
    entry["seq"] = queue["next_seq"]
    queue["next_seq"] += 1
    queue["jobs"].append(entry)
    queue["seen"].append(req_id)
    return entry


def build_plan(queue, counter):
    ordered = sorted(queue["jobs"], key=lambda job: job["job_id"])
    plan = []
    blocked = []
    clock = 0
    for job in ordered:
        counter.scanned += 1
        plan.append({
            "slot": len(plan) + 1,
            "job_id": job["job_id"],
            "recipe": job["recipe"],
            "start": clock,
            "end": clock + job["minutes"],
        })
        clock += job["minutes"]
    return {"plan": plan, "order": [slot["job_id"] for slot in plan], "blocked": blocked,
            "slots": len(plan), "scanned": counter.scanned}
