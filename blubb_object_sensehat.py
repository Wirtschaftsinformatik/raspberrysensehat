from sense_hat import SenseHat
import time

"""
  Sense HAT Sensors Objekt Spielerein
"""

# Wir inititialisieren das SenseHat Objekt "sense", 
# um auf alle Sensoren und das Display zugreifen zu können


sense = SenseHat()

# Um einen Wert auszulesen, genügt es das "sense" Objekt
# mit dem passenden Selector anzusprechen, hier ".pressure"
# Wir speichern den Luftdruckwert in der Variable "pressure"
pressure = sense.pressure

# Diesen können wir auch ausgeben, über die Standardausgabe (Bildschirm)
print(pressure)

# Objekte haben Methoden, so hat unser SenseHat eine Methode "show_message"
# Die Methode "show_message" wird ähnlich wie ein Selector angesprochen
# Eine Methode ist nichts anderes als eine Funktion, die zu einem Objekt gehört

# Wir übergeben der Methode "show_message" eine Textvariable "myText", 
# die aus unsereer Variable "pressure" und einem String besteht. Die Methode wird dann
# den Inhalt der Variable "myText" als Lauftext auf dem Display anzeigen.
# Wir nutzen eine globale Funktion str() um eine numerische Variable "pressure" in einen 
# String (also Text) umzuwandeln

myText = "Luftdruck: " + str(pressure)
#sense.show_message(myText)

#################################################################################################
#################################################################################################

# Jetzt schreiben wir unsere erste Klasse "Blubb"
# alle Objekte der Klasse "Blubb" können nichts anderes als Blubb... machen
# außerdem haben die Objekte der Klasse "Blubb" einen Namen, der aber immer auf Blubb 
# endet. Und jedes Blubb Objekt hat einen Glückslevel
# Eine weitere Methode der Klasse Blubb ist die Möglichkeit, 
# ein Objekt der Klasse "Blubb" nach seinem Namen zu fragen "wieHeisstDu"

#### START Klassendefinition für Blubb ####

class Blubb:
  # Das ist eine Standardmethode, die beim Erzeugen
  # des Objekts automatisch durchgeführt wird, hier wird der
  # Name des Blubbs festgelegt
  def __init__(self, name):
    self.name = name
    print("Objekt " + name + " Blubb wurde erzeugt")
    self.glueckslevel = 128
    #Glueckswert als Farbe anzeigen -> siehe def setColor() weiter unten
    self.setColor()
  
  # Die Methode zum Blubb machen ...
  def machBlubb(self):
    print("blubb...")
    
  # Eine Methode zur Abfrage des Namens des Blubbs
  def wieHeisstDu(self):
    print("Ich heiße " + self.name + " Blubb")
    
  def streicheln(self):
    print("Meaooowww")
    self.glueckslevel = self.glueckslevel + 5
    # Farben gehen nur bis 255, deswegen ist da auch mit dem
    # Glück schluss
    if self.glueckslevel > 255:
      self.glueckslevel = 255
    self.setColor()
    time.sleep(0.2)
  
  def aergern(self):
    print("Grrrrr")
    self.glueckslevel = self.glueckslevel - 10
    # Farben gehen nur bis 255, deswegen ist da auch mit dem
    # Glück schluss
    if self.glueckslevel < 0:
      self.glueckslevel = 0
    self.setColor()
    time.sleep(0.2)
  
  def wieGehtsDir(self):
    print(self.glueckslevel)

  #Eine eigen Methode um die Farbe anhand des Glueckslevels zu setzen
  def setColor(self):
    # wenig glück -> viel rot, glöück -> viel grün
    color = ((255-self.glueckslevel), self.glueckslevel, 0)
    # 64 mal die farbe weiderholen in einer Liste
    display = [color] * 64
    sense.set_pixels(display)
    
#### ENDE Klassendefinition für Blubb ####


# Nachdem die Klasse deklariert wurde, können wir einzelne Objekte
# der Klasse "Blubb" erzeugen, das nennt man instanziieren, da wir eine
# Instanz der Klasse erzeugen, das geschieht ähnlich zu Deklaration von Variablen:
myBlubb1 = Blubb("Ernst")


# Nun können wir die Objekte ansprechen und deren Methoden nutzen
myBlubb1.machBlubb()
myBlubb1.wieHeisstDu()

# Jetzt rägern wir unseren Blubb mal ordentlich
myBlubb1.aergern()
myBlubb1.aergern()

myBlubb1.aergern()
myBlubb1.aergern()
myBlubb1.aergern()
myBlubb1.aergern()
myBlubb1.aergern()
myBlubb1.aergern()
myBlubb1.aergern()
myBlubb1.aergern()
myBlubb1.aergern()
myBlubb1.aergern()
myBlubb1.wieGehtsDir()
input("Taste drücken...")
# Und jetzt machen wir alles wieder gut ...
# gaaanz viel streicheln

myBlubb1.streicheln()
myBlubb1.streicheln()
myBlubb1.streicheln()
myBlubb1.streicheln()
myBlubb1.streicheln()
myBlubb1.streicheln()
myBlubb1.streicheln()
myBlubb1.streicheln()
myBlubb1.streicheln()
myBlubb1.streicheln()
myBlubb1.streicheln()
myBlubb1.streicheln()
myBlubb1.streicheln()
myBlubb1.streicheln()
myBlubb1.streicheln()
myBlubb1.streicheln()
myBlubb1.streicheln()
myBlubb1.streicheln()
myBlubb1.streicheln()
myBlubb1.streicheln()
myBlubb1.streicheln()
myBlubb1.streicheln()
myBlubb1.streicheln()

myBlubb1.streicheln()
myBlubb1.wieGehtsDir()


  
# Start der endlosschleife -> unser blubb lebt ...
# Wenn wir den joystick nach oben drücken -> streicheln
# wenn wir den joystick nach untern drücken -> ärgern
while True:
      for event in sense.stick.get_events():
          print('You pressed ', event.direction, event.action)
          if event.direction == 'up' and event.action == 'pressed':
              myBlubb1.streicheln()
          elif event.direction == 'down' and event.action == 'pressed':
              myBlubb1.aergern()
          elif event.direction == 'middle' and event.action == 'pressed':
              sense.show_message(str(myBlubb1.glueckslev
                                     el))
              
# Hausaufgabe:
# Fügen Sie weitere Events hinzu -> rechts, links 
