"""
Test script to debug Tidal search functionality
"""

from tidal_auth import get_tidal_session
import inspect

def test_search_methods():
    """Test different search method signatures"""
    session = get_tidal_session()
    
    # First, let's see what methods are available
    print("Session search method signature:")
    print(inspect.signature(session.search))
    print("\nSession search method docstring:")
    print(session.search.__doc__)
    
    # Test different search approaches
    test_query = "Blinding Lights The Weeknd"
    
    print("\n" + "="*60)
    print("Testing different search methods:")
    print("="*60)
    
    # Test 1: Simple search with just query
    try:
        print("\nTest 1: session.search(query)")
        results = session.search(test_query)
        print(f"Success! Type of results: {type(results)}")
        if hasattr(results, '__len__'):
            print(f"Number of results: {len(results)}")
        if results:
            print(f"First result type: {type(results[0] if isinstance(results, list) else results)}")
            if isinstance(results, list) and len(results) > 0:
                track = results[0]
                print(f"Track: {track.name} by {track.artist.name}")
    except Exception as e:
        print(f"Failed: {e}")
    
    # Test 2: Search with limit parameter
    try:
        print("\nTest 2: session.search(query, limit=5)")
        results = session.search(test_query, limit=5)
        print(f"Success! Type of results: {type(results)}")
    except Exception as e:
        print(f"Failed: {e}")
    
    # Test 3: Search for tracks specifically
    try:
        print("\nTest 3: session.search_track(query)")
        if hasattr(session, 'search_track'):
            results = session.search_track(test_query)
            print(f"Success! Type of results: {type(results)}")
        else:
            print("session.search_track method doesn't exist")
    except Exception as e:
        print(f"Failed: {e}")
    
    # Test 4: Check if there's a tracks attribute
    try:
        print("\nTest 4: Checking for tracks attribute")
        if hasattr(session, 'tracks'):
            print("session.tracks exists")
            if hasattr(session.tracks, 'search'):
                print("session.tracks.search exists")
                results = session.tracks.search(test_query)
                print(f"Success! Type of results: {type(results)}")
        else:
            print("session.tracks doesn't exist")
    except Exception as e:
        print(f"Failed: {e}")

if __name__ == "__main__":
    test_search_methods()