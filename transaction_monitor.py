from iota import * 

class TransactionMonitor:
    # this class monitors an address on the tangle
    # for song votes.
    def __init__(self, finished_transactions):
        self._node = 'http://nodes.iota.fm:80'
        self._api = Iota(self._node)
        self._address = self.set_address()     
        self._finished_transactions = finished_transactions
        self._new_transactions = []

    def get_address(self):
        return self._address
    
    def set_address(self):
        # sets an address to the class attibutes.
        gna_result = self._api.get_new_addresses()
        address = gna_result['addresses'][0]
        return address

    def change_address(self, new_address):
        # swaps the class attribute address with a
        # user-provided address.
        self._address = new_address

    def extract_song(self, string):
        # given a string message, this function
        # decodes and removes non-song information
        # and returns the cleaned string.
        song_name = ""
        for letter in string:
            if letter != "9":
                song_name += letter
        song_name = TryteString(song_name)
        return song_name

    def get_transactions(self):
        # this method cycles through the transactions
        # on an address in the tangle. if the transaction
        # tag is in the dictionary self._finished_transactions,
        # the message is not processed. if not, the message is
        # stripped to access the song data. the data is added
        # to a list to be returned and the tag is added to finished
        # transactions, along with a time-stamp of finish-time.
        print("Searching the tangle for song votes...")
        self._new_transactions = []
        transaction_dict = self._api.find_transactions(bundles=None, \
                            addresses=[self._address], tags=None, approvees=None)
        for transaction_hash in transaction_dict['hashes']:
            trytes = self._api.get_trytes([transaction_hash])['trytes'][0]
            transaction = Transaction.from_tryte_string(trytes)
            if transaction.tag not in self._finished_transactions:
                self._finished_transactions[transaction.tag] = 0
                song = self.extract_song(str(transaction.signature_message_fragment))
                self._new_transactions.append(song)
        print("Complete")
        print()
        return self._new_transactions
        




    

