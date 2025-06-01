from gtts import gTTS
import os
import uuid

def generate_speech(text, lang='en'):
    """
    Generate speech from text using gTTS and return the filename.
    """
    try:
        os.makedirs("temp_audio", exist_ok=True)
        filename = f"temp_audio/{uuid.uuid4()}.mp3"
        tts = gTTS(text=text, lang=lang)
        tts.save(filename)
        return filename
    except Exception as e:
        print(f"Text-to-Speech Error: {e}")
        return None
