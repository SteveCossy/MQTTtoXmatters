# Subscribe to a Mosquitto broker, and send messages to an xMatters integration
# Steve Cosgrove 20 August 2018, mqtt@rata.co.nz
# originally based on http://www.steves-internet-guide.com/python-mqtt-publish-subscribe/

import time, requests
import paho.mqtt.client as paho

from pathlib import Path
# from https://stackoverflow.com/questions/4028904/how-to-get-the-home-directory-in-python

confpath = str(Path.home())
confxmatters=confpath+'/xmatters.conf'

# Get the URL for xMatters POST
fileContent	= open(confxmatters,'r')
comment		= fileContent.readline()
base_URL	= fileContent.readline()
endpoint_URL	= fileContent.readline()
configuration	= fileContent.readline()
broker		= fileContent.readline()
topic		= fileContent.readline()

base_URL	= base_URL.rstrip('\n')
endpoint_URL	= endpoint_URL.rstrip('\n')
configuration	= configuration.rstrip('\n')
broker		= broker.rstrip('\n')
topic		= topic.rstrip('\n')

def xmattersEvent(url, subject, message):
	data = {
	  "properties": {
	    "subject": subject,
	    "message": message
	  }
	}
	response = requests.post(url, json=data)
	print( 'Return Code: ' + str(response.status_code) + ' at '+ time.ctime(time.time()) )

#define callback
def on_message(client, userdata, message):
	time.sleep(1)
#	print("received message =",str(message.payload.decode("utf-8")))
	urlFull = base_URL + endpoint_URL + configuration
	xmattersEvent(urlFull, topic, str(message.payload.decode("utf-8")))

client= paho.Client("client-001") #create client object 

######Bind function to callback
client.on_message=on_message
#####
print("connecting to broker ",broker + ' at '+ time.ctime(time.time()))
client.connect(broker)#connect
client.loop_start() #start loop to process received messages
print("subscribing ")
client.subscribe(topic)#subscribe

# Initialise timing variables
timedata = time.time()
Run_flag=True
while Run_flag:
	try:
		time.sleep(1)
	except KeyboardInterrupt:
		Run_flag=False

client.disconnect() #disconnect
client.loop_stop() #stop loop


