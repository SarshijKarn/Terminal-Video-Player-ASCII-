Terminal Video Player (ASCII + Audio)

A simple terminal-based video player that renders video frames as ASCII art in your terminal and plays the video's audio in sync. Built with Python, OpenCV, Pygame, and FFmpeg.

Features
- Renders videos as ASCII art directly in the terminal
- Plays extracted audio alongside the ASCII video
- Uses FFmpeg to extract audio to a temporary MP3 file
- Supports selecting a video by number from an assets folder, by filename, or by full path
- Adjustable terminal output width and FPS (or auto-use the video FPS)
- Works on Windows, macOS, and Linux (requires FFmpeg on PATH)

Project Structure
- terminal_player.py — main script
- assets/ — optional folder for your video files (auto-created when needed)

Supported Video Formats
Common formats via OpenCV/FFmpeg: .mp4, .avi, .mov, .mkv, .flv, .wmv, .webm

Prerequisites
1) Python 3.8+
2) Pip packages:
   pip install opencv-python pygame numpy
3) FFmpeg installed and available on PATH:
   - Windows (chocolatey): choco install ffmpeg
   - Windows (scoop): scoop install ffmpeg
   - macOS (Homebrew): brew install ffmpeg
   - Linux (Debian/Ubuntu): sudo apt-get update && sudo apt-get install -y ffmpeg
   - Verify: ffmpeg -version should print version info

Installation
1) Clone or copy this project directory.
2) Install Python dependencies:
   pip install opencv-python pygame numpy
3) Ensure FFmpeg is installed and accessible from your terminal (ffmpeg -version).

Usage
Option A: Place videos in the assets folder
- Put your video file(s) into the assets/ directory (e.g., assets/my_clip.mp4)
- Run the player:
  python terminal_player.py
- When prompted, you can:
  - Enter the number corresponding to a listed video in assets
  - Enter the filename within assets (e.g., my_clip.mp4)
  - Or enter a full path to a video elsewhere (e.g., C:\Videos\demo.mp4 or /home/user/demo.mp4)
- Enter desired terminal width (columns). Default is 80.
- Enter desired FPS. Enter 0 to use the video’s native FPS.

Option B: Play a video by full path directly
- Run:
  python terminal_player.py
- Paste the full path when prompted, e.g.:
  - Windows: C:\Users\you\Videos\sample.mp4
  - macOS/Linux: /Users/you/Videos/sample.mp4

How It Works (Overview)
- Video frames are read with OpenCV (cv2.VideoCapture)
- Each frame is resized to the target width and converted to grayscale
- Pixels are mapped to ASCII characters by brightness to form the frame text
- The terminal is cleared and the ASCII frame is printed at a cadence matching the FPS
- Audio is extracted to a temporary .mp3 with FFmpeg and played via pygame.mixer in a background thread
- Temporary audio files are cleaned up after playback

Key Runtime Options
- Terminal width: Controls the rendered ASCII width (height is auto-calculated to preserve aspect ratio; a 0.5 factor is applied for character aspect)
- FPS: If 0 (or left empty), uses the video’s FPS; otherwise, enforces your chosen FPS

Notes and Tips
- Larger widths increase detail but require more CPU and a larger terminal window
- Terminal fonts are not square; the script compensates with a 0.5 height factor for a better aspect ratio
- On Windows, the screen is cleared using cls; on macOS/Linux, clear is used
- If your terminal cannot keep up with high FPS and wide widths, reduce width or FPS
- If audio and video seem desynced, try a small width or rely on the native video FPS (enter 0)

Troubleshooting
- Error: Video file not found
  - Ensure the path or filename is correct
  - If you typed only a filename, it must exist in the assets folder
- Warning: Could not extract audio
  - FFmpeg not installed or not on PATH; install and verify with ffmpeg -version
  - Some videos may have unsupported audio codecs; try another video
- Warning: Could not play audio
  - Pygame mixer issues; ensure pygame is installed and your audio device works
  - On headless servers, audio playback may not be supported
- Blank or garbled output
  - Reduce width
  - Use a monospace font
  - Increase terminal size
- Low FPS or stutter
  - Lower width and/or FPS
  - Close other CPU-heavy applications

Security and Cleanup
- Audio is extracted to a secure temporary file and deleted after playback
- If the script crashes or is interrupted, temporary audio may remain; you can delete stray temp .mp3 files in your system temp directory

Cross-Platform Details
- Windows: Requires cmd/PowerShell terminal; ensure PATH includes FFmpeg and Python Scripts
- macOS/Linux: Run from a standard shell (Terminal, iTerm2, bash, zsh)

Example Session
1) Place sample.mp4 into assets/
2) Run:
   python terminal_player.py
3) Select the listed number for sample.mp4
4) Enter width (e.g., 100)
5) Enter FPS (e.g., 0 to use the video’s FPS)
6) Enjoy ASCII playback with audio

Implementation Notes (from terminal_player.py)
- convert_frame_to_ascii(frame, width=80): maps pixels to ASCII characters (" .:-=+*#%@") after grayscale normalization
- extract_audio(video_path): uses FFmpeg to export audio to an MP3 temp file; returns its path
- play_audio_thread(audio_path, stop_event): plays audio via pygame.mixer in a background thread and exits when stopped
- play_video_in_terminal(video_path, width=80, fps=30): core loop that renders frames to ASCII, prints them, and times frames based on video/native FPS
- get_video_path(user_input): resolves filenames to assets/ or uses provided path
- list_videos_in_assets(): returns supported video files in assets/
- Main prompt: lists assets, asks for video, width, and FPS; validates existence and starts playback

---
<div align="center">

### Created with ❤️ by Sarshij Karn

[![Website](https://img.shields.io/badge/Website-sarshijkarn.com.np-8a2be2?style=for-the-badge&logo=google-chrome&logoColor=white)](https://sarshijkarn.com.np)
[![LinkedIn](https://img.shields.io/badge/LinkedIn-Connect-0077B5?style=for-the-badge&logo=linkedin&logoColor=white)](https://www.linkedin.com/in/sarshij-karn-1a7766236/)

</div>
