# coding: utf8

from sense_hat import SenseHat, ACTION_PRESSED, ACTION_HELD, ACTION_RELEASED
sense = SenseHat()
#import os
import gps
from gps import *
import time as t
import datetime
from signal import pause
import mysql.connector
sys.setrecursionlimit(10000000)

afkmode = 0

idnumber = 1

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


# Verschiedene Zustände (mode)
# start = Ausgangszustand (Wechsel zwischen Temp, Luftdruck, Luftfeuchtigkeit, Periodeneinstellung, Text "Zum Starten Button Drücken"; 
# periode = Messperiode einstellen
# messung = Laufende Messung
mode = "start"


#~~~~~~~ Verschiedene Ausgangszustände (situation) ~~~~~~~
#0.0 = Welcome (Einschalten)
#0.1 = Erklärung
#0.2 = Messperiodenanzeige
#0.3 = Nachricht "Zum Starten und Stoppen der Messung..."
#0.4 = Temperaturanzeige
#0.5 = Luftdruckanzeige
#0.6 = Luftfeuchtigkeitanzeige
#0.7 = Herunterfahren
#-1 = aus
#1.0 = Messung Erklärung
#1.1 = Messung Temperatur
#1.2 = Messung Luftdruck
#1.3 = Messung Luftfeuchtigkeit
situation = 0.0


#Standardmessperiode:
periode = 90

maxMesswerte = 100000

#Zhäler für Messdurchläufe
counter = 1

#Auf Antwort warten?
afk = 0  
messwerte = 0
begin = 0


actualtable = -1


#gpsvariable setzen
gpsd = gps(mode=WATCH_ENABLE)



#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#Funktion zur Anzeige einzelner Zahlen (für Periodeneinstellung)
OFFSET_LEFT = 1
OFFSET_TOP = 2

NUMS =[1,1,1,1,0,1,1,0,1,1,0,1,1,1,1,  # 0
       0,1,0,0,1,0,0,1,0,0,1,0,0,1,0,  # 1
       1,1,1,0,0,1,0,1,0,1,0,0,1,1,1,  # 2
       1,1,1,0,0,1,1,1,1,0,0,1,1,1,1,  # 3
       1,0,0,1,0,1,1,1,1,0,0,1,0,0,1,  # 4
       1,1,1,1,0,0,1,1,1,0,0,1,1,1,1,  # 5
       1,1,1,1,0,0,1,1,1,1,0,1,1,1,1,  # 6
       1,1,1,0,0,1,0,1,0,1,0,0,1,0,0,  # 7
       1,1,1,1,0,1,1,1,1,1,0,1,1,1,1,  # 8
       1,1,1,1,0,1,1,1,1,0,0,1,0,0,1]  # 9

# Displays a single digit (0-9)
def show_digit(val, xd, yd, r, g, b):
  offset = val * 15
  for p in range(offset, offset + 15):
    xt = p % 3
    yt = (p-offset) // 3
    sense.set_pixel(xt+xd, yt+yd, r*NUMS[p], g*NUMS[p], b*NUMS[p])

# Displays a two-digits positive number (0-99)
def show_number(val, r, g, b):
  abs_val = abs(val)
  tens = abs_val // 10
  units = abs_val % 10
  if (abs_val > 9): show_digit(tens, OFFSET_LEFT, OFFSET_TOP, r, g, b)
  show_digit(units, OFFSET_LEFT+4, OFFSET_TOP, r, g, b)


sense.clear()
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

#gps Messung durchführen
def rungps():
  global gpsd
  gpsd.next() #this will continue to loop and grab EACH set of gpsd info to clear the buffer


#Funktionen um Aktuelle Tabelle auszulesen
def getaktuelleTabelle():
    global actualtable
    fileAT = open("/home/pi/SenseHat/AktuelleTabelle.txt", "r")
    actualtable = int(fileAT.read())
    fileAT.close()


def overwriteTabelle():
    global actualtable
    fileAT = open("/home/pi/SenseHat/AktuelleTabelle.txt", "w")
    actualtable = actualtable + 1
    fileAT.write(str(actualtable))
    fileAT.close()






#Nummernanzeige (z.B. Periode)
def displaynumber(inpt):
  global periode
  global mode
  global situation
  global afk
  afk = 1
  show_number(inpt, 255,255,255)

