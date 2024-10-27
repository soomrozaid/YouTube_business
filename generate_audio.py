import openai
from gtts import gTTS
from pydub import AudioSegment
import os

ENV: dict = {}

with open(".env", "r") as f:
    for line in f.readlines():
        k, v = line.split("=")
        ENV[k] = v


def generate_youtube_short_script(prompt):
    # Replace 'YOUR_OPENAI_API_KEY' with your actual OpenAI API key
    openai.api_key = ENV['OPENAI_API']

    # System message to guide the assistant
    system_message = (
        "You are a creative scriptwriter tasked with creating engaging, 1-minute YouTube short scripts "
        "tailored for a Gen-Z audience. The script should be lively, informative, and contain only the spoken content "
        "without any scene descriptions, stage directions, or bracketed content."
    )

    # User prompt incorporating the provided prompt
    user_message = f'Create a script for a YouTube short based on the following prompt:\n\n"{prompt}"\n\nThe script should not exceed 1 minute when spoken aloud.'

    # Call the OpenAI ChatCompletion API
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",  # Use 'gpt-4' if you have access
        messages=[
            {"role": "system", "content": system_message},
            {"role": "user", "content": user_message},
        ],
        max_tokens=200,  # Adjust as needed to limit the length
        temperature=0.7,
        n=1,
        stop=None,
    )

    # Extract the assistant's reply
    script = response["choices"][0]["message"]["content"].strip()
    return script


def text_to_speech(text, filename="output.wav", speed=1.25):
    try:
        # Initialize gTTS object and save as temporary mp3
        temp_filename = "temp_audio.mp3"
        tts = gTTS(text=text, lang="en", slow=False)
        tts.save(temp_filename)

        # Check if the temporary file was created successfully
        if not os.path.exists(temp_filename):
            raise Exception("Failed to create temporary audio file with gTTS.")

        # Load the temporary audio and increase speed
        audio = AudioSegment.from_mp3(temp_filename)
        faster_audio = audio.speedup(playback_speed=speed)

        # Export the modified audio to the final output file
        faster_audio.export(filename, format="wav")

        # Clean up temporary file
        os.remove(temp_filename)

        print(f"Audio file saved as {filename} with {speed}x speed")
    except Exception as e:
        print(f"An error occurred: {e}")


# Example usage
if __name__ == "__main__":
    user_prompt = input("Enter your prompt: ")
    youtube_script = generate_youtube_short_script(user_prompt)
    print("\nGenerated YouTube Short Script:\n")
    print(youtube_script)

    # Convert the script to speech and save as WAV
    text_to_speech(youtube_script, filename="youtube_short.wav")

# if __name__ == "__main__":
#     print(ENV)
