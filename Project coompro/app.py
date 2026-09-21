import json
from datetime import date, datetime, time, timedelta
import re
from pathlib import Path
from uuid import uuid4

import streamlit as st

CATEGORIES = ["Personal", "Study", "Work", "Project"]
PRIORITIES = ["Low", "Medium", "High"]
REMINDER_OPTIONS = {
    "No reminder": 0,
    "5 minutes before": 5,
    "15 minutes before": 15,
    "30 minutes before": 30,
    "1 hour before": 60,
    "1 day before": 1440,
}

st.set_page_config(
    page_title="Focus Board",
    page_icon="✅",
    layout="wide",
    initial_sidebar_state="collapsed",
)

st.markdown(
    """
    <style>
    :root {
        --focus-accent: #e07a5f;
        --focus-success: #81b29a;
    }
    .main { background: var(--background-color); }
    [data-testid="stSidebar"], [data-testid="stSidebarCollapsedControl"] { display: none; }
    .hero { padding: 1.2rem 0 1rem; }
    .eyebrow { color: var(--focus-accent); font-weight: 700; letter-spacing: .12em; text-transform: uppercase; font-size: .78rem; }
    .hero h1, .hero p, .metric, .metric h2 { color: var(--text-color) !important; }
    .hero h1 { font-size: 3rem; margin: .2rem 0; }
    .hero p { font-size: 1.05rem; }
    .metric { background: var(--secondary-background-color); border: 1px solid var(--text-color); border-radius: 10px; padding: 1rem; }
    .metric h2 { margin: .35rem 0 0; }
    .task-card { background: var(--secondary-background-color); border-left: 5px solid var(--focus-accent); border-radius: 8px; padding: .85rem 1rem; margin-bottom: .65rem; box-shadow: 0 2px 8px rgba(32,38,37,.04); }
    .task-card.done { border-left-color: var(--focus-success); opacity: .7; }
    .task-title, .task-meta { color: var(--text-color) !important; }
    .task-title { font-size: 1.05rem; font-weight: 650; }
    .task-title.done { text-decoration: line-through; }
    .task-meta { font-size: .82rem; margin-top: .35rem; opacity: .8; }
    @media (max-width: 768px) {
        .hero h1 { font-size: 2.2rem; }
        .metric { padding: .7rem; }
        .metric h2 { font-size: 1.35rem; }
    }
    </style>
    """,
    unsafe_allow_html=True,
)


if "profile_name" not in st.session_state:
    st.markdown("# Focus Board")
    st.write("ใส่ชื่อของคุณเพื่อเปิดรายการงานส่วนตัว")
    with st.form("profile_form"):
        entered_name = st.text_input("Your name", placeholder="เช่น Alice")
        continue_button = st.form_submit_button("Continue", type="primary")
    if continue_button:
        clean_name = entered_name.strip()
        if not clean_name:
            st.error("กรุณาใส่ชื่อก่อนเข้าใช้งาน")
        else:
            st.session_state.profile_name = clean_name
            st.rerun()
    st.info("ข้อมูลจะแยกตามชื่อที่กรอกในเบราว์เซอร์นี้")
    st.stop()


profile_key = re.sub(r"[^a-zA-Z0-9_-]", "_", st.session_state.profile_name)[:40]
DATA_FILE = Path("user_data") / f"{profile_key}.json"
DATA_FILE.parent.mkdir(exist_ok=True)


def load_tasks():
    """Load tasks from JSON and return an empty list when no file exists."""
    try:
        if DATA_FILE.exists():
            with DATA_FILE.open("r", encoding="utf-8") as file:
                data = json.load(file)
                return data if isinstance(data, list) else []
    except (json.JSONDecodeError, OSError):
        st.warning("ไม่สามารถอ่านไฟล์ข้อมูลเดิมได้ จึงเริ่มรายการใหม่")
    return []


def save_tasks(tasks):
    """Save the current task list as readable JSON."""
    try:
        with DATA_FILE.open("w", encoding="utf-8") as file:
            json.dump(tasks, file, ensure_ascii=False, indent=2)
    except OSError as error:
        st.error(f"บันทึกข้อมูลไม่สำเร็จ: {error}")


def add_task(tasks, title, category, priority, due_date, due_time, reminder, notes):
    due_at = ""
    if due_date:
        due_at = datetime.combine(due_date, due_time or time(17, 0)).isoformat()
    tasks.append(
        {
            "id": str(uuid4()),
            "title": title.strip(),
            "category": category,
            "priority": priority,
            "due_at": due_at,
            "reminder_minutes": REMINDER_OPTIONS[reminder],
            "notes": notes.strip(),
            "completed": False,
        }
    )


