FILENAME = "Pink_Floyd_DB.txt"

file = open(FILENAME, 'r')
DATA = file.read()
file.close()

ALBUM_NOT_FOUND_ERROR = "ERROR# Album not found"
SONG_NOT_FOUND_ERROR = "ERROR# Song not found"
NO_SONG_WITH_WORD_ERROR = "ERROR# there are no song names including this word"
NO_LYRICS_WITH_WORD_ERROR = "ERROR# no songs including that word in the lyrics"

albums_dict = {}
songs_dict = {}

for album in DATA[1:].split("#"):
    songs_list = []
    for line in album.split("\n"):
        if '*' in line:
            songs_list.append(line.split("::")[0][1:])
    albums_dict[album.split("::")[0]] = ", ".join(songs_list)

for song in DATA.split("*"):
    if "#" not in song:
        song_data = {}
        song_data["length"] = song.split("::")[2]
        song_data["lyrics"] = "\n".join(song.split("\n")[1:-1])
        songs_dict[song.split("::")[0]] = song_data


def albums_list():
    """
    The following function will return the list of albums in the file
    :return: The message that should be given back to the user 
    :rtype: string
    """
    list_string = ""
    for album in albums_dict.keys():
        list_string += album + "\n"
    return "SEND_ALBUMS_LIST:{" + list_string + "}"


def album_songs_list(album_name):
    """
    The following function will return the songs within a given
    album
    :param album_name: The name of the album
    :type album_name: string
    :return: the message that should be given back to the user 
    :rtype: string
    """
    if not (album_name in albums_dict.keys()):
        return ALBUM_NOT_FOUND_ERROR
    message =  "SEND_ALBUM:{" + album_name + "}#songs_list:{" + albums_dict[album_name].replace(", ", "\n") + "}"
    # print(returning_string)
    return message

def song_data(song_name):
    """
    The following function will return information about a given song
    :param song_name: The name of the song
    :type song_name: string
    :return: the message that should be given back to the user
    :rtype: string
    """
    if not (song_name in songs_dict.keys()):
        return SONG_NOT_FOUND_ERROR
    message = "SEND_SONG:{" + song_name + "}#song_length:{" + songs_dict[song_name]["length"] + "}#song_lyrics:{" + songs_dict[song_name]["lyrics"] + "}"
    return message

def search_for_album(song_name):
    """
    The following function will return the album that the given
    song is from
    :param song_name: the name of the song
    :type song_name: a string
    :return: the message that should be given back to the user 
    :rtype: string
    """
    for album in albums_dict.keys():
        if song_name in albums_dict[album]:
            return album_songs_list(album)

def songs_with_word(word):
    """
    The following function will return the list of songs including the given word in their name
    :param word: the given word
    :type word: string
    :return: the message that should be given back to the user
    :rtype: string
    """
    song_list = ""
    for song_name in songs_dict.keys():
        if word in song_name:
            song_list += song_name + ","
    if song_list != "":
        message = "SEND_SONGS_LIST:{" + song_list + "}"
        return message
    return NO_SONG_WITH_WORD_ERROR

def lyrics_with_word(word):
    """
    The following function will return the list of songs including the given word in their lyrics
    :param word: the given word
    :type word: string
    :return: the message that should be given back to the user
    :rtype: string
    """
    song_list = ""
    for song in songs_dict.keys():
        if word in songs_dict[song]["lyrics"]:
            song_list += song + ","
    if song_list != "":
        message = "SEND_SONGS_LIST:{" + song_list + "}"
        return message
    return NO_LYRICS_WITH_WORD_ERROR

def word_statistics():
    common_words = {}
    for song in songs_dict.values():
        for word in song["lyrics"].split(" "):
            if word not in common_words:
                common_words[word] = 0
            common_words[word] += 1
    return str(common_words)
