# Smart Traffic Management System for Emergency Services

##OVERVIEW
This is a simulated demonstration of realtime traffic control to enable passage of an ambulance through an ad-hoc, on-demand traffic corridor.   


##INTRODUCTION
This demo assumes a pre defined route starting from Mount Zion Hospital, San Francisco to San Francisco General Hospital, along with a bunch of traffic signals which man the intersections enroute. 

The client application consists of a mapbox based web interface for simulating ambulance movement through this pre-defined route. Whenever an ambulance starts its journey from Mount Zion hospital, it periodically sends its location data to a Traffic Management Server (TMS) hosted on IBM Bluemix.  The TMS also keeps a tab of the traffic signals and tracks the movement of ambulance along the route. Whenever the ambulance is within a centain distance of an approaching signal, the TMS commands that traffic signal to turn Green to allow the passage of traffic. After the ambulance crosses the signal, TMS issues another command to the signal to resume its normal operation. 

The entire communication between the ambulance, the TMS and the individual traffic signals happens via PubNub. 


##RUN THE DEMO
The TMS is implemented as a [python program](server/traffic_server.py)

An existing instance of TMS is already hosted on IBM Bluemix and is currently running.

To run the client application , perform the following steps

1. Open the [Demo Link](http://shyampurk.github.io/m2m-traffic-corridor/client/) in a web browser.

2. Wait for the map to load and show the route and the traffic signal lights along with the ambulance icon at the start point.

3. Click on the ambulance icon to start its journey. You will notice that the ambulance icon will start moving along the route.

4. Notice how the individual traffic signal changes its status when ambulance approaches and crosses it.

5. The updates on traffic signal are also captured in a status message displayed at the bottom left corner of the screen.


##HOST YOUR OWN DEMO

For hosting your own demo, follow the steps as given below

1. Download/fork the source code of this repository and update the PubNub keys at the [server side](server/traffic_server.py)  and [client side](client/index.html)

2. Run the python script 

3. Open a web browser and load the [client side web page](client/index.html) and follow the steps as defined above in "RUN THE DEMO" section, from step 2 onwards. 


##ASSUMPTIONS

1. For the sake of brevity, the client web applciation only shows the traffic signal status at the approaching side of the route. 
2. The server is assumed to be always on and available. Server outage is not handled by the client.