#Ausgangszustandsabfrage
def checksituation():
  global periode
  global mode
  global situation
  print("Situation: " + str(situation))
  print("Mode: " + mode)
  if situation == 0.0:
    #Welcome
    sense.show_message("Herzlich Willkommen", scroll_speed=0.05)
    situation = 0.1
    checksituation()
  elif situation == 0.1:
    #Erklärung
    sense.show_message("Zum Swipen: Button links/rechts. Zur Auswahl: Button mitte", scroll_speed=0.05)
  elif situation == 0.2:
    sense.show_message("Messperiode einstellen (Sekunden)", scroll_speed=0.05)
  elif situation == 0.3:
    sense.show_message("Messung starten", scroll_speed = 0.05)    
  elif situation == 0.4:
    sense.show_message("Aktuelle Temperatur: " + str(round(sense.get_temperature_from_pressure(),2)) + " Grad Celsius", scroll_speed = 0.05)
  elif situation == 0.5:
    sense.show_message("Aktueller Luftdruck: " + str(round(sense.get_pressure(),2)) +" Pa", scroll_speed = 0.05)
  elif situation == 0.6:
    sense.show_message("Aktuelle Luftfeuchtigkeit: " + str(round(sense.get_humidity(),2)) + " g/m3", scroll_speed = 0.05)
  elif situation == 0.7:
    sense.show_message("Zum Ausschalten, Button druecken!", scroll_speed = 0.05)
  elif situation == 1.0:
    sense.show_message("Zum Beenden Button druecken. Angezeige: bisher gesammelte Messwerte. (MAX 99)", scroll_speed = 0.05)


def writedata(idnumb, date, time, temp, hum, pres, long, lat):
  global actualtable
  getaktuelleTabelle()
  wet = "Wetterstation" + str(actualtable)
  sql = "INSERT INTO `" + wet + "` (`id`, `date`, `time`, `temperature`, `humidity`, `pressure`, `longitude`, `latitude` ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"
  val = (idnumb, date, time, temp, hum, pres, long, lat)
  mycursor.execute(sql, val)
  mydb.commit()


def messung():
  global gpsd
  global periode
  global messwerte
  global mode
  global counter
  global afk
  global idnumber
  global latitude
  global longitude
  global situation
  displaynumber(messwerte)
  afk = 1
  rungps()
  selection = False
  events = sense.stick.get_events()
  if mode == "messung":
    for event in events:
      if event.action != "released":
        if event.direction == "middle":
          selection = "mid"
        if selection == "mid":
          mode = "start"
          sense.show_message("Messung beendet! Anzahl gesammelter Messwerte:" + str(messwerte) , scroll_speed = 0.05)
          situation = 0.3
          checksituation()
  if not selection:
    temperature = round(sense.get_temperature_from_pressure(),2)
    pressure = round(sense.get_pressure(),2)
    humidity = round(sense.get_humidity(),2)
    datum = datetime.datetime.now().date()
    time = t.strftime("%H:%M:%S")
    #print("Temperatur: " +str(temperature))
    #print("Druck: " +str(pressure))
    #print("Feuchtigkeit: " + str(humidity))
    #print("Datum: " + str(datum))
    #print("Uhrzeit: " + str(time))
    t.sleep(1)
    if str(gpsd.fix.latitude) != "nan" and gpsd.fix.latitude != 0.0:    
      latitude = gpsd.fix.latitude
      #print("Breitengrad: " + str(latitude))
    if str(gpsd.fix.longitude) != "nan" and gpsd.fix.longitude != 0.0:
      longitude = gpsd.fix.longitude
      #print("Längengrad: " + str(longitude))
    #print("---------------------")
    if counter < periode:
      counter +=1
     # t.sleep(1)
#      print("counter: " + str(counter))
      if messwerte <= maxMesswerte:
        messung()
      else:
        mode = "start"
        sense.show_message("Messung beendet! Anzahl gesammelter Messwerte:" + str(messwerte) , scroll_speed = 0.05)
        situation = 0.3
        checksituation()
    elif counter == periode:
      print("Messwert gespeichert")
      messwerte +=1
      counter = 1
     # t.sleep(1)      
      writedata(idnumber, datum, time, temperature, humidity, pressure, longitude, latitude)
      idnumber += 1
      if messwerte <= maxMesswerte:
        messung()
      else:
        mode = "start"
        sense.show_message("Messung beendet! Anzahl gesammelter Messwerte:" + str(messwerte) , scroll_speed = 0.05)
        situation = 0.3
        checksituation()


#Wenn Button nach oben gedrückt wird
def pushed_up(event):
  global periode
  global mode
  global situation
  global afk
  global afkmode
  if afk != -1:
    if event.action != ACTION_RELEASED:
      if afkmode == 0:
        afk = 1
        if mode == "periode" and periode <=80:
          periode += 10
          displaynumber(periode)
        elif mode == "periode" and periode == 90:
          sense.show_message("Maximale Messperiode = 90 Sekunden", scroll_speed = 0.05)
          displaynumber(periode)

#Wenn Button nach unten gedrückt wird   
def pushed_down(event):
  global periode
  global mode
  global situation
  global afk
  global afkmode 
  if afk != -1:
    if event.action != ACTION_RELEASED:
      if afkmode == 0:
        afk = 1
        if mode == "periode" and periode !=10:
          periode -= 10
          displaynumber(periode)
        elif mode == "periode" and periode == 10:
          sense.show_message("Minimale Messperiode = 10 Sekunden", scroll_speed = 0.05)
          displaynumber(periode)
  

