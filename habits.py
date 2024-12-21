import spotipy
from spotipy.oauth2 import SpotifyOAuth
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime
import dateutil.parser

# Spotify credentials
CLIENT_ID = 'f2d43d6bd63b433d9512a04c2bba3ff6'
CLIENT_SECRET = '7f306ac69e8c4b098d78e6e158fec41d'
REDIRECT_URI = 'http://127.0.0.1:5000/redirect'
scope = 'user-read-recently-played user-top-read'

# Authenticate and initialize the Spotipy client
sp = spotipy.Spotify(auth_manager=SpotifyOAuth(CLIENT_ID, CLIENT_SECRET, REDIRECT_URI, scope=scope))

def fetch_recent_tracks():
    # Fetch the user's recently played tracks
    recent_tracks = sp.current_user_recently_played(limit=50)['items']
    data = []
    for track in recent_tracks:
        # Convert ISO 8601 string to datetime object
        timestamp = dateutil.parser.isoparse(track['played_at'])
        track_name = track['track']['name']
        artist_name = ', '.join(artist['name'] for artist in track['track']['artists'])
        data.append([timestamp, track_name, artist_name])
    return pd.DataFrame(data, columns=['Timestamp', 'Track', 'Artist'])

def analyze_and_visualize(df):
    # Add additional columns for analysis
    df['Date'] = df['Timestamp'].dt.date
    df['Hour'] = df['Timestamp'].dt.hour
    df['DayOfWeek'] = df['Timestamp'].dt.day_name()

    # Count listens by hour of the day
    plt.figure(figsize=(12, 6))
    sns.countplot(x='Hour', data=df, palette='viridis')
    plt.title('Number of Tracks Played by Hour of the Day')
    plt.xlabel('Hour of the Day')
    plt.ylabel('Count')
    plt.show()

    # Count listens by day of the week
    plt.figure(figsize=(12, 6))
    sns.countplot(x='DayOfWeek', data=df, palette='viridis', order=['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday'])
    plt.title('Number of Tracks Played by Day of the Week')
    plt.xlabel('Day of the Week')
    plt.ylabel('Count')
    plt.show()

    # Count listens by artist
    top_artists = df['Artist'].value_counts().head(10)
    plt.figure(figsize=(12, 8))
    sns.barplot(x=top_artists.values, y=top_artists.index, palette='viridis')
    plt.title('Top 10 Artists by Number of Plays')
    plt.xlabel('Count')
    plt.ylabel('Artist')
    plt.show()

def provide_insights(df):
    # Provide insights based on the analysis
    hours_count = df['Hour'].value_counts().sort_index()
    most_played_hour = hours_count.idxmax()
    days_count = df['DayOfWeek'].value_counts()
    most_played_day = days_count.idxmax()

    print(f"You listen to music the most at {most_played_hour}:00 hours.")
    print(f"You listen to music the most on {most_played_day}.")

# Fetch recent tracks
recent_tracks_df = fetch_recent_tracks()

# Analyze and visualize the data
analyze_and_visualize(recent_tracks_df)

# Provide insights
provide_insights(recent_tracks_df)
