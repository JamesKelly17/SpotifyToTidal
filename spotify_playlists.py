"""
Spotify Playlists Module
Fetches user playlists and their tracks from Spotify
"""

from spotify_auth import get_spotify_client
from typing import List, Dict, Optional


def get_user_playlists(limit: Optional[int] = None) -> List[Dict]:
    """
    Fetch all user's playlists from Spotify
    
    Args:
        limit: Optional limit on number of playlists to fetch
        
    Returns:
        List[Dict]: List of playlist information dictionaries
    """
    spotify = get_spotify_client()
    playlists = []
    offset = 0
    batch_limit = 50  # Max allowed by Spotify API
    
    print("Fetching your playlists from Spotify...")
    
    while True:
        # Fetch a batch of playlists
        results = spotify.current_user_playlists(limit=batch_limit, offset=offset)
        
        if not results['items']:
            break
            
        for playlist in results['items']:
            # Only include playlists owned by the user
            if playlist['owner']['id'] == spotify.current_user()['id']:
                playlist_info = {
                    'id': playlist['id'],
                    'name': playlist['name'],
                    'description': playlist.get('description', ''),
                    'public': playlist['public'],
                    'collaborative': playlist['collaborative'],
                    'total_tracks': playlist['tracks']['total'],
                    'spotify_url': playlist['external_urls']['spotify']
                }
                playlists.append(playlist_info)
                
                if limit and len(playlists) >= limit:
                    break
        
        print(f"Fetched {len(playlists)} playlists so far...")
        
        if limit and len(playlists) >= limit:
            playlists = playlists[:limit]
            break
            
        # Check if there are more playlists to fetch
        if results['next'] is None:
            break
            
        offset += batch_limit
    
    print(f"Total playlists fetched: {len(playlists)}")
    return playlists


def get_playlist_tracks(playlist_id: str) -> List[Dict]:
    """
    Fetch all tracks from a specific playlist
    
    Args:
        playlist_id: Spotify playlist ID
        
    Returns:
        List[Dict]: List of track information dictionaries
    """
    spotify = get_spotify_client()
    tracks = []
    offset = 0
    limit = 100  # Max allowed by Spotify API for playlist tracks
    
    while True:
        # Fetch a batch of tracks
        results = spotify.playlist_tracks(playlist_id, limit=limit, offset=offset)
        
        if not results['items']:
            break
            
        # Process each track
        for item in results['items']:
            # Skip if track is None (deleted tracks)
            if item['track'] is None:
                continue
                
            track = item['track']
            
            # Skip if it's not a track (could be a podcast episode)
            if track['type'] != 'track':
                continue
            
            # Extract relevant information
            track_info = {
                'name': track['name'],
                'artists': [artist['name'] for artist in track['artists']],
                'album': track['album']['name'],
                'isrc': track.get('external_ids', {}).get('isrc'),
                'duration_ms': track['duration_ms'],
                'spotify_id': track['id'],
                'spotify_uri': track['uri']
            }
            
            tracks.append(track_info)
        
        # Check if there are more tracks to fetch
        if results['next'] is None:
            break
            
        offset += limit
    
    return tracks


def display_playlist_info(playlist: Dict) -> str:
    """
    Format playlist information for display
    
    Args:
        playlist: Playlist information dictionary
        
    Returns:
        str: Formatted playlist information
    """
    visibility = "Public" if playlist['public'] else "Private"
    collaborative = " (Collaborative)" if playlist['collaborative'] else ""
    return f"{playlist['name']} - {playlist['total_tracks']} tracks - {visibility}{collaborative}"


if __name__ == "__main__":
    # Test fetching playlists
    try:
        playlists = get_user_playlists(limit=5)
        print("\nYour playlists:")
        for i, playlist in enumerate(playlists, 1):
            print(f"{i}. {display_playlist_info(playlist)}")
            
        # Test fetching tracks from first playlist
        if playlists:
            print(f"\nFetching tracks from '{playlists[0]['name']}'...")
            tracks = get_playlist_tracks(playlists[0]['id'])
            print(f"Found {len(tracks)} tracks")
            if tracks:
                print("\nFirst 5 tracks:")
                for i, track in enumerate(tracks[:5], 1):
                    artists_str = ", ".join(track['artists'])
                    print(f"  {i}. {track['name']} by {artists_str}")
    except Exception as e:
        print(f"Error: {e}")