#Wenn Button nach links gedrückt wird
def pushed_left(event):
  global periode
  global mode
  global situation
  global messwerte
  global afk
  global afkmode
  if afk != -1:
    if event.action != ACTION_RELEASED:
      if afkmode == 0:
        afk = 1
        if situation == 0.3:
          situation = 0.2
          checksituation()
        elif situation == 0.4:
          situation = 0.3
          checksituation()
        elif situation == 0.5:
          situation = 0.4
          checksituation()
        elif situation == 0.6:
          situation = 0.5
          checksituation()
        elif situation == 0.7:
          situation = 0.6
          checksituation()  
        elif situation == 0.2:
          situation = 0.7
          checksituation()
        elif situation == 0.1:
          situation = 0.7
          checksituation()

      

#Wenn Button nach rechts gedrückt wird
def pushed_right(event):
  global periode
  global mode
  global situation
  global messwerte
  global afk
  global afkmode
  if afk != -1:
    if event.action != ACTION_RELEASED:
      if afkmode == 0:
        afk = 1
        if situation == 0.1:
          situation = 0.2
          checksituation()
        elif situation == 0.2:
          situation = 0.3
          checksituation()
        elif situation == 0.3:
          situation = 0.4
          checksituation()
        elif situation == 0.4:
          situation = 0.5
          checksituation()
        elif situation == 0.5:
          situation = 0.6
          checksituation()
        elif situation == 0.6:
          situation = 0.7
          checksituation() 
        elif situation == 0.7:
          situation = 0.2
          checksituation()
        elif mode == "messung" and situation != -1 and situation != 1.3:
          situation += 0.1
          checksituation()
        elif mode == "messung" and situation == 1.3:
          situation = 1.0
          checksituation()
        

#Wenn Button gedrückt wird(Mitte)
def pushed_middle(event):
  global afkmode
  print("pushed middle")
  global periode
  global mode
  global situation
  global messwerte
  global afk
  global counter
  global idnumber
  global latitude
  global longitude
  global actualtable
  events = sense.stick.get_events()
  if afk != -1:
    if event.action != ACTION_RELEASED:
      if afkmode == 0:
        afk = 1
        if situation == 0.2:
          situation = -1
          mode = "periode"  
          sense.show_message("Messperiode anpassen: hoch/runter", scroll_speed = 0.05)
          t.sleep(1)
          displaynumber(periode)
        elif mode =="periode":
          sense.show_message("Messung alle " + str(periode) + " Sekunden!", scroll_speed = 0.05)
          mode = "start"
          situation = 0.2
          t.sleep(0.5)
          #checksituation()
        elif situation == 0.3:
          getaktuelleTabelle()
          overwriteTabelle()
          idnumber = 1
          latitude = -1
          longitude = -1
          wet ="Wetterstation" + str(actualtable)
          sql = "CREATE TABLE " + wet + "(id INT AUTO_INCREMENT PRIMARY KEY, date VARCHAR(255), time VARCHAR(255), temperature FLOAT, humidity FLOAT, pressure FLOAT, longitude FLOAT, latitude FLOAT)"
          mycursor.execute(sql)
          mode = "messung"
          print("Messung gestartet")
          sense.show_message("Messung gestartet.", scroll_speed = 0.05)
          counter = 1
          situation = 1.0
          messwerte = 0
          checksituation()
          messung()
        elif situation == 0.1 or situation == 0.4 or situation == 0.5 or situation == 0.6 or situation == 1.0 or situation == 1.1 or situation == 1.2 or situation == 1.3:
          checksituation()  
        elif situation == 0.7:
          from subprocess import call
          sense.show_message("Bye Bye!", scroll_speed = 0.05)
          call("sudo shutdown -h now", shell=True)



#Nichtafk setzen/afk setzen
def notafk():
  global afk
  if mode == "periode" or mode =="messung":
    afk = 1
  else:
    afk = 0
  print("notafk" + str(afk))
  time.sleep(1)



#Wenn afk --> Message von aktuellen Zustand abspielen
def checkafk():
  global afk
  global begin
  global afkmode
  global mode 
#  if mode != "messung":
  print("begin: " + str(begin))
  if afk == 1:
    begin = 0
    t.sleep(1)
    checkafk()
  elif begin <= 7:
    begin +=1
    t.sleep(1)
    checkafk()
  elif begin == 8:
    afkmode = 1
    afk = -1
    begin = 0
    t.sleep(1)
    checksituation()
    time.sleep(2)
    afk = 0
    afkmode = 0
    checkafk()



#MAIN

def checkaction():
  #Auf Button reagieren
  sense.stick.direction_up = pushed_up
  sense.stick.direction_down = pushed_down
  sense.stick.direction_left = pushed_left
  sense.stick.direction_right = pushed_right
  sense.stick.direction_middle = pushed_middle
  sense.stick.direction_any = notafk

#Test-GPS Werte:
rungps()
rungps()
rungps()
rungps()
print("RunGPS durchgeführt")
t.sleep(2)

#Intro Text starten
if situation == 0.0:
  checksituation()
  


checkaction()

#AFK-Endlosschleife einleiten
checkafk()
















