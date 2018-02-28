# IOTA Jukebox - Prototype Software for Distributed Action Selection through IOTA Transactions, with Value Transfer Optional

This program is a large work in progress. Information will be added as it comes. This project will eventually be open-source licensed, but I have not yet set it up. However, if you are interested in this software, feel free to contact me. Though this particular program is a simple jukebox app, the base communication features allow a wide variety of addition and tweaking for any set of activities that rely on listening for votes, with or without money attached. 

Instructions

To run the main program, use main.py. To vote for songs, use the phone_simulator.py.

Dependencies

This program was made with Python 3.6.4. To run this program, pyota needs to be installed. You can find pyota at https://github.com/iotaledger/iota.lib.py

Todo: 
```
-Better commenting
-Code cleanup
-Implement address generation on start - print address to add to phone_simulator
-Prompt for file-path on start
-Make GUI - Try kivy, pyqt
-Pass in file path to play_song class
-Only add songs to reference list if they have correct file ending(not sure which work, start with .mp3, .m4a, .wav)
-Implement qr generator after GUI
-Add more instruction info to readme
```
