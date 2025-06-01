import uuid
from flask import Blueprint, request, jsonify
import speech_recognition as sr
from googletrans import Translator
from werkzeug.utils import secure_filename
import os
import subprocess
from gtts import gTTS
from flask import send_file
from utils.text_to_speech import generate_speech


convert = Blueprint('convert', __name__)
recognizer = sr.Recognizer()
translator = Translator()



@convert.route('/speech-to-text', methods=['POST'])
def speech_to_text():
    try:
        print("Incoming speech-to-text request...")

        if 'audio' not in request.files:
            return jsonify({"error": "No audio file uploaded"}), 400

        lang = request.form.get('lang', 'en')
        audio_file = request.files['audio']

        # Generate temp folder
        os.makedirs("temp_audio", exist_ok=True)

        # Save to fixed path
        webm_path = os.path.join("temp_audio", "recording.webm")
        wav_path = os.path.join("temp_audio", "recording.wav")

        print("Saving uploaded audio...")
        audio_file.save(webm_path)

        if not os.path.exists(webm_path):
            return jsonify({"error": "Upload failed"}), 500

        # Convert webm to wav using ffmpeg
        print("Converting webm to wav...")
        conversion_result = subprocess.run([
            "ffmpeg", "-y", "-i", webm_path, "-ar", "16000", "-ac", "1", wav_path
        ], stdout=subprocess.PIPE, stderr=subprocess.PIPE)

        if conversion_result.returncode != 0:
            return jsonify({"error": "Audio conversion failed"}), 500

        # Process WAV with speech_recognition
        print("Recognizing speech...")
        with sr.AudioFile(wav_path) as source:
            audio = recognizer.record(source)
            text = recognizer.recognize_google(audio)

        print(f"Recognized text: {text}")
        translation = translator.translate(text, dest=lang).text
        print(f"Translated text: {translation}")

        return jsonify({
            "original_text": text,
            "translated_text": translation
        })

    except Exception as e:
        print(f"Error: {e}")
        return jsonify({"error": f"Processing failed: {str(e)}"}), 500

    finally:
        # Cleanup
        for f in ['recording.webm', 'recording.wav']:
            try:
                os.remove(os.path.join("temp_audio", f))
            except:
                pass

@convert.route('/text-to-speech', methods=['POST'])
def text_to_speech():
    data = request.get_json()
    text = data.get("text", "")
    lang = data.get("lang", "en")

    if not text:
        return jsonify({"error": "No text provided"}), 400

    try:
        tts = gTTS(text, lang=lang)
        output_path = os.path.join("temp_audio", "output.mp3")
        os.makedirs("temp_audio", exist_ok=True)
        tts.save(output_path)

        # Send audio file
        return send_file(output_path, mimetype="audio/mpeg")
    except Exception as e:
        return jsonify({"error": str(e)}), 500
