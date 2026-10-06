"""队列与排产核心。"""

from bisect import insort


class Counter:
    """记录本轮检查过的作业条数。"""

    def __init__(self):
        self.scanned = 0


def new_queue():
    return {"jobs": [], "next_seq": 0, "seen": {},
            "ready": [], "blocked": [], "upto": 0}


def add(queue, job, req_id):
    if req_id in queue["seen"]:
        return queue["jobs"][queue["seen"][req_id]]
    entry = dict(job)
    entry["seq"] = queue["next_seq"]
    queue["next_seq"] += 1
    queue["jobs"].append(entry)
    queue["seen"][req_id] = entry["seq"]
    return entry


def _sort_key(job):
    return (-job["priority"], job["seq"])


def build_plan(queue, counter):
    jobs = queue["jobs"]
    for entry in jobs[queue["upto"]:]:
        counter.scanned += 1
        if entry["ready"]:
            insort(queue["ready"], entry, key=_sort_key)
        else:
            queue["blocked"].append(entry["job_id"])
    queue["upto"] = len(jobs)
    plan = []
    clock = 0
    for job in queue["ready"]:
        plan.append({
            "slot": len(plan) + 1,
            "job_id": job["job_id"],
            "recipe": job["recipe"],
            "start": clock,
            "end": clock + job["minutes"],
        })
        clock += job["minutes"]
    return {"plan": plan, "order": [slot["job_id"] for slot in plan],
            "blocked": list(queue["blocked"]),
            "slots": len(plan), "scanned": counter.scanned}
