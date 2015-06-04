
import smtplib
from email.mime.text import MIMEText


def send_email(to, from_, subject, body):
    msg = MIMEText(body)
    msg['Subject']    = subject
    msg['From']       = from_
    msg['To']         = to
    msg['Body']       = body
    msg['Precedence'] = 'bulk'
    msg['Auto-Submitted'] = 'auto-generated'
    s = smtplib.SMTP('localhost')
    s.sendmail(msg['From'], msg['To'], msg.as_string())
    s.quit()


        
