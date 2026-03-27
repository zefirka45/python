from flask import Flask, render_template, request, redirect, url_for, session as flask_session
from sqlalchemy.orm import sessionmaker
from InitDB import engine, User,Tasks 
app = Flask(__name__)
app.secret_key = 'your_secret_key'

Session = sessionmaker(bind=engine)
db_session = Session()

menu = [{"name":"Главная","url":"dashboard_main"},
        {"name":"Задачи","url":"dashboard_tasks"},
        {"name":"Пользователи","url":"dashboard_users"}]
#Логин
@app.route('/')
def index():
    return render_template("index.html")

@app.route('/login', methods=['POST']) # Добавляем маршрут для обработки формы
def login():
    login_val = request.form.get('Login')
    password_val = request.form.get('Password')
    user = db_session.query(User).filter_by(name=login_val, password=password_val).first()
    if user:
        flask_session['user_id'] = user.id
        return redirect(url_for('dashboard_main'))
    else:
        return '<h1>Invalid credentials!</h1>'
#панель
@app.route('/dashboard')
def dashboard_main():
    return render_template('dashboard.html', menu=menu)

#Пользователи
@app.route('/dashboard_users')
def dashboard_users():
    read_user = db_session.query(User).all()
    return render_template('dashboard.html', menu=menu, user = read_user)

#Задачи
@app.route('/dashboard_tasks')
def dashboard_tasks():
    all_tasks = db_session.query(Tasks).all()
    return render_template('dashboard.html', menu=menu, tasks=all_tasks)

@app.route('/dashboard_tasks_create', methods=['GET', 'POST'])
def dashboard_tasks_create():
    if request.method == 'POST':
        # 1. Получаем данные из формы (те, что в <input name="...">)
        theme = request.form.get('theme')
        message = request.form.get('message')
        deadline = request.form.get('deadline')
        
        current_user_id = flask_session.get('user_id')
        user = db_session.query(User).get(current_user_id) if current_user_id else None
        
        new_task = Tasks(
            theme=theme,
            message=message,
            deadline=deadline,
            user_id=user.name if user else "Аноним",
            status="В работе"
        )
        db_session.add(new_task)
        db_session.commit()
        return redirect(url_for('dashboard_tasks'))

    return render_template('dashboard.html', menu=menu)


if __name__ == "__main__":
    app.run(debug=True)
