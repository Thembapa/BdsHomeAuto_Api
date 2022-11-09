""" 
Created By:Themba Pakula
Date Created: 2022/11/04
Description: This mudule will be used to manage create user account and midify the accounts. 
"""
import homeautodata
import authentication
import notifications
import systemErrors

#This fuctuion will be used to create a user acount and send a verification email to the user
def createAccout(Email,password,usertypeid):
    Created= False
    try:
        
        UserID = homeautodata.pgsql_get_scalar('homeauto','fn_Create_Account',{'_usertypeid':usertypeid,'_password':password,'_email':Email})        
        VefificationCode = authentication.generate_key().decode()
        print('VefificationCode: ',VefificationCode)
        verificatinID = homeautodata.pgsql_get_scalar('homeauto','fn_accoungverification_add',{'_UserID':UserID,'_VerificationCode':VefificationCode})
                
        if verificatinID>0:
            msg='Account create: ' + VefificationCode
            notifications.sendWelcome_msg(Email,VefificationCode)
        else:
            msg= '''Hi, \n \n
                    
We ran into some problem while creating your accout.\n
Please try again or contact our support team on support@bdstech.co.za\n\n

We applogies for the inconvinience, your business is valueble to us.\n\n

Kind Regards\n
BDS Team '''

            notifications.sendmail('Error Acount creation',msg,Email)
        Created = True
    except Exception as ex:
        systemErrors.sendErroToSupport('UserAccounts','createAccout',ex)
    
    return Created

#User Account Varification
def accountverification(verificationcode):
    Isvalid= False
    try:
        Isvalid = homeautodata.pgsql_get_scalar('homeauto','fn_validateemail',{'_verificationcode':verificationcode})
    except Exception as ex:
        systemErrors.sendErroToSupport('UserAccounts','accountverification',ex)
    return Isvalid
