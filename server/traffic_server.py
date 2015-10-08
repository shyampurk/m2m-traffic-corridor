#*****************************************************************************************
#			Smart Traffic Management System for Emergency Services
#*****************************************************************************************

#!usr/bin/python
import os
import sys
from pubnub import Pubnub
from traffic_calc.distance_calculation	import dis_calc
from traffic_calc.bearing import bearng
import time

# publish and subscribe keys

pubnub = Pubnub(publish_key="pub-c-f94f01bd-5e0f-4a75-95ab-33c8928b5fc4",       
				subscribe_key="sub-c-75be36e2-602a-11e5-b50b-0619f8945a4f")   
'''
	Names of the variables in the 'dic_ID[L_ID]' list
	dic_ID[L_ID][0] = L_ID --> client's unique identification number
	dic_ID[L_ID][1] = (NAS)Next approaching signal's number
	dic_ID[L_ID][2] = (PASA)Present approaching signal's angle
	dic_ID[L_ID][3] = command flag 

'''
# Dictionary to store each clients necessary data for calculation
dic_ID = {} 
# List to store the timestamp value of each client
dic_tme = []
# List to store the unique identification number of the client
g_process_list = ["bff29478-089c-4dff-8895-883580885661"]


def calculation_function(L_ID,lat,lng):
  	# List of the lattitude and longitude values of the signals
  	L_list1 = ["37.786188 -122.440033","37.787237 -122.431801",
				"37.785359 -122.424704","37.778739 -122.423349",
				"37.776381 -122.419514","37.772811 -122.412835",
		   		"37.765782 -122.407557"]
		   		
	
	L_ID =  str(L_ID)

	if (dic_ID != 0):
		if (dic_ID[L_ID][1]<=7):
			parameter_lat1 = float(lat)
			parameter_lng1 = float(lng)
			
			#selecting the signal from the list based on the NAS value 
			L_lat2 = (L_list1[dic_ID[L_ID][1]-1][0:9])
			L_lng2 = (L_list1[dic_ID[L_ID][1]-1][10:21])
					
			# calculating the distancse between the vehicle and the approaching signal
			L_distance = dis_calc(parameter_lat1,parameter_lng1,L_lat2,L_lng2) 
					
			# calculating the angle between the vehicle and the approaching signal						
			L_bearing  = bearng(parameter_lat1,parameter_lng1,L_lat2,L_lng2)   
					
			#print L_distance		
			# Quadrant change
			if (L_bearing >180 and L_bearing <= 360):                  
				L_bearing = str(180-L_bearing)
			L_brng2 = str (L_bearing)
					
				
			L_temp1 = dic_ID[L_ID][2]
			L_temp1 = str(L_temp1)
			L_temp2  = L_brng2
			L_temp2 = str(L_temp2)
			
			# checking for the signal crossover  
			if(L_temp1[0] != (L_temp2[0])):	                              
				if (dic_ID[L_ID][3] == False):	
					# sending vehicle crossed message to the respective client
					pubnub.publish(channel = dic_ID[L_ID][0] ,message = {"signal_type":"withdraw","sig_num":dic_ID[L_ID][1]-1})
					print "server sent clearance message to %s " %(L_ID)
					# updating the NAS value
					
					dic_ID[L_ID][1] = dic_ID[L_ID][1]+1	
					# setting the command flag 
					dic_ID[L_ID][3] = True			
			
			# checking for the vehicle approaching near the signal				
			if (L_distance <=200 and L_distance >=100):	 
				if (dic_ID[L_ID][3] == True):
					# sending vehicle approaching message to the respective client
					pubnub.publish(channel=dic_ID[L_ID][0] ,message = {"signal_type":"green","sig_num":dic_ID[L_ID][1]-1})
					print "server sent green signal message to %s " %(L_ID)
					# updating the PASA	
					dic_ID[L_ID][2]= L_brng2
					# setting the flag 	
					dic_ID[L_ID][3] = False
			
	else:
		print "None of the clients are CONNECTED"	

# Function to clear the all stored values in the dictionary once it is discarded in the middle

def clearing_function():
	for i in range (0,len(dic_tme)):
		if (len(dic_tme) >=1):
			client = dic_tme[i]
			client_hour = int(client[0:2])
			client_min = int(client[3:5])
			client_sec = int(client[6:8])
			# getting the actual time in UTC
			present_time = time.gmtime()
			present_hours   = int(present_time[3])
			present_minutes = int(present_time[4])
			present_secs    = int(present_time[5])
			presenttime = (present_hours *60*60) + (present_minutes*60) + (present_secs)
			clienttime = (client_hour *60*60) + (client_min*60) + (client_sec)
			# Time difference between present Time and the client's starting time 
			time_difference =  (presenttime-clienttime)
			time_difference = time_difference/60
			
			# checking the TIMEOUT  of the clients in the timestamp list and 
			# removing the data in the dictionaries and lists of Timeout client's
			
			if (time_difference >= 30 and len(dic_tme)>=1 ):
				L_ID = g_process_list[i+1]
				print L_ID
				del dic_ID[L_ID]
				del dic_tme[i]
				del g_process_list[i+1]
				print dic_ID,dic_tme,g_process_list,len(dic_tme)
				break

# callback function starts here
def callback(message,channel):
	UUID = message['ID']
	L_count = 0

	# checking for the new clients
	if (message['status'] == "start"):  
		L_ID = UUID
		clearing_function()
		day = message['day']
		client_time = str(day[17:25])
		dic_tme.append(client_time)
		print dic_tme
		# checking the whole list for the clients id
		for i in range (0,len(g_process_list),1):
			if (UUID != g_process_list[i]):
				L_count = L_count+1
		# adding the new client if not existed in the list
		if (L_count == len(g_process_list)):
			L_count = 0
			g_process_list.append(UUID)
			dic_ID[L_ID] = [L_ID,1,'167',True]
	
	# checking for the ending of the route		
	if(message['status'] == "stop"):
		S_ID = str(message['ID'])
		del dic_ID[S_ID]
		for i in range (0,len(g_process_list)):
			if (S_ID == g_process_list[i]):
				del g_process_list[i]
				del dic_tme[i-1]
				break
	
	#Receiving the lattitude and longitude from the client and calling the calcuation function
	if(message['status'] == "run"):
		L_count2 = 0
		for i in range(0,len(g_process_list),1):
			if(message['ID'] != g_process_list[i]):
				L_count2+=1
		if(L_count2 == len(g_process_list)):
			id = message['ID']
			print "this id is expired ",message['ID'] 
			# sending  a TIMEOUT message if the clients time got expired  
			pubnub.publish(channel= id ,message = {"signal_type":"timeout"})	
		else:
			L_ID = message['ID']
			lat = message['lat']	
			lng = message['lon']
			calculation_function(L_ID,lat,lng)
	return True
	
def error(message):
    print("ERROR : " + str(message))

def connect(message):
	print("CONNECTED")
	
def reconnect(message):
    print("RECONNECTED")

def disconnect(message):
    print("DISCONNECTED")
 
 # main function
if __name__ == "__main__":	
	pubnub.subscribe(channels='pub_channel', callback=callback,error=callback,
    	connect=connect, reconnect=reconnect, disconnect=disconnect)
	




    
