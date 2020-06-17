from sense_hat import SenseHat, ACTION_PRESSED, ACTION_HELD, ACTION_RELEASED


import mysql.connector
import time as t
import datetime
import sys

# Get Station Name from command line argument
if len(sys.argv)>0:
        stationName = str(sys.argv[1])
else:
        stationName = "lazarus"

print("Station Name is: " + stationName)

sense = SenseHat()
sense.clear()


# Connect to the SQL Server
mydb = mysql.connector.connect(
        host="localhost",
        user="pi",
        passwd="raspberry",
        db="SensorHat"
    )

mycursor = mydb.cursor()

latitude = 0
longitude = 0

print("start messung")
do = True
while do:
        print("next cylce ...")
        temp = sense.temperature
        hum = sense.humidity
        pres = sense.pressure
        date = datetime.datetime.now().date()
        time = t.strftime("%H:%M:%S")
    
        sql = "INSERT INTO `homestation` ( `date`, `time`, `temperature`, `humidity`, `pressure`, `longitude`, `latitude` , `station` ) VALUES ( %s, %s, %s, %s, %s, %s, %s, %s)"
        val = (date, time, temp, hum, pres, 0, 0, stationName)
        
        mycursor.execute(sql, val)
        mydb.commit()
        print("Database update ... done")
        sense.show_message("...")
        t.sleep(120)
