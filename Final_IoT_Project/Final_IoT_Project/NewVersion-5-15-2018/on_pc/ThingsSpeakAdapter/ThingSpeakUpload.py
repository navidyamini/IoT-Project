import requests
import json
import paho.mqtt.publish as publish
import time

class ThingSpeak(object):

    def __init__(self,url):
        self.url = url
        self.THINGSPEAK_HOST = ""
        self.ACCESS_TOKEN = ""
        self.channelID = ""
        self.tTransport = ""
        self.tPort = 0
        self.mqttHost = ""

    def setThingSpeakVariables(self):
        try:
            respond = requests.get(self.url)
        except:
            print "ThingSpeak: ERROR IN CONNECTING TO THE SERVER FOR READING THINGSPEAKCONNECTIONINFO.JSON"
            return
        json_format = json.loads(respond.text)
        self.THINGSPEAK_HOST = json_format["thingspeak"]["THINGSPEAK_HOST"]
        self.ACCESS_TOKEN = json_format["thingspeak"]["ACCESS_TOKEN"]
        self.channelID = json_format["thingspeak"]["channelID"]
        self.tTransport = json_format["thingspeak"]["tTransport"]
        self.tPort = int(json_format["thingspeak"]["tPort"])
        self.mqttHost =json_format["thingspeak"]["mqttHost"]
        # Create the topic string
        self.topic = "channels/" + self.channelID + "/publish/" + self.ACCESS_TOKEN
        print "ThingSpesk: THINGSPEAK VARIABLES ARE READY"
        return

    def sending_dht_data(self,meesage):
        temperature = meesage["temperature"]
        humidity= meesage["humidity"]

        print "From thingspeak"
        print 'Temp: {0:0.1f} C  Humidity: {1:0.1f} %'.format(temperature, humidity)

        # build the payload string
        payload = "&field1=" + str(temperature) + "&field2=" + str(humidity)

        # attempt to publish this data to the topic
        try:
            publish.single(self.topic, payload, hostname = self.mqttHost, transport = self.tTransport, port = self.tPort)
            #time.sleep(10)
        except:
            print("ThingSpeak: ERROR IN PUBLISHING THE HUM AND TEMP TO THINGSPEAK")
        #time.sleep(10)
        return

    def number_of_people(self,meesage):

        result = meesage["bluetooth counter"]
        print result
        #time.sleep(10)
        # build the payload string
        payload = "&field3=" + str(result)
        # attempt to publish this data to the topic
        try:
            publish.single(self.topic, payload, hostname = self.mqttHost, transport = self.tTransport, port = self.tPort)
        except:
            print("ThingSpeak: ERROR IN PUBLISHING THE NUMBER OF PEOPLE TO THINGSPEAK.")
        return

    def ac_status(self,order):
        status = order["Status"]
        if(status == "It is ON"):
            result =1
        if(status == "It is OFF"):
            result =0
        # build the payload string
        self.setThingSpeakVariables()
        payload = "&field4=" + str(result)
        # attempt to publish this data to the topic
        try:
            publish.single(self.topic, payload, hostname=self.mqttHost, transport=self.tTransport, port=self.tPort)
        except:
            print("ThingSpeak: ERROR IN PUBLISHING THE AIR CONDITION STATUS TO THINGSPEAK")
        return

if __name__ == '__main__':

    thingspeak = ThingSpeak()
    while True:
        thingspeak.setThingSpeakVariables()
        thingspeak.sending_dht_data()
        time.sleep(40)
        thingspeak.number_of_people()
        time.sleep(20)