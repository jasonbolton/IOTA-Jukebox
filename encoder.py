from iota import TryteString
import os

class Encoder:
    """this class is used to encode reference lists and
    playlists to send as transactions to the tangle. it
    also decodes the song messages sent from voters."""
    def __init__(self):
        pass

    def encode_play_list(self, play_list):
        """encodes the current play list to send to the tangle."""
        encoded_play_list = "::"
        for song in play_list:
            encoded_play_list += song
            encoded_play_list += ":"
        encoded_play_list += ":"
        print(encoded_play_list)
        encoded_play_list = TryteString.from_unicode(encoded_play_list)
        print(encoded_play_list)
        return encoded_play_list

    def encode_reference_list(self, reference_list):
        """encodes the song reference list to send to the tangle."""
        encoded_ref_list = "**"
        for song in reference_list:
            encoded_ref_list += song
            encoded_ref_list += "*"
        encoded_ref_list += "*"
        encoded_ref_list = TryteString.from_unicode(encoded_ref_list)
        return encoded_ref_list

    def decode_list(self, song_list):
        """decodes a list of messages from the tangle. if the
        song contains the song trytes 'IBIB' they're added to
        the decoded_list to be played."""
        decoded_list = []
        for song in song_list:
            print(song)
            if "IBIB" in song:
                print(song)
                song = TryteString.from_unicode(song)
                song = song.decode()
                print(song)
                song = song.strip("??")
                print(song)
                decoded_list.append(song)
        return decoded_list






