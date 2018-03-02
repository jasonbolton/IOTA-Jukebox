# IOTA Jukebox - Proof of concept software for action selection through IOTA transactions, value transfer optional

This program is a large work in progress. Information will be added as it comes. This project will eventually be open-source licensed, but I have not yet set it up. However, if you are interested in this software, feel free to contact me. Though this particular program is a simple jukebox app, the base communication features allow a wide variety of addition and tweaking for any set of activities that rely on listening for votes, with or without money attached. 

Instructions

This program reads in song info from a folder on your computer(This folder must be inputted in the main.py code at the moment). The program sends the song reference list to an address on the tangle then listens for incoming song votes to play. The phone simulator program, which acts as a mobile app, reads in the song reference list and is able to vote for songs to play on the tangle. To run the main program, use main.py. To vote for songs, use the phone_simulator.py. 

Dependencies

This program was made with Python 3.6.4. To run this program, pyota needs to be installed. You can find pyota at: https://github.com/iotaledger/iota.lib.py

Todo: 
```
-Better commenting
-Code cleanup
-Make GUI - Try kivy, pyqt
-Implement qr generator after GUI
-Add more instruction info to readme
-Add License
-Test the IOTA sandbox POW node: https://powbox.testnet.iota.org/
```
