import paho.mqtt.client as mqttclient
import time
import naoqi
from naoqi import ALProxy

broker = "192.168.0.9"
nao_host = "localhost"
nao_port = 9559

tts = ALProxy("ALTextToSpeech", nao_host, nao_port)
motion = ALProxy("ALMotion", nao_host, nao_port)
posture = ALProxy("ALRobotPosture", nao_host, nao_port)


topics = ['POSTURE','SAY','MOTION','NAO']


def extract_ip():
    st = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        st.connect(('10.255.255.255', 1))
        IP = st.getsockname()[0]
    except Exception:
        IP = '127.0.0.1'
    finally:
        st.close()
    return IP




def on_message(client, userdata, message):
    content = str(message.payload.decode("utf-8"))
    topic =  str(message.topic.decode("utf-8"))
    print("message topic=",topic)
    print("message received ", content)

    if (topic == "SAY") :
        global tts
        tts.say(content)

    if (topic == "POSTURE") :
        global posture
        posture.goToPosture(content,1)

    if (topic == "MOTION") :
        global motion
        if (content == "REST") :
            motion.rest()
        if (content == "HEADLEFT") :
            motion.setAngles("HeadYaw",1.0, 0.3)
        if (content == "HEADRIGHT") :
            motion.setAngles("HeadYaw",-1.0, 0.3)
        if (content == "HEADFRONT") :
            motion.setAngles("HeadYaw",0, 0.3)




    if (topic == "NAO") :
        global nao_host, nao_port,tts
        if (content == "BATTERY") :
            battery = ALProxy("ALBattery", nao_host, nao_port)
            batteryLevel = battery.getBatteryCharge()
            tts.say("Mijn batterijniveau is")
            tts.say(str(batteryLevel))
            tts.say("percent")




client=mqttclient.Client("Client1")
client.connect(broker)
client.loop_start() #start the loop

for topic in topics :
    client.subscribe(topic)

client.on_message=on_message #attach function to callback
time.sleep(3600)
client.loop_stop() #stop the loop

