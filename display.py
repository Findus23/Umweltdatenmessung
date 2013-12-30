#!/usr/bin/python
# -*- coding: utf-8 -*-
# Originales Programm von http://www.schnatterente.net/technik/raspberry-pi-32-zeichen-hitachi-hd44780-display
# von mir modifiziert (Anzeige ausgelagert, ergänzt, um Text aus einer Datei anzuzeigen)
import time
import RPi.GPIO as GPIO

# Zuordnung der GPIO Pins (ggf. anpassen)
DISPLAY_RS = 7
DISPLAY_E  = 8
DISPLAY_DATA4 = 25 
DISPLAY_DATA5 = 24
DISPLAY_DATA6 = 23
DISPLAY_DATA7 = 18




DISPLAY_WIDTH = 16 	# Zeichen je Zeile
DISPLAY_LINE_1 = 0x80 	# Adresse der ersten Display Zeile
DISPLAY_LINE_2 = 0xC0 	# Adresse der zweiten Display Zeile
DISPLAY_CHR = True
DISPLAY_CMD = False
E_PULSE = 0.00005
E_DELAY = 0.00005


def anzeige(): # Anzeige auslagern, um es wiederholt anzuzeigen
	lcd_byte(DISPLAY_LINE_1, DISPLAY_CMD)
	lcd_string(oben)
	lcd_byte(DISPLAY_LINE_2, DISPLAY_CMD)
	lcd_string(unten)

def main():
	GPIO.setmode(GPIO.BCM)
	GPIO.setup(DISPLAY_E, GPIO.OUT)
	GPIO.setup(DISPLAY_RS, GPIO.OUT)
	GPIO.setup(DISPLAY_DATA4, GPIO.OUT)
	GPIO.setup(DISPLAY_DATA5, GPIO.OUT)
	GPIO.setup(DISPLAY_DATA6, GPIO.OUT)
	GPIO.setup(DISPLAY_DATA7, GPIO.OUT)
	display_init()

#	GPIO.cleanup()





def display_init():
	lcd_byte(0x33,DISPLAY_CMD)
	lcd_byte(0x32,DISPLAY_CMD)
	lcd_byte(0x28,DISPLAY_CMD)
	lcd_byte(0x0C,DISPLAY_CMD)  
	lcd_byte(0x06,DISPLAY_CMD)
	lcd_byte(0x01,DISPLAY_CMD)  

def lcd_string(message):
	message = message.ljust(DISPLAY_WIDTH," ")  
	for i in range(DISPLAY_WIDTH):
	  lcd_byte(ord(message[i]),DISPLAY_CHR)

def lcd_byte(bits, mode):
	GPIO.output(DISPLAY_RS, mode)
	GPIO.output(DISPLAY_DATA4, False)
	GPIO.output(DISPLAY_DATA5, False)
	GPIO.output(DISPLAY_DATA6, False)
	GPIO.output(DISPLAY_DATA7, False)
	if bits&0x10==0x10:
	  GPIO.output(DISPLAY_DATA4, True)
	if bits&0x20==0x20:
	  GPIO.output(DISPLAY_DATA5, True)
	if bits&0x40==0x40:
	  GPIO.output(DISPLAY_DATA6, True)
	if bits&0x80==0x80:
	  GPIO.output(DISPLAY_DATA7, True)
	time.sleep(E_DELAY)    
	GPIO.output(DISPLAY_E, True)  
	time.sleep(E_PULSE)
	GPIO.output(DISPLAY_E, False)  
	time.sleep(E_DELAY)      
	GPIO.output(DISPLAY_DATA4, False)
	GPIO.output(DISPLAY_DATA5, False)
	GPIO.output(DISPLAY_DATA6, False)
	GPIO.output(DISPLAY_DATA7, False)
	if bits&0x01==0x01:
	  GPIO.output(DISPLAY_DATA4, True)
	if bits&0x02==0x02:
	  GPIO.output(DISPLAY_DATA5, True)
	if bits&0x04==0x04:
	  GPIO.output(DISPLAY_DATA6, True)
	if bits&0x08==0x08:
	  GPIO.output(DISPLAY_DATA7, True)
	time.sleep(E_DELAY)    
	GPIO.output(DISPLAY_E, True)  
	time.sleep(E_PULSE)
	GPIO.output(DISPLAY_E, False)  
	time.sleep(E_DELAY)   

#Beginn der Ergaenzung
main() # Initialisierung
Seiten = 4 # hier kann man die Anzahl der Seiten ändern
while True: # endlos wiederholen
	Seite = 1 # von Vorne zu zählen beginnen
	while Seite <= Seiten: # so lange durchlaufen bis man bei der letzten Seite angekommen ist -> dann von vorne beginnen
		zeile1 = (Seite * 2) - 2 # Die obere Zeile ist das Doppelte der Seiten anzahl - 2 (!!! Array fängt bei 0 zu zählen an !!!)
		zeile2 = (Seite * 2) - 1 # Die untere Zeile ist das Doppelte der Seiten anzahl - 1 (!!! Array fängt bei 0 zu zählen an !!!)
		datei = open("text.txt", "r") # Datei text.txt zum Lesen oeffnen
		inhalt = datei.readlines() # alle Zeile lesen und in Array "inhalt" speichern
		datei.close() # Datei schliessen
		oben = inhalt[zeile1] # die Richtigen Zeilen aus dem Array speichern
		unten = inhalt[zeile2] # die Richtigen Zeilen aus dem Array speichern
		oben = oben[:-1] # Steuerzeichen am Ende loeschen (erzeugt ein komisches Symbol (|n) am Display)
		unten = unten[:-1] # Steuerzeichen am Ende loeschen
		anzeige() # oben und unten anzeigen
		time.sleep(2) # 2 Sekunden warten
		Seite += 1 # Seite um 1 erhöhen
