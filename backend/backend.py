from flask import Flask, request, send_file,jsonify

from flask_cors import CORS
import llama as llama
import time

app = Flask(__name__)
CORS(app)

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'audio' not in request.files:
        return 'No file part', 400

    file = request.files['audio']

    if file.filename == '':
        return 'No selected file', 400

    file.save('audio.wav')

    return 'File uploaded successfully', 200

    
@app.route('/notes', methods=["GET"])
def get_notes():
    llama.process("Summarize the document")

    # time.sleep(10)
    return send_file("notes.pdf", mimetype='application/pdf')


@app.route('/quiz', methods=["GET"])
def get_quiz():
    # time.sleep(10)
    response =  llama.process("Prepare a quiz based on the document. Format is a json list of questions: Each question containing the question text, options and the answer as string. Your output should contain only the json without any text before json.")

    print(response)


    return jsonify(response)

if __name__ == '__main__':
    app.run(debug=True)
