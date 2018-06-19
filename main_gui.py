import tkinter as tk
from tkinter import filedialog, scrolledtext
from transaction_monitor import TransactionMonitor
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
    # main page of the jukebox program
    def __init__(self, master):
        tk.Frame.__init__(self, master)

        # initalizing the variables.
        self._jukebox_state = False
        self._song_location = ""
        self._address = ""
        self._play_list = []
        self._vote_list = []
        self._finished_transactions = {}

        # initializing the class objects.
        self._listener = TransactionMonitor(self._finished_transactions)
        self._send_bot = None

        # creating the ui elements.
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

        # packing the ui elements
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
        # if the jukebox is running, the next song is taken from
        # the vote list and played.
        if self._jukebox_state == True:
            next_song = self._vote_list[len(self._vote_list)-1]
            print(next_song)
            self._vote_list = self._vote_list[0:len(self._vote_list)-1]
            self.refresh_votes()
            print(self._song_location + next_song)
            webbrowser.open(self._song_location + "/" + next_song)

    def get_file_location(self):
        # if the jukebox is not playing, a choose directory will
        # pop up to choose the song directory, and the file path
        # will be saved.
        if self._jukebox_state == False:
            self._song_location = filedialog.askdirectory(initialdir \
                                    = "/",title = "Select file")
            self._location_entry.delete(0, tk.END)
            self._location_entry.insert(0, self._song_location)
            self._play_list = os.listdir(self._song_location)
            self._play_list = self.determine_valid_format()
            self.print_play_list()
            print(self._song_location)
        
    def print_play_list(self):
        # prints the play list to the play list scrolled
        # text box.
        self._play_list_box.config(state="normal")
        self._play_list_box.delete(0.0, tk.END)
        self._play_list = self._play_list[::-1]
        for song in self._play_list:
            self._play_list_box.insert(0.0, "\n")
            self._play_list_box.insert(0.0, song)
        self._play_list_box.config(state="disabled")
        self._play_list = self._play_list[::-1]


    def start_jukebox(self):
        # turns the jukebox state on if the song location is not empty
        # and the jukebox is off. the address is loaded and the play list
        # is sent to the tangle. the votes are then printed to the vote box.
        if self._song_location != "" and self._jukebox_state == False:
            self._jukebox_state = True
            print(self._address)
            if self._address_entry.get() == "":
                self._address = self._listener.get_address()
            else:
                self._address = self._address_entry.get()
                self._listener.change_address(self._address)
            self._address_entry.delete(0, tk.END)
            self._address_entry.insert(0, self._address)
            self._send_bot = MessageSender(self._address)
            self.send_play_list()
            self.refresh_votes()

    def send_play_list(self):
        # send a message to the tangle with the encoded play list.
        encoded_play_list = self._send_bot.encode_play_list(self._play_list)
        self._send_bot.send_message(encoded_play_list)

    def refresh_votes(self):
        # reads in song votes from the tangle and reprints
        # the play list to the vote box.
        if self._jukebox_state == True:
            temp_list = self._send_bot.decode_list(self._listener.get_transactions())
            for song in temp_list:
                self._vote_list.append(song) 
            print(self._vote_list)
            self._vote_list_box.config(state="normal")
            self._vote_list_box.delete(0.0, tk.END)
            for song in self._vote_list:
                self._vote_list_box.insert(0.0, "\n")
                self._vote_list_box.insert(0.0, song)
            self._vote_list_box.config(state="disabled")

    def determine_valid_format(self):
        # loops through the incoming song reference
        # list to determine if the file format is valid
        # for playing as an audio file.
        valid_song_list = []
        for song in self._play_list:
            if "." in song:
                possible_song = song
                possible_song = possible_song[::-1]
                possible_song = possible_song.split(".")
                file_format = possible_song[0][::-1]
                if file_format == "m4a" or \
                   file_format == "mp3":
                    valid_song_list.append(song)
        return valid_song_list

if __name__ == "__main__":
    app = App()
    app.mainloop()
