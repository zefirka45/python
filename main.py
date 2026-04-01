from flask import Flask, render_template, request, redirect, url_for, session as flask_session
from sqlalchemy.orm import sessionmaker, scoped_session
from InitDB import engine, User, Tasks 

app = Flask(__name__)
app.secret_key = 'super_secret_key_123'

# Настройка сессии БД
session_factory = sessionmaker(bind=engine)
db_session = scoped_session(session_factory)

@app.teardown_appcontext
def shutdown_session(exception=None):
    db_session.remove()

menu = [
    {"name": "Главная", "url": "dashboard_main"},
    {"name": "Задачи", "url": "dashboard_tasks"},
    {"name": "Пользователи", "url": "dashboard_users"},
    {"name": "Архив", "url": "dashboard_archive"}
]

@app.route('/')
def index():
    return render_template("index.html")

@app.route('/login', methods=['POST']) 
def login():
    login_val = request.form.get('Login')
    password_val = request.form.get('Password')
    user = db_session.query(User).filter_by(name=login_val, password=password_val).first()
    if user:
        flask_session['user_id'] = user.id
        return redirect(url_for('dashboard_main'))
    return '<h1>Неверные данные!</h1>'

@app.route('/dashboard')
def dashboard_main():
    return render_template('dashboard.html', menu=menu)

# --- ПОЛЬЗОВАТЕЛИ ---
@app.route('/dashboard_users')
def dashboard_users():
    read_user = db_session.query(User).all()
    return render_template('dashboard.html', menu=menu, user=read_user)

@app.route('/dashboard_users_create', methods=['GET', 'POST'])
def dashboard_users_create():
    if request.method == 'POST':
        new_user = User(
            name=request.form.get('name'),
            password=request.form.get('password'),
            role=request.form.get('role'),
            status='Активен'
        )
        db_session.add(new_user)
        db_session.commit()
        return redirect(url_for('dashboard_users'))
    return render_template('dashboard.html', menu=menu)

# --- ЗАДАЧИ ---
@app.route('/dashboard_tasks')
def dashboard_tasks(): 
    all_tasks = db_session.query(Tasks).all()
    return render_template('dashboard.html', menu=menu, tasks=all_tasks)

@app.route('/dashboard_tasks_create', methods=['GET', 'POST'])
def dashboard_tasks_create():
    if request.method == 'POST':
        new_task = Tasks(
            applicant_id=flask_session.get('user_id'), 
            executor_id=request.form.get('executor'),
            theme=request.form.get('theme'),
            message=request.form.get('message'),
            deadline=request.form.get('deadline'),
            status="Распределение"
        )
        db_session.add(new_task)
        db_session.commit()
        return redirect(url_for('dashboard_tasks'))
    
    all_user = db_session.query(User).all()
    return render_template('dashboard.html', menu=menu, user=all_user)

# Универсальный маршрут: и детали, и сохранение статуса (из таблицы или карточки)
@app.route('/dashboard_tasks_detal/<int:task_id>', methods=['GET', 'POST'])
def dashboard_tasks_detal(task_id):
    task = db_session.query(Tasks).get(task_id)
    if not task:
        return "Задача не найдена", 404

    if request.method == 'POST':
        task.status = request.form.get('status')
        db_session.commit()
        # Возвращаем туда, откуда пришел запрос (в список или в детали)
        return redirect(request.referrer or url_for('dashboard_tasks'))
    
    return render_template('dashboard.html', menu=menu, current_task=task)
# Архив
@app.route('/dashboard_archive')
def dashboard_archive():
    all_tasks = db_session.query(Tasks).all()
    return render_template('dashboard.html', menu=menu,tasks=all_tasks)

if __name__ == "__main__":
    app.run(debug=True)
