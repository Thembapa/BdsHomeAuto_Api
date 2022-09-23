from twilio.rest import Client 
import bdsconfig
 
account_sid = bdsconfig.account_sid
auth_token = bdsconfig.auth_token
client = Client(account_sid, auth_token) 
 
#send msg 
message = client.messages.create(  
                              messaging_service_sid=bdsconfig.msg_serviceID, 
                              body='Alerm triggered at house 145 Tembisa street',      
                              to='+27742280003' 
                          ) 
 
print(message.sid)