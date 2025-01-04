# from TTS import TTS
# import os

# tts=TTS()

# tts.run(source_file_path = './src/src.wav', reference_file_paths = ['./ref/ref_trump.wav'], output_name = 'flask_out')




from flask import Flask, request, jsonify, send_file
from werkzeug.utils import secure_filename
import os
from TTS import TTS

app = Flask(__name__)

# Set up folders
SRC_FOLDER = './src'
REF_FOLDER = './ref'
OUT_FOLDER = './out'

app.config['SRC_FOLDER'] = SRC_FOLDER
app.config['REF_FOLDER'] = REF_FOLDER
app.config['OUT_FOLDER'] = OUT_FOLDER

# Ensure folders exist
os.makedirs(SRC_FOLDER, exist_ok=True)
os.makedirs(REF_FOLDER, exist_ok=True)
os.makedirs(OUT_FOLDER, exist_ok=True)

# Initialize TTS instance
tts = TTS()

@app.route('/process', methods=['POST'])
def process_audio():
    try:
        # Check and save source file
        if 'source_file' not in request.files:
            return jsonify({'error': 'No source file provided'}), 400
        source_file = request.files['source_file']
        source_filename = secure_filename(source_file.filename)
        source_path = os.path.join(app.config['SRC_FOLDER'], source_filename)
        source_file.save(source_path)

        # Check and save reference files
        if 'reference_files' not in request.files:
            return jsonify({'error': 'No reference files provided'}), 400
        reference_files = request.files.getlist('reference_files')
        reference_paths = []
        for ref_file in reference_files:
            ref_filename = secure_filename(ref_file.filename)
            ref_path = os.path.join(app.config['REF_FOLDER'], ref_filename)
            ref_file.save(ref_path)
            reference_paths.append(ref_path)

        # Define output file path
        output_name = 'flask_out'
        output_path = os.path.join(app.config['OUT_FOLDER'], f'{output_name}.wav')

        # Run TTS process
        tts.run(source_file_path=source_path, reference_file_paths=reference_paths, output_name=output_name)

        # Return output file to user
        return send_file(output_path, as_attachment=True)

    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
