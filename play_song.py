import webbrowser
import time
from tinytag import TinyTag

class PlaySong:
    """this class handles the playing of songs,
    using webbrowser library. i'm not sure which
    types of audio files are limited by this
    approach."""
    def __init__(self):
        pass

    def play_song(self, song):
        """given a song, the song is located in the
        file structure and played. the length of the
        song and the start-time are returned."""
        webbrowser.open("C:\\Users\Honey Booboo\\Desktop\\songs\\" \
                        + song)
        tag = TinyTag.get("C:\\Users\Honey Booboo\\Desktop\\songs\\" \
                        + song)
        print(tag.duration)
        return tag.duration, time.time()
        
        
