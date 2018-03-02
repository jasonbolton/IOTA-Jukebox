# time between scanning the tangle for new song votes.
REFRESH_TIME = 10 #(seconds)
# add extra time between song switching.
SONG_SWITCH_DELAY = 2 #(seconds)
# minimum transaction value to be read into the program.
MINIMUM_TRANSACTION_VALUE = 0 #(iota)

from transaction_monitor import TransactionMonitor
from choose_song import ChooseSong
from encoder import Encoder
from transaction_send_bot import MessageSender
import time
import os

def main():
    """this is the main loop for the program. the iota address will
    be scanned for song votes and added to a playlist, then played."""
    finished_transactions = {}
    # location of songs on the computer.
    print("(Example: C:\\Users\Honey Booboo\\Desktop\\songs\\)")
    song_file_path = input("Enter location of songs on the computer: ")
    reference_list = os.listdir(song_file_path)

    # initializing class objects
    listener = TransactionMonitor(finished_transactions, MINIMUM_TRANSACTION_VALUE)
    address = listener.get_address()
    print("The broadcast address is: " + str(address))
    print()
    chooser = ChooseSong(reference_list, song_file_path)
    send_bot = MessageSender(address)
    encoder = Encoder()
    
    reference_list = chooser.determine_valid_format(reference_list)
    print("The reference song list is:")
    print(reference_list)
    print()

    # send a message to the tangle with the encoded reference list.
    encoded_list = encoder.encode_reference_list(reference_list)
    send_bot.send_message(encoded_list)
        
    song_value_list, transaction_time = listener.get_transactions()
    song_value_list = encoder.decode_list(song_value_list)

    # send a message to the tangle with the encoded play list.
    #current_play_list = chooser.get_play_list()
    #print(current_play_list)
    #encoded_play_list = encoder.encode_play_list(current_play_list)
    #print(encoded_play_list)
    #send_bot.send_message(encoded_play_list)
    #print("The song playlist was successfully attached to the tangle")

    chooser.update_current_order(song_value_list)
    next_song = chooser.pick_next_song()
    song_length, song_start_time = chooser.play_song(next_song)
    
    while True:
        """
        get song length, start a timer, if song length - timer < 0,
        get a new song. to stop the program, close the console.
        """
        if time.time() - transaction_time > REFRESH_TIME:
            song_value_list, transaction_time = listener.get_transactions()
            song_value_list = encoder.decode_list(song_value_list)
            chooser.update_current_order(song_value_list)
        if time.time() - song_start_time > song_length + SONG_SWITCH_DELAY:
            next_song = chooser.pick_next_song()
            song_length, song_start_time = chooser.play_song(next_song)

main()



