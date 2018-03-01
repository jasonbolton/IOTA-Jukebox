import webbrowser
import time
from tinytag import TinyTag

class PlaySong:
    """this class handles the playing of songs,
    using webbrowser library. i'm not sure which
    types of audio files are limited by this
    approach."""
    def __init__(self, song_file_path):
        self._song_file_path = song_file_path

    def play_song(self, song):
        """given a song, the song is located in the
        file structure and played. the length of the
        song and the start-time are returned."""
        webbrowser.open(self._song_file_path + song)
        tag = TinyTag.get(self._song_file_path + song)
        print(tag.duration)
        return tag.duration, time.time()
        
        
