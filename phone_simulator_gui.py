PLAY_LIST_DECODER_CHAR = "*"

import tkinter as tk
from tkinter import scrolledtext
from iota import *
import random
import time


class App(tk.Tk):
    def __init__(self):
        tk.Tk.__init__(self)
        self._frame = None
        self.iconbitmap("images\icon.ico")
        self.switch_frame(StartPage)
        self.title("Phone Simulator")
        self.geometry("350x600")

    def switch_frame(self, frame_class):
        # destroys current frame and replaces it.
        new_frame = frame_class(self)
        if self._frame is not None:
            self._frame.destroy()
        self._frame = new_frame
        self._frame.pack()

class StartPage(tk.Frame):
    # the main page of the phone simulator program
    def __init__(self, master):
        tk.Frame.__init__(self, master)

        # initalizing the variables.
        self._address = ""
        self._api = Iota('http://nodes.iota.fm:80')
        self._monitor_state = False
        self._spent_transactions = {}
        self._play_list = []
        self._display_list = []

        # creating the ui elements.
        self._address_label = tk.Label(self, text="Enter Address:")
        self._address_entry = tk.Entry(self, width=82)
        self._begin_monitor_button = tk.Button(self, text="Begin Monitoring",
                                 command=lambda: self.get_songs())
        self._play_list_box = scrolledtext.ScrolledText(self, state="disabled", width=25, height=15)
        
        self._vote_label = tk.Label(self, text="Vote for a song with a number:")
        self._vote_entry = tk.Entry(self, width=10)
        self._vote_button = tk.Button(self, text="Press to Vote",
                                 command=lambda: self.vote_button_press())

        self._end_button = tk.Button(self, text="End Program",
                                 command=lambda: app.destroy())

        # packing the ui elements.
        self._address_label.pack(side="top", fill="x", pady=10)
        self._address_entry.pack()
        self._begin_monitor_button.pack()
        self._play_list_box.pack(side="top", fill="x", pady=10)
        self._vote_label.pack()
        self._vote_entry.pack()
        self._vote_button.pack()
        self._end_button.pack(side="top", pady=10)

    def vote_button_press(self):
        # if the phone is monitoring and the vote field
        # is not empty, a vote is sent to the tangle corresponding
        # to the number in the vote entry field.
        if self._monitor_state == True and \
           self._vote_entry.get() != "":
            if int(self._vote_entry.get()) < len(self._play_list):
                print(self._play_list[int(self._vote_entry.get())])
                self.vote_for_song(self._play_list[int(self._vote_entry.get())])
            
    def get_songs(self):
        # sets the monitor state to true, loads in the play list,
        # decodes it, and displays it to the ui.
        self._address = self._address_entry.get()
        if len(self._address) == 81:
            self._monitor_state = True
            encoded_message_list = self.get_tangle_info()
            decoded_message = self.decode_message_list(encoded_message_list, PLAY_LIST_DECODER_CHAR)
            self._play_list = self.make_message_list(decoded_message, PLAY_LIST_DECODER_CHAR)
            print(self._play_list)
            print()
            self.display_song_list() 
    
    def get_tangle_info(self):
        # reads in transactions from the tangle. if the tag has already
        # been read, it is not processed. the messages are returned in a list
        message_list = []
        transaction_dict = self._api.find_transactions(bundles=None, \
                            addresses=[self._address], tags=None, approvees=None)
        for transaction_hash in transaction_dict['hashes']:
            trytes = self._api.get_trytes([transaction_hash])['trytes'][0]
            transaction = Transaction.from_tryte_string(trytes)
            if transaction.tag not in self._spent_transactions:
                message_list.append(transaction.signature_message_fragment)
                self._spent_transactions[transaction.tag] = 0
        print("Tangle info successfully loaded")
        print()
        return message_list

    def decode_message_list(self, message_list, decoder_char):
        # decodes and returns the first message found that
        # contains the decoder_char sequence.
        for message in message_list:
            message = message.decode()
            print(message)
            for i in range(len(message)):
                if message[i] == decoder_char and \
                   message[i+1] == decoder_char:
                    return message[i:]
                
    def make_message_list(self, message, decoder_char):
        # returns a song list by splitting a song string
        # containing songs split by a decoder_char.
        print(message)
        song_split = message.split(decoder_char)
        clean_song_split = []
        for i in range(len(song_split)):
            if len(song_split[i]) > 0:
                clean_song_split.append(song_split[i])
        return clean_song_split
                
    def display_song_list(self):
        # given a list of songs, print out a formatted
        # number: song_name string.
        self._play_list_box.config(state="normal")
        for i in range(len(self._play_list) - 1, -1, -1):
            self._play_list_box.insert(0.0, "\n")
            self._play_list_box.insert(0.0, str(i) + ": " + self._play_list[i])
        self._play_list_box.config(state="disabled")
        

    def make_random_tag(self):
        # this method constructs a random tag to include
        # in outgoing transactions.
        construct_tag = ""
        for i in range(27):
            rand_char = chr(random.randint(80, 90))
            construct_tag += rand_char
        construct_tag = TryteString.from_unicode(construct_tag)
        if len(construct_tag) > 27:
            excess = len(construct_tag) - 27
            construct_tag = construct_tag[excess:]
        return construct_tag

    def vote_for_song(self, song):
        # this function is used for encoding and voting
        # for a song to play. a song name is enclosed by
        # two ?? and encoded to trytes. this is the transaction
        # messsage. a random tag is generated. the transaction
        # is sent to the monitored address.
        random_tag = self.make_random_tag()
        song = "??" + song + "??"
        song = TryteString.from_unicode(song)
        send_confirmation = False
        while not send_confirmation:
            try:
                print("Sending song vote to the Tangle...")
                self._api.send_transfer(
                  depth = 3,
                  transfers = [
                    ProposedTransaction(
                      address =
                        Address(
                          self._address,
                        ),
                      value = 0,
                      tag = Tag(random_tag),
                      message = song,
                    ),
                  ],
                )
                print("The song vote was successfully attached to the Tangle")
                print()
                send_confirmation = True
            except:
                print("Error: Retrying tangle attachment")
                print()
                time.sleep(2)
                pass

if __name__ == "__main__":
    app = App()
    app.mainloop()
