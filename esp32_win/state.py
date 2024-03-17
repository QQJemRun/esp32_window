import json
import time
from ST7735 import TFT
from sysfont import sysfont
from machine import SPI,Pin,PWM,ADC
from dht import DHT11
import gc


spi = SPI(2, baudrate=20000000, polarity=0, phase=0, sck=Pin(18), mosi=Pin(5), miso=Pin(13))
tft=TFT(spi,16,17,4)
tft.initr()
tft.rgb(True)
height = 10

adc_boom=ADC(Pin(34,Pin.IN))
adc_co=ADC(Pin(35,Pin.IN))
adc_boom.atten(ADC.ATTN_11DB)
adc_co.atten(ADC.ATTN_11DB)

dht_temp_humi = DHT11(Pin(23))

rudder_1 = PWM(Pin(12))
rudder_1.freq(50)
rudder_2 = PWM(Pin(14))
rudder_2.freq(50)

rudder_1.duty(200)
rudder_2.duty(200)

aqi_in_the_room={}

def state_ch_aqi_out(aqi_out_of_door:str):
    with open("./state.json","r", encoding="utf-8") as file:
        state_dict = json.load(file)
        state_dict["params"]["aqi_out_of_door"] = aqi_out_of_door
    with open("./state.json","w", encoding="utf-8") as file:
        json.dump(state_dict, file)

def state_ch_aqi_in(aqi_in_the_room:str):
    with open("./state.json","r", encoding="utf-8") as file:
        state_dict = json.load(file)
        state_dict["params"]["aqi_in_the_room"] = aqi_in_the_room
    with open("./state.json","w", encoding="utf-8") as file:
        json.dump(state_dict, file)
def state_ch_win_state(win_state:bool):
    if win_state:
        rudder_1.duty(int(1.5/20*1023))
        rudder_2.duty(int(1.5/20*1023))
    else:
        rudder_1.duty(int(0.5/20*1023))
        rudder_2.duty(int(0.5/20*1023))
    with open("./state.json","r", encoding="utf-8") as file:
        state_dict = json.load(file)
        state_dict["params"]["win_state"] = win_state
    with open("./state.json","w", encoding="utf-8") as file:
        json.dump(state_dict, file)

def get_temp_and_humi():
    global height
    try:
        dht_temp_humi.measure()
        aqi_in_the_room["temp"] = dht_temp_humi.temperature()
        tft.text((0, height), "temp:"+str(aqi_in_the_room["temp"])+"*C", TFT.PURPLE, sysfont)
        height += sysfont["Height"] * 2
        aqi_in_the_room["humi"] = dht_temp_humi.humidity()
        tft.text((0, height), "humi:"+str(aqi_in_the_room["humi"])+"%", TFT.PURPLE, sysfont)
        height += sysfont["Height"] * 2
        print("temp:",dht_temp_humi.temperature(),'°C')
        print("humi:",dht_temp_humi.humidity(),'%')
    except Exception as e:
        print(e)
    
def get_aqi_in_room():
    global height
    try:
        aqi_in_the_room["boom"] = adc_boom.read()/4095*3.3
        print(aqi_in_the_room["boom"])
        print(type(aqi_in_the_room["boom"]))
        print(aqi_in_the_room["boom"]>2.0)
        if aqi_in_the_room["boom"]>2.0:
            gc.collect()
            print(gc.mem_free())
            import umail
            smtp = umail.SMTP('smtp.qq.com', 465,ssl=True) 
            smtp.login('715640167@qq.com', 'tihpmboxgjdabbdg')    #xxxx为授权码
            smtp.to('715640167@qq.com')
            smtp.write("From: Win <715640167@qq.com>\n")
            smtp.write("To: Master <715640167@qq.com>\n")
            smtp.write("Subject: Warnning\n\n")
            smtp.write("可燃气体浓度超标，警惕爆炸.\n")
            smtp.write("请及时处理（2分钟后自动开窗）.\n")
            smtp.write("...\n")
            smtp.send()
            smtp.quit()
        print("boom:"+str('%.2f'%(+aqi_in_the_room["boom"])))
        tft.text((0, height), "boom:"+str('%.2f'%(+aqi_in_the_room["boom"])), TFT.PURPLE, sysfont)
        height += sysfont["Height"] * 2
    except Exception as e:
        print("get_aqi_in_room_1",e)
    try:
        aqi_in_the_room["CO"] = adc_co.read()/4095*3.3
        if aqi_in_the_room["CO"]>2.0:
            gc.collect()
            import umail
            smtp = umail.SMTP('smtp.qq.com', 465,ssl=True) 
            smtp.login('715640167@qq.com', 'tihpmboxgjdabbdg')    #xxxx为授权码
            smtp.to('71640167@qq.com')
            smtp.write("From: Win <715640167@qq.com>\n")
            smtp.write("To: Master <715640167@qq.com>\n")
            smtp.write("Subject: Warnning\n\n")
            smtp.write("CO浓度超标，警惕中毒.\n")
            smtp.write("请及时打开窗户（2分钟后自动开开窗通风）\n")
            smtp.write("...\n")
            smtp.send()
            smtp.quit()

        print("CO:"+str('%.2f'%(+aqi_in_the_room["CO"])))
        tft.text((0, height), "CO:"+str('%.2f'%(+aqi_in_the_room["CO"])), TFT.PURPLE, sysfont)
        height += sysfont["Height"] * 2
    except Exception as e:
        print("get_aqi_in_room_2",e)

def get_aqi_out_of_room():
    gc.collect()
    import urequests
    import config
    res = urequests.get(config.url)
    res.encoding = "utf-8"
    aqi = res.json()['result']['realtime']['air_quality']
    aqi['aqi'] = aqi['aqi']['chn']
    aqi['description'] = aqi['description']['chn']
    state_ch_aqi_out(json.dumps(aqi))

def state_check():
    global angle_1,angle_2,height
    tft.fill(TFT.BLACK)
    get_temp_and_humi()
    get_aqi_in_room()
    height = 10
    state_ch_aqi_in(json.dumps(aqi_in_the_room))
    #rudder_1.duty(int((0.5+angle_1/90)/20*1023))          # set duty cycle
    #angle_1=(angle_1 + 45)%225
    #rudder_2.duty(int((0.5+angle_2/90)/20*1023))          # set duty cycle
    #angle_2=(angle_2 + 45)%225
    
    time.sleep(3)

state_check()

