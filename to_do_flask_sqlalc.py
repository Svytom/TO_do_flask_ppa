from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///tasks.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(80), nullable=False)
    description = db.Column(db.String(200), nullable=True)
    status = db.Column(db.String(20), nullable=False, default="Не выполнено")

with app.app_context():
    db.create_all()
    Task.query.delete()
    tasks = [
        Task(title="Проснуться", description="Выпить кофе"),
        Task(title="Позаботиться о себе", description="Сделать перерыв"),
        Task(title="Пообщаться с кем нибудь", description="Позвонить или написать другу")
    ]
    db.session.bulk_save_objects(tasks)
    db.session.commit()

@app.route('/')
def home():
    return "Перейдите на /tasks для работы с задачами."

@app.route('/tasks', methods=['POST'])
def create_task():
    data = request.json
    new_task = Task(title=data['title'], description=data.get('description', ''))
    db.session.add(new_task)
    db.session.commit()
    return jsonify({"message": "Задача создана"}), 201

@app.route('/tasks', methods=['GET'])
def get_tasks():
    tasks = Task.query.all()
    return jsonify([{"id": t.id, "title": t.title, "description": t.description, "status": t.status} for t in tasks]), 200

@app.route('/tasks/<int:task_id>', methods=['PUT'])
def update_task_status(task_id):
    task = Task.query.get_or_404(task_id)
    task.status = "Выполнено"
    db.session.commit()
    return jsonify({"message": "Статус задачи обновлен"}), 200

@app.route('/tasks/<int:task_id>', methods=['DELETE'])
def delete_task(task_id):
    task = Task.query.get_or_404(task_id)
    db.session.delete(task)
    db.session.commit()
    return jsonify({"message": "Задача удалена"}), 200

if __name__ == '__main__':
    app.run(debug=True)