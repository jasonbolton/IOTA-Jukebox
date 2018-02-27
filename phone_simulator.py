from iota import *
import random

def main():
    spent_transactions = {}
    address = 'BJAKMIXYBLAAPKLBCGHELQCSKOMZLSAYLOHDBOYRJFQJIHBWCCCIUBVLQKYPTHWVBQWTZM9JGMAPFUCBCBCSRTKJLY'
    node = 'https://iotanode.us:443'
    api = Iota(node)
    encoded_message_list = get_tangle_info(spent_transactions, api, address)
    decoded_message = decode_message(encoded_message_list)
    reference_list = make_reference_list(decoded_message)
    display_reference_list(reference_list)
    print(reference_list)
    song = reference_list[1]
    #sends a song out to the tangle. comment out when not desired.
    #vote_for_song(song, address, api)

def get_tangle_info(spent_transactions, api, address):
    message_list = []
    transaction_dict = api.find_transactions(bundles=None, \
                        addresses=[address], tags=None, approvees=None)
    for transaction_hash in transaction_dict['hashes']:
        trytes = api.get_trytes([transaction_hash])['trytes'][0]
        transaction = Transaction.from_tryte_string(trytes)
        if transaction.tag not in spent_transactions:
            message_list.append(transaction.signature_message_fragment)
    return message_list

def decode_message(message_list): 
    for message in message_list:
        message = message.decode()
        print(message)
        for i in range(len(message)):
            if message[i] == "*":
                return message[i:]
            
def make_reference_list(message):
    song_split = message.split("*")
    clean_song_split = []
    for i in range(len(song_split)):
        if len(song_split[i]) > 0:
            clean_song_split.append(song_split[i])
    return clean_song_split
            
def display_reference_list(reference_list):
    for i in range(len(reference_list)):
        print(str(i) + ":", reference_list[i])

def vote_for_song(song, address, api):
    random_tag = ""
    song = "??" + song + "??"
    print(song)
    for i in range(27):
        rand_char = chr(random.randint(80, 90))
        random_tag += rand_char
    print(song)
    song = TryteString.from_unicode(song)
    print(song)
    if len(random_tag) > 27:
        excess = len(random_tag) - 27
        random_tag = random_tag[excess:]
    print(len(random_tag))
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
