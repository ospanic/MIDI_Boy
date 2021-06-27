from machine import Pin, Timer
from time import sleep_ms
import ubluetooth
from esp32 import raw_temperature

class BLE():
  
    def __init__(self, name):
        
        self.name = name
        self.ble = ubluetooth.BLE()
        self.ble.active(True)

        self.led = Pin(14, Pin.OUT)
        self.timer1 = Timer(0)
        self.timer2 = Timer(1)
        
        self.disconnected()
        self.ble.irq(self.ble_irq)
        self.register()
        self.advertiser()
        self.isConnected = False


    def connected(self):
        
        self.timer1.deinit()
        self.timer2.deinit()


    def disconnected(self):
        
        self.timer1.init(period=1000, mode=Timer.PERIODIC, callback=lambda t: self.led(1))
        sleep_ms(200)
        self.timer2.init(period=1000, mode=Timer.PERIODIC, callback=lambda t: self.led(0))
    

    def ble_irq(self, event, data): # 蓝牙事件处理

        if event == 1: # Central disconnected

          self.isConnected = True
          self.connected()
          self.led(1)
        
        elif event == 2: # Central disconnected
            self.isConnected = False
            self.advertiser()
            self.disconnected()
        
        elif event == 4: # New message received
            
            buffer = self.ble.gatts_read(self.midi)
            message = buffer.decode('UTF-8')[:-1]
            print(message)
            
            if received == 'blue_led':
                blue_led.value(not blue_led.value())
                
    def register(self): # 注册MIDI蓝牙服务
      
        MIDI_SERVER_UUID = ubluetooth.UUID('03B80E5A-EDE8-4B33-A751-6CE34EC4C700')
        MIDI_CHAR_UUID   = (ubluetooth.UUID('7772E5DB-3868-4112-A1A9-F2669D106BF3'), 
          ubluetooth.FLAG_READ | ubluetooth.FLAG_WRITE | ubluetooth.FLAG_NOTIFY , )
            
        BLE_MIDI_SERVER = (MIDI_SERVER_UUID, (MIDI_CHAR_UUID , ) , )
        SERVICES = (BLE_MIDI_SERVER, )
        
        ((self.midi,), ) = self.ble.gatts_register_services(SERVICES)


    def send(self, data):

      if self.isConnected :
        self.ble.gatts_notify(0, self.midi, data)


    def advertiser(self): # 设置广播及扫描响应数据
        name = bytes(self.name, 'UTF-8')
        self.ble.gap_advertise(100, adv_data = b'\x02\x01\x05' + bytearray((len(name) + 1, 0x09)) + name ,  
          resp_data = b'\x11\x07\x00\xC7\xC4\x4E\xE3\x6C\x51\xA7\x33\x4B\xE8\xEd\x5A\x0E\xB8\x03')
        
ble = BLE("MIDI_Boy")

k_d6 = Pin(32, Pin.IN, Pin.PULL_UP)
k_b5 = Pin(33, Pin.IN, Pin.PULL_UP)
k_g5 = Pin(25, Pin.IN, Pin.PULL_UP)
k_e5 = Pin(26, Pin.IN, Pin.PULL_UP)
k_c5 = Pin(27, Pin.IN, Pin.PULL_UP)
k_a4 = Pin(12, Pin.IN, Pin.PULL_UP)
k_f4 = Pin(13, Pin.IN, Pin.PULL_UP)
k_d4 = Pin(15, Pin.IN, Pin.PULL_UP)

k_c4 = Pin(4,  Pin.IN, Pin.PULL_UP)

k_e4 = Pin(16, Pin.IN, Pin.PULL_UP)
k_g4 = Pin(17, Pin.IN, Pin.PULL_UP)
k_b4 = Pin(5,  Pin.IN, Pin.PULL_UP)
k_d5 = Pin(18, Pin.IN, Pin.PULL_UP)
k_f5 = Pin(19, Pin.IN, Pin.PULL_UP)
k_a5 = Pin(21, Pin.IN, Pin.PULL_UP)
k_c6 = Pin(22, Pin.IN, Pin.PULL_UP)
k_e6 = Pin(23, Pin.IN, Pin.PULL_UP)

key_pin_list   = [k_c4,k_d4,k_e4,k_f4,k_g4,k_a4,k_b4,k_c5,k_d5,k_e5,k_f5,k_g5,k_a5,k_b5,k_c6,k_d6,k_e6]
key_name_list  = ['k_c4','k_d4','k_e4','k_f4','k_g4','k_a4','k_b4','k_c5','k_d5','k_e5','k_f5','k_g5','k_a5','k_b5','k_c6','k_d6','k_e6']
key_value_last = [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1]
key_value_now  = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]

midi_start = 0x48
midi_inve  = [0,2,4,5,7,9,11,12,14,16,17,19,21,23,24,26,28]
while True :
  
  for i in range(17):
    key_value_now[i] = key_pin_list[i].value()

    if not key_value_last[i] == key_value_now[i] :
      if key_value_now[i] == 0:
        print("on+" + key_name_list[i])
        ble.send(bytearray([0x80, 0x80, 0x90, midi_start + midi_inve[i] , 0x63]))
      else :
        print("off")
        ble.send(bytearray([0x80, 0x80, 0x80, midi_start + midi_inve[i] , 0x00]))
        
      key_value_last[i] = key_value_now[i]
      sleep_ms(10)
  


