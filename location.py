#Shreyan Sequeira, 02.03.2024
#MQTT data logger for dog collar project
#The functions regarding connecting to owntracks were created using the assistance of Dr. Stamou's videos and presentation on Aula
#However, I feel as though I have made enough changes to the source code that I feel I can gain credit for it
import paho.mqtt.client as mqtt
from datetime import datetime
import time
#18/03/2024: imported the re library which is needed so as to be able to use regular expressions regarding the battery topic
import re

#this will hold incoming messages
messages = []
'''Callback function that connects the broker
 Upon connection, subscribes to the topic. In this case, as owntracks publishes location data, 
 this what will be obtained from the messages.'''
#08/03/2024: added a connection to the collar/logs topic
def connection(client, userdata, flags, rc):
    if rc == 0:
        client.connected_flag = True
        print("Connected OK Returned code=", rc)
        client.subscribe("owntracks/SS/#")
        client.subscribe("collar/logs")
    else:
        print("Connection Unsuccessful, Error message:", rc)

#18/03/2024: defined extract_battery_info, a function that extracts the section of the data recieved from 
#owntracks that pertains to the battery life of the phone
def extract_battery_info(message):
#these variables define the word to be extracted by the regex and the amount of characters to be extracted after
    word_to_extract = "batt"
    characters_after_word = 4
    
#the regex pattern is constructed and a match is attempted
    pattern = re.compile(r'\b{}\b(.{{0,{}}})'.format(re.escape(word_to_extract), characters_after_word))
    match = pattern.search(message)
    if match:
        extracted_text = match.group(1)
        return extracted_text
    else:
        return None

#08/03/2024: data from the collar/logs topic is now saved to an array
def on_message(client, userdata, msg):
    topic = msg.topic
    try:
        payload = msg.payload.decode("utf8")
        messages.append(msg.payload.decode("utf8"))
#18/03/2024: added a print statement for testing if the data has been properly recieved and appended to the list
#this will likely be removed in the final code
        print(messages)
    except Exception as e:
        print(f"Cannot decode data on topic {topic}: {e}")
    userdata['logs'].append(msg.payload.decode())
    battery_info = extract_battery_info(payload)
    if battery_info:
            print("Battery Info:", battery_info)

def on_disconnect(client, userdata, rc):
    print("Disconnected with result code "+str(rc))


client = mqtt.Client(userdata={'logs': []})
client.on_connect = connection
client.on_message = on_message
client.on_disconnect = on_disconnect

"""18/03/2024: removed the client.username_pw_set because it had no actual 
functionality in the program"""
#client.username_pw_set("SS", "mqttBROKER")
client.connect("broker.hivemq.com", 1883)

#this ensures the code loops forever which is vital for recieving continuous realtime information
client.loop_forever()

