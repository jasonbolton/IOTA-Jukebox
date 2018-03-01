from iota import *
import random

class MessageSender:
    """this class handles the sending of transactions
    requested by the main program. a proof of work node
    is required."""
    def __init__(self, send_address):
        self._send_address = send_address
        self._api = Iota('https://iotanode.us:443')

    def make_random_tag(self):
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
    
    def send_message(self, message):
        """a random tag transaction with a passed-in
        pre-encrypted message is sent using this method."""
        random_tag = self.make_random_tag()
        
        self._api.send_transfer(
          depth = 100,
          transfers = [
            ProposedTransaction(
              address =
                Address(
                  self._send_address,
                ),
              value = 0,
              tag = Tag(random_tag),
              message = message,
            ),
          ],
        )
    
    

##
##api.send_transfer(
##  depth = 100,
##  transfers = [
##    ProposedTransaction(
##      # Recipient of the transfer.
##      address =
##        Address(
##          ADDRESS_WITH_CHECKSUM_SECURITY_LEVEL_2,
##        ),
##      value = 0,
##      tag = Tag(b'EXAMPLE'),
##      message = TryteString.from_string('Hello!'),
##    ),
##  ],
##)
