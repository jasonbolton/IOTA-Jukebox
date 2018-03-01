REFERENCE_LIST_DECODER_CHAR = "*"
PLAY_LIST_DECODER_CHAR = ":"

from iota import *
import random

def main():
    """this is the main program for the phone simulation
    function of the jukebox. this program reads in encoded
    playlist and reference list information from the tangle,
    decodes and displays that information, and is able to vote
    for songs based on that information."""
    spent_transactions = {}
    # address to monitor.
    address = 'BJAKMIXYBLAAPKLBCGHELQCSKOMZLSAYLOHDBOYRJFQJIHBWCCCIUBVLQKYPTHWVBQWTZM9JGMAPFUCBCBCSRTKJLY'
    # a proof of work node is required.
    node = 'https://iotanode.us:443'
    api = Iota(node)

    # reads in the encoded messages from the tangle.
    encoded_message_list = get_tangle_info(spent_transactions, api, address)

    # decodes the reference list, processes, displays.
    decoded_message = decode_message_list(encoded_message_list, REFERENCE_LIST_DECODER_CHAR)
    reference_list = make_message_list(decoded_message, REFERENCE_LIST_DECODER_CHAR)
    display_song_list(reference_list)
    print(reference_list)
    
    # decodes the play list, processes, displays.
    decoded_message = decode_message_list(encoded_message_list, PLAY_LIST_DECODER_CHAR)
    play_list = make_message_list(decoded_message, PLAY_LIST_DECODER_CHAR)
    display_song_list(play_list)
    print(play_list)
    
    # sends a song out to the tangle. comment out when not desired.
    song = reference_list[3]
    vote_for_song(song, address, api)

def get_tangle_info(spent_transactions, api, address):
    """reads in transactions from the tangle. if the tag has already
    been read, it is not processed. the messages are returned in a list"""
    message_list = []
    transaction_dict = api.find_transactions(bundles=None, \
                        addresses=[address], tags=None, approvees=None)
    for transaction_hash in transaction_dict['hashes']:
        trytes = api.get_trytes([transaction_hash])['trytes'][0]
        transaction = Transaction.from_tryte_string(trytes)
        if transaction.tag not in spent_transactions:
            message_list.append(transaction.signature_message_fragment)
            spent_transactions[transaction.tag] = 0
    return message_list

def decode_message_list(message_list, decoder_char):
    """decodes and returns the first message found that
    contains the decoder_char sequence"""
    for message in message_list:
        message = message.decode()
        print(message)
        for i in range(len(message)):
            if message[i] == decoder_char and \
               message[i+1] == decoder_char:
                return message[i:]
            
def make_message_list(message, decoder_char):
    """returns a song list by splitting a song string
    containing songs split by a decoder_char"""
    song_split = message.split(decoder_char)
    clean_song_split = []
    for i in range(len(song_split)):
        if len(song_split[i]) > 0:
            clean_song_split.append(song_split[i])
    return clean_song_split
            
def display_song_list(song_list):
    """given a list of songs, print out a formatted
    number: song_name string"""
    for i in range(len(song_list)):
        print(str(i) + ":", song_list[i])

def make_random_tag():
    """this method constructs a random tag to include
    in outgoing transactions."""
    construct_tag = ""
    for i in range(27):
        rand_char = chr(random.randint(80, 90))
        construct_tag += rand_char
    construct_tag = TryteString.from_unicode(construct_tag)
    if len(construct_tag) > 27:
        excess = len(construct_tag) - 27
        construct_tag = construct_tag[excess:]
    return construct_tag

def vote_for_song(song, address, api):
    """this function is used for encoding and voting
    for a song to play. a song name is enclosed by
    two ?? and encoded to trytes. this is the transaction
    messsage. a random tag is generated. the transaction
    is sent to the monitored address."""
    random_tag = make_random_tag()
    song = "??" + song + "??"
    song = TryteString.from_unicode(song)
    print(song)
    api.send_transfer(
          depth = 100,
          transfers = [
            ProposedTransaction(
              address =
                Address(
                  address,
                ),
              value = 0,
              tag = Tag(random_tag),
              message = song,
            ),
          ],
        )
    
main()
