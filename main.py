#time between scanning the tangle for new song votes
REFRESH_TIME = 10 #(seconds)
#add extra time between song switching
SONG_SWITCH_DELAY = 2 #(seconds)
#minimum transaction value to be read into the program
MINIMUM_TRANSACTION_VALUE = 0 #(iota)

from transaction_monitor import TransactionMonitor
from choose_song import ChooseSong
from play_song import PlaySong
from encoder import Encoder
from transaction_send_bot import MessageSender
import time
import os

def main():
    """this is the main loop for the program. the iota address will
    be scanned for song votes and added to a playlist, then played."""
    finished_transactions = {}
    #location of songs on the computer
    reference_list = os.listdir("C:\\Users\Honey Booboo\\Desktop\\songs\\")
    #iota address to monitor. if using the same address, old songs will be loaded to playlist
    address = 'BJAKMIXYBLAAPKLBCGHELQCSKOMZLSAYLOHDBOYRJFQJIHBWCCCIUBVLQKYPTHWVBQWTZM9JGMAPFUCBCBCSRTKJLY'
    #any node can be chosen
    node = 'http://node03.iotatoken.nl:15265'

    listener = TransactionMonitor(address, node, finished_transactions, MINIMUM_TRANSACTION_VALUE)
    chooser = ChooseSong(reference_list)
    player = PlaySong()
    send_bot = MessageSender(address)
    encoder = Encoder()

##send a message to the tangle with the encoded reference list
##    encoded_list = encoder.encode_reference_list(reference_list)
##    send_bot.send_message(encoded_list)
    
    song_value_list, transaction_time = listener.get_transactions()
    print(song_value_list)
    song_value_list = encoder.decode_list(song_value_list)
    print(song_value_list)

    chooser.update_current_order(song_value_list)
    next_song = chooser.pick_next_song()
    song_length, song_start_time = player.play_song(next_song)
    print(next_song)

    
    while True:
        """
        get song length, start a timer, if song length - timer < 0,
        get a new song. to stop the program, close the console.
        """
        if time.time() - transaction_time > REFRESH_TIME:
            song_value_list, transaction_time = listener.get_transactions()
            song_value_list = encoder.decode_list(song_value_list)
            chooser.update_current_order(song_value_list)
            print(song_value_list)
        if time.time() - song_start_time > song_length + SONG_SWITCH_DELAY:
            next_song = chooser.pick_next_song()
            song_length, song_start_time = player.play_song(next_song)
            print(next_song)

main()



