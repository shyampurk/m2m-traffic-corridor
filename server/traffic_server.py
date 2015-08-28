
#*****************************************************************************************
#			M2M TRAFFIC CORRIDOR FOR EMERGENCY
#*****************************************************************************************

#!usr/bin/python

import os
import sys
from pubnub import Pubnub
from traffic_calc.distance_calculation	import dis_calc
from traffic_calc.bearing import bearng
import math
import time
import random
					# publish and subscribe keys
pubnub = Pubnub(publish_key="demo",       
				subscribe_key="demo")   
g_NAS = int(1)  		# Next Approaching Signal 
g_PASA =str('167')      	# Present Approaching Signal Angle
g_approachingFlag = True	# status flag 
g_count = int(0)		# count variable
g_random1 = random.randrange(2,4,1)	#random number generation
g_random2 = random.randrange(5,7,1)	#random number generation
g_flag  = True	#status flag

								# vehicle starting and destination place names
vehicle_starting_place 	= "UCSF Medical Center at Mount Zion"
vehicle_destination_place = "SF General Hospital"
def main_function(lat,lng):
  	global g_flag,g_PASA,g_NAS,g_count,g_random1,g_random2,g_approachingFlag
	
	L_list1 = ["37.786188 -122.440033","37.787237 -122.431801",
				"37.785359 -122.424704","37.778739 -122.423349",
				"37.776381 -122.419514","37.772811 -122.412835",
		   		"37.765782 -122.407557","37.756809 -122.406781",
				"37.756930 -122.405238"]
	L_signal = ["Divisaderostreet",
				"Websterstreet",
				"Goughstreet",
				"Fultonstreet",
				"Fellstreet",
				"FolsomStreet",
				"sixteenthstreet"]
	if (g_flag == False):
		g_NAS  = int(1)  					# Next Approaching Signal 
		g_PASA =str('167')      			# Present Approaching Signal Angle
		g_approachingFlag = True			# Command flag
		g_count= int(0)						# count variable
		g_random1 = random.randrange(2,4,1) # random number generation 
		g_random2 = random.randrange(5,7,1) # random number generation 
		g_flag = True 						# status flag
			
	parameter_lat1 = float(lat)
	parameter_lng1 = float(lng)
	
	L_lat2 = (L_list1[g_NAS-1][0:9])
	L_lng2 = (L_list1[g_NAS-1][10:21])

	# calculating the distancse between the vehicle and the approaching signal
	L_distance = dis_calc(parameter_lat1,parameter_lng1,L_lat2,L_lng2) 
	
	# calculating the angle between the vehicle and the approaching signal						
	L_bearing  = bearng(parameter_lat1,parameter_lng1,L_lat2,L_lng2)   
	
							
	if (L_bearing >180 and L_bearing <= 360):                           
		L_bearing = str(180-L_bearing)
	L_brng2 = str (L_bearing)
	
	# checking the for the end of the route
	if (g_NAS<=7):	
	
		# condition to check vehicle crossed signal or not

		if((g_PASA[0]) != (L_brng2[0])):	# checking for the signal crossover                                
			if (g_approachingFlag == False): 
				# publishing withdraw signal to the traffic signal
				pubnub.publish(channel ='sub_channel' ,message = "withdraw")
				print "server sent a command to %s signal to set normal flow \n"%(L_signal[g_NAS-1])
				print "Ambulance crossed %s signal \n" %(L_signal[g_NAS-1])  
				if (g_NAS<=6):
					print "Ambulance is approaching %s signal \n" %(L_signal[g_NAS])      
				g_NAS = int(g_NAS+1)	# updating the NAS value
				g_approachingFlag = True			# updating the status flag
		
		#	condition to check vehicle is approaching signal or not
		if (L_distance <=200 and L_distance >=100):	# checking for vehicle distance 
			if (g_approachingFlag == True):
				print "Ambulance is %d meter away from %s signal \n"%(L_distance,L_signal[g_NAS-1])
				if(g_NAS == g_random1 or g_NAS == g_random2):
					if (g_count < 2):
						pubnub.publish(channel='sub_channel' ,message ="red")
						time.sleep(14)
						print "Ambulance halted, at %s after seeing RED signal \n"%(L_signal[g_NAS-1])
						g_count = int(g_count +1)
						time.sleep(4)
						print "Ambulance resumed its journey from %s after seeing GREEN signal\n"%(L_signal[g_NAS-1])

				# publishing the green signal message to traffic signal
				pubnub.publish(channel='sub_channel' ,message ="green")
				print "server sent a command to %s signal to stay GREEN \n"%(L_signal[g_NAS-1])
				time.sleep(1)
				print "%s signal changed to green \n" %(L_signal[g_NAS-1]) 				
				g_PASA = L_brng2	# updating the present approaching signal angle
				g_approachingFlag = False		# upadating the status flag
		
def callback(message,channel):
	global g_flag
	if (message == "start"):
		g_flag = False
		print "connection established between ambulance and the server\n"
		time.sleep(1)
		print "Ambulance started from %s \n"%(vehicle_starting_place)
	elif(message == "stop"):
		print "Ambulance reached the %s \n"%(vehicle_destination_place)
		
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

if __name__ == "__main__":
	pubnub.subscribe(channels='pub_channel', callback=callback, error=callback,
                 connect=connect, reconnect=reconnect, disconnect=disconnect)
