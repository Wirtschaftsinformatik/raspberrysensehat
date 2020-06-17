from sense_hat import SenseHat, ACTION_PRESSED, ACTION_HELD, ACTION_RELEASED
import time
import mysql.connector

# Connect to the SQL Server
mydb = mysql.connector.connect(
        host="localhost",
        user="pi",
        passwd="raspberry",
        db="SensorHat"
    )
print(mydb)

sense = SenseHat()
sense.clear()

# get Sensor Data
pressure = sense.get_pressure()
temp = sense.get_temperature_from_humidity()
hum = sense.get_humidity()

# get GeoData

longitude = 52.999999 # muss aus GPS Donkel ausgelesen werden
latitude  = 10.99999 # same 

# print / check Data
print(pressure)
print(temp)
print(hum)

# insert Sensor Data in Database
mycursor = mydb.cursor()

sql = "INSERT INTO `SensorData` (`temp`, `air_pressure`, `air_humidity`, `longitude`, `latitude` ) VALUES (%s, %s, %s, %s, %s)"
val = (temp, pressure, hum, longitude, latitude)
mycursor.execute(sql, val)
mydb.commit()
print(mycursor.rowcount, "record inserted.")

#Button steuern
sense.stick.direction_any = do_thing
def do_thing(event):
    if event_action == 'pressed':
        trypi.py

# The END
myText = "Ready!"
sense.show_message(myText)

