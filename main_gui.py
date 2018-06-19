import tkinter as tk
from tkinter import filedialog, scrolledtext
from transaction_monitor import TransactionMonitor
from choose_song import ChooseSong
from encoder import Encoder
from transaction_send_bot import MessageSender
import webbrowser
import os

class App(tk.Tk):
    def __init__(self):
        tk.Tk.__init__(self)
        self._frame = None
        self.iconbitmap("images\icon.ico")
        self.switch_frame(StartPage)
        self.title("IOTA Jukebox")
        self.geometry("800x420")

    def switch_frame(self, frame_class):
        # destroys current frame and replaces it.
        new_frame = frame_class(self)
        if self._frame is not None:
            self._frame.destroy()
        self._frame = new_frame
        self._frame.pack()

class StartPage(tk.Frame):
    # todo
    def __init__(self, master):
        tk.Frame.__init__(self, master)
        
        self._jukebox_state = False
        self._song_location = ""
        self._address = ""
        self._play_list = []
        self._vote_list = []
        self._finished_transactions = {}
        
        self._listener = TransactionMonitor(self._finished_transactions)
        self._chooser = None
        self._send_bot = None
        self._encoder = Encoder()

        self._location_label = tk.Label(self, \
                                        text="Enter location of songs on the computer:")
        self._get_songs_button = tk.Button(self, text="Choose Location",
                                  command=lambda: self.get_file_location())
        
        self._song_location_label = tk.Label(self, text="Song location:")
        self._location_entry = tk.Entry(self, width=82)
        self._address_label = tk.Label(self, text="Address:")
        self._address_entry = tk.Entry(self, width=82)

        self._begin_button = tk.Button(self, text="Begin Jukebox",
                                  command=lambda: self.start_jukebox())
        self._refresh_button = tk.Button(self, text="Search for new votes",
                                  command=lambda: self.refresh_votes())

        self._play_list_box = scrolledtext.ScrolledText(self, state="disabled", width=25, height=15)
        self._vote_list_box = scrolledtext.ScrolledText(self, state="disabled", width=25, height=15)

        self._play_button = tk.Button(self, text="Play Next Song",
                                 command=lambda: self.play_next_song())
        self._end_button = tk.Button(self, text="End Program",
                                 command=lambda: app.destroy())

        self._location_label.grid(row=1, column=1)
        self._get_songs_button.grid(row=2, column=1)
        
        self._song_location_label.grid(row=3, column=1)
        self._location_entry.grid(row=3, column=2)
        self._address_label.grid(row=4, column=1)
        self._address_entry.grid(row=4, column=2)
        
        self._begin_button.grid(row=5, column=1)
        self._refresh_button.grid(row=5, column=2)

        self._play_list_box.grid(row=6, column=1)
        self._vote_list_box.grid(row=6, column=2)

        self._play_button.grid(row=7, column=2)
        self._end_button.grid(row=8, column=1)

    def play_next_song(self):
        if self._jukebox_state == True:
            print("play it, sam")
            if self._vote_list != []:
                print("there are songs")
            else:
                print("play random song")

    def get_file_location(self):
        if self._jukebox_state == False:
            self._song_location = filedialog.askdirectory(initialdir \
                                    = "/",title = "Select file")
            self._location_entry.delete(0, tk.END)
            self._location_entry.insert(0, self._song_location)
            self._play_list = os.listdir(self._song_location)
            self._chooser = ChooseSong(self._play_list, self._song_location)
            self._play_list = self._chooser.determine_valid_format(self._play_list)
            self.reprint_play_list()
            print(self._song_location)
        
    def reprint_play_list(self):
        self._play_list_box.config(state="normal")
        self._play_list_box.delete(0.0, tk.END)
        self._play_list = self._play_list[::-1]
        for song in self._play_list:
            self._play_list_box.insert(0.0, "\n")
            self._play_list_box.insert(0.0, song)
        self._play_list_box.config(state="disabled")
        self._play_list = self._play_list[::-1]


    def start_jukebox(self):
        if self._song_location != "" and self._jukebox_state == False:
            self._jukebox_state = True
            print(self._address)
            if self._address_entry.get() == "":
                self._address = self._listener.get_address()
            else:
                self._address = self._address_entry.get()
            self._listener = TransactionMonitor(self._finished_transactions, self._address)
            self._address_entry.delete(0, tk.END)
            self._address_entry.insert(0, self._address)
            self._send_bot = MessageSender(self._address)
            #self.send_play_list()
            self.refresh_votes()

    def send_play_list(self):
        # send a message to the tangle with the encoded play list.
        encoded_play_list = self._encoder.encode_reference_list(self._play_list)
        print(encoded_play_list)
        print(self._play_list)
        print("gonna send")
        self._send_bot.send_message(encoded_play_list)
        print("The song playlist was successfully attached to the tangle")

    def refresh_votes(self):
        if self._jukebox_state == True:
            temp_list = self._encoder.decode_list(self._listener.get_transactions())
            for song in temp_list:
                self._vote_list.append(song) 
            print(self._vote_list)
            self._vote_list_box.config(state="normal")
            self._vote_list_box.delete(0.0, tk.END)
           
            for song in self._vote_list:
                self._vote_list_box.insert(0.0, "\n")
                self._vote_list_box.insert(0.0, song)
            self._vote_list_box.config(state="disabled")
           
            
    def play_next_song(self):
        next_song = self._vote_list[len(self._vote_list)-1]
        print(next_song)
        self._vote_list = self._vote_list[0:len(self._vote_list)-1]
        self.refresh_votes()
        print(self._song_location + next_song)
        webbrowser.open(self._song_location + "/" + next_song)

if __name__ == "__main__":
    app = App()
    app.mainloop()
