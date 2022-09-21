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

def email(Name, Service, Finish):
    print(Finish)
    msg['Subject'] = f"ส่งคำร้องขอเรื่อง {Service}"
    body = f"คุณ {Name} ส่งคำร้องขอใช้งานเรื่อง {Service} ให้เสร็จสิ้นภายในวันที่ {Finish}"
    msg.attach(MIMEText(body, 'plain'))
    filename = "forIT.docx"
    attachment = open("./static/document/แบบคำขอใช้งานส่งไอที.docx", "rb")
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