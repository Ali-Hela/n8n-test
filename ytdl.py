from pytube import YouTube, Playlist
import os
from pathlib import Path
import re

def display_video_info(yt):
    print("\nVideo Information:")
    print(f"Title: {yt.title}")
    print(f"Length: {yt.length // 60}:{yt.length % 60:02d} minutes")
    print(f"Views: {yt.views:,}")
    print(f"Author: {yt.author}")

def get_download_path():
    while True:
        path = input("\nEnter download path (press Enter for current directory): ").strip()
        if not path:
            return os.getcwd()
        if os.path.exists(path):
            return path
        print("Invalid path. Please try again.")

def get_stream_choice(yt):
    print("\nAvailable streams:")
    streams = list(yt.streams.filter(progressive=True))
    for i, stream in enumerate(streams, 1):
        print(f"{i}. {stream.resolution} - {stream.mime_type}")
    
    while True:
        try:
            choice = int(input("\nSelect quality (number): "))
            if 1 <= choice <= len(streams):
                return streams[choice - 1]
        except ValueError:
            pass
        print("Invalid choice. Please try again.")

def download_progress_callback(stream, chunk, bytes_remaining):
    total_size = stream.filesize
    bytes_downloaded = total_size - bytes_remaining
    percentage = (bytes_downloaded / total_size) * 100
    print(f"\rProgress: {percentage:0.2f}%", end="")

def is_playlist(url):
    return 'playlist' in url.lower()

def download_video(url, download_path):
    try:
        yt = YouTube(url, on_progress_callback=download_progress_callback)
        display_video_info(yt)

        print("\nDownload options:")
        print("1. Video")
        print("2. Audio only")
        option = input("Choose option (1/2): ").strip()

        if option == "2":
            stream = yt.streams.get_audio_only()
        else:
            stream = get_stream_choice(yt)

        print(f"\nStarting download of: {yt.title}")
        stream.download(download_path)
        print("\nDownload completed!")
        
    except Exception as e:
        print(f"\nAn error occurred: {str(e)}")
        return False
    return True

def download_playlist(url, download_path):
    try:
        pl = Playlist(url)
        print(f"\nPlaylist: {pl.title}")
        print(f"Total videos: {len(pl.video_urls)}")
        
        for i, video_url in enumerate(pl.video_urls, 1):
            print(f"\n[{i}/{len(pl.video_urls)}] Downloading...")
            download_video(video_url, download_path)
            
    except Exception as e:
        print(f"\nAn error occurred with playlist: {str(e)}")

def main():
    while True:
        url = input("\nEnter YouTube URL (or 'q' to quit): ").strip()
        if url.lower() == 'q':
            break
            
        if not url.startswith('http'):
            print("Invalid URL. Please enter a valid YouTube URL.")
            continue

        download_path = get_download_path()
        
        if is_playlist(url):
            download_playlist(url, download_path)
        else:
            download_video(url, download_path)
        
        print("\n" + "="*50)

if __name__ == "__main__":
    main()
