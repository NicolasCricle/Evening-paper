import datetime
import smtplib
import os
from dotenv import load_dotenv 
from email.mime.text import MIMEText
from email.header import Header

from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText


# 加载env环境
basePath = os.path.dirname(os.path.dirname(__file__))
load_dotenv(os.path.join(basePath, ".env"))


class MyMail(object):
    SMTP_SERVER = "smtp.exmail.qq.com"
    SENDER = os.environ.get("SENDER")
    PASSWORD = os.environ.get("PASSWORD")
    RECEIVERS = [
        "17625905485@163.com",
        "470588044@qq.com"
    ]
    COPY_RECEIVERS = [
        "17625905485@163.com",
        "470588044@qq.com"
    ]
    SUBJECT = "{today} 日武汉晚报"

    def __init__(self, *files):
        self._smtp = smtplib.SMTP_SSL(self.SMTP_SERVER)
        self._files = files

    @property
    def subject(self):
        today = str(datetime.date.today())
        return self.SUBJECT.format(today=today)

    @property
    def sender(self):
        return self.SENDER
    
    @sender.setter
    def sender(self, value):
        # TODO 正则校验
        self.SENDER = value
    
    @property
    def pw(self):
        return self.PASSWORD

    @pw.setter
    def pw(self, value):
        self.PASSWORD = value

    @property
    def auth(self):
        return self.sender, self.pw

    @property
    def receivers(self):
        return self.RECEIVERS

    @receivers.setter
    def receivers(self, value):
        if isinstance(value, list):
            self.RECEIVERS = value
        elif isinstance(value, str):
            self.RECEIVERS = [value]
        else:
            raise Exception("错误的receivers")

    @property
    def copyReceivers(self):
        return self.COPY_RECEIVERS

    @copyReceivers.setter
    def copyReceivers(self, value):
        if isinstance(value, list):
            self.COPY_RECEIVERS = value
        elif isinstance(value, str):
            self.COPY_RECEIVERS = [value]
        else:
            raise Exception("错误的receivers")


    def login(self, sender=None, pw=None):
        if sender:
            self.SENDER = sender
        if pw:
            self.PASSWORD = pw
        
        self._smtp.ehlo()
        self._smtp.login(*self.auth)

    @property
    def content(self):
        msg = MIMEMultipart("related")
        msg["Subject"]  = self.subject
        msg["From"]     = self.sender
        msg["To"]       = ",".join(self.receivers)
        msg["Cc"]       = ",".join(self.copyReceivers)

        mailBody = "<p>Dear:</p>"

        for i in range(len(self._files)):
            mailBody += f"<p><img src='cid:image_{i}'></p>"

        msgText = MIMEText(mailBody, 'html', 'utf-8')
        msg.attach(msgText)  

        for index, file in enumerate(self._files):
            with open(file, "rb") as img:
                msgImage = MIMEImage(img.read())
                msgImage.add_header('Content-ID', f'<image_{index}>')
                msg.attach(msgImage)

        return msg.as_string()

    def run(self):
        self.login()
        content = self.content

        self._smtp.sendmail(self.sender, self.receivers + self.copyReceivers, content)
        self._smtp.quit()


if __name__ == "__main__":
    MyMail("3.jpg").run()


