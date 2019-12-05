import smtplib
from email.mime.text import MIMEText
from email.header import Header
from smtplib import SMTP_SSL

from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText


#qq邮箱smtp服务器
host_server = 'smtp.163.com'
#sender_qq为发件人的qq号码
sender_qq = '17625905485@163..com'
#pwd为qq邮箱的授权码
pwd = 'Z470588044l' #
sender_qq_mail = '17625905485@163.com'
receiver = ['17625905485@163.com']

#邮件的正文内容
mail_content = ""
#邮件标题
mail_title = '2019-12-5日武汉晚报'

#邮件正文内容
#msg = MIMEMultipart()
msg = MIMEMultipart('related')
msg["Subject"] = Header(mail_title, 'utf-8')
msg["From"] = sender_qq_mail
msg["To"] = Header("接收者测试", 'utf-8') ## 接收者的别名

msgAlternative = MIMEMultipart('alternative')
msg.attach(msgAlternative)


#邮件正文内容
mail_body = """
 <p>你好，Python 邮件发送测试...</p>
 <p>这是使用python登录qq邮箱发送HTML格式和图片的测试邮件：</p>
 <p><a href='http://www.yiibai.com'>易百教程</a></p>
 <p>图片演示：</p>
 <p>![](cid:send_image)</p>
"""

#msg.attach(MIMEText(mail_body, 'html', 'utf-8'))
msgText = (MIMEText(mail_body, 'html', 'utf-8'))
msgAlternative.attach(msgText)

 
# 指定图片为当前目录
fp = open('my.png', 'rb')
msgImage = MIMEImage(fp.read())
fp.close()
 
# 定义图片 ID，在 HTML 文本中引用
msgImage.add_header('Content-ID', '<send_image>')
msg.attach(msgImage)


#ssl登录
smtp = SMTP_SSL(host_server)
#set_debuglevel()是用来调试的。参数值为1表示开启调试模式，参数值为0关闭调试模式
smtp.set_debuglevel(1)
smtp.ehlo(host_server)
smtp.login(sender_qq, pwd)

smtp.sendmail(sender_qq_mail, receiver, msg.as_string())
smtp.quit()