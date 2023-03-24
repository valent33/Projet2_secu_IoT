import smtplib, ssl
from email.message import EmailMessage

msg = EmailMessage()
msg.set_content("Apéro")
msg["Subject"] = "Pti Jaune?"
msg["From"] = "samuel.elard@sfr.fr"
msg["To"] = "sylvie.elard@sfr.fr"

context=ssl.create_default_context()

with smtplib.SMTP_SSL("smtp.sfr.fr", port=465, context=context) as smtp:

    smtp.login(msg["From"], "XXXXXXXXXXXX")
    smtp.send_message(msg)