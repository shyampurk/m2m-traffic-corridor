#!usr/bin/python
'''
/********************************************************************************************
Name 		      :  dis_calc 
Description  	:  calculates the distance between given two lattitude and longitude 
		             points 
Parameters   	:  l_lt1 and l_ln1 are point one lattitude and longitude respectively 
		             l_lt2 and l_ln2 are point two lattitude and longitude respectively
Return       	:  This function will return the distance between given two lattitude 
	               and longitude points 
**********************************************************************************************/
'''
import math
g_r = 6378.137 # radius of the earth

def dis_calc(l_lt1,l_ln1,l_lt2,l_ln2):	
	l_lt1 = float(l_lt1)
	l_ln1 = float(l_ln1)	
	l_lt2 = float(l_lt2)
	l_ln2 = float(l_ln2)
	l_lt1 = math.radians(l_lt1)
	l_ln1 = math.radians(l_ln1)
	l_lt2 = math.radians(l_lt2)
	l_ln2 = math.radians(l_ln2)
	c1 = float(math.cos(l_lt2))
	c2 = float(math.cos(l_lt1))
	s1 = float((l_lt1-l_lt2)/2)
	s2 = float((l_ln1-l_ln2)/2)
	si1 = float(pow(s1,2))
	si2 = float(pow(s2,2))
	rad = float(2*g_r)
	inside = float(si1 + c1*c2*si2)
	inside2 = float(math.sqrt(inside))
	dis1 = float(rad*inside2)
	dis1 = dis1 *1000
	return dis1
    
    

