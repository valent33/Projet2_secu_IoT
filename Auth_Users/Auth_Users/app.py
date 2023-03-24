from flask import Flask, render_template, request, redirect
import mysql.connector
from flask_mysqldb import MySQL

app = Flask(__name__)

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'tp2_Utilisateurs'

mysql = MySQL(app)


@app.route('/',methods=['GET','POST'])

def index():
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
def users():
    cur = mysql.connection.cursor()
    contenuUsers = cur.execute("SELECT * FROM users") 
    if contenuUsers > 0:
        userInfos = cur.fetchall()
        return render_template('liste_user.html',userInfos=userInfos)
        
if __name__ == '__main__':
    # Run the app server on localhost:4449
    app.run('localhost', 4449)
