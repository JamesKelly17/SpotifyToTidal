#!/usr/bin/env python3
"""
Spotify to Tidal Transfer Tool
Transfers your liked songs from Spotify to Tidal
"""

import sys
import argparse
from spotify_tracks import get_liked_songs, display_track_info
from tidal_tracks import transfer_tracks
from spotify_auth import test_connection as test_spotify
from tidal_auth import test_connection as test_tidal


def main():
    """Main function to orchestrate the transfer"""
    parser = argparse.ArgumentParser(
        description='Transfer liked songs from Spotify to Tidal',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Transfer all liked songs
  python main.py

  # Test connections only
  python main.py --test

  # Preview first 10 songs without transferring
  python main.py --preview 10
        """
    )

    parser.add_argument(
        '--test',
        action='store_true',
        help='Test Spotify and Tidal connections without transferring'
    )

    parser.add_argument(
        '--preview',
        type=int,
        metavar='N',
        help='Preview first N songs from Spotify without transferring'
    )

    parser.add_argument(
        '--limit',
        type=int,
        metavar='N',
        help='Only transfer first N songs (useful for testing)'
    )

    args = parser.parse_args()

    print("=" * 60)
    print("Spotify to Tidal Transfer Tool")
    print("=" * 60)

    # Test connections
    if args.test:
        print("\nTesting Spotify connection...")
        spotify_ok = test_spotify()

        print("\nTesting Tidal connection...")
        tidal_ok = test_tidal()

        if spotify_ok and tidal_ok:
            print("\n✓ All connections successful!")
            return 0
        else:
            print("\n✗ Some connections failed. Please check your credentials.")
            return 1

    # Fetch liked songs from Spotify
    try:
        print("\nStep 1: Fetching liked songs from Spotify...")
        liked_songs = get_liked_songs()

        if not liked_songs:
            print("No liked songs found on Spotify.")
            return 0

        # Preview mode
        if args.preview:
            print(f"\nPreview of first {args.preview} songs:")
            print("-" * 60)
            for i, song in enumerate(liked_songs[:args.preview], 1):
                print(f"{i}. {display_track_info(song)}")
            return 0

        # Limit songs if specified
        if args.limit:
            liked_songs = liked_songs[:args.limit]
            print(f"\nLimited to first {args.limit} songs for transfer")

        # Confirm transfer
        print(f"\nReady to transfer {len(liked_songs)} songs to Tidal.")
        response = input("Do you want to continue? (yes/no): ").lower().strip()

        if response not in ['yes', 'y']:
            print("Transfer cancelled.")
            return 0

        # Transfer songs
        print("\nStep 2: Transferring songs to Tidal...")
        stats = transfer_tracks(liked_songs)

        # Determine exit code based on results
        if stats['added'] == stats['total']:
            return 0  # All successful
        elif stats['added'] > 0:
            return 0  # Partial success (still consider success)
        else:
            return 1  # No songs transferred

    except KeyboardInterrupt:
        print("\n\nTransfer interrupted by user.")
        return 130

    except Exception as e:
        print(f"\nError: {e}")
        import traceback
        traceback.print_exc()
        return 1


if __name__ == "__main__":
    sys.exit(main())
