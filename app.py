from flask import Flask, render_template, request, redirect, url_for, flash, send_from_directory
from deep_translator import GoogleTranslator
from gtts import gTTS
import language_tool_python  # Import language_tool_python

import os

app = Flask(__name__)
app.secret_key = os.environ.get('FLASK_SECRET_KEY', 'default_secret')

LANGUAGES = {
    'en': 'English',
    'es': 'Spanish',
    'ta': 'Tamil',
    'fr': 'French',
    'de': 'German',
    'it': 'Italian',
    'zh-cn': 'Chinese (Simplified)',
    'ja': 'Japanese',
    'ko': 'Korean',
    'ar': 'Arabic'
}

@app.route("/", methods=["GET", "POST"])
def index():
    input_text = ""
    input_lang = 'en'
    output_lang = 'ta'
    translated_text = ""
    audio_file = None

    if request.method == "POST":
        input_text = request.form["input_text"]
        input_lang = request.form["input_lang"]
        output_lang = request.form["output_lang"]

        if input_lang == output_lang:
            flash("Input and output languages must be different. Please select another output language.", "error")
            return redirect(url_for("index"))

        try:
            # Correct the input text using language_tool_python
            if input_lang == "en":  # language_tool_python works for multiple languages, but we will use it for english here.
                tool = language_tool_python.LanguageTool('en-US')
                input_text = tool.correct(input_text)  # Correct grammar
                tool.close() #close the tool.

            # Translate the corrected input text
            translator = GoogleTranslator(source=input_lang, target=output_lang)
            translated_text = translator.translate(input_text)

            # Generate speech file using gTTS
            audio_file = "static/translated_audio.mp3"
            tts = gTTS(text=translated_text, lang=output_lang)
            tts.save(audio_file)
        except Exception as e:
            flash(f"Translation error: {str(e)}", "error")
            return redirect(url_for("index"))

    return render_template("index.html", input_text=input_text, input_lang=input_lang,
                           output_lang=output_lang, translated_text=translated_text,
                           audio_file=audio_file, languages=LANGUAGES)

@app.route("/static/<path:filename>")
def serve_audio(filename):
    return send_from_directory("static", filename)

if __name__ == "__main__":
    app.run(debug=True)
    