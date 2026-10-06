"""队列与排产核心。"""


class Counter:
    """记录本轮检查过的作业条数。"""

    def __init__(self):
        self.scanned = 0


def new_queue():
    return {"jobs": [], "next_seq": 0, "seen": [], "cache": None}


def add(queue, job, req_id):
    if req_id in queue["seen"]:
        return queue["jobs"][queue["seen"].index(req_id)]
    entry = dict(job)
    entry["seq"] = queue["next_seq"]
    queue["next_seq"] += 1
    queue["jobs"].append(entry)
    queue["seen"].append(req_id)
    return entry


def build_plan(queue, counter):
    jobs = queue["jobs"]
    cache = queue.get("cache")
    done = cache["done"] if cache else 0
    if done < len(jobs):
        counter.scanned += len(jobs) - done
    ordered = sorted(jobs, key=lambda job: (-job["priority"], job["seq"]))
    plan = []
    blocked = []
    clock = 0
    for job in ordered:
        if not job["ready"]:
            blocked.append(job["job_id"])
            continue
        plan.append({
            "slot": len(plan) + 1,
            "job_id": job["job_id"],
            "recipe": job["recipe"],
            "start": clock,
            "end": clock + job["minutes"],
        })
        clock += job["minutes"]
    queue["cache"] = {"done": len(jobs)}
    return {"plan": plan, "order": [slot["job_id"] for slot in plan], "blocked": blocked,
            "slots": len(plan), "scanned": counter.scanned}
