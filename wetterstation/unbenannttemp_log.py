from sense_hat import SenseHat, ACTION_PRESSED, ACTION_HELD, ACTION_RELEASED


import mysql.connector
import time as t
import datetime


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

while true:
        print("next cylce ...")
        temp = sense.temperature
        hum = sense.humidity
        pres = sense.pressure
        date = datetime.datetime.now().date()
        time = t.strftime("%H:%M:%S")
    
        sql = "INSERT INTO `homestation` ( `date`, `time`, `temperature`, `humidity`, `pressure`, `longitude`, `latitude` ) VALUES ( %s, %s, %s, %s, %s, %s, %s)"
        val = (date, time, temp, hum, pres, 0, 0)
        
        mycursor.execute(sql, val)
        mydb.commit()
        print("Database update ... done")
        sense.show_message("...")
        sleep(90)
