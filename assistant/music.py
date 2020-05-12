import spotipy
from spotipy.oauth2 import SpotifyOAuth
from pprint import pprint
from time import sleep
import spotipy.util as util

util.prompt_for_user_token('Oculus',
                           'streaming',
                           client_id='4876797530b244f1888967346b4ce1fd',
                           client_secret='235a3ef81629464e8d75e1c57b5f4d65',
                           redirect_uri='https://open.spotify.com/track/5JKU2tXiG3yvJtefNwe7ZQ')



    scope = "user-read-playback-state,user-modify-playback-state"
    sp = spotipy.Spotify(client_credentials_manager=SpotifyOAuth(scope=scope))

    # Shows playing devices
    res = sp.devices()
    pprint(res)

    # Change track
    sp.start_playback(uris=['spotify:track:6gdLoMygLsgktydTQ71b15'])

    # Change volume
    sp.volume(100)
    sleep(2)
    sp.volume(50)
    sleep(2)
    sp.volume(100)
