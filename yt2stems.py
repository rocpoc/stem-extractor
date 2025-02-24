import os
import json
import subprocess
import logging
import tkinter as tk
from tkinter import END

# Configure logging
logging.basicConfig(
    filename='app.log',
    level=logging.INFO,
    format='%(asctime)s %(levelname)s: %(message)s'
)

# JSON file to track downloaded video IDs
TRACKER_FILE = 'downloaded_videos.json'

# Directories for downloads and separated stems
DOWNLOAD_DIR = '/Users/rockylubbers/Desktop/Music/stem-extractor/download'
SEPARATED_DIR = '/Users/rockylubbers/Desktop/Music/stem-extractor/separated'

# Ensure directories exist
os.makedirs(DOWNLOAD_DIR, exist_ok=True)
os.makedirs(SEPARATED_DIR, exist_ok=True)

def load_downloaded_ids():
    """Load the JSON file that tracks downloaded video IDs."""
    if os.path.exists(TRACKER_FILE):
        try:
            with open(TRACKER_FILE, 'r') as f:
                return json.load(f)
        except json.JSONDecodeError as e:
            logging.error("Error decoding JSON: %s", e)
    return {}

def save_downloaded_ids(ids):
    """Save the updated video IDs to the JSON file."""
    with open(TRACKER_FILE, 'w') as f:
        json.dump(ids, f, indent=4)

def update_download_tracker(video_id):
    """Add a new video ID to the tracker JSON."""
    downloaded = load_downloaded_ids()
    if video_id not in downloaded:
        downloaded[video_id] = True
        save_downloaded_ids(downloaded)

def download_playlist(playlist_url):
    """
    Download audio from the YouTube playlist.
    Uses yt-dlp to extract audio in WAV format.
    Only new videos (i.e., not in our JSON tracker) will be processed.
    The downloaded files use the YouTube title as the filename and are saved in DOWNLOAD_DIR.
    """
    try:
        # Retrieve video IDs from the playlist using yt-dlp's flat-playlist mode.
        result = subprocess.run(
            ['yt-dlp', '--flat-playlist', '--print', '%(id)s', playlist_url],
            capture_output=True, text=True, check=True
        )
        video_ids = result.stdout.strip().split('\n')
    except subprocess.CalledProcessError as e:
        logging.error("Error retrieving playlist info: %s", e)
        return

    downloaded = load_downloaded_ids()
    new_videos = [vid for vid in video_ids if vid not in downloaded]

    if not new_videos:
        logging.info("No new videos found in the playlist.")
        return

    logging.info("Found %d new videos.", len(new_videos))

    for vid in new_videos:
        # Construct full video URL from video ID.
        video_url = f"https://www.youtube.com/watch?v={vid}"
        # Command to download and extract audio in WAV format using the title as filename.
        command = [
            'yt-dlp',
            '-x',  # extract audio
            '--audio-format', 'wav',
            '--output', os.path.join(DOWNLOAD_DIR, '%(title)s.%(ext)s'),
            video_url
        ]
        try:
            logging.info("Downloading video: %s", video_url)
            subprocess.run(command, check=True)
            update_download_tracker(vid)
        except subprocess.CalledProcessError as e:
            logging.error("Error downloading video %s: %s", video_url, e)

import sys  # add this at the top with your other imports

def process_audio_with_demucs(audio_file):
    command = [
        sys.executable, '-m', 'demucs',
        '--out', SEPARATED_DIR,
        audio_file
    ]
    try:
        logging.info("Processing file with Demucs: %s", audio_file)
        result = subprocess.run(command, check=True, capture_output=True, text=True)
        logging.info("Demucs output for %s: %s", audio_file, result.stdout)
    except subprocess.CalledProcessError as e:
        logging.error("Error processing %s with Demucs: %s", audio_file, e.stderr)


def run_pipeline(playlist_url):
    """
    Run the full pipeline:
      1. Download new videos' audio from the provided playlist.
      2. Process each WAV file in DOWNLOAD_DIR with Demucs for stem extraction.
    """
    download_playlist(playlist_url)
    
    # Process all WAV files in the DOWNLOAD_DIR
    for file in os.listdir(DOWNLOAD_DIR):
        if file.endswith('.wav'):
            file_path = os.path.join(DOWNLOAD_DIR, file)
            process_audio_with_demucs(file_path)

class App:
    def __init__(self, master):
        self.master = master
        master.title("YouTube Playlist to Stem Extractor")
        master.geometry("500x200")
        master.configure(bg="white")

        self.label = tk.Label(master, text="Enter YouTube Playlist URL:", bg="white", fg="black", font=("Helvetica", 12))
        self.label.pack(pady=10)

        self.entry = tk.Entry(master, width=50, bg="white", fg="black", font=("Helvetica", 12), relief="solid", borderwidth=1)
        self.entry.pack(pady=5)

        self.run_button = tk.Button(master, text="Run Pipeline", command=self.on_run_pipeline, bg="white", fg="black", font=("Helvetica", 12))
        self.run_button.pack(pady=10)

        self.status_label = tk.Label(master, text="", bg="white", fg="black", font=("Helvetica", 12))
        self.status_label.pack(pady=5)

    def on_run_pipeline(self):
        playlist_url = self.entry.get().strip()
        if not playlist_url:
            self.status_label.config(text="Please enter a valid URL.")
            return
        self.status_label.config(text="Running pipeline...")
        try:
            run_pipeline(playlist_url)
            self.status_label.config(text="Pipeline completed successfully.")
        except Exception as e:
            logging.error("Unexpected error in pipeline: %s", e)
            self.status_label.config(text="An error occurred. Check log for details.")
        finally:
            self.entry.delete(0, END)

if __name__ == '__main__':
    root = tk.Tk()
    app = App(root)
    root.mainloop()
