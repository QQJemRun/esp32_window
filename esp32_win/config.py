import json

wifi_ssid          ="颦儿的 Mi 11"
wifi_password      ="QQ715640167"

longitude     = 116.39
latitude      = 39.90
base_url      = "https://api.caiyunapp.com/v2.6/fuwhPNzXsYXIvMya/"
url           = base_url+str(longitude)+","+str(latitude)+"/realtime"

mqtt_clientid = "ikl8SEBFw6a.esp32_dev|securemode=2,signmethod=hmacsha256,timestamp=1709755694733|"
mqtt_username = "esp32_dev&ikl8SEBFw6a"
mqtt_password = "983317b9fb90945c034e5fa58fdddc35916f4aa2bbdb7fd0507e7dfaa29be4f9"
mqtt_hostname = "iot-06z00a6l3gle6wu.mqtt.iothub.aliyuncs.com"
mqtt_port     = 1883
mqtt_subscribe_topic = "/sys/ikl8SEBFw6a/esp32_dev/thing/service/property/set"
mqtt_publish_topic   = "/sys/ikl8SEBFw6a/esp32_dev/thing/event/property/post"


def load_config():
    global config_dict
    with open("./config.json", "r", encoding="utf-8") as file:
        config_dict = json.load(file)
        try:
            global wifi_ssid,wifi_password,base_url,url,mqtt_clientid,mqtt_username,mqtt_password,mqtt_hostname,longitude,latitude,mqtt_port,mqtt_subscribe_topic,mqtt_publish_topic
            wifi_ssid = config_dict["wifi_ssid"]
            wifi_password = config_dict["wifi_password"]
            longitude = config_dict["longitude"]
            latitude = config_dict["latitude"]
            base_url = config_dict["base_url"]
            url = base_url+str(longitude)+","+str(latitude)+"/realtime"
            mqtt_clientid = config_dict["mqtt_clientid"]
            mqtt_username = config_dict["mqtt_username"]
            mqtt_password = config_dict["mqtt_password"]
            mqtt_hostname = config_dict["mqtt_hostname"]
            mqtt_port = config_dict["mqtt_port"]
            mqtt_subscribe_topic = config_dict["mqtt_subscribe_topic"]
            mqtt_publish_topic   = config_dict["mqtt_publish_topic"]


        except Exception as e:
            print(e)



def save_config():
    with open("./config.json", "w", encoding="utf-8") as file:
        json.dump({
                   "wifi_ssid":wifi_ssid,
                   "wifi_password":wifi_password,
                   "base_url":base_url,
                   "url":url,
                   "longitude":longitude,
                   "latitude":latitude,
                   "mqtt_clientid":mqtt_clientid,
                   "mqtt_username":mqtt_username,
                   "mqtt_password":mqtt_password,
                   "mqtt_hostname":mqtt_hostname,
                   "mqtt_port":mqtt_port,
                   "mqtt_subscribe_topic":mqtt_subscribe_topic,
                   "mqtt_publish_topic":mqtt_publish_topic,
                   }, 
                        file
                   )


def set_location(longitude_now,latitude_now):
    global longitude,latitude,url
    longitude = longitude_now
    latitude = latitude_now
    print("设置经纬度：",'(',longitude,"，",latitude,')')
    url = base_url+str(longitude)+","+str(latitude)+"/realtime"

def set_wifi(ssid:str,password:str):
    global wifi_ssid,latitude,url
    wifi_ssid = ssid
    wifi_password = password

def set_mqtt(clientid:str,username:str,password:str,hostname:str,port:int,subscribe_topic:str,publish_topic:str):
    global mqtt_clientid, mqtt_username,mqtt_password,mqtt_hostname,mqtt_port,mqtt_publish_topic,mqtt_subscribe_topic
    
    mqtt_clientid = clientid
    mqtt_username = username
    mqtt_password = password
    mqtt_hostname = hostname
    mqtt_port     = port

    mqtt_publish_topic = publish_topic
    mqtt_subscribe_topic = subscribe_topic


