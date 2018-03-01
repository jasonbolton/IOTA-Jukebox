import random
import webbrowser
import time
from tinytag import TinyTag

class ChooseSong:
    """"this class holds the song reference list and
    the current playlist. it handles updating the order
    given new songs and picking the next song."""
    def __init__(self, reference_list, song_file_path):
        self._song_file_path = song_file_path
        self._reference_list = self.determine_valid_format(reference_list)
        self._play_list = []

    def get_play_list(self):
        return self._play_list

    def get_play_list(self):
        return self._play_list

    def determine_valid_format(self, song_list):
        """loops through the incoming song reference
        list to determine if the file format is valid
        for playing as an audio file."""
        valid_song_list = []
        for song in song_list:
            if "." in song:
                possible_song = song
                possible_song = possible_song[::-1]
                possible_song = possible_song.split(".")
                file_format = possible_song[0][::-1]
                if file_format == "m4a" or \
                   file_format == "mp3":
                    valid_song_list.append(song)
        return valid_song_list

    def update_current_order(self, new_song_list):
        """given a new list of song arrivals, if the
        song is in the reference song list, it is added
        to the end of the playlist"""
        for song in new_song_list:
            if song in self._reference_list:
                self._play_list.append(song)

    def pick_next_song(self):
        """this method takes the first entry
        of the playlist, removes it, then returns
        it to played. also functions as a skip
        button. if no songs are in the playlist,
        a random song is played from the reference
        list"""
        if len(self._play_list) < 1:
            reference_length = len(self._reference_list)
            rand_int = random.randint(0, reference_length - 1)
            print(self._reference_list[rand_int])
            return self._reference_list[rand_int]
        next_song = self._play_list[0]
        print(next_song)
        print(self._play_list)
        self._play_list.pop(0)
        print(self._play_list)
        return next_song

    def play_song(self, song):
        """given a song, the song is located in the
        file structure and played. the length of the
        song and the start-time are returned."""
        webbrowser.open(self._song_file_path + song)
        tag = TinyTag.get(self._song_file_path + song)
        print(tag.duration)
        return tag.duration, time.time()
        
        
        
