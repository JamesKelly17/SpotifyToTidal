#!/usr/bin/env python3
"""
Spotify to Tidal Transfer Tool
Transfers your liked songs and playlists from Spotify to Tidal
"""

import sys
import argparse
from spotify_tracks import get_liked_songs, display_track_info
from spotify_playlists import get_user_playlists, get_playlist_tracks, display_playlist_info
from tidal_tracks import transfer_tracks
from tidal_playlists import transfer_playlist, playlist_exists
from spotify_auth import test_connection as test_spotify
from tidal_auth import test_connection as test_tidal


def transfer_playlists_mode(args):
    """Handle playlist transfer mode"""
    try:
        # Fetch playlists from Spotify
        print("\nFetching your playlists from Spotify...")
        playlists = get_user_playlists(limit=args.playlist_limit)
        
        if not playlists:
            print("No playlists found on Spotify.")
            return 0
        
        # Show playlists
        print(f"\nFound {len(playlists)} playlist(s):")
        print("-" * 60)
        for i, playlist in enumerate(playlists, 1):
            print(f"{i}. {display_playlist_info(playlist)}")
        
        # Ask which playlists to transfer
        if not args.all_playlists:
            print("\nWhich playlists would you like to transfer?")
            print("Enter playlist numbers separated by commas (e.g., 1,3,5)")
            print("Or enter 'all' to transfer all playlists: ")
            
            selection = input().strip().lower()
            
            if selection == 'all':
                selected_playlists = playlists
            else:
                try:
                    # Parse the selection
                    indices = [int(x.strip()) - 1 for x in selection.split(',')]
                    selected_playlists = [playlists[i] for i in indices if 0 <= i < len(playlists)]
                    
                    if not selected_playlists:
                        print("No valid playlists selected.")
                        return 0
                except (ValueError, IndexError):
                    print("Invalid selection.")
                    return 1
        else:
            selected_playlists = playlists
        
        # Check for existing playlists if not overwriting
        if not args.overwrite:
            print("\nChecking for existing playlists on Tidal...")
            existing = []
            for playlist in selected_playlists:
                if playlist_exists(playlist['name']):
                    existing.append(playlist['name'])
            
            if existing:
                print(f"\nWarning: The following playlists already exist on Tidal:")
                for name in existing:
                    print(f"  - {name}")
                print("\nDo you want to:")
                print("1. Skip existing playlists")
                print("2. Create duplicates (will have the same name)")
                print("3. Cancel")
                
                choice = input("Enter your choice (1/2/3): ").strip()
                
                if choice == '1':
                    selected_playlists = [p for p in selected_playlists if p['name'] not in existing]
                    if not selected_playlists:
                        print("No playlists to transfer after skipping existing ones.")
                        return 0
                elif choice == '3':
                    print("Transfer cancelled.")
                    return 0
                # Choice 2 continues with all playlists
        
        # Confirm transfer
        total_tracks = sum(p['total_tracks'] for p in selected_playlists)
        print(f"\nReady to transfer {len(selected_playlists)} playlist(s) with approximately {total_tracks} total tracks.")
        response = input("Do you want to continue? (yes/no): ").lower().strip()
        
        if response not in ['yes', 'y']:
            print("Transfer cancelled.")
            return 0
        
        # Transfer playlists
        print("\n" + "=" * 60)
        print("Starting Playlist Transfer")
        print("=" * 60)
        
        successful = 0
        failed = 0
        
        for i, playlist in enumerate(selected_playlists, 1):
            print(f"\n[{i}/{len(selected_playlists)}] Processing: {playlist['name']}")
            
            # Fetch tracks for this playlist
            tracks = get_playlist_tracks(playlist['id'])
            
            if transfer_playlist(playlist, tracks):
                successful += 1
            else:
                failed += 1
        
        # Final summary
        print("\n" + "=" * 60)
        print("Playlist Transfer Complete!")
        print("=" * 60)
        print(f"Successfully transferred: {successful} playlist(s)")
        if failed > 0:
            print(f"Failed: {failed} playlist(s)")
        
        return 0 if successful > 0 else 1
        
    except KeyboardInterrupt:
        print("\n\nTransfer interrupted by user.")
        return 130
    except Exception as e:
        print(f"\nError: {e}")
        import traceback
        traceback.print_exc()
        return 1


