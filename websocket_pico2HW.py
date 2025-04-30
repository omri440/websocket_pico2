import machine
import network
from microdot import Microdot, send_file
from microdot.websocket import with_websocket
import gc
import uasyncio as asyncio
import json
import time
from machine import Pin
from machine import ADC

# Replace with your Wi-Fi credentials
ssid = 'wifi-name'
password = 'password'
adc = ADC(4)  # channel 4 = internal temperature sensor
ledGreen = machine.Pin(15,Pin.OUT)
ledRed = machine.Pin(14,Pin.OUT)
conversion_factor = 3.3 / 65535

alarm_enabled = True
pir_triggered = False
pir = Pin(13, Pin.IN)

def connect_to_wifi():
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    
    if not wlan.isconnected():
        print('Connecting to network...')
        wlan.connect(ssid, password)

        timeout = 10  # seconds
        start = time.time()
        while not wlan.isconnected():
            if time.time() - start > timeout:
                print('Connection timeout')
                return
            time.sleep(1)
    
    print('Connected! IP address:', wlan.ifconfig()[0])

connect_to_wifi()
ledGreen.value(1)
ledRed.value(1)
print("Checking PIR sensor responsiveness...")
for i in range(10):
    if pir.value() == 1:
        print("✅ PIR is working – motion detected!")
        break
    time.sleep(0.5)
else:
    print("⚠️ PIR did not detect motion in initial check.")

app = Microdot()

adc = machine.ADC(4)



@app.route('/')

async def index(req):
    return send_file('index.html')


@app.route('control')
@with_websocket


async def controlPanel(request, ws):
    while True:
        try:
            # 🟢 קבלת פקודה מהלקוח (אם קיימת)
            message = await asyncio.wait_for(ws.receive(), timeout=1.0)
            if message:
                data = json.loads(message)
                if 'ledRed' in data:
                    ledRed.value(data['ledRed'])
                if 'ledGreen' in data:
                    ledGreen.value(data['ledGreen'])

        except asyncio.TimeoutError:
            pass

        used_memory = gc.mem_alloc() / 1024
        free_memory = gc.mem_free() / 1024
        total_memory = round(free_memory + used_memory, 2)

        sensor_value = adc.read_u16() * conversion_factor
        temperature = 27 - (sensor_value - 0.706) / 0.001721

        memory_data = {
            'used_memory': round(used_memory, 2),
            'free_memory': round(free_memory, 2),
            'total_memory': total_memory,
            'temperature': round(temperature, 2)
        }

        json_data = json.dumps(memory_data)
        await ws.send(json_data)

        await asyncio.sleep(1)  #
        
    
@app.route('alarm')
@with_websocket
async def alarm_ws(request, ws):
    global alarm_enabled
    while True:
        try:
            msg = await asyncio.wait_for(ws.receive(), timeout=0.1)
            if msg:
                data = json.loads(msg)
                if 'alarm' in data:
                    alarm_enabled = bool(data['alarm'])

        except asyncio.TimeoutError:
            pass

        if alarm_enabled and pir.value() == 1:
            if not pir_triggered:
                pir_triggered = True
                await ws.send(json.dumps({'event': 'motion_detected'}))
        else:
            pir_triggered = False

        await asyncio.sleep(0.1)


app.run(debug=True,port=80)






