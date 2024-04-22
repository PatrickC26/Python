import paho.mqtt.client as mqtt
import time

import dataprocess
import data
import log

mqtt_broker_ip = "10.42.0.1"


def on_connect(client, userdata, flags, rc):
    print("Connected!", str(rc))
    client.subscribe("#")


def on_message(client, userdata, msg):
    try:
        inSB = msg.payload  # Get everything in
        inS = inSB.decode("utf-8")

        if msg.topic == 'A':
            if ('g' in inS) | ('a' in inS) :
                return
            data.timeModule().setBox1Time()

        elif msg.topic == 'B':
            if 's' in inS:
                return
            data.timeModule().setBox2Time()

        elif msg.topic == 'C':
            if 'm' in inS:
                return
            data.timeModule().setBox3Time()

        if "%" in inS:
            dataprocess.dataprocess(msg.topic, inS)
        elif "@" in inS:
            data.version().setVersion(msg.topic, inS[1:])

        print("Topic: ", msg.topic + "\tMessage: " + inS)  # Print out every message come in
    except Exception as e:
        log.addError(e)


client = mqtt.Client()


def init():
    try:
        print("Starting MQTT Service")
        client.on_connect = on_connect
        client.on_message = on_message
        client.connect(mqtt_broker_ip, 1883)
        log.addlog("MQTT Service Initial Successfull")
    except Exception as e:
        log.addError(e)


sendRequestMsgValue = ""
sendRequestinfoValue = ""
sendRequestServoValue = 0
sendRequestMotorValue = 0

time_millis = 0
time_collect = 0


def sendRequest():
    try:
        client.subscribe("abc")

        global sendRequestMsgValue
        global sendRequestServoValue
        global sendRequestMotorValue
        global sendRequestinfoValue

        global time_millis
        global time_collect

        if (time.time() - time_millis) > 0.1:
            time_millis = int(time.time())
            time_collect = time_collect + 1
            time_collect_max = 100
            if time_collect > time_collect_max:
                time_collect = 0
            
            motor = data.Box_3().getMotor()
            if not (sendRequestMotorValue == motor):
                # print("HERE")
                client.publish("C", 'm' + str(motor) + "%")
                time.sleep(0.01)
                client.publish("C", 'm' + str(motor) + "%")
                log.addlog("[Control] Box3 motor value sent, current data is : " + str(motor))
                sendRequestMotorValue = motor
            elif time_collect >= time_collect_max:
                log.addlog("[Control] Box3 motor value REsent, current data is : " + str(motor))
                client.publish("C", 'm' + str(motor) + "%")

            servo = data.Box_2().getServo()
            if not (sendRequestServoValue == servo):
                client.publish("B", 's' + str(servo) + "%")
                time.sleep(0.01)
                client.publish("B", 's' + str(servo) + "%")
                log.addlog("[Control] Box2 Servo value sent, current data is : " + str(servo))
                sendRequestServoValue = servo
            elif time_collect >= time_collect_max:
                log.addlog("[Control] Box2 Servo value REsent, current data is : " + str(servo))
                client.publish("B", 's' + str(servo) + "%")

            msg = data.Box_1().getMSG()
            if not (sendRequestMsgValue == msg):
                client.publish("A", 'g' + msg + "%")
                time.sleep(0.01)
                client.publish("A", 'g' + msg + "%")
                log.addlog("[Control] Box1 msg value sent, current is : " + msg)
                sendRequestMsgValue = msg
            elif time_collect >= time_collect_max:
                log.addlog("[Control] Box1 msg value REsent, current is : " + msg)
                client.publish("A", 'g' + msg + "%")

            info = data.Box_1().getRFIDinfo()
            if not (sendRequestinfoValue == info):
                client.publish("A", 'a' + info + "%")
                time.sleep(0.01)
                client.publish("A", 'a' + info + "%")
                log.addlog("[Control] Box1 RFID info value sent, current is : " + info)
                sendRequestinfoValue = info
            elif time_collect >= time_collect_max:
                log.addlog("[Control] Box1 RFID info value REsent, current is : " + info)
                client.publish("A", 'a' + info + "%")


            client.subscribe("#")
            time.sleep(0.01)

        else:
            time.sleep(0.1)
    except Exception as e:
        log.addError(e)



