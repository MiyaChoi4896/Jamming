ReadMe

//insert description of project


//insert a how to guide

Done:
user can create multiple devices
user can choose to enable jamming
devices send messages to eachother in the form of packets, each packet is simulated as a letter in the input text.
if a packet is jammed it appears as a "." to the recieving device.
3 types of jamming the user can select, spot, sweep, barrage
added it so that each type of jamming does something different,
spot picks one frequency and jams it
sweep picks a random frequency each message and jams that
barrage just straight up jams everything

----Started adding a GUI -----
added the gui for the menu, it kinda broke all the code so ill have to re add all of that network
added a submit button that opens a new window
- window shows the devices and another device as physical objects you can move around
added lines between each of the devices
added another circle as the jamming radius that attaches itself to the jammer 


TODO:
add something that simulates each device sending a message to eachtother
have a pop up saying a device has been disconnected from the network when touching the radius
if the radius touches the line then the messages sent get jammed
- later make it so the percentage chance to get jammed increases the more the intesection is
- calculate the tangent of the circle, the greater the secant, the increased probability
have a percentage bar along the line between devices showing either percentage jammed or percentage that get through



//git testing