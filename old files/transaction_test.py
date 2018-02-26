from iota import Iota, Transaction
api = Iota('http://node03.iotatoken.nl:15265')

transaction_hash = ''  # starting hash

while True:
    transaction_hash = api.find_transactions(approvees=[transaction_hash])['hashes'][0]
    trytes = api.get_trytes([transaction_hash])['trytes'][0]
    transaction = Transaction.from_tryte_string(trytes)
    print(transaction.hash)
    if transaction.is_tail:
        break
print(transaction_hash)
