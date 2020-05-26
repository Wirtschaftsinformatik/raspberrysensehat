from sense_hat import SenseHat
#from sense_hat import SenseHat
import time

class SenseHatExtended(SenseHat):
    sense = SenseHat()

    def __init__(self):
        super().__init__()
        self.sense = SenseHat()

    def printHello(self):
        print("Hello")

    def fillWhite(self):
        white = (255, 255, 255)
        whites = [white for i in range(64)]
        self.sense.set_pixels(whites)
    
    def blinkCol(self,color,rounds, delay):
        fills = [color for i in range(64)]       
        for i in range(rounds):
            self.sense.set_pixels(fills)
            time.sleep(delay)
            self.sense.clear()
            time.sleep(delay)
            
    def blink(self, color, rounds):
        fill = (color, color, color)
        fills = [fill for i in range(64)]

        for i in range(rounds):
            self.sense.set_pixels(fills)
            time.sleep(0.5)
            self.sense.clear()
            time.sleep(0.5)

    def blinkWhite(self):
        self.blink(255, 3)