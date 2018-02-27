from iota import TryteString
import os

class Encoder:

    def __init__(self):
        pass

    def encode_play_list(self, play_list):
        encoded_play_list = "::"
        for song in play_list:
            encoded_play_list += song
            encoded_play_list += ":"
        encoded_play_list += ":"
        encoded_play_list = TryteString.from_unicode(encoded_play_list)
        return encoded_play_list

    def encode_reference_list(self, reference_list):
        encoded_ref_list = "**"
        for song in reference_list:
            encoded_ref_list += song
            encoded_ref_list += "*"
        encoded_ref_list += "*"
        encoded_ref_list = TryteString.from_unicode(encoded_ref_list)
        return encoded_ref_list

    def decode_list(self, song_list):
        return_list = []
        for song in song_list:
            print(song)
            if "IBIB" in song:
                print(song)
                song = TryteString.from_unicode(song)
                song = song.decode()
                print(song)
                song = song.strip("??")
                print(song)
##                if "?" in song:
##                    index = song.index("?")
##                    song = song[index+1:]
##                    print(song)
                return_list.append(song)
        return return_list






