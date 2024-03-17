import time
import network
import config
import state
import mqttservice
import gc


def wifi_connect():
    from machine import Pin
    wlan=network.WLAN(network.STA_IF)
    wlan.active(False)
    wlan.active(True)
    start_time=time.time()
    led1=Pin(22,Pin.OUT)
    if not wlan.isconnected():
        print("connecting to network…")
        wlan.connect(config.wifi_ssid,config.wifi_password)
        while not wlan.isconnected():
            led1.value(1)
            time.sleep_ms(300)
            led1.value(0)
            time.sleep_ms(500)
            if time.time()-start_time>30:
                print("WiFi Connect TimeOut!")
                break
    if wlan.isconnected():
        led1.value(1)
        print("network information:",wlan.ifconfig())

def get_poem():
    import urequests
    BASE_URL = "https://v1.jinrishici.com/all.json"
    res = urequests.get(BASE_URL)
    poem = res.json()['content']
    print(poem)


config.load_config()

wifi_connect()
gc.collect()
print(gc.mem_free())
mqttservice.mqtt_start()

config.save_config()

while True:
    state.state_check()
    gc.collect()
    print(gc.mem_free())
    time.sleep(5)

#time.sleep(1000)