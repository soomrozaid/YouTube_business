import argparse
from moviepy.editor import VideoFileClip, AudioFileClip, concatenate_videoclips

def combine_audio_video(video_path, audio_path, output_path):
    # Load the video and audio files
    video = VideoFileClip(video_path)
    audio = AudioFileClip(audio_path)
    
    # Get durations
    video_duration = video.duration
    audio_duration = audio.duration
    
    # Calculate the number of loops required if audio is longer than video
    if audio_duration > video_duration:
        loops = int(audio_duration // video_duration) + 1
        video = concatenate_videoclips([video] * loops)
    
    # Set audio to video and trim the video to match the audio duration
    final_video = video.set_audio(audio).subclip(0, audio_duration)
    
    # Write the result to a file
    final_video.write_videofile(output_path, codec="libx264", audio_codec="aac")
    print(f"Video created successfully as {output_path}")

def main():
    parser = argparse.ArgumentParser(description="Combine audio and video, looping or trimming video to match audio duration.")
    parser.add_argument("video_path", type=str, help="Path to the input video file")
    parser.add_argument("audio_path", type=str, help="Path to the input audio file")
    parser.add_argument("output_path", type=str, help="Path for the output video file")

    args = parser.parse_args()
    
    combine_audio_video(args.video_path, args.audio_path, args.output_path)

if __name__ == "__main__":
    main()
