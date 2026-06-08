from flask import Flask, request, jsonify
from datetime import datetime, timezone
import uuid

app = Flask(__name__)

# In-memory storage (no database needed to run this project)
tasks = {}


def make_task(title, description="", priority="medium"):
    return {
        "id": str(uuid.uuid4()),
        "title": title,
        "description": description,
        "priority": priority,
        "completed": False,
        "created_at": datetime.now(timezone.utc).isoformat().replace("+00:00", "Z"),
        "updated_at": datetime.now(timezone.utc).isoformat().replace("+00:00", "Z"),
    }


def error(message, status=400):
    return jsonify({"error": message}), status


# ── GET /tasks ── List all tasks (with optional filter) ──────
@app.route("/tasks", methods=["GET"])
def list_tasks():
    completed_filter = request.args.get("completed")
    priority_filter = request.args.get("priority")

    result = list(tasks.values())

    if completed_filter is not None:
        is_completed = completed_filter.lower() == "true"
        result = [t for t in result if t["completed"] == is_completed]

    if priority_filter:
        result = [t for t in result if t["priority"] == priority_filter]

    return jsonify({
        "tasks": result,
        "count": len(result)
    }), 200


# ── POST /tasks ── Create a new task ─────────────────────────
@app.route("/tasks", methods=["POST"])
def create_task():
    data = request.get_json()

    if not data:
        return error("Request body must be JSON")

    title = data.get("title", "").strip()
    if not title:
        return error("'title' is required and cannot be empty")

    priority = data.get("priority", "medium")
    if priority not in ("low", "medium", "high"):
        return error("'priority' must be one of: low, medium, high")

    task = make_task(
        title=title,
        description=data.get("description", ""),
        priority=priority,
    )
    tasks[task["id"]] = task
    return jsonify(task), 201


# ── GET /tasks/<id> ── Get a single task ─────────────────────
@app.route("/tasks/<task_id>", methods=["GET"])
def get_task(task_id):
    task = tasks.get(task_id)
    if not task:
        return error(f"Task '{task_id}' not found", 404)
    return jsonify(task), 200


# ── PATCH /tasks/<id> ── Update a task ───────────────────────
@app.route("/tasks/<task_id>", methods=["PATCH"])
def update_task(task_id):
    task = tasks.get(task_id)
    if not task:
        return error(f"Task '{task_id}' not found", 404)

    data = request.get_json()
    if not data:
        return error("Request body must be JSON")

    if "title" in data:
        title = data["title"].strip()
        if not title:
            return error("'title' cannot be empty")
        task["title"] = title

    if "description" in data:
        task["description"] = data["description"]

    if "priority" in data:
        if data["priority"] not in ("low", "medium", "high"):
            return error("'priority' must be one of: low, medium, high")
        task["priority"] = data["priority"]

    if "completed" in data:
        if not isinstance(data["completed"], bool):
            return error("'completed' must be true or false")
        task["completed"] = data["completed"]

    task["updated_at"] = datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")
    return jsonify(task), 200


# ── DELETE /tasks/<id> ── Delete a task ──────────────────────
@app.route("/tasks/<task_id>", methods=["DELETE"])
def delete_task(task_id):
    if task_id not in tasks:
        return error(f"Task '{task_id}' not found", 404)
    del tasks[task_id]
    return jsonify({"message": f"Task '{task_id}' deleted"}), 200


# ── GET /tasks/stats ── Summary statistics ───────────────────
@app.route("/tasks/stats", methods=["GET"])
def get_stats():
    all_tasks = list(tasks.values())
    total = len(all_tasks)
    completed = sum(1 for t in all_tasks if t["completed"])
    by_priority = {"low": 0, "medium": 0, "high": 0}
    for t in all_tasks:
        by_priority[t["priority"]] += 1

    return jsonify({
        "total": total,
        "completed": completed,
        "pending": total - completed,
        "by_priority": by_priority,
    }), 200


if __name__ == "__main__":
    app.run(debug=True, port=5000)
