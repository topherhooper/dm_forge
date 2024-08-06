import logging
from moviepy.editor import VideoFileClip
import speech_recognition as sr
from tqdm import tqdm
import requests

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

import gdown

def download_from_google_drive(file_id, destination):
    url = f"https://drive.google.com/uc?id={file_id}"
    gdown.download(url, destination, quiet=False, fuzzy=True)

def extract_audio_from_video(video_path, audio_path):
    logging.info(f"Loading video file from {video_path}")
    video = VideoFileClip(video_path)
    logging.info("Extracting audio from video")
    audio = video.audio
    logging.info(f"Writing audio to {audio_path}")
    audio.write_audiofile(audio_path)
    logging.info("Audio extraction completed")

def transcribe_audio(audio_path):
    logging.info(f"Loading audio file from {audio_path}")
    recognizer = sr.Recognizer()
    with sr.AudioFile(audio_path) as source:
        logging.info("Recording audio data")
        audio_data = recognizer.record(source)
        logging.info("Transcribing audio to text")
        text = recognizer.recognize_google(audio_data)
        logging.info("Transcription completed")
        return text

def main():
    video_url = "https://drive.google.com/file/d/1BRuIprEwtlYQ1_z-2MMq4riqTfWlTvAY/view?usp=sharing"
    video_path = "/app/data/video.mp4"
    audio_path = "/app/data/audio.wav"
    
    logging.info("Starting main process")
    
    # Download the video from Google Drive
    download_from_google_drive(video_url, video_path)
    
    # Extract audio from video
    extract_audio_from_video(video_path, audio_path)
    
    # Transcribe the audio
    transcript = transcribe_audio(audio_path)
    
    # Print the transcript
    logging.info("Printing the transcript")
    print(transcript)

if __name__ == "__main__":
    main()