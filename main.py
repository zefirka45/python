from flask import Flask, render_template, request, redirect, url_for, session as flask_session
from sqlalchemy.orm import sessionmaker
from InitDB import engine, User,Tasks 
app = Flask(__name__)
app.secret_key = 'your_secret_key'

Session = sessionmaker(bind=engine)
db_session = Session()

menu = [{"name":"Главная","url":"dashboard_main"},
        {"name":"Задачи","url":"dashboard_tasks"},
        {"name":"Пользователи","url":"dashboard_users"},
        {"name":"Архив","url":"dashboard_archive"}]
#Логин
@app.route('/')
def index():
    return render_template("index.html")

@app.route('/login', methods=['POST','GET']) 
def login():
    login_val = request.form.get('Login')
    password_val = request.form.get('Password')
    user = db_session.query(User).filter_by(name=login_val, password=password_val).first()
    if user:
        flask_session['user_id'] = user.id
        return redirect(url_for('dashboard_main'))
    else:
        return '<h1>Invalid credentials!</h1>'

@app.route('/register', methods=['POST','GET'])
def register():
    if request.method == 'POST':
        user_reg = User(
            name = request.form.get('Login'),
            password = request.form.get('Password'),
            role = 'Пользователь',
            status = 'Активный'
        )
        db_session.add(user_reg)
        db_session.commit()
        return redirect(url_for('/'))
    return render_template('index.html')
#панель
@app.route('/dashboard')
def dashboard_main():
    return render_template('dashboard.html', menu=menu)

#Пользователи
@app.route('/dashboard_users')
def dashboard_users():
    read_user = db_session.query(User).all()
    return render_template('dashboard.html', menu=menu, user = read_user)

@app.route('/dashboard_users_create',methods=['GET', 'POST'])
def dashboard_users_create():
    if request.method == 'POST':
        new_user = User(
            name = request.form.get('name'),
            password = request.form.get('password'),
            role = request.form.get('role'),
            status = 'active'
        )
        db_session.add(new_user)
        db_session.commit()
        return redirect(url_for('dashboard_users'))
    return render_template('dashboard.html', menu=menu)

#Задачи
@app.route('/dashboard_tasks')
def dashboard_tasks(): 
    all_tasks = db_session.query(Tasks).all()
    return render_template('dashboard.html', menu=menu, tasks=all_tasks)

@app.route('/dashboard_tasks_create', methods=['GET', 'POST'])
def dashboard_tasks_create():
    if request.method == 'POST':
        executor = request.form.get('executor')
        theme = request.form.get('theme')
        message = request.form.get('message')
        deadline = request.form.get('deadline')
        
        current_user_id = flask_session.get('user_id')
        applicant = db_session.query(User).get(current_user_id) if current_user_id else None

        new_task = Tasks(
            applicant_id = applicant.name if  applicant else "Аноним",
            executor_id=executor,
            theme=theme,
            message=message,
            deadline=deadline,
            status="В работе"
        )
        db_session.add(new_task)
        db_session.commit()
        return redirect(url_for('dashboard_tasks'))
    
    all_user = db_session.query(User).all()
    return render_template('dashboard.html', menu=menu, user=all_user)

@app.route('/dashboard_tasks_detal/<task_id>')
def dashboard_tasks_detal(task_id):
        task = db_session.query(Tasks).get(task_id)
        return render_template('dashboard.html', menu=menu, current_task = task)

#Архив
@app.route('/dashboard_archive')
def dashboard_archive():
    return render_template('dashboard.html', menu=menu)



if __name__ == "__main__":
    app.run(debug=True)
