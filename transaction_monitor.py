from iota import *
import time

class TransactionMonitor:

    def __init__(self, address, node, finished_transactions, minimum_value):
        self._address = TryteString(address)
        self._node = node
        self._finished_transactions = finished_transactions
        self._minimum_value = minimum_value
        self._new_transactions = []
        self._api = Iota(node)

    def get_address(self):
        return self._address

    def get_node(self):
        return self._node

    def get_finished_transactions(self):
        return self._node

    def extract_song(self, string):
        song_name = ""
        for letter in string:
            if letter != "9":
                song_name += letter
        song_name = TryteString(song_name)
        return song_name

    def get_transactions(self):
        self._new_transactions = []
        transaction_dict = self._api.find_transactions(bundles=None, \
                            addresses=[self._address], tags=None, approvees=None)
        for transaction_hash in transaction_dict['hashes']:
            trytes = self._api.get_trytes([transaction_hash])['trytes'][0]
            transaction = Transaction.from_tryte_string(trytes)
            if transaction.tag not in self._finished_transactions and \
               transaction.value >= self._minimum_value:
                self._finished_transactions[transaction.tag] = 0
                song = self.extract_song(str(transaction.signature_message_fragment))
                print(song)
                self._new_transactions.append(song)
        return self._new_transactions, time.time()
        




    

