import cv2
import os
import time
import numpy as np
import pygame
import tempfile
import subprocess
import threading

def convert_frame_to_ascii(frame, width=80):
    ascii_chars = " .:-=+*#%@"
    
    height = int(frame.shape[0] * width / frame.shape[1] / 2) 
    if height == 0:
        height = 1
        
    resized_frame = cv2.resize(frame, (width, height))

    if len(resized_frame.shape) > 2:
        gray_frame = cv2.cvtColor(resized_frame, cv2.COLOR_BGR2GRAY)
    else:
        gray_frame = resized_frame
    
    normalized = gray_frame / 255.0
    ascii_frame = ""
    
    for row in normalized:
        for pixel in row:
            index = int(pixel * (len(ascii_chars) - 1)) 
            ascii_frame += ascii_chars[index]
        ascii_frame += "\n"
    
    return ascii_frame

def extract_audio(video_path):
    """Extract audio from video to a temporary file"""
    try:
        # Create a temporary audio file
        temp_audio = tempfile.NamedTemporaryFile(delete=False, suffix='.mp3')
        temp_audio_path = temp_audio.name
        temp_audio.close()
        
        # Use ffmpeg to extract audio
        command = [
            'ffmpeg', '-i', video_path,
            '-vn',  # No video
            '-acodec', 'mp3',
            '-y',  # Overwrite output file
            temp_audio_path
        ]
        
        # Run ffmpeg silently
        subprocess.run(command, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=True)
        return temp_audio_path
    except Exception as e:
        print(f"Warning: Could not extract audio: {e}")
        return None

def play_audio_thread(audio_path, stop_event):
    """Play audio in a separate thread"""
    try:
        pygame.mixer.init()
        pygame.mixer.music.load(audio_path)
        pygame.mixer.music.play()
        
        # Keep thread alive while audio plays
        while pygame.mixer.music.get_busy() and not stop_event.is_set():
            time.sleep(0.1)
            
    except Exception as e:
        print(f"Warning: Could not play audio: {e}")

def play_video_in_terminal(video_path, width=80, fps=30):
    if not os.path.exists(video_path):
        print(f"Error: Video file '{video_path}' not found.")
        return
    
    cap = cv2.VideoCapture(video_path)
    video_fps = cap.get(cv2.CAP_PROP_FPS)
    frame_delay = 1.0 / video_fps if video_fps > 0 else 1.0 / fps
    
    # Extract and play audio
    audio_path = None
    audio_thread = None
    stop_event = threading.Event()
    
    print("Extracting audio... (this may take a moment)")
    audio_path = extract_audio(video_path)
    
    if audio_path:
        print("Starting playback with audio...")
        audio_thread = threading.Thread(target=play_audio_thread, args=(audio_path, stop_event))
        audio_thread.start()
        time.sleep(0.5)  # Small delay to sync audio startup
    else:
        print("Playing video without audio...")
    
    try:
        start_time = time.time()
        frame_count = 0
        
        while True:
            ret, frame = cap.read()
            if not ret:
                break
            
            ascii_art = convert_frame_to_ascii(frame, width)
            
            os.system('cls' if os.name == 'nt' else 'clear')
            print(ascii_art)
            
            # More accurate frame timing
            frame_count += 1
            expected_time = start_time + (frame_count * frame_delay)
            current_time = time.time()
            sleep_time = expected_time - current_time
            
            if sleep_time > 0:
                time.sleep(sleep_time)
            
    except KeyboardInterrupt:
        print("\nVideo playback interrupted.")
    
    finally:
        # Cleanup
        stop_event.set()
        cap.release()
        
        if audio_thread:
            pygame.mixer.music.stop()
            audio_thread.join()
            
        if audio_path and os.path.exists(audio_path):
            try:
                os.unlink(audio_path)
            except:
                pass

def get_video_path(user_input):
    """Get the full path to the video file"""
    # Get the script's directory
    script_dir = os.path.dirname(os.path.abspath(__file__))
    assets_folder = os.path.join(script_dir, "assets")
    
    # Create assets folder if it doesn't exist
    if not os.path.exists(assets_folder):
        os.makedirs(assets_folder)
        print(f"Created assets folder at: {assets_folder}")
    
    # If user input is just a filename (no path separators), look in assets folder
    if os.sep not in user_input and "/" not in user_input:
        video_path = os.path.join(assets_folder, user_input)
    else:
        # User provided a full or relative path
        video_path = user_input
    
    return video_path

def list_videos_in_assets():
    """List all video files in the assets folder"""
    script_dir = os.path.dirname(os.path.abspath(__file__))
    assets_folder = os.path.join(script_dir, "assets")
    
    if not os.path.exists(assets_folder):
        return []
    
    video_extensions = ['.mp4', '.avi', '.mov', '.mkv', '.flv', '.wmv', '.webm']
    videos = []
    
    for file in os.listdir(assets_folder):
        if any(file.lower().endswith(ext) for ext in video_extensions):
            videos.append(file)
    
    return sorted(videos)

if __name__ == "__main__":
    print("Terminal Video Player with Audio")
    print("=" * 40)
    print("Requirements: pip install opencv-python pygame")
    print("Also requires ffmpeg to be installed on your system")
    print("=" * 40 + "\n")
    
    # Show available videos in assets folder
    videos = list_videos_in_assets()
    if videos:
        print("Available videos in assets folder:")
        for i, video in enumerate(videos, 1):
            print(f"  {i}. {video}")
        print()
    else:
        script_dir = os.path.dirname(os.path.abspath(__file__))
        assets_folder = os.path.join(script_dir, "assets")
        print(f"No videos found in assets folder: {assets_folder}")
        print("You can add videos there or enter a full path.\n")
    
    video_input = input("Enter video number, filename (from assets), or full path: ").strip()
    
    # Check if input is a number
    if video_input.isdigit():
        video_num = int(video_input)
        if 1 <= video_num <= len(videos):
            video_path = get_video_path(videos[video_num - 1])
            print(f"Selected: {videos[video_num - 1]}")
        else:
            print(f"\nError: Invalid video number. Please enter a number between 1 and {len(videos)}")
            exit(1)
    else:
        video_path = get_video_path(video_input)
    
    if not os.path.exists(video_path):
        print(f"\nError: Video file not found at '{video_path}'")
        print("Please check the filename or path and try again.")
        exit(1)
    
    try:
        width = int(input("Enter terminal width (default 80): ") or "80")
    except ValueError:
        width = 80

    try:
        fps = int(input("Enter FPS (default: use video FPS): ") or "0")
    except ValueError:
        fps = 0
    
    play_video_in_terminal(video_path, width, fps)