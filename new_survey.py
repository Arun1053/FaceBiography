import json
import base64
from deepface import DeepFace
from PIL import Image
import io
import cv2
import numpy as np


from flask import Flask, render_template, redirect, request, jsonify

app = Flask(__name__)

@app.route('/')
def index():
    title = "Survey"
    return render_template('camcap_tp.html', title=title)


@app.route('/form', methods=['POST', 'GET'])
def form():
    if request.method == 'POST':
        print('got a post request')
        form = request.form
        images = json.loads(form['images'])
        z = []
        for img in images:
            x = base64.b64decode(img.split(',')[1])
            image = Image.open(io.BytesIO(x))
            image = cv2.cvtColor(np.array(image), cv2.COLOR_BGR2RGB)
            obj = DeepFace.analyze(img_path=image)
            z.append(obj['dominant_emotion'])



        print(z)
        return jsonify({'status':True})
    return render_template('form1.html')


if __name__ == '__main__':
    app.run(port=7777, debug=True)