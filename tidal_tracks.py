"""
Tidal Tracks Module
Handles searching for and adding tracks to Tidal
"""

from tidal_auth import get_tidal_session
from typing import Dict, List, Optional
import time


def search_track_on_tidal(session, track_info: Dict) -> Optional[object]:
    """
    Search for a track on Tidal

    Args:
        session: Authenticated Tidal session
        track_info: Dictionary containing track information from Spotify

    Returns:
        Tidal track object if found, None otherwise
    """
    # Try searching with ISRC first (most accurate)
    if track_info.get('isrc'):
        try:
            results = session.search('track', track_info['isrc'])
            if results and len(results) > 0:
                return results[0]
        except Exception:
            pass  # ISRC search failed, continue to other methods

    # Try searching with track name and artist
    query = f"{track_info['name']} {track_info['artists'][0]}"

    try:
        results = session.search('track', query)

        if not results or len(results) == 0:
            return None

        # Try to find the best match
        for result in results[:5]:  # Check top 5 results
            # Check if artist matches
            result_artists = [artist.name.lower() for artist in result.artists]
            spotify_artists = [artist.lower() for artist in track_info['artists']]

            # Check if track name matches (case-insensitive, allowing for slight variations)
            track_name_match = result.name.lower().strip() == track_info['name'].lower().strip()

            # Check if at least one artist matches
            artist_match = any(
                spotify_artist in result_artist or result_artist in spotify_artist
                for spotify_artist in spotify_artists
                for result_artist in result_artists
            )

            if track_name_match and artist_match:
                return result

        # If no exact match, return the first result
        return results[0]

    except Exception as e:
        print(f"Error searching for track: {e}")
        return None


def add_track_to_favorites(session, track) -> bool:
    """
    Add a track to Tidal favorites

    Args:
        session: Authenticated Tidal session
        track: Tidal track object

    Returns:
        bool: True if successful, False otherwise
    """
    try:
        user = session.user
        user.favorites.add_track(track.id)
        return True
    except Exception as e:
        print(f"Error adding track to favorites: {e}")
        return False


def transfer_tracks(spotify_tracks: List[Dict]) -> Dict[str, int]:
    """
    Transfer Spotify tracks to Tidal favorites

    Args:
        spotify_tracks: List of track information from Spotify

    Returns:
        Dict containing statistics about the transfer
    """
    session = get_tidal_session()

    stats = {
        'total': len(spotify_tracks),
        'found': 0,
        'added': 0,
        'not_found': 0,
        'failed': 0
    }

    not_found_tracks = []

    print(f"\nStarting transfer of {stats['total']} tracks to Tidal...")
    print("=" * 60)

    for i, track_info in enumerate(spotify_tracks, 1):
        track_name = track_info['name']
        artists = ", ".join(track_info['artists'])

        print(f"\n[{i}/{stats['total']}] {track_name} by {artists}")

        # Search for track on Tidal
        tidal_track = search_track_on_tidal(session, track_info)

        if tidal_track:
            stats['found'] += 1
            print(f"  ✓ Found on Tidal: {tidal_track.name} by {tidal_track.artist.name}")

            # Add to favorites
            if add_track_to_favorites(session, tidal_track):
                stats['added'] += 1
                print(f"  ✓ Added to favorites")
            else:
                stats['failed'] += 1
                print(f"  ✗ Failed to add to favorites")
        else:
            stats['not_found'] += 1
            not_found_tracks.append(f"{track_name} by {artists}")
            print(f"  ✗ Not found on Tidal")

        # Small delay to avoid rate limiting
        if i % 10 == 0:
            time.sleep(1)

    # Print summary
    print("\n" + "=" * 60)
    print("Transfer Complete!")
    print("=" * 60)
    print(f"Total tracks: {stats['total']}")
    print(f"Found on Tidal: {stats['found']}")
    print(f"Successfully added: {stats['added']}")
    print(f"Not found: {stats['not_found']}")
    print(f"Failed to add: {stats['failed']}")

    if not_found_tracks:
        print(f"\nTracks not found on Tidal ({len(not_found_tracks)}):")
        for track in not_found_tracks[:20]:  # Show first 20
            print(f"  - {track}")
        if len(not_found_tracks) > 20:
            print(f"  ... and {len(not_found_tracks) - 20} more")

    return stats


if __name__ == "__main__":
    # Test searching for a track
    session = get_tidal_session()
    test_track = {
        'name': 'Blinding Lights',
        'artists': ['The Weeknd'],
        'album': 'After Hours',
        'isrc': None
    }

    print("Testing track search...")
    result = search_track_on_tidal(session, test_track)
    if result:
        print(f"Found: {result.name} by {result.artist.name}")
    else:
        print("Track not found")
