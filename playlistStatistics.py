import spotipy
import time
from spotipy.oauth2 import SpotifyOAuth
from collections import Counter
from flask import Flask, request, url_for, session, redirect

# Initialize Flask app
app = Flask(__name__)

# Set the name of the session cookie
app.config['SESSION_COOKIE_NAME'] = 'Spotify Cookie'

# Set a random secret key to sign the cookie
app.secret_key = 'IamJoseMourinho'

# Set the key for the token info in the session dictionary
TOKEN_INFO = 'token_info'

# Spotify API credentials
CLIENT_ID = 'SPOTIFY_CLIENT_ID'
CLIENT_SECRET = 'SPOTIFY_CLIENT_SECRET'
REDIRECT_URI = 'http://localhost:5000/redirect'
SCOPE = 'playlist-read-private user-library-read'

# Route to handle logging in
@app.route('/')
def login():
    auth_url = create_spotify_oauth().get_authorize_url()
    return redirect(auth_url)

# Route to handle the redirect URI after authorization
@app.route('/redirect')
def redirect_page():
    session.clear()
    code = request.args.get('code')
    token_info = create_spotify_oauth().get_access_token(code)
    session[TOKEN_INFO] = token_info
    return redirect(url_for('track_playlist_statistics', _external=True))

# Route to calculate and display playlist statistics
@app.route('/trackPlaylistStatistics')
def track_playlist_statistics():
    try:
        token_info = get_token()
    except:
        return redirect('/')

    sp = spotipy.Spotify(auth=token_info['access_token'])
    playlist_id = '7gilgMldwWCdJddW082jwz'  # Replace with your playlist ID
    playlist = sp.playlist_items(playlist_id)

    durations = []
    artists = []
    genres = []

    for item in playlist['items']:
        track = item['track']
        durations.append(track['duration_ms'])
        artists.extend(artist['name'] for artist in track['artists'])
        for artist in track['artists']:
            artist_info = sp.artist(artist['id'])
            genres.extend(artist_info['genres'])

    average_duration = sum(durations) / len(durations) if durations else 0
    most_common_artists = Counter(artists).most_common(10)
    most_common_genres = Counter(genres).most_common(10)

    stats = {
        'average_duration': average_duration,
        'most_common_artists': most_common_artists,
        'most_common_genres': most_common_genres
    }

    return stats

# Function to get the token info from the session
def get_token():
    token_info = session.get(TOKEN_INFO, None)
    if not token_info:
        redirect(url_for('login', _external=False))
    
    now = int(time.time())
    is_expired = token_info['expires_at'] - now < 60
    if is_expired:
        spotify_oauth = create_spotify_oauth()
        token_info = spotify_oauth.refresh_access_token(token_info['refresh_token'])

    return token_info

def create_spotify_oauth():
    return SpotifyOAuth(
        client_id=CLIENT_ID,
        client_secret=CLIENT_SECRET,
        redirect_uri=url_for('redirect_page', _external=True),
        scope=SCOPE
    )

if __name__ == '__main__':
    app.run(debug=True)
