# Playlist Transfer - Quick Start Guide

This guide will help you get started with transferring playlists from Spotify to Tidal.

## Quick Setup

### 1. Ensure Prerequisites are Met

Make sure you have:
- Installed all requirements: `pip install -r requirements.txt`
- Set up your `.env` file with Spotify API credentials
- Both Spotify and Tidal accounts authenticated

### 2. Test the Playlist Functionality

Run the test script to verify everything works:

```bash
python test_playlists.py
```

This will:
- Test fetching playlists from Spotify
- Test creating playlists on Tidal
- Verify all components are working

## Usage Examples

### Transfer All Your Playlists

```bash
python main.py --playlists --all-playlists
```

### Interactive Selection

Choose which playlists to transfer:

```bash
python main.py --playlists
```

You'll see something like:
```
Found 10 playlist(s):
------------------------------------------------------------
1. Summer Vibes 2024 - 45 tracks - Public
2. Workout Mix - 30 tracks - Private
3. Chill Evening - 68 tracks - Public
4. Road Trip Songs - 120 tracks - Public (Collaborative)
5. Study Focus - 25 tracks - Private

Which playlists would you like to transfer?
Enter playlist numbers separated by commas (e.g., 1,3,5)
Or enter 'all' to transfer all playlists: 
```

### Transfer Specific Number of Playlists

Transfer only your first 3 playlists:

```bash
python main.py --playlists --playlist-limit 3
```

### Handle Existing Playlists

If playlists with the same names already exist on Tidal:

```bash
# Skip existing playlists (default behavior)
python main.py --playlists

# Or create duplicates anyway
python main.py --playlists --overwrite
```

### Combined Transfer

Transfer both liked songs and playlists:

```bash
python main.py --likes --playlists
```

## What to Expect

### During Transfer

The tool will show progress for each playlist:

```
Transferring playlist: Summer Vibes 2024
------------------------------------------------------------
  ✓ Created playlist: Summer Vibes 2024
  Searching for 45 tracks on Tidal...
    Searching... 10/45
    Searching... 20/45
    Searching... 30/45
    Searching... 40/45
    Searching... 45/45
  Found 43/45 tracks on Tidal
  Adding 43 tracks to playlist...
  ✓ Successfully added 43 tracks to playlist

  Playlist transfer summary:
    Total tracks: 45
    Successfully added: 43
    Not found: 2

  Tracks not found on Tidal (2):
    - Rare Demo Track by Underground Artist
    - Local Band Song by Garage Band
```

### After Transfer

You'll see a final summary:

```
============================================================
Playlist Transfer Complete!
============================================================
Successfully transferred: 8 playlist(s)
Failed: 2 playlist(s)
```

## Tips for Best Results

### 1. Start Small
Test with a few playlists first:
```bash
python main.py --playlists --playlist-limit 2
```

### 2. Check for Duplicates
The tool warns about existing playlists by default. Decide whether to skip or create duplicates.

### 3. Verify Results
After transfer, check your Tidal account to ensure playlists appear correctly.

### 4. Handle Missing Tracks
Some tracks might not be available on Tidal due to:
- Regional restrictions
- Different versions/remasters
- Exclusive content

The tool reports which tracks couldn't be found.

## Troubleshooting

### "No playlists found"
- Make sure you have playlists in your Spotify account
- Check that the playlists are created by you (not just followed)

### "Failed to create playlist"
- Verify your Tidal subscription is active
- Try re-authenticating by deleting `tidal_session.json`

### Slow Transfer Speed
- Normal behavior - the tool includes delays to avoid rate limiting
- Expect approximately 1-2 minutes per 100 tracks

### Too Many Playlists
If you have many playlists, transfer them in batches:
```bash
# First batch
python main.py --playlists --playlist-limit 10

# Next batch (will show remaining playlists)
python main.py --playlists --playlist-limit 10
```

## Advanced Options

### Automated Transfers
Create a script to transfer playlists regularly:

```bash
#!/bin/bash
# transfer_playlists.sh
python main.py --playlists --all-playlists --overwrite
```

### Selective Transfer
For more control, modify the code to filter playlists by:
- Creation date
- Number of tracks
- Public/private status
- Specific keywords in names

## Need Help?

1. Run the test script: `python test_playlists.py`
2. Check the main README for detailed documentation
3. Enable verbose output by adding print statements in the code
4. Check the GitHub issues for similar problems

## Happy Transferring! 🎵

Your music library awaits on Tidal!
