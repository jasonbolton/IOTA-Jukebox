class ChooseSong:

    def __init__(self, reference_list):
        self._reference_list = reference_list
        self._play_list = []

    def get_play_list(self):
        return self._play_list

    def get_play_list(self):
        return self._play_list

    def update_current_order(self, new_song_list):
        for song in new_song_list:
            if song in self._reference_list:
                self._play_list.append(song)

    def pick_next_song(self):
        next_song = self._play_list[0]
        print(next_song)
        print(self._play_list)
        self._play_list.pop(0)
        print(self._play_list)
        return next_song
        
        
        