def task_matches(task, search_text, category, status):
    searchable_text = f"{task['title']} {task.get('notes', '')}".lower()
    matches_search = search_text.lower() in searchable_text
    matches_category = category == "All" or task["category"] == category
    matches_status = (
        status == "All"
        or (status == "Active" and not task["completed"])
        or (status == "Completed" and task["completed"])
    )
    return matches_search and matches_category and matches_status


def sort_tasks(tasks):
    priority_order = {"High": 0, "Medium": 1, "Low": 2}
    return sorted(
        tasks,
        key=lambda task: (
            task["completed"],
            task.get("due_at", task.get("due_date", "")) or "9999-12-31T23:59:59",
            priority_order.get(task["priority"], 3),
        ),
    )


def format_due_date(value):
    if not value:
        return "No deadline"
    try:
        if "T" in value:
            due = datetime.fromisoformat(value)
            return f"Due {due.strftime('%d %b %Y at %H:%M')}"
        due = date.fromisoformat(value)
        return f"Due {due.strftime('%d %b %Y')}"
    except ValueError:
        return "Invalid deadline"


def get_task_due(task):
    """Read new date-time data and remain compatible with old date-only tasks."""
    return task.get("due_at") or task.get("due_date", "")


def ics_escape(value):
    return str(value).replace("\\", "\\\\").replace(";", "\\;").replace(",", "\\,").replace("\n", "\\n")


def create_calendar_event(task):
    """Create a calendar file with an optional reminder alarm."""
    due_value = get_task_due(task)
    due = datetime.fromisoformat(due_value)
    end = due.replace(second=0, microsecond=0) + timedelta(minutes=30)
    start_text = due.strftime("%Y%m%dT%H%M%S")
    end_text = end.strftime("%Y%m%dT%H%M%S")
    reminder = int(task.get("reminder_minutes", 0))
    alarm = ""
    if reminder:
        alarm = (
            "BEGIN:VALARM\n"
            f"TRIGGER:-PT{reminder}M\n"
            "ACTION:DISPLAY\n"
            f"DESCRIPTION:{ics_escape(task['title'])}\n"
            "END:VALARM\n"
        )
    return (
        "BEGIN:VCALENDAR\nVERSION:2.0\nPRODID:-//Focus Board//EN\n"
        "BEGIN:VEVENT\n"
        f"UID:{task['id']}@focus-board\n"
        f"DTSTART:{start_text}\nDTEND:{end_text}\n"
        f"SUMMARY:{ics_escape(task['title'])}\n"
        f"DESCRIPTION:{ics_escape(task.get('notes', ''))}\n"
        f"CATEGORIES:{ics_escape(task.get('category', ''))}\n"
        f"{alarm}END:VEVENT\nEND:VCALENDAR\n"
    )


if "tasks" not in st.session_state:
    st.session_state.tasks = load_tasks()

st.markdown(
    """
    <div class="hero">
      <div class="eyebrow">Personal productivity workspace</div>
      <h1>Focus Board</h1>
      <p>จัดระเบียบงาน เริ่มจากสิ่งสำคัญ และเห็นความคืบหน้าในที่เดียว</p>
    </div>
    """,
    unsafe_allow_html=True,
)

account_columns = st.columns([8, 1])
with account_columns[0]:
    st.caption(f"โปรไฟล์: {st.session_state.profile_name}")
with account_columns[1]:
    if st.button("Change profile"):
        del st.session_state["profile_name"]
        st.rerun()

all_tasks = st.session_state.tasks
completed_count = sum(task["completed"] for task in all_tasks)
active_count = len(all_tasks) - completed_count
high_priority_count = sum(
    task["priority"] == "High" and not task["completed"] for task in all_tasks
)
progress = completed_count / len(all_tasks) if all_tasks else 0

metric_columns = st.columns(4)
metrics = [
    ("Total tasks", len(all_tasks)),
    ("Active", active_count),
    ("Completed", completed_count),
    ("High priority", high_priority_count),
]
for column, (label, value) in zip(metric_columns, metrics):
    column.markdown(
        f'<div class="metric"><div>{label}</div><h2>{value}</h2></div>',
        unsafe_allow_html=True,
    )

st.progress(progress, text=f"Progress: {completed_count}/{len(all_tasks)} completed")
st.divider()

with st.expander("➕ Add a task", expanded=False):
    with st.form("add_task_form", clear_on_submit=True):
        title = st.text_input("Task name", placeholder="What needs to happen?")
        form_columns = st.columns(3)
        with form_columns[0]:
            category = st.selectbox("Category", CATEGORIES)
        with form_columns[1]:
            priority = st.select_slider("Priority", options=PRIORITIES, value="Medium")
        with form_columns[2]:
            due_date = st.date_input("Deadline", value=None)
        due_time = st.time_input("Time", value=time(17, 0))
        reminder = st.selectbox("Reminder", list(REMINDER_OPTIONS))
        notes = st.text_area("Notes", placeholder="Optional details...")
        submitted = st.form_submit_button("Add task", use_container_width=True)

    if submitted:
        if not title.strip():
            st.error("กรุณาใส่ชื่องานก่อนเพิ่มรายการ")
        else:
            add_task(st.session_state.tasks, title, category, priority, due_date, due_time, reminder, notes)
            save_tasks(st.session_state.tasks)
            st.success("เพิ่มงานแล้ว")
            st.rerun()

