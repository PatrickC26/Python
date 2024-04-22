import platform

fileLocation = ""

if platform.system() == "Linux":
    fileLocation = "/home/pi/Desktop/project/"
elif platform.system() == "Darwin":
    fileLocation = "/Users/slothsmba/Desktop/CGU_project/SmartBox/"


# Use in _2_data.py & _5_log.py & Internet.py


#import webbrowser
#webbrowser.open('https://www.google.com')
#webbrowser.open('https://willy01010.github.io/newwebsite/root/backfence.html')
#webbrowser.open('https://willy01010.github.io/newwebsite/root/back.html')