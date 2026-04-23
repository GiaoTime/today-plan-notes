#!/usr/bin/env python3
import argparse
import html
import json
import subprocess
from pathlib import Path


def html_escape(value: str) -> str:
    return html.escape(value, quote=True)


def task_heading_html(task_name: str) -> str:
    return (
        "<div>"
        f"<b><span style=\"font-size: 22px\">{html_escape(task_name)}</span></b>"
        "<b><span style=\"font-size: 22px\"><br></span></b>"
        "</div>"
    )


def monospace_line(label: str, value: str) -> str:
    return (
        "<div>"
        f"<font face=\"Menlo-Regular\"><tt>{html_escape(label)}{html_escape(value)}</tt></font>"
        "<font face=\".AppleSystemUIFont\"><span style=\"font-size: 13px\"><tt><br></tt></span></font>"
        "</div>"
    )


def bullet_list(lines: list[tuple[str, str]]) -> str:
    items = []
    for label, value in lines:
        items.append(
            "<li>"
            f"{html_escape(label)}{html_escape(value)}"
            "</li>"
        )
    return "<ul>" + "".join(items) + "</ul>"


def date_line(date_text: str) -> str:
    return f"<blockquote>{html_escape(date_text)}</blockquote>"


def details_block(task: dict) -> str:
    parts = [
        bullet_list(
            [
                ("预计耗时：", task["eta"]),
                ("建议时间段：", task["time"]),
                ("工作流程：", task["workflow"]),
            ]
        )
    ]
    codex_direct = task.get("codex_direct")
    if codex_direct:
        parts.append(monospace_line("Codex可直接执行：", codex_direct))
    return "\n".join(parts)


def build_note_html(title: str, tasks: list[dict], priority: str, date_text: str) -> str:
    sections = [
        f"<div><b><span style=\"font-size: 24px\">{html_escape(title)}</span></b><b><span style=\"font-size: 24px\"><br></span></b></div>",
        date_line(date_text),
        "<div><br></div>",
    ]

    for index, task in enumerate(tasks, start=1):
        task_label = f"{index:02d} {task['task']}"
        sections.append(task_heading_html(task_label))
        sections.append(details_block(task))
        sections.append("<div><br></div>")

    sections.append(monospace_line("今日优先级建议：", priority))
    return "\n".join(sections)


def upsert_note(note_title: str, note_html: str, folder: str, account: str) -> None:
    escaped_title = note_title.replace('"', '\\"')
    escaped_folder = folder.replace('"', '\\"')
    escaped_account = account.replace('"', '\\"')
    escaped_body = note_html.replace("\\", "\\\\").replace('"', '\\"')

    applescript = f'''
tell application "Notes"
  tell account "{escaped_account}"
    tell folder "{escaped_folder}"
      set targetNotes to every note whose name is "{escaped_title}"
      if (count of targetNotes) > 0 then
        set targetNote to first item of targetNotes
        set body of targetNote to "{escaped_body}"
      else
        make new note with properties {{name:"{escaped_title}", body:"{escaped_body}"}}
      end if
    end tell
  end tell
end tell
'''
    subprocess.run(["osascript", "-e", applescript], check=True)


def main() -> None:
    parser = argparse.ArgumentParser(description="Render a structured today-plan note into Apple Notes.")
    parser.add_argument("--input", required=True, help="Path to JSON input payload.")
    parser.add_argument("--note-title", default="今日待办事项", help="Target note title.")
    parser.add_argument("--folder", default="Notes", help="Apple Notes folder name.")
    parser.add_argument("--account", default="iCloud", help="Apple Notes account name.")
    args = parser.parse_args()

    payload = json.loads(Path(args.input).read_text(encoding="utf-8"))
    title = payload.get("title", "今日待办事项")
    date_text = payload.get("date", "2026-04-23")
    tasks = payload["tasks"]
    priority = payload["priority"]

    note_html = build_note_html(title, tasks, priority, date_text)
    upsert_note(args.note_title, note_html, args.folder, args.account)


if __name__ == "__main__":
    main()
