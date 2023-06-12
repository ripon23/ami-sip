#!/usr/bin/python
import os
import time
from settings import login, connection, Headers
from asterisk.ami import AMIClient
import requests

def event_notification(source, event):
    
    if event.name == 'Newchannel':
        
        #print(event)
        caller_id = event['CallerIDNum']
        callee = event['Exten']
        uniqueid = event['Uniqueid']
        if callee != 's':
            print("Caller: " , caller_id)
            print("Callee: " , callee)
            print("Uniqueid:", uniqueid)                        

            url = 'https://sip-api.doctime.com.bd/api/calls/audio/validate'
            myobj = {'caller': caller_id, 'connected': callee, 'uniqueid': uniqueid}

            requests.post(url, json = myobj, headers=Headers)

            #print(x.text)

    #os.system('notify-send "%s" "%s"' % (event.name, str(event)))

client = AMIClient(**connection)
future = client.login(**login)
if future.response.is_error():
    print(" === Error === ", str(future.response))
    #raise Exception(str(future.response))

client.add_event_listener(event_notification)

try:
    while True:
        time.sleep(10)
except (KeyboardInterrupt, SystemExit):
    client.logoff()
