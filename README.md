# Spotify to Tidal Transfer Tool

A Python tool to transfer your liked songs and playlists from Spotify to Tidal.

## Features

- **Transfer Liked Songs**: Transfers all your Spotify liked songs to Tidal favorites
- **Transfer Playlists**: Transfer your Spotify playlists to Tidal with all their tracks
- **Accurate Matching**: Uses ISRC codes for accurate track matching when available
- **Smart Fallback**: Falls back to track name and artist search when ISRC unavailable
- **Detailed Progress**: Provides detailed progress reporting during transfers
- **Duplicate Detection**: Checks for existing playlists on Tidal before creating duplicates
- **Batch Processing**: Efficiently handles large music libraries
- **Session Persistence**: Saves authentication sessions for future use

## Prerequisites

- Python 3.7 or higher
- A Spotify account with liked songs and/or playlists
- A Tidal account (subscription required)
- Spotify API credentials (Client ID and Client Secret)

## Setup

### 1. Clone the Repository
```bash
git clone https://github.com/JamesKelly17/SpotifyToTidal.git
cd spotifyToTidal
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
7. Add `http://127.0.0.1:8888/callback` to the Redirect URIs
8. Select "Web API"
9. Click "Save"

### 4. Configure Environment Variables

1. Copy the example environment file:
   ```bash
   cp .env.example .env
   ```

2. Edit the `.env` file and add your credentials:
   ```bash
   nano .env
   ```

   Then update with account info:
   ```
   SPOTIFY_CLIENT_ID=your_spotify_client_id_here
   SPOTIFY_CLIENT_SECRET=your_spotify_client_secret_here
   SPOTIFY_REDIRECT_URI=http://127.0.0.1:8888/callback

   TIDAL_USERNAME=your_tidal_username_here
   TIDAL_PASSWORD=your_tidal_password_here
   ```

## Usage

### Interactive Mode

Run the tool without arguments for an interactive menu:
```bash
python main.py
```

You'll be prompted to choose what to transfer:
- Liked songs only
- Playlists only
- Both

### Test Connections

Before transferring, test that both Spotify and Tidal connections work:
```bash
python main.py --test
```

### Transfer Liked Songs

Transfer all your liked songs from Spotify to Tidal:
```bash
python main.py --likes
```

Transfer a limited number of songs (useful for testing):
```bash
python main.py --likes --limit 50
```

### Transfer Playlists

#### Interactive Playlist Selection

Choose which playlists to transfer interactively:
```bash
python main.py --playlists
```

The tool will:
1. Show all your Spotify playlists
2. Let you select which ones to transfer
3. Check for existing playlists on Tidal
4. Transfer the selected playlists with all their tracks

#### Transfer All Playlists

Transfer all playlists without prompting:
```bash
python main.py --playlists --all-playlists
```

#### Limit Number of Playlists

Transfer only the first N playlists:
```bash
python main.py --playlists --playlist-limit 5
```

#### Handle Duplicate Playlists

By default, the tool warns about existing playlists on Tidal. To create duplicates anyway:
```bash
python main.py --playlists --overwrite
```

### Transfer Both Liked Songs and Playlists

Transfer everything in one go:
```bash
python main.py --likes --playlists
```

Or use interactive mode and select option 3.

### Preview Mode

Preview the first N songs that would be transferred (without actually transferring):
```bash
python main.py --preview 10
```

## Command Line Options

| Option | Description |
|--------|-------------|
| `--likes` | Transfer liked songs |
| `--playlists` | Transfer playlists |
| `--test` | Test connections without transferring |
| `--preview N` | Preview first N liked songs |
| `--limit N` | Limit liked songs transfer to first N songs |
| `--all-playlists` | Transfer all playlists without asking |
| `--playlist-limit N` | Limit to first N playlists |
| `--overwrite` | Create duplicate playlists even if they exist |

## How It Works

### Authentication

1. **Spotify**: Uses OAuth 2.0 with automatic browser authorization
   - Token cached in `.cache` file
   - Automatically refreshes when needed

2. **Tidal**: Uses OAuth 2.0 with browser authorization
   - Session saved in `tidal_session.json`
   - Persists across runs

### Track Matching Algorithm

For each track, the tool:
1. First attempts to match using ISRC code (most accurate)
2. Falls back to searching by track name and artist
3. Compares results to find the best match
4. Verifies artist names to ensure accuracy

### Playlist Transfer Process

1. Fetches playlist metadata from Spotify
2. Creates corresponding playlist on Tidal
3. Retrieves all tracks from Spotify playlist
4. Searches for each track on Tidal
5. Adds found tracks to the Tidal playlist in batches
6. Reports any tracks that couldn't be found

## Troubleshooting

### "Missing Spotify credentials" Error

Ensure your `.env` file exists and contains valid `SPOTIFY_CLIENT_ID` and `SPOTIFY_CLIENT_SECRET`.

### Spotify Authorization Failed

1. Check that `http://127.0.0.1:8888/callback` is added to your Spotify app's Redirect URIs
2. Make sure no other application is using port 8888

### Tidal Login Issues

1. Ensure you have an active Tidal subscription
2. Try deleting `tidal_session.json` and logging in again

### Tracks Not Found on Tidal

Some tracks may not be available due to:
- Regional licensing restrictions
- Different track versions or remasters
- Exclusive content not in Tidal's catalog

The tool will show a summary of tracks that couldn't be found.

### Playlist Already Exists

When transferring playlists, the tool will:
1. Detect existing playlists with the same name
2. Give you options to skip, create duplicates, or cancel
3. Use `--overwrite` flag to always create duplicates

## File Structure

```
.
├── main.py                 # Main script to run the transfer
├── spotify_auth.py         # Spotify authentication module
├── spotify_tracks.py       # Fetch liked songs from Spotify
├── spotify_playlists.py    # Fetch playlists from Spotify
├── tidal_auth.py          # Tidal authentication module
├── tidal_tracks.py        # Search and add tracks to Tidal
├── tidal_playlists.py     # Create playlists and add tracks on Tidal
├── requirements.txt       # Python dependencies
├── .env.example          # Example environment variables
├── .env                  # Your credentials (not in git)
├── .gitignore           # Git ignore file
└── README.md            # This file
```

## Performance

- **Liked Songs**: Typically processes 100-200 tracks per minute
- **Playlists**: Transfer speed depends on playlist size
- **Rate Limiting**: Built-in delays to avoid API rate limits
- **Batch Processing**: Tracks are added to playlists in batches for efficiency

## Privacy & Security

- Your Spotify and Tidal credentials are stored locally in `.env` file
- Authentication tokens are cached locally
- No data is sent to third parties
- The `.gitignore` file ensures credentials are not committed to git

## Limitations

- Cannot transfer:
  - Podcast episodes
  - Local files not available on streaming services
  - Tidal-exclusive content to Spotify (one-way transfer only)
- Collaborative playlist settings are not preserved
- Playlist descriptions may be truncated based on Tidal's limits
- Private/public playlist settings are attempted to be preserved but may vary

## License

This project is open source and available under the MIT License.

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## Acknowledgments

- [Spotipy](https://github.com/plamere/spotipy) - Spotify Web API wrapper
- [python-tidal](https://github.com/tamland/python-tidal) - Tidal API wrapper

## Support

If you encounter any issues or have questions:
1. Check the Troubleshooting section above
2. Search existing [GitHub Issues](https://github.com/JamesKelly17/SpotifyToTidal/issues)
3. Create a new issue with detailed information about your problem
