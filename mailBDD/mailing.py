from app import run_server
import smtplib, ssl
from email.message import EmailMessage
import mysql.connector as mc
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText


def send_mail(nom, prenom, mail, attaque): 

    # me == my email address
    # you == recipient's email address


    # Create message container - the correct MIME type is multipart/alternative.
    msg = MIMEMultipart('alternative')
    msg['Subject'] = "Tentative d'intrusion détectée"
    msg['From'] = "securnetworkiot@gmail.com"
    msg['To'] = mail

    # Create the body of the message (a plain-text and an HTML version).

    html = f"""
    <html>
    <body lang=FR>

    <div class=WordSection1>

    <p class=MsoNormal>Bonjour {nom} {prenom},<o:p></o:p></p>

    <p class=MsoNormal><o:p>&nbsp;</o:p></p>

    <p class=MsoNormal>Nous vous notifions une possibilité d'attaque de type  {attaque}, en cours sur votre réseau local. Pour la sécurité de celui-ci nous
    vous conseillons de&nbsp;:<o:p></o:p></p>

    <ul style='margin-top:0cm' type=disc>
    <li class=MsoListParagraph style='margin-left:0cm;'>Changer
        le mot de passe d'acces<o:p></o:p></li>
    <li class=MsoListParagraph style='margin-left:0cm;'>Vérifier
        via l'interface de votre box les appareils qui y sont authentifiés<o:p></o:p></li>
    <li class=MsoListParagraph style='margin-left:0cm;'>Réinitialiser
        les objets connectés de votre réseau.<o:p></o:p></li>
    </ul>

    <p class=MsoNormal><o:p>&nbsp;</o:p></p>

    <p class=MsoNormal>En espérant qu'il ne s'agit que d'une regrettable erreur<o:p></o:p></p>

    <p class=MsoNormal><o:p>&nbsp;</o:p></p>

    <p class=MsoNormal>Votre IDS securnetworkiot<o:p></o:p></p>



    </div>

    </body>

    </html>
    """

    part2 = MIMEText(html, 'html')

    # Attach parts into message container.
    # According to RFC 2046, the last part of a multipart message, in this case
    # the HTML message, is best and preferred.
    msg.attach(part2)

    context=ssl.create_default_context()

    with smtplib.SMTP_SSL("smtp.gmail.com", port=465, context=context) as smtp:
        smtp.login(user=msg["From"],password="ykbgciguwynwhkyc")
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


send_mails("Slowloris")
