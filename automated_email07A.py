import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders

def sendAutomatedMail(name, email_address):

    fromaddr = "@gmail.com"
    toaddr = str(email_address)
    name = name

    msg = MIMEMultipart()

    msg['From'] = fromaddr
    msg['To'] = toaddr
    msg['Subject'] = "WARNING: Logout Timed Out"
    body = f"{name} has not logged out before time 5'O Clock...\nPlease don't repeat this mistake again...\
                                            \nYou should contact Administration for further details."

    msg.attach(MIMEText(body, 'plain'))
    s = smtplib.SMTP('smtp.gmail.com', 587)
    s.starttls()
    conn = open('password.txt')
    password = conn.read()
    s.login(fromaddr, password=password)
    text = msg.as_string()
    s.sendmail(fromaddr, toaddr, text)
    s.quit()
