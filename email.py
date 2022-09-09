import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders

fromaddr = "skw39564@skw.ac.th"
toaddr = "sarawut.on.62@ubu.ac.th"

msg = MIMEMultipart()

msg['From'] = fromaddr
msg['To'] = toaddr

def email():
    msg['Subject'] = "Subject of the Mail"
    body = "Body_of_the_mail"
    msg.attach(MIMEText(body, 'plain'))
    filename = "Application_form.xls"
    attachment = open("FM-1430-006 ใบขอใช้บริการคอมพิวเตอร์ 01-04-65.xls", "rb")
    p = MIMEBase('application', 'octet-stream')
    p.set_payload((attachment).read())
    encoders.encode_base64(p)
    p.add_header('Content-Disposition', "attachment; filename= %s" % filename)
    msg.attach(p)
    s = smtplib.SMTP('smtp.gmail.com', 587)
    s.starttls()
    s.login(fromaddr, "non39564")
    text = msg.as_string()
    s.sendmail(fromaddr, toaddr, text)
    s.quit()