import spotipy
from spotipy.oauth2 import SpotifyOAuth
import logging

logger = logging.getLogger('recommendations')
logging.basicConfig(level='INFO')


def get_top_artists(time_range, limit, sp):
    artist_list = []
    results = sp.current_user_top_artists(time_range=time_range, limit=limit)
    for artist in results['items']:
        artist_list.append(artist)
    return artist_list


def get_related_artists_for_artist(artist, sp):
    related_artist = []
    results = sp.artist_related_artists(artist["uri"])
    for artist in results['artists']:
        related_artist.append(artist)
    return related_artist


def show_recommendations_for_artist(artist, sp):
    # print(artist)
    track_list = []
    results = sp.recommendations(seed_artists=[artist['id']])
    for track in results['tracks']:
        track_list.append(track)
        # logger.info('Recommendation: %s - %s', track['name'],
        #             track['artists'][0]['name'])
    return track_list


def create_playlist(name, sp):
    user_id = sp.me()['id']
    sp.user_playlist_create(user_id, name)


def add_tracks_to_playlist(playlist, tracks, sp):
    sp.playlist_add_items(playlist, tracks)


def list_playlists(sp):
    playlists = sp.user_playlists(sp.me()['id'])
    while playlists:
        for i, playlist in enumerate(playlists['items']):
            print("%4d %s %s" % (
                i + 1 + playlists['offset'], playlist['uri'],  playlist['name']))
        if playlists['next']:
            playlists = sp.next(playlists)
        else:
            playlists = None


def main():
    scope = ["user-top-read", "playlist-modify-public"]
    sp = spotipy.Spotify(auth_manager=SpotifyOAuth(
        scope=scope, open_browser=False))

    # list_playlists(sp)
    long_list = get_top_artists('long_term', 5, sp)
    medium_list = get_top_artists('medium_term', 5, sp)
    short_list = get_top_artists('short_term', 5, sp)
    artist_list = long_list + medium_list + short_list
    ids = []
    unique = []
    for i in artist_list:
        name = i["name"]
        if name not in ids:
            print(name)
            ids.append(name)
            unique.append(i)
    artist_list = unique
    print(len(artist_list))

    tracks = []
    for artist in artist_list:
        related_artist_list = get_related_artists_for_artist(artist, sp)
        for related_artist in related_artist_list:
            result = show_recommendations_for_artist(related_artist, sp)
            tracks = tracks + result
    print(len(tracks))

    filter_tracks = []
    for track in tracks:
        filter_tracks.append(track["uri"])

    filter_tracks = set(filter_tracks)
    print("total")
    print(len(filter_tracks))
    for i in filter_tracks:
        # print(i)
        add_tracks_to_playlist(
            "spotify:playlist:1VNn0rYoYXw6Si21IL91tj", [i], sp)
    print("------------ END ------------")


main()
