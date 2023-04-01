from flask import Flask, render_template, request, redirect
import mysql.connector
from flask_mysqldb import MySQL



app = Flask(__name__)# création d'un objet serveur

#Config du serveur
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'tp2users'#Nom BDD locale
mysql = MySQL(app) 


@app.route('/',methods=['GET','POST'])
def index():
    #Fonction permettant d'entrer un utilisateur de la base de données
    if request.method == 'POST':
        userInfos = request.form
        nom_user = userInfos['nom_user']
        prenom_user = userInfos['prenom_user']
        email = userInfos['email']
        password = userInfos['password']
        cur = mysql.connection.cursor()
        cur.execute ("INSERT INTO users(nom_user, prenom_user, email, password) VALUES (%s, %s, %s, %s)", (nom_user, prenom_user, email, password))
        mysql.connection.commit()
        return redirect('/liste_user')
    return render_template("index.html")


@app.route('/liste_user')
def render_infos():
    userInfos= getUsers()
    return render_template('liste_user.html',userInfos=userInfos)


def getUsers():
    cur = mysql.connection.cursor()
    contenuUsers = cur.execute("SELECT * FROM users") 
    if contenuUsers > 0:
        userInfos = cur.fetchall()
        return userInfos
        
def run_server():
    if __name__ == '__main__':
        # Run the app server on localhost:4449
        app.run('localhost', 4449)





