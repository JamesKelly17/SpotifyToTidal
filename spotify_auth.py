"""
Spotify Authentication Module
Handles authentication with Spotify API using OAuth 2.0
"""

import spotipy
from spotipy.oauth2 import SpotifyOAuth
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()


def get_spotify_client():
    """
    Create and return an authenticated Spotify client

    Returns:
        spotipy.Spotify: Authenticated Spotify client
    """
    client_id = os.getenv('SPOTIFY_CLIENT_ID')
    client_secret = os.getenv('SPOTIFY_CLIENT_SECRET')
    redirect_uri = os.getenv('SPOTIFY_REDIRECT_URI', 'http://localhost:8888/callback')

    if not client_id or not client_secret:
        raise ValueError(
            "Missing Spotify credentials. Please set SPOTIFY_CLIENT_ID and "
            "SPOTIFY_CLIENT_SECRET in your .env file"
        )

    # Define the required scope for accessing user's liked songs
    scope = "user-library-read"

    # Create OAuth manager
    auth_manager = SpotifyOAuth(
        client_id=client_id,
        client_secret=client_secret,
        redirect_uri=redirect_uri,
        scope=scope,
        cache_path=".cache"
    )

    # Create and return Spotify client
    spotify = spotipy.Spotify(auth_manager=auth_manager)

    return spotify


def test_connection():
    """
    Test the Spotify connection and display user information
    """
    try:
        spotify = get_spotify_client()
        user = spotify.current_user()
        print(f"Successfully connected to Spotify!")
        print(f"User: {user['display_name']}")
        print(f"User ID: {user['id']}")
        return True
    except Exception as e:
        print(f"Error connecting to Spotify: {e}")
        return False


if __name__ == "__main__":
    # Test the authentication
    test_connection()
