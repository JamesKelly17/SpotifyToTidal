# Spotify to Tidal Transfer Tool

A Python tool to transfer your liked songs from Spotify to Tidal.

## Features

- Transfers all your Spotify liked songs to Tidal favorites
- Uses ISRC codes for accurate track matching when available
- Falls back to track name and artist search
- Provides detailed progress reporting
- Shows which tracks couldn't be found on Tidal
- Saves authentication sessions for future use

## Prerequisites

- Python 3.7 or higher
- A Spotify account with liked songs
- A Tidal account (subscription required)
- Spotify API credentials (Client ID and Client Secret)

## Setup

### 1. Clone the Repository

```bash
git clone <your-repo-url>
cd spotify-tidal-transfer
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

### 3. Set Up Spotify API Credentials

1. Go to [Spotify Developer Dashboard](https://developer.spotify.com/dashboard)
2. Log in with your Spotify account
3. Click "Create an App"
4. Fill in the app name and description
5. Once created, you'll see your **Client ID** and **Client Secret**
6. Click "Edit Settings"
7. Add `http://localhost:8888/callback` to the Redirect URIs
8. Click "Save"

### 4. Configure Environment Variables

1. Copy the example environment file:
   ```bash
   cp .env.example .env
   ```

2. Edit the `.env` file and add your credentials:
   ```
   SPOTIFY_CLIENT_ID=your_spotify_client_id_here
   SPOTIFY_CLIENT_SECRET=your_spotify_client_secret_here
   SPOTIFY_REDIRECT_URI=http://localhost:8888/callback
   ```

## Usage

### Test Connections

Before transferring, test that both Spotify and Tidal connections work:

```bash
python main.py --test
```

### Preview Your Liked Songs

Preview the first 10 songs that will be transferred:

```bash
python main.py --preview 10
```

### Transfer All Songs

Transfer all your liked songs from Spotify to Tidal:

```bash
python main.py
```

You will be prompted to confirm before the transfer starts.

### Transfer Limited Number of Songs

For testing, you can limit the transfer to the first N songs:

```bash
python main.py --limit 50
```

## How It Works

1. **Spotify Authentication**: The tool uses OAuth 2.0 to authenticate with Spotify. On first run, a browser window will open for you to authorize the application.

2. **Fetch Liked Songs**: Retrieves all your liked songs from Spotify, including track names, artists, albums, and ISRC codes.

3. **Tidal Authentication**: Uses OAuth 2.0 to authenticate with Tidal. A browser window will open for authorization on first run.

4. **Track Matching**: For each Spotify track:
   - First tries to match using ISRC code (most accurate)
   - Falls back to searching by track name and artist
   - Compares results to find the best match

5. **Add to Favorites**: Adds matched tracks to your Tidal favorites.

## Authentication

### Spotify

- On first run, a browser window will open
- Log in with your Spotify account and authorize the app
- The authentication token is cached in `.cache` file
- The token is automatically refreshed when needed

### Tidal

- On first run, you'll get a URL to visit
- Log in with your Tidal account and authorize the app
- The session is saved in `tidal_session.json`
- The session persists across runs

## Troubleshooting

### "Missing Spotify credentials" Error

Make sure your `.env` file exists and contains valid `SPOTIFY_CLIENT_ID` and `SPOTIFY_CLIENT_SECRET`.

### Spotify Authorization Failed

1. Check that `http://localhost:8888/callback` is added to your Spotify app's Redirect URIs
2. Make sure no other application is using port 8888

### Tidal Login Issues

1. Make sure you have an active Tidal subscription
2. Try deleting `tidal_session.json` and logging in again

### Tracks Not Found on Tidal

Some tracks may not be available on Tidal due to:
- Regional licensing restrictions
- Different track versions or remasters
- Tracks not available in Tidal's catalog

The tool will show a list of tracks that couldn't be found at the end of the transfer.

## File Structure

```
.
├── main.py                 # Main script to run the transfer
├── spotify_auth.py         # Spotify authentication module
├── spotify_tracks.py       # Fetch liked songs from Spotify
├── tidal_auth.py           # Tidal authentication module
├── tidal_tracks.py         # Search and add tracks to Tidal
├── requirements.txt        # Python dependencies
├── .env.example           # Example environment variables
├── .env                   # Your credentials (not in git)
├── .gitignore            # Git ignore file
└── README.md             # This file
```

## Privacy & Security

- Your Spotify and Tidal credentials are stored locally in `.env` file
- Authentication tokens are cached locally
- No data is sent to third parties
- The `.gitignore` file ensures credentials are not committed to git

## License

This project is open source and available under the MIT License.

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## Acknowledgments

- [Spotipy](https://github.com/plamere/spotipy) - Spotify Web API wrapper
- [python-tidal](https://github.com/tamland/python-tidal) - Tidal API wrapper
