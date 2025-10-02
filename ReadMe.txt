ReadMe

//insert description of project

TO DO 
- simulate sending and recieving a message - done
- Simulate jamming with the option to change probabilities - done
- add a gui
- simulate multiple devices - done
- add visuals showing messages being sent and the jamming occuring
- add more options to the jamming probabilities by using different networks
- enable the devices to connect to eachtoher using ack
- while the devices are connected they have the abilitiy to disconnect lets say 1/60 secs


- make the network type simulate how the data gets transmitted
- enable jamming then ask what jamming method to use


thoughts:
Represent the jammer as an object with power, duty cycle and position

Why: Real jammers have physical constraints: transmit power (range), on/off duty cycles 
(intermittent), and possibly location relative to devices. Modeling a jammer object lets 
you simulate partial coverage (only devices inside radius are affected) and intermittent 
jamming.

add an option to enable packet ack
shows that we understand how real packets are sent, 

//git testing