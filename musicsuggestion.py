import spotipy
from spotipy.oauth2 import SpotifyOAuth

# Spotify credentials
CLIENT_ID = 'SPOTIFY_CLIENT_ID'
CLIENT_SECRET = 'SPOTIFY_CLIENT_SECRET'
REDIRECT_URI = 'http://127.0.0.1:5000/redirect'
scope = 'playlist-modify-public user-library-read user-top-read user-read-recently-played'

# Authenticate and initialize the Spotipy client
sp = spotipy.Spotify(auth_manager=SpotifyOAuth(CLIENT_ID, CLIENT_SECRET, REDIRECT_URI, scope=scope))

def suggest_new_music():
    # Fetch the user's recently played tracks
    recent_tracks = sp.current_user_recently_played(limit=10)['items']

    if not recent_tracks:
        print("No recent tracks found.")
        return

    # Get unique artist IDs from the recently played tracks
    artist_ids = list(set(track['track']['artists'][0]['id'] for track in recent_tracks))

    recommendations = []
    track_uris = []  # List to store URIs of recommended tracks

    for artist_id in artist_ids:
        related_artists = sp.artist_related_artists(artist_id)['artists']
        recommendations.extend(related_artists[:3])  # Get top 3 related artists

    if not recommendations:
        print("No recommendations found.")
        return

    print("Recommended Artists and Sample Tracks:")
    for artist in recommendations:
        print(f"Artist: {artist['name']}")
        top_tracks = sp.artist_top_tracks(artist['id'])['tracks']
        for track in top_tracks[:2]:  # Collect URIs of the top 2 tracks for each artist
            print(f"  Track: {track['name']}")
            track_uris.append(track['uri'])  # Add the track URI to the list
        print('-' * 30)

    if not track_uris:
        print("No tracks to add to the playlist.")
        return

    # Create a new playlist
    user_id = sp.current_user()['id']
    playlist_name = "Recommended Music Playlist"
    playlist = sp.user_playlist_create(user_id, playlist_name, public=True)

    # Add the recommended tracks to the playlist
    sp.playlist_add_items(playlist_id=playlist['id'], items=track_uris)

    print(f"Playlist '{playlist_name}' created with {len(track_uris)} tracks.")

# Execute the suggestion and playlist creation function
suggest_new_music()
