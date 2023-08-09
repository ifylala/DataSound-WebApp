import os
from flask import Flask, render_template, request, send_file
import pandas as pd
from gtts import gTTS

app = Flask(__name__)

# Define a route to the home page
@app.route('/')
def index():
    return render_template('index.html')

# Define a route to handle the file upload and conversion
@app.route('/upload', methods=['POST'])
def upload():
    try:
        if 'csv_file' not in request.files:
            return "No file part"

        csv_file = request.files['csv_file']
        if csv_file.filename == '':
            return "No selected file"

        if csv_file:
            df = pd.read_csv(csv_file)
            text_data = '\n'.join(df.to_string(index=False, header=False).split('\n'))

            # Convert text data to MP3 audio using gTTS
            tts = gTTS(text_data)
            audio_file = 'output.mp3'
            tts.save(audio_file)

            return send_file(audio_file, as_attachment=True)
    except Exception as e:
        return str(e)


if __name__ == "__main__":
    app.run(host='0.0.0.0' , debug=True)
