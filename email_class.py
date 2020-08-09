import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders


class SendEmail:
    def __init__(self,email,pdf_file,date):
        self.email_receiver = email
        self.pdf_file = pdf_file
        self.email_user = "c3proyect2020@gmail.com"
        self.email_user_password = "C3proyect123456789@"
        self.message = MIMEMultipart()
        self.message['From'] = self.email_user
        self.message['To'] = self.email_receiver
        self.message['Subject'] = "Invoice from "+str(date)
        self.body = "Hi, this is your new invoice"
        self.message.attach(MIMEText(self.body,"plain"))
        self.attachment = open(self.pdf_file, "rb")
        self.part = MIMEBase("application",'octet-stream')
        self.part.set_payload((self.attachment).read())
        encoders.encode_base64(self.part)
        self.part.add_header('Content-Disposition',"attachment; filename= "+self.pdf_file)
        self.message.attach(self.part)
        self.text = self.message.as_string()
        self.server = smtplib.SMTP("smtp.gmail.com",587)
        self.server.starttls()
        self.server.login(self.email_user,self.email_user_password)


    def send_email(self):
        self.server.sendmail(self.email_user,self.email_receiver,self.text)
        print("Email sent")
        self.server.quit()


