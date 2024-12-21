# Spotify Python Projects

This repository contains multiple Python scripts showcasing different functionalities built using the Spotify API. Below is an overview of each script and its purpose.

## Prerequisites

Before running the scripts, ensure the following:

1. **Spotify Developer Account:** Create a Spotify Developer account and register your app to get your `client_id` and `client_secret`.
2. **Python Environment:** Install the required libraries by running:
   ```bash
   pip install spotipy flask pandas matplotlib seaborn
   ```
3. Replace the placeholders for `CLIENT_ID`, `CLIENT_SECRET`, and `REDIRECT_URI` with your Spotify app credentials in the scripts.

---

## 1. Flask Application: Saving Discover Weekly Songs

### Features:

- Logs in users to their Spotify account.
- Fetches the "Discover Weekly" playlist and saves the tracks to a "Saved Weekly" playlist.

### Endpoints:

- `/`: Login route.
- `/redirect`: Handles Spotify OAuth callback.
- `/saveDiscoverWeekly`: Saves "Discover Weekly" songs to a new playlist.

### How to Run:

1. Start the Flask app:
   ```bash
   python app.py
   ```
2. Navigate to `http://127.0.0.1:5000` in your browser.

---

## 2. Analyze and Visualize Listening Habits

### Features:

- Fetches recently played tracks.
- Provides visualizations of:
  - Listening habits by hour of the day.
  - Listening trends by day of the week.
  - Top 10 most played artists.

### How to Run:

1. Replace your credentials in the script.
2. Execute the script:
   ```bash
   python analyze.py
   ```

### Example Insights:

- "You listen to music the most at 20:00 hours."
- "You listen to music the most on Saturday."

---

## 3. Music Recommendation Based on Recently Played Tracks

### Features:

- Fetches recently played tracks.
- Suggests related artists and their top tracks.
- Creates a playlist with recommended songs.

### How to Run:

1. Replace your credentials in the script.
2. Execute the script:
   ```bash
   python recommend.py
   ```

---

## 4. Playlist Creation Based on Genre

### Features:

- Fetches the user’s top tracks.
- Filters tracks based on a specified genre.
- Creates a new playlist with songs matching the genre.

### How to Run:

1. Replace your credentials in the script.
2. Execute the script and specify the genre:
   ```bash
   python genre_playlist.py
   ```

---

## 5. Playlist Statistics

### Features:

- Fetches all tracks from a specified playlist.
- Analyzes:
  - Average track duration.
  - Most common artists.
  - Most common genres.

### How to Run:

1. Replace your credentials and playlist ID in the script.
2. Start the Flask app:
   ```bash
   python playlist_stats.py
   ```
3. Navigate to `http://127.0.0.1:5000`.

---

## Note

Ensure to protect your credentials. Do not hardcode sensitive information into your scripts when sharing or deploying. Use environment variables or configuration files.

---

## License

This repository is licensed under the MIT License.
