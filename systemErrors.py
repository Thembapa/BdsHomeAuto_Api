""" 
Created BY: Themba Pakula
Date: 20221105
Description: This module will handdle all the syssytem error notifications
"""

import notifications

#This fuction will send the error to the support team 
def sendErroToSupport(Module,Fuction,Error):
    print('====================Support Error start=================================')
    print(Module,Fuction,Error)
    print('====================Support Error end=================================')

#This fuction will send the error to the system user
def sendErroToUser(MaillingList,Module,Fuction,Error):
    print(MaillingList,Module,Fuction,Error)