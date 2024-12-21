import spotipy
from spotipy.oauth2 import SpotifyOAuth

# Spotify credentials
SPOTIPY_CLIENT_ID = 'f2d43d6bd63b433d9512a04c2bba3ff6'
SPOTIPY_CLIENT_SECRET = '7f306ac69e8c4b098d78e6e158fec41d'
SPOTIPY_REDIRECT_URI = 'http://127.0.0.1:5000/redirect'

scope = 'playlist-modify-public user-top-read user-read-recently-played'

# Authenticate and initialize the Spotipy client
sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=SPOTIPY_CLIENT_ID,
                                               client_secret=SPOTIPY_CLIENT_SECRET,
                                               redirect_uri=SPOTIPY_REDIRECT_URI,
                                               scope=scope))

def create_playlist_based_on_genre(genre):
    # Get the current user's ID
    user_id = sp.current_user()['id']

    # Fetch top tracks of the user
    top_tracks = sp.current_user_top_tracks(limit=50)['items']

    # Filter tracks by the specified genre
    genre_tracks = []
    for track in top_tracks:
        track_genres = sp.artist(track['artists'][0]['id'])['genres']
        print(f"Track: {track['name']}, Genres: {track_genres}")  # Debugging line
        if genre.lower() in [g.lower() for g in track_genres]:
            genre_tracks.append(track['uri'])

    # Handle case where no tracks match the genre
    if not genre_tracks:
        print(f"No tracks found for genre '{genre}'. Please try a different genre.")
        return

    # Create a new playlist
    playlist_name = f"{genre.capitalize()} Mood Playlist"
    playlist = sp.user_playlist_create(user_id, playlist_name, public=True)

    # Add tracks to the playlist
    sp.playlist_add_items(playlist_id=playlist['id'], items=genre_tracks)

    print(f"Playlist '{playlist_name}' created with {len(genre_tracks)} tracks.")

# Example usage
create_playlist_based_on_genre('tollywood')
