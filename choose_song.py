class ChooseSong:
    """"this class holds the song reference list and
    the current playlist. it handles updating the order
    given new songs and picking the next song."""
    def __init__(self, reference_list):
        self._reference_list = reference_list
        self._play_list = []

    def get_play_list(self):
        return self._play_list

    def get_play_list(self):
        return self._play_list

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
        button."""
        next_song = self._play_list[0]
        print(next_song)
        print(self._play_list)
        self._play_list.pop(0)
        print(self._play_list)
        return next_song
        
        
        
