import os
import sys
import unittest

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from craftq import queueing, render


def job(job_id, priority=0, minutes=1, ready=True):
    return {"job_id": job_id, "recipe": "r", "priority": priority, "minutes": minutes, "ready": ready}


class CraftQueueTest(unittest.TestCase):
    def test_single_job_gets_first_slot(self):
        queue = queueing.new_queue()
        queueing.add(queue, job("a"), "r1")
        out = queueing.build_plan(queue, queueing.Counter())
        self.assertEqual(out["order"], ["a"])
        self.assertEqual(out["slots"], 1)

    def test_seq_numbers_increase(self):
        queue = queueing.new_queue()
        queueing.add(queue, job("a"), "r1")
        second = queueing.add(queue, job("b"), "r2")
        self.assertEqual(second["seq"], 1)

    def test_every_queue_entry_appears_in_output(self):
        queue = queueing.new_queue()
        queueing.add(queue, job("a"), "r1")
        queueing.add(queue, job("b"), "r2")
        out = queueing.build_plan(queue, queueing.Counter())
        self.assertEqual(len(out["order"]) + len(out["blocked"]), 2)

    def test_render_has_header_and_rows(self):
        queue = queueing.new_queue()
        queueing.add(queue, job("a", minutes=2), "r1")
        out = queueing.build_plan(queue, queueing.Counter())
        text = render.render(out, queue)
        self.assertIn("slot", text.splitlines()[0])
        self.assertIn("a", text)

    def test_empty_queue(self):
        out = queueing.build_plan(queueing.new_queue(), queueing.Counter())
        self.assertEqual(out["order"], [])
        self.assertEqual(out["slots"], 0)


if __name__ == "__main__":
    unittest.main()
