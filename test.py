
import pymysql

def getConnection():
    return pymysql.connect(
        host='localhost',
        db='water_di',
        user='root',
        password='',
        charset='utf8',
        cursorclass=pymysql.cursors.DictCursor
    )
###################################### Line notify #########################################################
# import requests
# from datetime import datetime

# now = datetime.now()
# url = 'https://notify-api.line.me/api/notify'
# token = '1ynH4ehbVZZK3ngffNqBjnZVdnU5gKtNIYLu14IOLD8'
# headers = {'content-type':'application/x-www-form-urlencoded','Authorization':'Bearer '+token}

# msg = """
# รายงานแจ้งเตือนสถานะค่าแรงดัน 
# ชื่อจุดติดตั้ง : PT-CW-250 RD.G13
# สถานะแจ้งเตือน : High
# ค่าแรงดันที่วัดได้ : 3.26 bar 
# วันที่รายงาน : 29/08/2022
# เวลาที่รายงาน : 08:18:11
# ไม่ต่ำกว่า : 1.5 bar 
# ไม่เกินกว่า : 3.25 bar"""
# r = requests.post(url, headers=headers, data = {'message':msg})
# print (r.text)
#############################################################################################################

############################################ Email ##########################################################

# import smtplib

# gmail_user = 'skw39564@skw.ac.th'
# gmail_password = 'non39564'

# sent_from = gmail_user
# to = ['sarawut.on.62@ubu.ac.th']
# subject = 'Test Send'
# body = 'Hi'

# email_text = """\
# From: %s
# To: %s
# Subject: %s
# %s
# """ % (sent_from, ", ".join(to), subject, body)

# try:
#     smtp_server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
#     smtp_server.ehlo()
#     smtp_server.login(gmail_user, gmail_password)
#     smtp_server.sendmail(sent_from, to, email_text)
#     smtp_server.close()
#     print ("Email sent successfully!")
# except Exception as ex:
#     print ("Something went wrong….",ex)

#############################################################################################################

def convertToBinaryData(filename):
    # Convert digital data to binary format
    with open(filename, 'rb') as file:
        binaryData = file.read()
    # return binaryData
    print(binaryData)
    
convertToBinaryData("./static/signature/Dullahan.png")