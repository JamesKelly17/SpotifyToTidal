"""
Spotify Tracks Module
Fetches liked songs from Spotify
"""

from spotify_auth import get_spotify_client
from typing import List, Dict


def get_liked_songs() -> List[Dict]:
    """
    Fetch all liked songs from Spotify

    Returns:
        List[Dict]: List of track information dictionaries
    """
    spotify = get_spotify_client()
    liked_songs = []
    offset = 0
    limit = 50  # Max allowed by Spotify API

    print("Fetching liked songs from Spotify...")

    while True:
        # Fetch a batch of liked songs
        results = spotify.current_user_saved_tracks(limit=limit, offset=offset)

        if not results['items']:
            break

        # Process each track
        for item in results['items']:
            track = item['track']

            # Extract relevant information
            track_info = {
                'name': track['name'],
                'artists': [artist['name'] for artist in track['artists']],
                'album': track['album']['name'],
                'isrc': track.get('external_ids', {}).get('isrc'),  # International Standard Recording Code
                'duration_ms': track['duration_ms'],
                'spotify_id': track['id'],
                'spotify_uri': track['uri']
            }

            liked_songs.append(track_info)

        print(f"Fetched {len(liked_songs)} songs so far...")

        # Check if there are more songs to fetch
        if results['next'] is None:
            break

        offset += limit

    print(f"Total liked songs fetched: {len(liked_songs)}")
    return liked_songs


def display_track_info(track: Dict) -> str:
    """
    Format track information for display

    Args:
        track: Track information dictionary

    Returns:
        str: Formatted track information
    """
    artists_str = ", ".join(track['artists'])
    return f"{track['name']} by {artists_str} (Album: {track['album']})"


if __name__ == "__main__":
    # Test fetching liked songs
    try:
        songs = get_liked_songs()
        print("\nFirst 5 songs:")
        for i, song in enumerate(songs[:5], 1):
            print(f"{i}. {display_track_info(song)}")
    except Exception as e:
        print(f"Error fetching liked songs: {e}")
