from twilio.rest import Client 
import bdsconfig
#Global Varibales
account_sid = bdsconfig.account_sid
auth_token = bdsconfig.auth_token
client = Client(account_sid, auth_token) 

#send msg 
def sendsms(smsType,body,numbrs):
    if smsType==1:
        for number in numbrs:
            message = client.messages.create(  
                                        messaging_service_sid=bdsconfig.msg_serviceID, 
                                        body=body,      
                                        to=number 
                                    ) 
            #log sms to DB
            print(message.sid)
