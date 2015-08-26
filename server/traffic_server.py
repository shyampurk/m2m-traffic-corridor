#!usr/bin/python

import os
import sys
from pubnub import Pubnub
import distance_calculation
import math
import time
import bearing
import random

pubnub = Pubnub(publish_key="demo",       # publish and subscribe keys
		subscribe_key="demo")   
g_NAS = int(1)  	# Next Approaching Signal 
g_PASA =str('167')      # Present Approaching Signal Angle
g_cmd = True		# Command flag
g_count = int(0)	# count variable
g_ran1 = random.randrange(2,4,1)
g_ran2 = random.randrange(5,7,1)
g_flag  = True
def main_function(lat,lng):
  	global g_flag,g_PASA,g_NAS,g_count,g_ran1,g_ran2,g_cmd
	
	l_list1 = ["37.786188 -122.440033","37.787237 -122.431801","37.785359 -122.424704","37.778739 -122.423349","37.776381 -122.419514","37.772811 -122.412835",
		   "37.765782 -122.407557","37.756809 -122.406781","37.756930 -122.405238"]
	l_signal = ["Divisaderostreet","Websterstreet","Goughstreet","Fultonstreet","Fellstreet","FolsomStreet","sixteenthstreet"]
	if (g_flag == False):
		g_NAS = int(1)  	# Next Approaching Signal 
		g_PASA =str('167')      # Present Approaching Signal Angle
		g_cmd = True		# Command flag
		g_count = int(0)	# count variable
		g_ran1 = random.randrange(2,4,1)
		g_ran2 = random.randrange(5,7,1)
		g_flag  = True
		
	p_lat1 = float(lat)
	p_lng1 = float(lng)
	
	l_lat2 = (l_list1[g_NAS-1][0:9])
	l_lng2 = (l_list1[g_NAS-1][10:21])
	l_distance = distance_calculation.dis_calc(p_lat1,p_lng1,l_lat2,l_lng2) # calculating the distance between the vehicle and the approaching signal
	l_bearing  = bearing.bearng(p_lat1,p_lng1,l_lat2,l_lng2)   # calculating the angle between the vehicle and the approaching signal
	if (l_bearing >180 and l_bearing <= 360):                           
		l_bearing = str(180-l_bearing)
	l_brng2 = str (l_bearing)
	
	
	if (g_NAS<=7):	
	
		if((g_PASA[0]) != (l_brng2[0])):                                
			if (g_cmd == False): 
				pubnub.publish(channel ='sub_channel' ,message = ("withdraw",g_NAS))
				print "server sent a command to %s signal to set ordinary flow \n"%(l_signal[g_NAS-1])
				print "Ambulance crossed %s signal \n" %(l_signal[g_NAS-1])  
				if (g_NAS<=6):
					print "Ambulance is approaching %s signal \n" %(l_signal[g_NAS])      
				g_NAS = int(g_NAS+1)
				g_cmd = True
		
		if (l_distance <=200 and l_distance >=100):
			if (g_cmd == True):
				print "Ambulance is %d meter away from %s signal \n" %(l_distance,l_signal[g_NAS-1])
				if(g_NAS == g_ran1 or g_NAS == g_ran2):
					if (g_count <= 2):
						pubnub.publish(channel='sub_channel' ,message =("red",g_NAS))
						time.sleep(15)
						print "Ambulance halted, at %s after seeing RED signal \n"%(l_signal[g_NAS-1])
						g_count = int(g_count +1)
						time.sleep(3)
						print "Ambulance resumed its journey from %s after seeing GREEN signal\n"%(l_signal[g_NAS-1])
				pubnub.publish(channel='sub_channel' ,message =("green",g_NAS))
				print "server sent a command to %s signal to set GREEN \n"%(l_signal[g_NAS-1])
				time.sleep(1)
				print "%s signal changed to green \n" %(l_signal[g_NAS-1]) 				
				g_PASA = l_brng2
				g_cmd = False
		
def callback(message,channel):
	global g_flag
	if (message == "start"):
		g_flag = False
		print "connection established between ambulance and the server\n"
		time.sleep(1)
		print "Ambulance started from UCSF Medical Center at Mount Zion\n"
	elif(message == "stop"):
		print "Ambulance reached the SF General Hospital"
	else:
		lat = message['lat']
		lng = message['lon']
		main_function(lat,lng)
	return True

def error(message):
    print("ERROR : " + str(message))

def connect(message):
	print("CONNECTED")
	
def reconnect(message):
    print("RECONNECTED")

def disconnect(message):
    print("DISCONNECTED")

pubnub.subscribe(channels='pub_channel', callback=callback, error=callback,
                 connect=connect, reconnect=reconnect, disconnect=disconnect)
