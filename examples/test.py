import pystrix

def handle_ami_event(event):
    if event.name == 'Newchannel':
        # Extract relevant information from the event, such as caller ID and callee
        caller_id = event.headers['CallerIDNum']
        callee = event.headers['Exten']
        
        # Make your API call using the extracted information
        # ...

# Connect to the Asterisk Manager Interface
ami = pystrix.AMI()
ami.connect('localhost', 'username', 'password')

# Register the event handler
ami.on_event += handle_ami_event

# Start listening for events
ami.start()

# Keep the script running to continue receiving events
while True:
    pass