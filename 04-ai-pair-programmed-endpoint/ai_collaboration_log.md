# AI Collaboration Log

## Project: Task Manager REST API

This document records how AI assisted in building this endpoint and where human judgment was applied.

---

## What AI Helped With

### 1. Endpoint Structure
**AI suggestion:** Use Flask with a single `app.py` file, in-memory dict for storage, and separate route functions per HTTP method.

**Why accepted:** Clean separation of concerns, no database setup required for students running this locally.

---

### 2. UUID for Task IDs
**AI suggestion:** Use `uuid.uuid4()` to generate unique task IDs instead of auto-incrementing integers.

**Why accepted:** UUIDs are stateless — they don't require a database counter and work even if you restart the server and re-add tasks.

---

### 3. Input Validation on `completed` Field
**AI initial suggestion:**
```python
if "completed" in data:
    task["completed"] = bool(data["completed"])
```

**Problem found by human:** `bool("false")` returns `True` in Python because any non-empty string is truthy. This would accept the string `"false"` and mark the task as completed.

**Fix applied:**
```python
if not isinstance(data["completed"], bool):
    return error("'completed' must be true or false")
```

Now only actual JSON `true`/`false` is accepted.

---

### 4. Stats Endpoint
**AI suggestion:** Add a `/tasks/stats` endpoint.

**Problem found by human:** Flask route `/tasks/stats` conflicts with `/tasks/<task_id>` — Flask would try to match "stats" as a task ID.

**Fix applied:** The `/tasks/stats` route was placed BEFORE the `/tasks/<task_id>` route in the file. Flask matches routes in the order they are defined, so `stats` is matched first.

---

### 5. Test Structure
**AI suggestion:** Use `pytest` with a `clear_tasks` fixture marked `autouse=True`.

**Why accepted:** Each test starts with a clean state automatically without having to call `clear()` manually in every test function.

---

## Summary

| Area | AI Contribution | Human Correction |
|------|----------------|-----------------|
| Project structure | Suggested Flask + in-memory dict | None needed |
| UUID generation | Suggested `uuid.uuid4()` | None needed |
| `completed` validation | Used `bool()` cast | Fixed to `isinstance` check |
| Stats route ordering | Did not warn about conflict | Manually reordered routes |
| Test fixtures | Suggested `autouse=True` pattern | None needed |

**Key takeaway:** AI is great at boilerplate and structure. Human review catches subtle bugs in type handling and framework-specific behaviour (like Flask route ordering).
