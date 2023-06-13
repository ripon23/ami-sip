#!/usr/bin/python
import os
import time
from settings import login, connection, Headers
from asterisk.ami import AMIClient
import requests

def api_post(caller_id, callee, uniqueid, status, call_status):
    url = 'https://sip-api.doctime.com.bd/api/calls/audio/validate'
    myobj = {'caller': caller_id, 'connected': callee, 'uniqueid': uniqueid, 'status': status, 'call_status': call_status }
    requests.post(url, json = myobj, headers=Headers)
    print(f"Call {status} - Caller ID: {caller_id}, Callee: {callee}, Uniqueid: {uniqueid}, Status: {status}, Call status: {call_status}")
    return 0

def event_notification(source, event):
    # every call initiate
    if event.name == 'Newchannel':
        
        caller_id = event['CallerIDNum']
        callee = event['Exten']
        uniqueid = event['Uniqueid']
        if callee != 's':            
            api_post(caller_id, callee, uniqueid, 'initiation', '')

    #os.system('notify-send "%s" "%s"' % (event.name, str(event)))

    # every call reception
    if event.name == 'DialEnd':
        caller_id = event['CallerIDNum']
        callee = event['DestCallerIDNum']
        uniqueid = event['Uniqueid']
        call_status = event['DialStatus']         
        api_post(caller_id, callee, uniqueid, 'received', call_status)

    # every call end
    if event.name == 'Hangup':
        
        caller_id = event['CallerIDNum']
        callee = event['Exten']
        uniqueid = event['Uniqueid']
        call_status = event['Cause-txt']
        if callee != 's':    
            api_post(caller_id, callee, uniqueid, 'end', call_status)

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