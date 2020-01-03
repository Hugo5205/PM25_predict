
import serial
from time import sleep
from sklearn.externals import joblib

ser = serial.Serial("/dev/ttyAMA0",baudrate=9600, stopbits=1, parity="N", timeout=2)
n = 2
Elastic_Net = joblib.load('./Elastic_Net.pkl')
try:
    while True:
        ser.flushInput()
        hugo = ser.readline(32)
	s = hugo.encode('hex')
        #print(s)
        sleep(1)
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
		temperature_hb = int(s[48]+s[49],16)
                temperature_lb = int(s[50]+s[51],16)
                temperature = float(temperature_hb * 16 + temperature_lb)
		temp_test = int(s[48]+s[49]+s[50]+s[51],16)
		humidity_hb = int(s[52]+s[53],16)
                humidity_lb = int(s[54]+s[55],16)
                humidity = float(humidity_hb * 16 + humidity_lb)

		print("Standard particle:")
		print("PM1:",pm1_std, "ug/m^3 PM2.5:", pm25_std, "ug/m^3 PM10:", pm10_std, "ug/m^3") 
                print("Atmospheric conditions:")
		print("PM1:", pm1_atm,"ug/m^3 PM2.5:", pm25_atm, "ug/m^3 PM10:",pm10_atm, "ug/m^3")
 		print("Number of particles:")
                print(">0.3:", part_03, " >0.5:", part_05, ">1.0:", part_1, " >2.5:", part_25)
		#print(s[48]+s[49],s[50]+s[51])
		#print(s[52]+s[53],s[54]+s[55])
		print("temperature:",temperature/10,"humidity:",humidity/10)
		print("temp_test",temp_test/10.)
		t=datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                hour = int(t.split(' ')[1].split(':')[0]) + 9 #next_hour
		
		#X_test = [[hour, temperature/10, humidity/10]]
		#Elastic_Net_pred = Elastic_Net.predict(X_test)
		#print(Elastic_Net_pred)
		sleep(5)
except KeyboardInterrupt:
    ser.close()
    print("Serial port closed")
