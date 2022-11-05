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
        verificatinID = homeautodata.pgsql_get_scalar('homeauto','fn_accoungverification_add',{'_UserID':UserID,'_VerificationCode':VefificationCode})
        if verificatinID>0:
            msg='Account create: ' + VefificationCode
            notifications.sendWelcome_msg(Email,VefificationCode)
        else:
            msg= 'Error Genarating verification code, try again latter'
            notifications.sendemail(Email,msg)
        Created = True
    except Exception as ex:
        systemErrors.sendErroToSupport('UserAccounts','createAccout',ex)
    
    return Created

