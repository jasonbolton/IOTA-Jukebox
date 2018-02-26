import webbrowser
import time
from tinytag import TinyTag

class PlaySong:

    def __init__(self):
        pass

    def play_song(self, song):
        webbrowser.open("C:\\Users\Honey Booboo\\Desktop\\songs\\" \
                        + song)
        tag = TinyTag.get("C:\\Users\Honey Booboo\\Desktop\\songs\\" \
                        + song)
        print(tag.duration)
        return tag.duration, time.time()
        
        
