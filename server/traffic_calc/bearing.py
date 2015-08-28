#!/usr/bin/python
'''
/***************************************************************************************
Name 		      :  bearng 
Description 	:  calculates the bearing(angle) between given two lattitude and 
		             longitude points 
Parameters  	:  l_lat1 and l_lng1 are point one lattitude and longitude respectively 
		             l_lat2 and l_lng2 are point two lattitude and longitude respectively
Return 		    :  This function will return the bearing(angle) between given two 
		             lattitude and longitude points 
****************************************************************************************/
'''
import math
def bearng(l_lat1,l_lng1,l_lat2,l_lng2):
	l_lat1 = float(l_lat1)
	l_lng1 = float(l_lng1)
	l_lat2 = float(l_lat2)
	l_lng2= float(l_lng2)
	lndif = (l_lng2 - l_lng1)
	y = math.sin(lndif) * math.cos(l_lat1)	
	x =  math.cos(l_lat2) * math.sin(l_lat1)  - math.sin(l_lat2) * math.cos(l_lat1)*math.cos(lndif)
	l_brng = math.atan2(y,x)
	l_brng = math.degrees(l_brng)
	l_brng = (l_brng +360)%360
	l_brng = (360-l_brng)
	return l_brng

