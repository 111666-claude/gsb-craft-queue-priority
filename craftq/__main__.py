"""命令行入口。"""

import argparse
import json

from . import queueing, render


def _load(path):
    with open(path, encoding="utf-8") as fh:
        return json.load(fh)


def _save(path, obj):
    with open(path, "w", encoding="utf-8") as fh:
        json.dump(obj, fh, ensure_ascii=False, indent=1)


def main(argv=None):
    ap = argparse.ArgumentParser(prog="craftq")
    ap.add_argument("--sample", choices=["priority", "tie", "blocked", "replay", "work"])
    sub = ap.add_subparsers(dest="cmd")

    add_parser = sub.add_parser("add")
    add_parser.add_argument("--state", required=True)
    add_parser.add_argument("--req-id", required=True)
    add_parser.add_argument("--job-id", required=True)
    add_parser.add_argument("--recipe", default="")
    add_parser.add_argument("--priority", type=int, default=0)
    add_parser.add_argument("--minutes", type=int, default=1)
    add_parser.add_argument("--ready", action="store_true")

    plan_parser = sub.add_parser("plan")
    plan_parser.add_argument("--state", required=True)
    plan_parser.add_argument("--req-id", required=True)

    args = ap.parse_args(argv)
    if args.sample:
        from . import samples
        return samples.run(args.sample)
    if args.cmd is None:
        ap.print_help()
        return 2

    if args.cmd == "add":
        queue = _load(args.state)
        out = queueing.add(queue, {"job_id": args.job_id, "recipe": args.recipe,
                                   "priority": args.priority, "minutes": args.minutes,
                                   "ready": args.ready}, args.req_id)
        _save(args.state, queue)
        print(json.dumps({"job_id": out["job_id"], "seq": out["seq"]}, ensure_ascii=False))
        return 0

    queue = _load(args.state)
    counter = queueing.Counter()
    out = queueing.build_plan(queue, counter)
    out["req_id"] = args.req_id
    out["status"] = "ok"
    print(json.dumps(out, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
