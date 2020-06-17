from sense_hat import SenseHat
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


# insert Sensor Data in Database
mycursor = mydb.cursor()

for x in range(3,6):
sql = "CREATE TABLE wetterstation%s( id INT , date DATE, time TIME, temperature FLOAT, humidity FLOAT, pressure FLOAT, longitude FLOAT, latitude FLOAT)"%x
mycursor.execute(sql)