def main():
    """Main function to orchestrate the transfer"""
    parser = argparse.ArgumentParser(
        description='Transfer liked songs and playlists from Spotify to Tidal',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Transfer all liked songs
  python main.py --likes

  # Transfer playlists interactively
  python main.py --playlists

  # Transfer all playlists automatically
  python main.py --playlists --all-playlists

  # Transfer first 5 playlists
  python main.py --playlists --playlist-limit 5

  # Test connections only
  python main.py --test

  # Preview first 10 liked songs without transferring
  python main.py --preview 10
        """
    )

    # Mode selection
    mode_group = parser.add_mutually_exclusive_group()
    mode_group.add_argument(
        '--likes',
        action='store_true',
        help='Transfer liked songs'
    )
    mode_group.add_argument(
        '--playlists',
        action='store_true',
        help='Transfer playlists'
    )

    # Test and preview options
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

    # Liked songs options
    parser.add_argument(
        '--limit',
        type=int,
        metavar='N',
        help='Only transfer first N songs (useful for testing)'
    )

    # Playlist options
    parser.add_argument(
        '--all-playlists',
        action='store_true',
        help='Transfer all playlists without asking'
    )

    parser.add_argument(
        '--playlist-limit',
        type=int,
        metavar='N',
        help='Limit number of playlists to fetch'
    )

    parser.add_argument(
        '--overwrite',
        action='store_true',
        help='Create duplicate playlists even if they already exist on Tidal'
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

    # If no mode specified, show menu
    if not args.likes and not args.playlists and not args.preview:
        print("\nWhat would you like to transfer?")
        print("1. Liked songs")
        print("2. Playlists")
        print("3. Both")
        
        choice = input("\nEnter your choice (1/2/3): ").strip()
        
        if choice == '1':
            args.likes = True
        elif choice == '2':
            args.playlists = True
        elif choice == '3':
            args.likes = True
            args.playlists = True
        else:
            print("Invalid choice.")
            return 1

    # Handle preview mode
    if args.preview:
        try:
            print("\nFetching liked songs from Spotify...")
            liked_songs = get_liked_songs()

            if not liked_songs:
                print("No liked songs found on Spotify.")
                return 0

            print(f"\nPreview of first {args.preview} songs:")
            print("-" * 60)
            for i, song in enumerate(liked_songs[:args.preview], 1):
                print(f"{i}. {display_track_info(song)}")
            return 0
        except Exception as e:
            print(f"\nError: {e}")
            return 1

    # Transfer playlists
    if args.playlists:
        result = transfer_playlists_mode(args)
        if not args.likes:
            return result

    # Transfer liked songs
    if args.likes:
        try:
            print("\nStep 1: Fetching liked songs from Spotify...")
            liked_songs = get_liked_songs()

            if not liked_songs:
                print("No liked songs found on Spotify.")
                return 0

            # Limit songs if specified
            if args.limit:
                liked_songs = liked_songs[:args.limit]
                print(f"\nLimited to first {args.limit} songs for transfer")

            # Confirm transfer
            print(f"\nReady to transfer {len(liked_songs)} liked songs to Tidal.")
            response = input("Do you want to continue? (yes/no): ").lower().strip()

            if response not in ['yes', 'y']:
                print("Transfer cancelled.")
                return 0

            # Transfer songs
            print("\nStep 2: Transferring liked songs to Tidal...")
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

    return 0


if __name__ == "__main__":
    sys.exit(main())