filter_columns = st.columns([2, 1, 1])
with filter_columns[0]:
    search_text = st.text_input("Search", placeholder="Search tasks or notes...")
with filter_columns[1]:
    selected_category = st.selectbox("Category", ["All"] + CATEGORIES)
with filter_columns[2]:
    selected_status = st.selectbox("Status", ["All", "Active", "Completed"])

st.caption("All = แสดงทุกหมวดหมู่หรือทุกสถานะ โดยไม่กรองรายการ")

visible_tasks = [
    task
    for task in sort_tasks(all_tasks)
    if task_matches(task, search_text, selected_category, selected_status)
]

st.subheader(f"Tasks · {len(visible_tasks)}")
if not visible_tasks:
    st.info("ยังไม่มีงานที่ตรงกับตัวกรอง ลองเพิ่มงานจากแถบด้านซ้าย")

for task in visible_tasks:
    is_done = task["completed"]
    card_class = "task-card done" if is_done else "task-card"
    title_class = "task-title done" if is_done else "task-title"
    notes_html = (
        f'<div class="task-meta">{task["notes"]}</div>'
        if task.get("notes")
        else ""
    )
    st.markdown(
        f'<div class="{card_class}"><div class="{title_class}">{"✓" if is_done else "○"} {task["title"]}</div>'
        f'<div class="task-meta">{task["category"]} · {task["priority"]} priority · {format_due_date(get_task_due(task))}</div>'
        f'{notes_html}</div>',
        unsafe_allow_html=True,
    )
    action_columns = st.columns([1, 1, 1, 1, 6])
    if action_columns[0].button("Undo" if is_done else "Done", key=f"done_{task['id']}"):
        task["completed"] = not task["completed"]
        save_tasks(all_tasks)
        st.rerun()
    if action_columns[1].button("Delete", key=f"delete_{task['id']}"):
        st.session_state.tasks = [item for item in all_tasks if item["id"] != task["id"]]
        save_tasks(st.session_state.tasks)
        st.rerun()
    if action_columns[2].button("Edit", key=f"edit_{task['id']}"):
        st.session_state[f"editing_{task['id']}"] = not st.session_state.get(f"editing_{task['id']}", False)
        st.rerun()
    if get_task_due(task):
        action_columns[3].download_button(
            "Calendar",
            data=create_calendar_event(task),
            file_name=f"{task['title']}.ics",
            mime="text/calendar",
            key=f"calendar_{task['id']}",
        )

    if st.session_state.get(f"editing_{task['id']}", False):
        current_due = get_task_due(task)
        try:
            parsed_due = datetime.fromisoformat(current_due)
            current_due_date = parsed_due.date()
            current_due_time = parsed_due.time().replace(second=0, microsecond=0)
        except (ValueError, TypeError):
            try:
                current_due_date = date.fromisoformat(current_due) if current_due else None
            except ValueError:
                current_due_date = None
            current_due_time = time(17, 0)

        with st.form(f"edit_form_{task['id']}"):
            edited_title = st.text_input("Task name", value=task["title"])
            edited_priority = st.select_slider("Priority", options=PRIORITIES, value=task["priority"])
            edited_due_date = st.date_input("Deadline", value=current_due_date)
            edited_due_time = st.time_input("Time", value=current_due_time)
            current_reminder = next(
                (
                    label
                    for label, minutes in REMINDER_OPTIONS.items()
                    if minutes == task.get("reminder_minutes", 0)
                ),
                "No reminder",
            )
            edited_reminder = st.selectbox(
                "Reminder", list(REMINDER_OPTIONS), index=list(REMINDER_OPTIONS).index(current_reminder)
            )
            edited_notes = st.text_area("Notes", value=task.get("notes", ""))
            save_edit = st.form_submit_button("Save changes")
        if save_edit and edited_title.strip():
            task["title"] = edited_title.strip()
            task["priority"] = edited_priority
            task["due_at"] = (
                datetime.combine(edited_due_date, edited_due_time).isoformat()
                if edited_due_date
                else ""
            )
            task["reminder_minutes"] = REMINDER_OPTIONS[edited_reminder]
            task["notes"] = edited_notes.strip()
            save_tasks(all_tasks)
            st.session_state[f"editing_{task['id']}"] = False
            st.rerun()
