""" 
Created BY: Themba Pakula
Date Created: 20221105
Description: This modeule is resposible for granting users access to the system.
"""

from cryptography.fernet import Fernet
import homeautodata
import systemErrors

#Generate keys for encryption
def generate_key():
    key = Fernet.generate_key()

    return key

def validate_device():
    device_list= [{'Device_ID':1,'Device_SID':'TZmPErE3koWuArfPPesdOFOHsV_ViTc5V8QVM58NTxs=','DeviceName':'BDS100','Model':'2022','Zone':'Zone1'}
                    ,{'Device_ID':2,'Device_SID':'TZmPErE3koWuArfPPesdOFOHsV_ViTc5V8QVM58NTxs=','DeviceName':'BDS100','Model':'2022','Zone':'Zone2'}  
                    ]

#Check if the SID is valid and active in the database
def validate_SID(SID):
    IsValid:bool
    IsValid = False
    try:
        IsValid = homeautodata.pgsql_get_scalar('homeauto','fn_validate_SID',{'_SID':SID})       
    except Exception as ex:
        systemErrors.sendErroToSupport('authentication','validate_SID',ex)

    return IsValid

#Data Encryption
def encryptData(SID,Data):
    key = str(SID).encode()
    f_obj= Fernet(key)
    Data = str(Data).encode()
    enc_msg= f_obj.encrypt(Data)
    return enc_msg.decode()

#DataDescryption
def decryptData(SID,Data):
    key = str(SID).encode()
    f_obj= Fernet(key)
    Data = str(Data).encode()
    enc_msg= f_obj.decrypt(Data)
    return enc_msg.decode()
