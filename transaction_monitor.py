from iota import *
import time

class TransactionMonitor:
    """this class monitors an address on the tangle
    for song votes."""
    def __init__(self, finished_transactions, minimum_value):
        self._node = 'http://node03.iotatoken.nl:15265'
        self._api = Iota(self._node)
        self._address = self.set_address()
        
        self._finished_transactions = finished_transactions
        self._minimum_value = minimum_value
        self._new_transactions = []

    def set_address(self):
        gna_result = self._api.get_new_addresses()
        address = gna_result['addresses'][0]
        return address

    def get_address(self):
        return self._address

    def get_node(self):
        return self._node

    def get_finished_transactions(self):
        return self._node

    def extract_song(self, string):
        """given a string message, this function
        decodes and removes non-song information
        and returns the cleaned string."""
        song_name = ""
        for letter in string:
            if letter != "9":
                song_name += letter
        song_name = TryteString(song_name)
        return song_name

    def get_transactions(self):
        """this method cycles through the transactions
        on an address in the tangle. if the transaction
        tag is in the dictionary self._finished_transactions,
        the message is not processed. if not, the message is
        stripped to access the song data. the data is added
        to a list to be returned and the tag is added to finished
        transactions, along with a time-stamp of finish-time."""
        print("Searching the tangle for song votes...")
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
                self._new_transactions.append(song)
        print("Complete")
        print()
        return self._new_transactions, time.time()
        




    

