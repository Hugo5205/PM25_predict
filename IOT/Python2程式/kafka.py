import datetime
import serial
import time
import requests, json
import binascii
ser = serial.Serial("/dev/ttyAMA0",baudrate=9600, stopbits=1, parity="N", timeout=2)
n = 2
#topic
pm25="http://192.168.0.111:8083/topics/pm25"
headers = { "Content-Type" : "application/vnd.kafka.json.v2+json" }
id="001"
if __name__ == "__main__":
	try:
	  while True:
	#t=datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
	#if t[14:16] == '00' and t[17:19] =='00':
            ser.flushInput()
            hugo = ser.readline(32)
            print(hugo)
            #s = binascii.b2a_hex(hugo)
            s = bytes(hugo).decode('ascii')
            #s = hugo.decode('utf-8')
            print(s)
            if s[0:2] == "42" and s[2:4]=="4d" and len(s)==64:
              print("Header is correct")
              cs = int(s[60]+s[61]+s[62]+s[63],16)
	#print(cs)
              check = 0
              for i in range(0, len(s)-4, n):
                #print(data[i:i+n])
                check=check+int(s[i:i+n],16)
	    #print(check)
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

                try:
                    t=datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
		    #hour = int(t.split(' ')[1].split(':')[0]) + 9 #next_hour
                    print(t)
                    payload = {"records":[{ "value": {"timestamp":t,"Temperature":str(temperature),"Humidity":str(humidity),"PM2.5":str(pm25_atm) }}]}
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
            #time.sleep(5)
	except KeyboardInterrupt:
    		ser.close()
    		print("Serial port closed")
