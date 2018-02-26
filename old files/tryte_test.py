from iota import *
import random

##message = "9"
##print(TryteString.from_unicode(message))
##print(TryteString(message))
##random_string = ""
##song = "?" + song
##for i in range(13 - 2 * len(song)):
##    rand_char = chr(random.randint(80, 90))
##    random_string += rand_char

string = "???KILLERISME.m4a"
string3 = "???"


string = TryteString.from_unicode(string)
print(string)
string = string.decode()
string3 = TryteString.from_unicode(string3)
print(string3)
string3 = string3.decode()

print(string)
