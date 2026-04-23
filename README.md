# today-plan-notes

把粗略的当天待办整理成适合 macOS `备忘录` 使用的中文日计划。

这个 skill 适合把一句话级别的任务主题，扩展成可直接执行的计划内容，包括：

- 两位序号任务标题，如 `01`、`02`、`03`
- `预计耗时`
- `建议时间段`
- `工作流程`
- `Codex可直接执行`
- `今日优先级建议`

## 适用场景

当用户提到这些需求时，可以触发这个 skill：

- `今日事项`
- `今日待办`
- `今日工作`
- `待办事项`
- `今日待办事项`
- `工作安排`
- `今日安排`
- `备忘录待办`
- `Today's tasks`
- `today's to-do list`
- `today's work`
- `to-do items`
- `today's to-do items`
- `work schedule`
- `today's schedule`
- `memo to-do`

## 输出结构

默认输出为适配 `备忘录` 的结构：

1. 顶部标题
2. 日期行
3. 每个任务带两位序号
4. 每个任务下方包含 4 个板块

示例：

```text
今日待办事项
2026-04-23

01 完成详情页文案 skill 上传到 git 仓库
- 预计耗时：1.5-2 小时
- 建议时间段：09:30-11:30
- 工作流程：梳理详情页文案最终版本；检查 skill 结构、说明文档、示例是否完整；本地自测可用性；上传到 git 仓库；上传后复查仓库内容是否缺文件。
Codex可直接执行：整理文案结构；补全说明文档；检查目录是否缺文件；生成标准 README；做上传前自查。
```

## 目录说明

- [`SKILL.md`](./SKILL.md)
  正式 skill 定义与规则说明。
- [`evals/evals.json`](./evals/evals.json)
  基础测试样例。
- [`scripts/render_today_plan_note.py`](./scripts/render_today_plan_note.py)
  将结构化任务数据写入 Apple Notes 的脚本。
- [`scripts/sample_today_plan.json`](./scripts/sample_today_plan.json)
  样例输入数据。
- [`scripts/today_events_plan.json`](./scripts/today_events_plan.json)
  当前扩展版样例输入数据。

## 使用方式

1. 提供当天的粗略待办主题。
2. 让 Codex 按规则补全计划内容。
3. 使用脚本把结果写入 `备忘录`。

脚本示例：

```bash
python3 scripts/render_today_plan_note.py \
  --input scripts/sample_today_plan.json \
  --note-title "今日待办事项"
```

## 设计原则

- 中文优先
- 结构清晰
- 高效优先，不为原生格式做慢速手工操作
- 优先保证稳定可复用，而不是一次性的精修排版
