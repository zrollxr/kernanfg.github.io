import os
import json
from flask import Flask, render_template, redirect, url_for, request

app = Flask(__name__)

# Ruta para cargar los usuarios desde el archivo JSON
def load_users():
    try:
        with open('page/data/users.json', 'r') as file:
            users = json.load(file)  # Cargar los usuarios desde el archivo JSON
    except FileNotFoundError:
        users = {}  # Si el archivo no existe, devolver un diccionario vacío
    return users

# Ruta para guardar los usuarios en el archivo JSON
def save_users(users):
    with open('page/data/users.json', 'w') as file:
        json.dump(users, file, indent=4)

# Ruta para la página principal (login)
@app.route('/')
def home():
    return render_template('index.html')  # Página de login

# Ruta para la página de registro
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        # Cargar los usuarios actuales desde el archivo
        users = load_users()

        # Verificar si el nombre de usuario ya existe
        if username in users:
            return "El usuario ya existe, por favor elige otro", 400
        
        # Guardar el nuevo usuario en el diccionario
        users[username] = password

        # Guardar los usuarios en el archivo JSON
        save_users(users)

        return redirect(url_for('home'))  # Redirige al login después del registro
    
    return render_template('register.html')  # Página donde se puede crear una cuenta

# Ruta para procesar el formulario de login
@app.route('/login', methods=['POST'])
def login():
    username = request.form['username']
    password = request.form['password']

    # Cargar los usuarios desde el archivo JSON
    users = load_users()

    # Verificar si las credenciales coinciden con el archivo de usuarios
    if username in users and users[username] == password:
        return redirect(url_for('dashboard'))  # Redirige al dashboard después de login
    else:
        return "Credenciales incorrectas", 400  # Mensaje de error si las credenciales son incorrectas

# Ruta para el dashboard
@app.route('/dashboard')
def dashboard():
    # Cargar los usuarios para mostrar quienes han ingresado (opcional)
    users = load_users()
    logged_in_users = [user for user in users if users[user] == 'logged_in']  # Puedes personalizar esta lógica
    return render_template('dashboard.html', logged_in_users=logged_in_users)

@app.route("/fights")
def fights():
    return render_template("fights.html")

@app.route('/contact')
def contact():
    return render_template("contact.html")

if __name__ ==  '__main__':
    app.run(debug=True, port=4200)
