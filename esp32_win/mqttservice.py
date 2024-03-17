from umqtt.robust import MQTTClient
import config
import time
import _thread
import json
import state
from machine import Timer


client = MQTTClient(config.mqtt_clientid, config.mqtt_hostname, config.mqtt_port, config.mqtt_username, config.mqtt_password,keepalive=30)
lock=_thread.allocate_lock()


def close_win():
    state.state_ch_win_state(False)
    mqtt_publish()

def sub_cb(topic, msg):
    print(msg.decode("utf8"))
    new_state = json.loads(msg.decode("utf8"))
    print(new_state["items"]["win_state"]["value"])
    state.state_ch_win_state(new_state["items"]["win_state"]["value"])
    if new_state["items"]["openning_time"]["value"] == -1:
        pass
    else:
        Timer(1).deinit()
        timer_1 = Timer(1)
        timer_1.init(mode=Timer.ONE_SHOT, period=1000*10*new_state["items"]["openning_time"]["value"],callback = close_win)
        
    

def mqtt_start():
    client.set_callback(sub_cb)
    client.connect()
    client.subscribe(config.mqtt_subscribe_topic)
    time.sleep(5)
    listen_thread = _thread.start_new_thread(mqtt_listen,())
    #publish_thread = _thread.start_new_thread(mqtt_publish,())

def mqtt_listen():
    count = 0
    while True:
        if lock.acquire():
            count+=1
            try:
                client.check_msg()
            except Exception as e:
                print(e)
            if count==10:
                count=0
                with open("./state.json","r", encoding="utf-8") as file:
                    message = file.read()
                try:
                    client.publish(config.mqtt_publish_topic, message.encode('utf-8'),qos=0)
                except Exception as e:
                    print(e,"失败")
            lock.release()
            time.sleep(1)
    #client.disconnect()
def close_win(timer):
    state.state_ch_win_state(False)
    mqtt_publish()
    Timer(1).deinit()