import datetime
import serial
import time
import requests, json
import binascii
#from sklearn.externals import joblib
import joblib
import RPLCD as RPLCD
from RPLCD import CharLCD
import RPi.GPIO as GPIO
lcd=CharLCD(cols=16, rows=2, pin_rs=26, pin_e=19, pins_data=[13, 6, 5 ,11], numbering_mode=GPIO.BCM)
ser = serial.Serial("/dev/ttyAMA0",baudrate=9600, stopbits=1, parity="N", timeout=2)
n = 2
#topic
pm25="http://192.168.0.111:8083/topics/pm25"
headers = { "Content-Type" : "application/vnd.kafka.json.v2+json" }
id="001"
#import warnings

#with warnings.catch_warnings():
      #warnings.simplefilter("ignore", category=UserWarning)
Elastic_Net = joblib.load('/root/hugo/Elastic_Net.pkl')
if __name__ == "__main__":
	#Elastic_Net = joblib.load('./Elastic_Net.pkl')
	try:
	  while True:
            ser.flushInput()
            #hugo = ser.readline(32)
            hugo = ser.read(32)
            #print(hugo)
            s = str(binascii.b2a_hex(hugo))[2:-1]
            #print(s)
            if s[0:2] == "42" and s[2:4]=="4d" and len(s)==64:
              print("Header is correct")
              cs = int(s[60]+s[61]+s[62]+s[63],16)
              check = 0
              for i in range(0, len(s)-4, n):
                check=check+int(s[i:i+n],16)
              if check == cs:
                print("data correct")
		# PM1, PM2.5 and PM10 values for standard particle in ug/m^3
                pm1_hb_std = int(s[8]+s[9],16)
                pm1_lb_std = int(s[10]+s[11],16)
                pm1_std = float(pm1_hb_std * 16 + pm1_lb_std)
                pm25_hb_std = int(s[12]+s[13],16)
                pm25_lb_std = int(s[14]+s[15],16)
                pm25_std = float(pm25_hb_std * 16 + pm25_lb_std)
                pm10_hb_std = int(s[16]+s[17],16)
                pm10_lb_std = int(s[18]+s[19],16)
                pm10_std = float(pm10_hb_std * 16 + pm10_lb_std)
		# PM1, PM2.5 and PM10 values for atmospheric conditions in ug/m^3
                pm1_hb_atm = int(s[20]+s[21],16)
                pm1_lb_atm = int(s[22]+s[23],16)
                pm1_atm = float(pm1_hb_atm * 16 + pm1_lb_atm)
                pm25_hb_atm = int(s[24]+s[25],16)
                pm25_lb_atm = int(s[26]+s[27],16)
                pm25_atm = float(pm25_hb_atm * 16 + pm25_lb_atm)
                pm10_hb_atm = int(s[28]+s[29],16)
                pm10_lb_atm = int(s[30]+s[31],16)
                pm10_atm = float(pm10_hb_atm * 16 + pm10_lb_atm)
		# Number of particles bigger than 0.3 um, 0.5 um, etc. in #/cm^3
                part_03_hb = int(s[32]+s[33],16)
                part_03_lb = int(s[34]+s[35],16)
                part_03 = part_03_hb * 16 + part_03_lb
                part_05_hb = int(s[36]+s[37],16)
                part_05_lb = int(s[38]+s[39],16)
                part_05 = part_05_hb * 16 + part_05_lb
                part_1_hb = int(s[40]+s[41],16)
                part_1_lb = int(s[42]+s[43],16)
                part_1 = part_1_hb * 16 + part_1_lb
                part_25_hb = int(s[44]+s[45],16)
                part_25_lb = int(s[46]+s[47],16)
                part_25 = part_25_hb * 16 + part_25_lb
		#temperature humidity
                temperature = int(s[48]+s[49]+s[50]+s[51],16)/10.
                humidity = int(s[52]+s[53]+s[54]+s[55],16)/10.

                print("Standard particle:")
                print("PM1:",pm1_std, "ug/m^3 PM2.5:", pm25_std, "ug/m^3 PM10:", pm10_std, "ug/m^3")
                print("Atmospheric conditions:")
                print("PM1:", pm1_atm,"ug/m^3 PM2.5:", pm25_atm, "ug/m^3 PM10:",pm10_atm, "ug/m^3")
                print("Number of particles:")
                print(">0.3:", part_03, " >0.5:", part_05, ">1.0:", part_1, " >2.5:", part_25)
		#print(s[48]+s[49],s[50]+s[51])
		#print(s[52]+s[53],s[54]+s[55])
                print("temperature:",temperature,"humidity:",humidity)
                t=datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                hour = int(t.split(' ')[1].split(':')[0]) + 9 #next_hour
                print(t)
                    #print(hour)
                X_test = [[hour, temperature, humidity]]
                print(X_test)
                Elastic_Net_pred = round(Elastic_Net.predict(X_test)[0],2)
                print(Elastic_Net_pred)
                #lcd.clear()
                #time.sleep(1)
                lcd.cursor_pos = (0, 0)
                lcd.write_string("PM2.5:" + str(pm25_atm))
                lcd.cursor_pos = (1, 0)
                lcd.write_string("NextPM2.5:" + str(Elastic_Net_pred))
                try:
                    payload = {"records":[{ "value": {"timestamp":t,"Temperature":str(temperature),"Humidity":str(humidity),"PM2.5":str(pm25_atm),"PM25predict":str(Elastic_Net_pred) }}]}
                    r = requests.post(pm25, data=json.dumps(payload), headers=headers)
               	    if r.status_code != 200:
                        print("Status Code(humd): " + str(r.status_code))
                        print(r.text)
                    else:
                        print("Updated")
                except Exception as ex:
            	    print(ex)
        #else:
                break
                #lcd.clear()
                #GPIO.cleanup()
                #time.sleep(5)
	except KeyboardInterrupt:
    		ser.close()
    		print("Serial port closed")
#GPIO.cleanup()
