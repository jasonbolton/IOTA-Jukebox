from iota import *

class MessageSender:

    def __init__(self, send_address):
        self._send_address = send_address
        self._api = Iota('https://iotanode.us:443')

    def send_message(self, message):
        tag = ""
        for i in range(27 - len(song) - 1):
            rand_char = chr(random.randint(80, 90))
            tag += rand_char
        tag = TryteString.from_unicode(tag)
        self._api.send_transfer(
          depth = 100,
          transfers = [
            ProposedTransaction(
              address =
                Address(
                  self._send_address,
                ),
              value = 0,
              tag = Tag(tag),
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
