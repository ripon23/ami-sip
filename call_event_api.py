#!/usr/bin/python
import os
import time
from settings import login, connection

from asterisk.ami import AMIClient

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

    #os.system('notify-send "%s" "%s"' % (event.name, str(event)))

client = AMIClient(**connection)
future = client.login(**login)
if future.response.is_error():
    print(str(future.response))
    #raise Exception(str(future.response))

client.add_event_listener(event_notification)

try:
    while True:
        time.sleep(10)
except (KeyboardInterrupt, SystemExit):
    client.logoff()
