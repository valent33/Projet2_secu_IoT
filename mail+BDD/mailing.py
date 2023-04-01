from app import run_server
import smtplib, ssl
from email.message import EmailMessage
import mysql.connector as mc



def send_mail(nom, prenom, mail, attaque): 
    """Fonction qui envoie un mail à une personne et qui permet de donner l'attaque précise"""
    msg = EmailMessage()
    msg.set_content(f"Bonjour {nom} {prenom}, nous avons détecté un risque d'attaque {attaque}, sur votre caméra conectée HOSAFE, nous vous conseillons de changer le mot de passe d'accès à celle-ci pour un plus sécurisé! ")
    msg["Subject"] = "teantative d'intrusion détectée"
    msg["From"] = "samuel.elard@sfr.fr"
    msg["To"] = mail

    context=ssl.create_default_context()

    with smtplib.SMTP_SSL("smtp.sfr.fr", port=465, context=context) as smtp:
        smtp.login(user=msg["From"],password="XXXX")
        smtp.send_message(msg)


def send_mails(attaque):
    """Récupère tous les emails de toutes les personnes qui se sont register et leur envoie le mail"""
    db_connection=connect_db()
    Users_registered=pullUsers(db_connection)#Récup des users a
    close_conn(db_connection)
    for user in Users_registered:
        send_mail(user[1].decode("utf-8"),user[2].decode("utf-8"),user[3].decode("utf-8"), attaque )#envoie un mail
    print("mails envoyés")

def connect_db():
    conn= mc.connect(host="127.0.0.1", user="root", password="", database="tp2users")
    return conn

def close_conn(conn):
    conn.close()
    return 0

def pullUsers(conn_db):
    """Récupération des users de la base"""
    cur = conn_db.cursor()
    cur.execute("SELECT * FROM users",) 
    userInfos = cur.fetchall()
    if userInfos != []:
        return userInfos
    else:
        print("liste user vide")


send_mails("Apéro")
