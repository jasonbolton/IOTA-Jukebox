# IOTA Jukebox - Software for song selection using the IOTA Tangle.

Instructions

This program reads in song info from a folder on your computer. The program sends the song reference list to an address on the tangle then listens for incoming song votes to play. The phone simulator program, which acts as a mobile app, reads in the song reference list and is able to vote for songs to play on the tangle. To run the main program, use main.py. To vote for songs, use the phone_simulator.py. 

Dependencies

This program was made with Python 3.6.4. To run this program, pyota needs to be installed. You will also need to install tinytag.

You can find pyota at: https://github.com/iotaledger/iota.lib.py

You can find python at https://www.python.org/downloads/

You can install tinytag with 'pip install tinytag'
