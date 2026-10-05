"""固定场景，用来复现题面里的锚点。"""

import json

from . import queueing


def _line(obj):
    print(json.dumps(obj, ensure_ascii=False))


def _job(job_id, priority=0, minutes=1, ready=True, recipe="r"):
    return {"job_id": job_id, "recipe": recipe, "priority": priority,
            "minutes": minutes, "ready": ready}


def _plan(queue):
    out = queueing.build_plan(queue, queueing.Counter())
    return {"order": out["order"], "blocked": out["blocked"]}


def run(name):
    if name == "priority":
        queue = queueing.new_queue()
        queueing.add(queue, _job("a", priority=1), "p-1")
        queueing.add(queue, _job("b", priority=9), "p-2")
        _line(_plan(queue))
        return 0
    if name == "tie":
        queue = queueing.new_queue()
        queueing.add(queue, _job("b", priority=3), "t-1")
        queueing.add(queue, _job("a", priority=3), "t-2")
        _line(_plan(queue))
        return 0
    if name == "blocked":
        queue = queueing.new_queue()
        queueing.add(queue, _job("a", priority=5, ready=False), "b-1")
        queueing.add(queue, _job("b", priority=1), "b-2")
        _line(_plan(queue))
        return 0
    if name == "replay":
        queue = queueing.new_queue()
        queueing.add(queue, _job("a", priority=1), "rep-1")
        queueing.add(queue, _job("a", priority=1), "rep-1")
        _line({"jobs": len(queue["jobs"])})
        return 0
    if name == "work":
        queue = queueing.new_queue()
        counter = queueing.Counter()
        for i in range(2000):
            queueing.add(queue, _job("j%04d" % i, priority=i), "w-%d" % i)
            queueing.build_plan(queue, counter)
        _line({"jobs": 2000, "scanned": counter.scanned})
        return 0
    raise SystemExit("未知场景：" + name)
