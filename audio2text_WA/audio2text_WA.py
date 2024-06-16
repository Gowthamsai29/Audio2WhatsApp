import pywhatkit as pyw
import speech_recognition as sr
import sounddevice as sd
import numpy as np
import scipy.io.wavfile as wav

# Constants for file names
FILENAME_FROM_MIC = "RECORDING.WAV"
VOICE_TEXT_FILENAME = "VOICE_AS_TEXT.txt"

# Initialize the recognizer
r = sr.Recognizer()

def recognize_from_file(filename):
    """
    Recognizes speech from an audio file and converts it to text using Google Speech Recognition.

    :param filename: Path to the audio file
    :return: Recognized text from the audio or an error message if recognition fails
    """
    try:
        with sr.AudioFile(filename) as source:
            # Load audio data into memory
            audio_data = r.record(source)
            # Convert speech to text
            text = r.recognize_google(audio_data)
            return text
    except sr.UnknownValueError:
        print("Google Speech Recognition could not understand the audio")
        return ""
    except sr.RequestError as e:
        print(f"Could not request results from Google Speech Recognition service; {e}")
        return ""

def recognize_from_microphone(file_to_write):
    """
    Records audio from the microphone and saves it to a file.

    :param file_to_write: Path to the file where the recording will be saved
    """
    SAMPLE_RATE = 44100
    duration = 5  # seconds (adjust as needed)
    print("Recording Audio")
    audio_recording = sd.rec(duration * SAMPLE_RATE, samplerate=SAMPLE_RATE, channels=1, dtype='int32')
    sd.wait()  # Wait until recording is finished
    print("Audio recording complete")
    wav.write(file_to_write, SAMPLE_RATE, audio_recording)

def save_text_to_file(text, filename):
    """
    Saves the given text to a file.

    :param text: The text to be saved
    :param filename: The name of the file where the text will be saved
    """
    with open(filename, 'w') as f:
        f.write(text)

def send_whatsapp_message(phone_number, message):
    """
    Sends a WhatsApp message using pywhatkit.

    :param phone_number: The recipient's phone number (in international format)
    :param message: The message to be sent
    """
    try:
        # Sending message at a specified time (change as needed)
        pyw.sendwhatmsg(phone_number, message, 12, 10) #it reprents 12:10 and the format should be in 24 hour format
        print("WhatsApp message sent successfully!")
    except Exception as e:
        print(f"Error sending WhatsApp message: {str(e)}")

if __name__ == "__main__":
    # Step 1: Record audio from microphone and save to file
    recognize_from_microphone(FILENAME_FROM_MIC)
    
    # Step 2: Recognize speech from the recorded file
    text_from_voice = recognize_from_file(FILENAME_FROM_MIC)
    
    if text_from_voice:
        # Step 3: Save recognized text to file
        save_text_to_file(text_from_voice, VOICE_TEXT_FILENAME)
        
        # Placeholder phone number (replace with actual number)
        phone_number = 'YOUR_PHONE_NUMBER'
        
        # Step 4: Send the recognized text via WhatsApp
        send_whatsapp_message(phone_number, text_from_voice)
    else:
        print("No text recognized, nothing to send via WhatsApp")
