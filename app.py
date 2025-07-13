from flask import Flask, request, jsonify

app = Flask(__name__)

# Список для хранения задач (вместо базы данных)
tasks = [
    {"id": 1, "title": "Изучить Python", "completed": False},
    {"id": 2, "title": "Сделать домашку", "completed": True},
]


# Получить все задачи
@app.route("/tasks", methods=["GET"])
def get_tasks():
    return jsonify({"tasks": tasks})


# Получить задачу по ID
@app.route("/tasks/<int:task_id>", methods=["GET"])
def get_task(task_id):
    for task in tasks:
        if task["id"] == task_id:
            return jsonify(task)
    return jsonify({"error": "Задача не найдена"}), 404


# Создать новую задачу
@app.route("/tasks", methods=["POST"])
def create_task():
    data = request.get_json()
    if not data or "title" not in data:
        return jsonify({"error": "Укажите название задачи"}), 400

    new_task = {
        "id": len(tasks) + 1,
        "title": data["title"],
        "completed": data.get("completed", False),
    }
    tasks.append(new_task)
    return jsonify(new_task), 201


# Обновить задачу
@app.route("/tasks/<int:task_id>", methods=["PUT"])
def update_task(task_id):
    data = request.get_json()
    if not data or "title" not in data:
        return jsonify({"error": "Укажите название задачи"}), 400

    for task in tasks:
        if task["id"] == task_id:
            task["title"] = data["title"]
            task["completed"] = data.get("completed", task["completed"])
            return jsonify(task)
    return jsonify({"error": "Задача не найдена"}), 404


# Удалить задачу
@app.route("/tasks/<int:task_id>", methods=["DELETE"])
def delete_task(task_id):
    for i, task in enumerate(tasks):
        if task["id"] == task_id:
            tasks.pop(i)
            return jsonify({}), 204
    return jsonify({"error": "Задача не найдена"}), 404


if __name__ == "__main__":
    app.run(debug=True)
