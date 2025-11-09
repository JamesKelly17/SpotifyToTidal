"""
Test script for playlist transfer functionality
Run this to verify playlist operations work correctly
"""

from spotify_auth import get_spotify_client
from tidal_auth import get_tidal_session
from spotify_playlists import get_user_playlists, get_playlist_tracks
from tidal_playlists import create_playlist, playlist_exists, get_user_playlists_tidal
import sys


def test_spotify_playlists():
    """Test fetching playlists from Spotify"""
    print("\n" + "="*60)
    print("Testing Spotify Playlist Functions")
    print("="*60)
    
    try:
        # Test authentication
        spotify = get_spotify_client()
        user = spotify.current_user()
        print(f"✓ Connected to Spotify as: {user['display_name']}")
        
        # Test fetching playlists
        print("\nFetching your playlists...")
        playlists = get_user_playlists(limit=3)
        
        if not playlists:
            print("No playlists found. Create some playlists on Spotify first.")
            return False
        
        print(f"✓ Found {len(playlists)} playlist(s)")
        
        # Display playlists
        for i, playlist in enumerate(playlists, 1):
            print(f"\n{i}. {playlist['name']}")
            print(f"   Tracks: {playlist['total_tracks']}")
            print(f"   Public: {playlist['public']}")
            
            # Test fetching tracks from first playlist
            if i == 1 and playlist['total_tracks'] > 0:
                print(f"\n   Testing track fetch for '{playlist['name']}'...")
                tracks = get_playlist_tracks(playlist['id'])
                print(f"   ✓ Successfully fetched {len(tracks)} tracks")
                
                if tracks:
                    # Show first 3 tracks
                    print("   Sample tracks:")
                    for j, track in enumerate(tracks[:3], 1):
                        artists = ", ".join(track['artists'])
                        print(f"     {j}. {track['name']} by {artists}")
        
        return True
        
    except Exception as e:
        print(f"✗ Error testing Spotify playlists: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_tidal_playlists():
    """Test playlist operations on Tidal"""
    print("\n" + "="*60)
    print("Testing Tidal Playlist Functions")
    print("="*60)
    
    try:
        # Test authentication
        session = get_tidal_session()
        if not session.check_login():
            print("✗ Failed to authenticate with Tidal")
            return False
        
        user = session.user
        print(f"✓ Connected to Tidal (User ID: {user.id})")
        
        # Test fetching existing playlists
        print("\nFetching your Tidal playlists...")
        existing_playlists = get_user_playlists_tidal()
        print(f"✓ Found {len(existing_playlists)} existing playlist(s)")
        
        if existing_playlists:
            print("   Your playlists:")
            for i, playlist in enumerate(existing_playlists[:5], 1):
                print(f"     {i}. {playlist.name}")
        
        # Test playlist existence check
        test_name = "Spotify Transfer Test Playlist"
        print(f"\nChecking if '{test_name}' exists...")
        exists = playlist_exists(test_name)
        print(f"   Exists: {exists}")
        
        # Test creating a playlist
        if not exists:
            print(f"\nTesting playlist creation...")
            new_playlist = create_playlist(
                name=test_name,
                description="Test playlist created by Spotify to Tidal transfer tool"
            )
            
            if new_playlist:
                print(f"✓ Successfully created test playlist: {test_name}")
                print("  You can delete this test playlist from Tidal if you wish.")
            else:
                print("✗ Failed to create test playlist")
                return False
        
        return True
        
    except Exception as e:
        print(f"✗ Error testing Tidal playlists: {e}")
        import traceback
        traceback.print_exc()
        return False


def main():
    """Run all playlist tests"""
    print("\n" + "="*60)
    print("Spotify to Tidal - Playlist Functionality Test")
    print("="*60)
    
    spotify_ok = test_spotify_playlists()
    tidal_ok = test_tidal_playlists()
    
    print("\n" + "="*60)
    print("Test Results")
    print("="*60)
    print(f"Spotify Playlists: {'✓ PASSED' if spotify_ok else '✗ FAILED'}")
    print(f"Tidal Playlists:   {'✓ PASSED' if tidal_ok else '✗ FAILED'}")
    
    if spotify_ok and tidal_ok:
        print("\n✓ All playlist tests passed! You're ready to transfer playlists.")
        return 0
    else:
        print("\n✗ Some tests failed. Please check the errors above.")
        return 1


if __name__ == "__main__":
    sys.exit(main())
