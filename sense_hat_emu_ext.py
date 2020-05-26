from sense_emu_extended import SenseHatExtended

sense = SenseHatExtended()

sense.printHello()
print("###")
sense.fillWhite()
print("### BLINK")
sense.blink(125, 3)
print("### BLINKWHITE")
sense.blinkWhite()

print("### BLINK COLOR ###")
sense.blinkCol((255,0,0),5,0.2)
print("### BLINK COLOR ###")
sense.blinkCol((0,255,0),5,0.2)
print("### BLINK COLOR ###")
sense.blinkCol((0,0,255),5,0.2)

sense.show_message("Hello")