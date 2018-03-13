TRIGGER = 40 #the pin the board is connected to

from tkinter import *
from tkinter.font import Font
from threading import Thread


try:
    import RPi.GPIO as GPIO
    setupGPIO = True
except:
    print ("Not running on a raspberry pi. GPIO controls not available")
    setupGPIO = False

if setupGPIO:
    GPIO.setmode(GPIO.BOARD)
    GPIO.setup(TRIGGER, GPIO.IN)

class scan_for_input(Thread):
    def __init__(self, ammoVar, ammoCount):
        Thread.__init__(self)
        self.ammoVar = ammoVar
        self.ammoCount = ammoCount


    def scanner(self):
        global ammoCount
        preventShooting = False;
        while True:
            if GPIO.input(TRIGGER) == 1:
                if preventShooting == False:
                    decrement_after_keypress()
            else:
                preventShooting = False           #lets counter reset after 0 because user let go
            time.sleep(10)                        #sets rate of fire
            if ammoCount == 0:                    #if ammo empty, stop decrement
                preventShooting = True


def close(event):
    sys.exit();

def reload(event):
    global ammoVar
    global ammoCount

    ammountCount = 36
    ammoVar.set(ammountCount)

def decrement_after_keypress(event):
    global ammoCount
    global ammoVar

    if ammoCount == 0:
        ammoCount = 36
    else:
        ammoCount=ammoCount-1

    ammoVar.set(ammoCount)


root = Tk()

ammoCount = 36
ammoVar = StringVar ()
ammoVar.set(ammoCount)
root.attributes('-fullscreen',True)
#ammoFont = Font(family = "Arame", size = root.winfo_height() - 1)
ammoFont = Font(family = "Arame", size = (root.winfo_screenheight() - 50))
#ammoFont = Font(family = "Arame", size = 239)


Label(root, bg = "#02262d", fg = "#2DFCFB", font = ammoFont, textvariable=ammoVar).pack(fill="none", expand=True)

root.configure(background='#02262d')
root.bind("<Key>", decrement_after_keypress)
root.bind("<Button-1>", reload)
root.bind("<Escape>", close)

input_scan = scan_for_input(ammoVar, ammoCount)
input_scan_thead = Thread(target=input_scan.scanner)

root.mainloop()


#pudb
