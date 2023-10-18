from flask import Flask, request, jsonify, render_template, redirect, flash, session
from flask_session import Session

import json
import requests

from flask_cors import CORS, cross_origin

from Backend.blueprints.task_blueprint import task_blueprint
from Backend.models.task_model import TaskModel

host = 'http://localhost:5000'

model = TaskModel()

app = Flask(__name__, template_folder='Frontend', static_folder='Frontend/static')

app.register_blueprint(task_blueprint) 

cors = CORS(app)



Session(app)
#################### ERRORES ########################

# Manejador de error para el código de respuesta 403

@app.errorhandler(403)
def forbidden_error(error):
    return render_template('home/page-403.html'), 403

# Manejador de error para el código de respuesta 404 Not Found

@app.errorhandler(404)
def not_found_error(error):
    return render_template('home/page-404.html'), 404

# Manejador de error para el código de respuesta 500 Internal Server Error

@app.errorhandler(500)
def internal_error(error):
    return render_template('home/page-500.html'), 500

##################### FUNCIONES ######################


def authenticate_user(username, password):

    user = model.get_user_username(username)
    if user and user['password'] == password:
        return user
    return None

###################### RUTAS ########################

@app.route('/month', methods=['GET'])
def evaluateMonth():
    selectedMonth = request.args.get('month-input')
    print(selectedMonth)
    data_ = model.get_evaluate_month(selectedMonth)
    return render_template('/index.html', data=data_, selectedMonth_=selectedMonth)

@app.route('/day', methods=['GET'])
def evaluateDay():
    selectedDay = request.args.get('day-input')
    print(selectedDay)
    data_ = model.get_evaluate_day(selectedDay)
    return render_template('/index.html', data=data_, selectedDay_=selectedDay)

@app.route('/week', methods=['GET'])
def evaluateWeek():
    selectedWeek = request.args.get('selected-week')
    print(selectedWeek)

@app.route('/evaluate', methods=['GET'])
def evaluate():
    selectedMonth = request.args.get('selected-month')
    selectedDay = request.args.get('selected-day')

    if selectedMonth:
        data = model.get_evaluate_month(selectedMonth)
        evaluation_counts = model.get_evaluate_month_count(selectedMonth)

    elif selectedDay:
        data = model.get_evaluate_day(selectedDay)
        evaluation_counts = model.get_evaluate_day_count(selectedDay)
    else:
        data = []

    return render_template('/index.html', data=data, _evaluation_counts=evaluation_counts)

@app.route('/')
def evaluatee():
    data_ = model.get_evaluate()
    evaluation_counts = model.get_evaluate_count()
    print(evaluation_counts['good_count'])
    print(evaluation_counts['neutral_count'])
    print(evaluation_counts['bad_count'])
    return render_template('/index.html', data=data_, _evaluation_counts=evaluation_counts)


@app.route('/dashboard')
def dashboard():
    if 'username' in session and 'role' in session and 'iduser' in session:
        username = session['username']
        role = session['role']
        
        if role == 'admin':
            # Mostrar página de administrador
            return render_template('home/admin/Adashboard.html', username=username)
        elif role == 'estudiante':
            # Mostrar página de usuario normal
            return render_template('home/student/Sdashboard.html', username=username)
        elif role == 'profesor':
            # Mostrar página de profesor
            return render_template('home/teacher/Tdashboard.html', username=username)
        elif role == 'usuario':
            # Mostrar página de usuario
            return render_template('home/index.html', username=username)
    
    # Redirigir a la página de inicio de sesión si no hay sesión válida
    return redirect('/login')




@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        user = authenticate_user(username, password)

        if user:
            # Establecer los datos de sesión para el usuario
            session['username'] = user['username']
            session['iduser'] = user['iduser']

            return redirect('/')
        else:
            flash('Error, intentelo de nuevo', 'error')

    return render_template('accounts/login.html')


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':

        username = request.form['username']
        password = request.form['password']

        data = {
            'username': username,
            'password': password
        }

        headers = {'Content-Type': 'application/json'}
        response = requests.post(
            host + '/user/add_user', json=data, headers=headers)

        return redirect('/')

    return render_template('accounts/register.html')


@app.route('/registerteacher', methods=['GET', 'POST'])
def register_teacher():
    if 'username' in session and 'role' in session and 'iduser' in session:
        username_ = session['username']
        iduser_ = session['iduser']

        if request.method == 'POST':
            nombre = request.form['first_name']
            apellidoP = request.form['apellido_paterno']
            apellidoM = request.form['apellido_materno']
            dni = request.form['dni']
            mail = request.form['mail']
            celular = request.form['telefono_celular']
            ciudad = request.form['city']
            datePos = request.form['datef']
            curso = request.form['course']
            data = {
                'iduser': iduser_,
                'nombre': nombre,
                'apellidoP': apellidoP,
                'apellidoM': apellidoM,
                'dni': dni,
                'correo': mail,
                'celular': celular,
                'ciudad': ciudad,
                'datePos': datePos,
                'curso': curso,
                'estado': "Pendiente"
            }

            headers = {'Content-Type': 'application/json'}
            response = requests.post(
                host + '/postulant/add_postulant', json=data, headers=headers)

            return redirect('/dashboard')

        return render_template('home/register-teacher.html', username=username_)
    else:
        return redirect('/login')


@app.route('/despedir/<int:id>')
def despedir_profesor(id):
    if 'role' in session and session['role'] == 'admin':
        model.estado_despedido(id)
        return redirect('/teachers')
    else:
        return render_template('/home/admin/contratado.html')

@app.route('/contratar/<int:id>')
def contratar_profesor(id):
    if 'role' in session and session['role'] == 'admin':
        model.estado_contratado(id)
        return redirect('/teachers')
    else:
        return render_template('/home/admin/contratado.html')


@app.route('/logout')
def logout():
    # Eliminar la información de sesión del usuario
    session.pop('username', None)
    session.pop('role', None)

    # Redirigir al usuario a la página de inicio
    return render_template('home/index.html')

if __name__ == "__main__":      app.run(debug=True)