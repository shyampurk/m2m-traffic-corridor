#!usr/bin/python

import os
import sys
from pubnub import Pubnub
import dis_cal
import sys
import math
import time
import bearing
import random

pubnub = Pubnub(publish_key="your-publish-key",       # publish and subscribe keys
				subscribe_key="your-subscribe-key")   

g_NAS = int(1)  	# Next Approaching Signal 
g_PASA =str('167')  # Present Approaching Signal Angle
g_cmd = True		# Command flag
g_flag = True       # check flag
g_count = int(0)	# count variable
def main_function(lat,lng):
  global g_flag,g_count,g_NAS,g_PASA,g_cmd
	
	l_list1 = ["37.786188 -122.440033","37.787237 -122.431801","37.785359 -122.424704","37.778739 -122.423349","37.776381 -122.419514","37.772811 -122.412835",
			   "37.765782 -122.407557","37.756809 -122.406781","37.756930 -122.405238"]
	l_signal = ["Divisadero_st","Webster_st","Gough_st","Fulton_st","Fell_st","Folsom_St","sixteenth_st",""]
	if (g_flag == True):
		print "Ambulance started from UCSF MEDICAL CENTER AT MOUNT ZION\n"
		g_flag = False
		
	p_lat1 = float(lat)
	p_lng1 = float(lng)
	
	l_lat2 = (l_list1[g_NAS-1][0:9])
	l_lng2 = (l_list1[g_NAS-1][10:21])
	l_distance = dis_cal.dis_calc(p_lat1,p_lng1,l_lat2,l_lng2)      # calculating the distance between the vehicle and the approaching signal
	l_bearing  = bearing.bearng(p_lat1,p_lng1,l_lat2,l_lng2)        # calculating the angle between the vehicle and the approaching signal
	if (l_bearing >180 and l_bearing <= 360):                           
		l_bearing = str(180-l_bearing)
	l_brng2 = str (l_bearing)
	ran = random.randrange(1,7,1) 
	if (g_NAS<=7):	
	
		if((g_PASA[0]) != (l_brng2[0])):                                
			if (g_cmd == False): 
				pubnub.publish(channel ='pub_channel' ,message = ("NO",g_NAS))
				print "server sent a revert back message to %s signal \n"%(l_signal[g_NAS-1])
				print "Ambulance crossed %s signal \n" %(l_signal[g_NAS-1])  
				if (g_NAS<=7):
					print "Ambulance is approaching %s signal next \n" %(l_signal[g_NAS])      
				g_NAS = int(g_NAS+1)
				g_cmd = True
		
		if (l_distance <=200 and l_distance >=100):
			if (g_cmd == True):
				print "Ambulance is %d meter far from %s signal \n" %(l_distance,l_signal[g_NAS-1])
				
				if(g_NAS == ran):
					if (count <= 2):
						print "Ambulance halted, at %s it has not received the message from server\n"%(l_signal[g_NAS-1])
						time.sleep(10)
						count = int(count +1)
						print "Ambulance resumed from %s  as it received the message from server\n"%(l_signal[g_NAS-1])
				pubnub.publish(channel='pub_channel' ,message =("yes",g_NAS))
				print "server sent a clearance message to %s signal \n"%(l_signal[g_NAS-1])
				print "%s signal changed to green \n" %(l_signal[g_NAS-1]) 				
				g_PASA = l_brng2
				g_cmd = False
	else:
		print "Ambulance reached the hospital"	

def callback(message,channel):
	lat = message['lat']
	lng = message['lon']
	main_function(lat,lng)
	return True

def error(message):
    print("ERROR : " + str(message))

def connect(message):
	print("CONNECTED")
	print "connection established between ambulance and server\n"
	

def reconnect(message):
    print("RECONNECTED")

def disconnect(message):
    print("DISCONNECTED")

pubnub.subscribe(channels='sub_channel', callback=callback, error=callback,
                 connect=connect, reconnect=reconnect, disconnect=disconnect)
