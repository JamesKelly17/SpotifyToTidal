"""
Tidal Authentication Module
Handles authentication with Tidal API
"""

import tidalapi
import os
import json
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

SESSION_FILE = "tidal_session.json"


def get_tidal_session():
    """
    Create and return an authenticated Tidal session

    Returns:
        tidalapi.Session: Authenticated Tidal session
    """
    session = tidalapi.Session()

    # Try to load existing session
    if os.path.exists(SESSION_FILE):
        try:
            with open(SESSION_FILE, 'r') as f:
                session_data = json.load(f)
                session.load_oauth_session(
                    session_data['token_type'],
                    session_data['access_token'],
                    session_data['refresh_token'],
                    session_data.get('expiry_time')
                )
                if session.check_login():
                    print("Loaded existing Tidal session")
                    return session
        except Exception as e:
            print(f"Could not load existing session: {e}")

    # Need to perform new login
    print("\nTidal Login Required")
    print("===================")
    print("A browser window will open for you to authorize this application.")
    print("Please follow the instructions in your browser.\n")

    # OAuth2 login
    login, future = session.login_oauth()

    print(f"Visit this URL to authorize: {login.verification_uri_complete}")
    print("Waiting for authorization...")

    future.result()  # Wait for login to complete

    # Save session for future use
    try:
        session_data = {
            'token_type': session.token_type,
            'access_token': session.access_token,
            'refresh_token': session.refresh_token,
            'expiry_time': session.expiry_time.isoformat() if session.expiry_time else None
        }
        with open(SESSION_FILE, 'w') as f:
            json.dump(session_data, f)
        print("Session saved for future use")
    except Exception as e:
        print(f"Warning: Could not save session: {e}")

    return session


def test_connection():
    """
    Test the Tidal connection and display user information
    """
    try:
        session = get_tidal_session()
        if session.check_login():
            user = session.user
            print(f"\nSuccessfully connected to Tidal!")
            print(f"User ID: {user.id}")
            return True
        else:
            print("Failed to login to Tidal")
            return False
    except Exception as e:
        print(f"Error connecting to Tidal: {e}")
        return False


if __name__ == "__main__":
    # Test the authentication
    test_connection()
