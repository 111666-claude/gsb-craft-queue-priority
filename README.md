# craft-queue-priority

制造队列的排产与计划渲染：先把队列排成计划，再把计划渲染成可读的表。只用 Python 标准库。

```
python3 -m unittest discover -s tests
python3 -m craftq add  --state s.json --req-id r1 --job-id j1 --recipe sword --priority 5 --minutes 3 --ready
python3 -m craftq plan --state s.json --req-id r1
python3 -m craftq --sample=priority|tie|blocked|replay|work
```

作业字段：`job_id`、`recipe`、`priority`、`minutes`、`ready`（材料是否齐）、`seq`（入队顺序）。

## 口径

- **优先级**：按 `priority` 从大到小排；同一优先级按入队顺序（`seq` 小的先）。
- **材料门槛**：材料不齐（`ready` 为 false）的作业不排进计划，进 `blocked` 列表。
- **时间接续**：作业依次占用时间片，后一个的起点等于前一个的终点，单位为分钟。
- **幂等**：同一个 `req_id` 的入队只生效一次，重复请求不再追加作业。

## 不变量

- 计划里的作业数加上 `blocked` 里的作业数等于队列里的作业数。
- 计划内作业的下标与 `slot` 从 1 起严格递增。
- `scanned` 不随队列长度放大：两千次入队加显示计划，`scanned` 不超过 9000。

## 输出契约

`plan` 打印一行 JSON：`req_id`、`status`（`ok`）、`order`（作业 id 列表）、`blocked`（id 列表）、
`slots`、`scanned`，另含 `plan` 明细（每项的 `slot`、`job_id`、`recipe`、`start`、`end`）。
渲染出来的文本表列顺序为 `slot`、`job`、`recipe`、`start`、`end`，末尾可选一行 `blocked:`。

`--sample=work` 只打印 `{"jobs": N, "scanned": N}`。
