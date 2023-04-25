from flask import Flask, render_template, request, redirect, session
import mysql.connector
from flask_mysqldb import MySQL
import os

app = Flask(__name__)  # création d'un objet serveur
app.secret_key = 'IOT'

# Config du serveur
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'tp2_utilisateurs'  # Nom BDD locale
app.config['MYSQL_UNIX_SOCKET'] = '/opt/lampp/var/mysql/mysql.sock'
mysql = MySQL(app)

emailEdit=""
@app.route('/', methods=['GET', 'POST'])
def index():
    error = None
    # Fonction permettant de faire la connexion  d'un utilisateur de la base de données
    if request.method == 'POST':
        userInfos = request.form
        cur = mysql.connection.cursor()
        contenuUsers = cur.execute("SELECT * FROM users WHERE email = %s AND password = %s ", (userInfos['email'],userInfos['password'],))

        if contenuUsers > 0:
            session['loggedin'] = True
            session['email'] = userInfos['email']
            return redirect('/liste_user')
        else :
            error = "E-mail ou mot de passe incorrect!! "
        return render_template('index.html', error=error)
    return render_template("index.html")


@app.route('/analyse_fichier', methods=['GET', 'POST'])
def analyse_fichier():
    error = None
    if request.method == 'POST':
        file = request.files['file']
        # Définir le chemin de destination pour enregistrer le fichier
        upload_folder = './uploads'
        if not os.path.exists(upload_folder):
            os.makedirs(upload_folder)
        file_path = os.path.join(upload_folder, file.filename) # type: ignore
        # Enregistrer le fichier dans le dossier uploads
        file.save(file_path)
        # Exécuter le script avec le chemin du fichier en tant qu'argument
        cmd = f"python ./analyse_LSTM.py {file_path} -test"
        os.system(cmd)

    return render_template('analyse_fichier.html')

@app.route('/analyse_fichier')
def toanalyse():
    return render_template('analyse_fichier.html')


@app.route('/register', methods=['GET', 'POST'])
def register():
    # Fonction permettant d'entrer un utilisateur de la base de données
    if request.method == 'POST':
        userInfos = request.form
        nom_user = userInfos['nom_user']
        prenom_user = userInfos['prenom_user']
        email = userInfos['email']
        password = userInfos['password']
        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO users(nom_user, prenom_user, email, password) VALUES (%s, %s, %s, %s)",
                    (nom_user, prenom_user, email, password))
        mysql.connection.commit()
        return redirect('/liste_user')
    return render_template("register.html")


@app.route('/edit', methods=['GET', 'POST'])
def editInfos():
    # Fonction permettant d'editer les infos d'un utilisateur 
    if request.method == 'POST':
        userInfos = request.form
        nom_user = userInfos['nom_user']
        prenom_user = userInfos['prenom_user']
        email = userInfos['email']
        password = userInfos['password']
        cur = mysql.connection.cursor()
        cur.execute("UPDATE users SET nom_user=%s, prenom_user=%s, email=%s, password=%s WHERE email=%s",
                    (nom_user, prenom_user, email, password, session['email']))
        mysql.connection.commit()
        return redirect('/liste_user')
    return render_template("edit_infos.html")


@app.route('/liste_user')
def render_infos():
    userInfos = getUsers()
    return render_template('liste_user.html', userInfos=userInfos)

@app.route('/liste_user')
def toliste():
    return render_template('liste_user.html')


@app.route('/deconnexion')
def deconnexion():
    return redirect('/')

def getUsers():
    # Fonction permettant de recuperer tous les utilisateurs de la base de données
    cur = mysql.connection.cursor()
    contenuUsers = cur.execute("SELECT * FROM users")
    if contenuUsers > 0:
        userInfos = cur.fetchall()
        return userInfos


def run_server():
    if __name__ == '__main__':
        # Run the app server on localhost:4449
        app.run('localhost', 4449)


@app.route('/register')
def pageregister():
    return render_template('register.html')


run_server()
