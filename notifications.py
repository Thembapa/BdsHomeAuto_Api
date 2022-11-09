from twilio.rest import Client 
import smtplib, ssl
from email.mime.text import MIMEText
from email.message import EmailMessage
import bdsconfig
#Global Varibales
account_sid = bdsconfig.ACCOUNT_SID
auth_token = bdsconfig.AUTH_TOCKET
client = Client(account_sid, auth_token) 

#send msg to sms list
def sendsms(smsType,body,numbrs):
    if smsType==1:
        for number in numbrs:
            message = client.messages.create(  
                                        messaging_service_sid=bdsconfig.MSG_SERVICE_ID, 
                                        body=body,      
                                        to=number 
                                    ) 
            #log sms to DB
            print(message.sid)

#Send email to a mailing list
def sendmail(usubject, message, emaillist,htmlBody =''):
    
    sender = bdsconfig.EMAIL_USER
    receivers = emaillist
    body_of_email = message
    msg = MIMEText(body_of_email, 'plain')
    # html_body_of_email = '<h1>The html body of the email</h1>'
    # msg = MIMEText(html_body_of_email, 'html')
    msg['Subject'] = usubject
    msg['From'] = sender
    msg['To'] = ','.join(receivers)

    s = smtplib.SMTP_SSL(host = bdsconfig.EMAIL_SERVER, port = 465)
    s.login(user = bdsconfig.EMAIL_USER, password = bdsconfig.EMAIL_PASS)
    s.sendmail(sender, receivers, msg.as_string())
    s.quit()


def sendWelcome_msg(email,tocken):
    msg='''Hi,\n\n
Thank you for signing up with BDS home Auto. Just few more steps and you are done.\n
Please follow the link below to verify your email Address\n
link:https://safety.bdstech.co.za/accountverification/{}\n\n


NB: Your acount will only be active once you email is veryfied. \n
The account will be deleted autmatically should the email not be verified withing 7 days\n\n

Kind Regards 
BDS Team
    '''.format(tocken)
    
    sendmail('Email Verification',msg,email)

