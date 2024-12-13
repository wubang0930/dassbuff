from email.mime.text import MIMEText
from email.header import Header
import smtplib




def notify_email(msg, has_notified):
    # 通知一次就可以，如果已经通知过了，则打印日志，并返回
    # 设置一个全局变量，记录是否已经通知过
    if has_notified:
        print("已经通知过了")
        return

    print("通知管理员："+msg)

    # 邮件服务器配置
    smtp_server = "smtp.qq.com" 
    smtp_port = 587
    sender = "524925243@qq.com"
    password = "prtckhscqlftbhjh"
    receiver = "bangwu1992@qq.com"

    # 创建邮件内容
    message = MIMEText(msg, 'plain', 'utf-8')
    message['From'] = Header(sender)
    message['To'] = Header(receiver)
    message['Subject'] = Header('系统通知-fb_异常')

    try:
        # 连接SMTP服务器
        smtp_obj = smtplib.SMTP(smtp_server, smtp_port)
        smtp_obj.starttls()
        smtp_obj.login(sender, password)
        
        # 发送邮件
        smtp_obj.sendmail(sender, [receiver], message.as_string())
        print("邮件发送成功")
        # 关闭连接
        smtp_obj.quit()
        # 标记通知过
    except Exception as e:
        print("邮件发送失败:", str(e))