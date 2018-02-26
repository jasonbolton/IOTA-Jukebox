from iota import *
from time import sleep
import webbrowser


def extract_song(string):
    new_string = ""
    for letter in string:
        if letter == "9":
            break
        new_string += letter
    return new_string

#address to monitor
my_address = TryteString('TKWNVZJUMPQGMUKT9OETHFAJIIPR9SEJDOFENJWIJAB9WMVAN9HVURJFBRJIPSVVMHDGMXRYTTUCHJMKWFBSYBNZUD')
#my_tags = TryteString("PLAYJEREMY99999999999999999")

#specify seed. to monitor address, seed is not needed
api = Iota('http://node03.iotatoken.nl:15265')


finished_transactions = {}
"""loop throught the transactions"""
while True:
    transaction_dict = api.find_transactions(bundles=None, addresses=[my_address], tags=None, approvees=None)

    for transaction_hash in transaction_dict['hashes']:
        trytes = api.get_trytes([transaction_hash])['trytes'][0]
        transaction = Transaction.from_tryte_string(trytes)
        print(transaction.hash)
        print(transaction.tag)
        if transaction.tag[0:4] == 'PLAY' and \
           transaction.hash not in finished_transactions:
            finished_transactions[transaction.hash] = 1
            song = extract_song(str(transaction.tag[4:])) + ".m4a"
            print(song)
            webbrowser.open("C:\\Users\Honey Booboo\\Desktop\\songs\\" + song)
    sleep(20)
    
    
##    if input() == "stop":
##        break







