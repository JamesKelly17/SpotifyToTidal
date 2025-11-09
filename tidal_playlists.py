"""
Tidal Playlists Module
Handles creating playlists and adding tracks to them on Tidal
"""

from tidal_auth import get_tidal_session
from tidal_tracks import search_track_on_tidal
from typing import Dict, List, Optional
import time


def create_playlist(name: str, description: str = "") -> Optional[object]:
    """
    Create a new playlist on Tidal
    
    Args:
        name: Name of the playlist
        description: Description of the playlist
        
    Returns:
        Tidal playlist object if successful, None otherwise
    """
    session = get_tidal_session()
    
    try:
        # Create the playlist
        user = session.user
        playlist = user.create_playlist(name, description)
        
        print(f"  ✓ Created playlist: {name}")
        return playlist
    except Exception as e:
        print(f"  ✗ Error creating playlist '{name}': {e}")
        return None


def add_tracks_to_playlist(playlist, tracks: List[Dict]) -> Dict[str, int]:
    """
    Add tracks to a Tidal playlist
    
    Args:
        playlist: Tidal playlist object
        tracks: List of track information from Spotify
        
    Returns:
        Dict containing statistics about the transfer
    """
    session = get_tidal_session()
    
    stats = {
        'total': len(tracks),
        'found': 0,
        'added': 0,
        'not_found': 0,
        'failed': 0
    }
    
    not_found_tracks = []
    found_track_ids = []
    
    print(f"  Searching for {stats['total']} tracks on Tidal...")
    
    # First, search for all tracks
    for i, track_info in enumerate(tracks, 1):
        track_name = track_info['name']
        artists = ", ".join(track_info['artists'])
        
        # Show progress every 10 tracks
        if i % 10 == 0 or i == stats['total']:
            print(f"    Searching... {i}/{stats['total']}")
        
        # Search for track on Tidal
        tidal_track = search_track_on_tidal(session, track_info)
        
        if tidal_track:
            stats['found'] += 1
            found_track_ids.append(tidal_track.id)
        else:
            stats['not_found'] += 1
            not_found_tracks.append(f"{track_name} by {artists}")
        
        # Small delay to avoid rate limiting
        if i % 20 == 0:
            time.sleep(0.5)
    
    print(f"  Found {stats['found']}/{stats['total']} tracks on Tidal")
    
    # Now add all found tracks to the playlist in batches
    if found_track_ids:
        print(f"  Adding {len(found_track_ids)} tracks to playlist...")
        
        try:
            # Add tracks to playlist (Tidal API typically accepts track IDs)
            # Note: The exact method might vary depending on tidalapi version
            playlist.add(found_track_ids)
            stats['added'] = len(found_track_ids)
            print(f"  ✓ Successfully added {stats['added']} tracks to playlist")
        except Exception as e:
            print(f"  ✗ Error adding tracks to playlist: {e}")
            # Try adding tracks one by one as fallback
            print("  Attempting to add tracks individually...")
            for track_id in found_track_ids:
                try:
                    playlist.add([track_id])
                    stats['added'] += 1
                except Exception as track_error:
                    stats['failed'] += 1
                    
            if stats['added'] > 0:
                print(f"  ✓ Successfully added {stats['added']} tracks individually")
    
    # Report tracks not found
    if not_found_tracks and len(not_found_tracks) <= 10:
        print(f"\n  Tracks not found on Tidal ({len(not_found_tracks)}):")
        for track in not_found_tracks:
            print(f"    - {track}")
    elif not_found_tracks:
        print(f"\n  {len(not_found_tracks)} tracks not found on Tidal")
    
    return stats


def transfer_playlist(spotify_playlist: Dict, spotify_tracks: List[Dict]) -> bool:
    """
    Transfer a complete playlist from Spotify to Tidal
    
    Args:
        spotify_playlist: Playlist information from Spotify
        spotify_tracks: List of tracks in the playlist
        
    Returns:
        bool: True if successful, False otherwise
    """
    print(f"\nTransferring playlist: {spotify_playlist['name']}")
    print("-" * 60)
    
    # Create the playlist on Tidal
    tidal_playlist = create_playlist(
        name=spotify_playlist['name'],
        description=spotify_playlist.get('description', '')
    )
    
    if not tidal_playlist:
        return False
    
    # Add tracks to the playlist
    if spotify_tracks:
        stats = add_tracks_to_playlist(tidal_playlist, spotify_tracks)
        
        # Print summary for this playlist
        print(f"\n  Playlist transfer summary:")
        print(f"    Total tracks: {stats['total']}")
        print(f"    Successfully added: {stats['added']}")
        print(f"    Not found: {stats['not_found']}")
        if stats['failed'] > 0:
            print(f"    Failed to add: {stats['failed']}")
        
        return stats['added'] > 0
    else:
        print("  No tracks to transfer (empty playlist)")
        return True


def get_user_playlists_tidal():
    """
    Get all user playlists from Tidal (useful for checking duplicates)
    
    Returns:
        List of Tidal playlist objects
    """
    session = get_tidal_session()
    
    try:
        user = session.user
        playlists = user.playlists()
        return playlists
    except Exception as e:
        print(f"Error fetching Tidal playlists: {e}")
        return []


def playlist_exists(playlist_name: str) -> bool:
    """
    Check if a playlist with the given name already exists on Tidal
    
    Args:
        playlist_name: Name of the playlist to check
        
    Returns:
        bool: True if playlist exists, False otherwise
    """
    playlists = get_user_playlists_tidal()
    
    for playlist in playlists:
        if playlist.name.lower() == playlist_name.lower():
            return True
    
    return False


if __name__ == "__main__":
    # Test creating a playlist
    session = get_tidal_session()
    
    test_playlist_name = "Test Playlist from Python"
    
    # Check if playlist already exists
    if playlist_exists(test_playlist_name):
        print(f"Playlist '{test_playlist_name}' already exists on Tidal")
    else:
        # Create a test playlist
        playlist = create_playlist(
            name=test_playlist_name,
            description="Created by Spotify to Tidal transfer tool"
        )
        
        if playlist:
            print(f"Successfully created playlist: {test_playlist_name}")
            
            # Test adding a track
            test_track = {
                'name': 'Blinding Lights',
                'artists': ['The Weeknd'],
                'album': 'After Hours',
                'isrc': None
            }
            
            print("\nTesting track addition...")
            stats = add_tracks_to_playlist(playlist, [test_track])
            print(f"Added {stats['added']} tracks to playlist")
