""" 
Created By:Themba Pakula
Description: This api will be used by the Home Auto web and Mobile app to talk to the DB
"""

import json
import os
from flask import Flask, render_template, session, redirect, request, send_from_directory, url_for
import bdsconfig
import random
from datetime import datetime
import homeautodata
import notifications
import authentication
import UserAccount
import systemErrors

#Application variables 
app = Flask(__name__, static_url_path='')
app.secret_key = "bdsHomeAuto"
 


@app.route('/device_status')
def device_status():
    req = request.get_json()
    db_status={'LED2':req.get('LED2')}
    print(req)
    
    
    return json.dumps(db_status)

@app.route('/zone_alert')
def zone_alert():
    req = request.get_json()
    OTP = random.randint(1000, 9999)
    zone_id = req.get('ZoneID')
    fn_parameters={'_zoneid':zone_id,'_otp':OTP,'_generateddate':datetime.now()}
    AlertID= homeautodata.pgsql_get_scalar('homeauto','fn_alert_log',fn_parameters)
    zone_details= homeautodata.pgsql_call_Tablefunction_P('homeauto','fn_get_zone',{'_ZoneID':int(zone_id)})[0]
    #send SMS
    body= 'Alert! {} at {} has been triggered, please follow the link to deactivate https://safety.bdstech.co.za/{}. OTP: {}'.format(zone_details[1],zone_details[2],AlertID,OTP)
    numbrs=['+27742280003','+27738195149']
    notifications.sendsms(1,body,numbrs)
    
    resp = {'AlertID':AlertID}
    print(resp)    
    
    return json.dumps(resp)


@app.route('/alert_status')
def alert_status():
    req = request.get_json()
    AlertID = req.get('AlertID')
    fn_parameters={'_AlertID':AlertID}
    Status_check= homeautodata.pgsql_call_Tablefunction_P('homeauto','fn_alert_checkStatus',fn_parameters)[0]
    if int(Status_check[7])>2:
        api_alert_deactivate(AlertID, 1)
        Status_check= homeautodata.pgsql_call_Tablefunction_P('homeauto','fn_alert_checkStatus',fn_parameters)[0]
    
    resp = {'IsDeactivated':Status_check[8],'OTP': Status_check[4],'Zone':Status_check[9]}
    print(resp)    
    
    return json.dumps(resp)



@app.route('/alert_deactivate', methods=['GET', 'POST'])
def alert_deactivate():
    req = request.get_json()
    AlertID = req.get('AlertID')
    UserID = req.get('UserID')
    api_alert_deactivate(AlertID, UserID)

    fn_parameters={'_AlertID':AlertID}
    Status_check= homeautodata.pgsql_call_Tablefunction_P('homeauto','fn_alert_checkStatus',fn_parameters)[0]

    resp = {'IsDeactivated':Status_check[8],'OTP': Status_check[4],'Zone':Status_check[9]}
    print(resp)    
    
    return json.dumps(resp)

#In API fuction
def api_alert_deactivate(alertid, userid):
    req = request.get_json()
    AlertID = req.get('AlertID')
    fn_parameters={'_AlertID':AlertID,'_UserID':userid}
    DeactivatedID = homeautodata.pgsql_call_Tablefunction_P('homeauto','fn_alert_Deactivate',fn_parameters)
    print(DeactivatedID)

#Create Account
@app.route('/createAccount', methods=['GET', 'POST'])
def createAccount():
    try:
        req = request.get_json()
        CreateStatus={'SID':'','Status':0,'StatusDescription':'Account creation failed'}#0: Account creation failed, 1:Account created ,2:Invalid SID
        RequestSID = req.get('SID')
        CreateStatus['SID']=RequestSID
        if (authentication.validate_SID(RequestSID)):
            req_Data = req.get('Data')
            Email = authentication.decryptData(RequestSID,req_Data.get('Email'))
            password= authentication.decryptData(RequestSID,req_Data.get('Password'))
            password = authentication.encryptData(bdsconfig.HOME_AUTO_API_SID,password) #encrypt with api key
            AccountType = req_Data.get('AccountType')
            if (UserAccount.createAccout(Email,password,AccountType)):                
                CreateStatus['Status']=1
                CreateStatus['StatusDescription']= 'Account created '
                
        else:
            CreateStatus['Status']=2
            CreateStatus['StatusDescription']= 'Invalid SID'
            
    except Exception as ex:
        systemErrors.sendErroToSupport('homeautoapi','createAccount',ex)
        return json.dumps({'Error':str(ex)})
        
    return json.dumps(CreateStatus)

#Verify email Addresss
@app.route('/emailverification', methods=['GET', 'POST'])
def emailverification():
    try:
        req = request.get_json()       
        Verification_status={'SID':'','IsValidated': False}
        RequestSID = req.get('SID')
        Verification_status['SID']=RequestSID
        if (authentication.validate_SID(RequestSID)):
            req_Data = req.get('Data')
            VerificationCode = req_Data.get('VerificationCode')
          
            if (UserAccount.accountverification(VerificationCode)):                
                Verification_status['IsValidated']=True
                
    except Exception as ex:
        systemErrors.sendErroToSupport('homeautoapi','createAccount',ex)
        return json.dumps({'Error':str(ex)})
        
    return json.dumps(Verification_status)
    

@app.route('/')
@app.route('/index')
def index():
   return  'Where do you think you are going?'

if __name__ == "__main__":
    # from waitress import serve
    # serve(app, host="192.168.178.1", port=8080)
    app.run(host="192.168.8.5", port=8080)