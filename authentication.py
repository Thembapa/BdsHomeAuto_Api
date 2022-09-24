from cryptography.fernet import Fernet


#Generate keys for encryption
def generate_key():
    key = Fernet.generate_key()

    return key

def validate_device():
    device_list= [{'Device_ID':1,'Device_SID':'TZmPErE3koWuArfPPesdOFOHsV_ViTc5V8QVM58NTxs=','DeviceName':'BDS100','Model':'2022','Zone':'Zone1'}
                    ,{'Device_ID':2,'Device_SID':'TZmPErE3koWuArfPPesdOFOHsV_ViTc5V8QVM58NTxs=','DeviceName':'BDS100','Model':'2022','Zone':'Zone2'}  
                    ]