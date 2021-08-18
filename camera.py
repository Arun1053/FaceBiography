import cv2
from flask import Flask
from pywebio.input import *
from pywebio.output import *
from pywebio.platform.flask import webio_view


app = Flask(__name__)

def cam():
    name = input('Enter your Name to start the exam', type='text')

    cap = cv2.VideoCapture(0)

    # Check if the webcam is opened correctly
    if not cap.isOpened():
        raise IOError("Cannot open webcam")

    while True:
        ret, frame = cap.read()
        frame = cv2.resize(frame, None, fx=0.5, fy=0.5, interpolation=cv2.INTER_AREA)
        cv2.imshow('Input', frame)

        c = cv2.waitKey(1)
        if c == 27:
            break

    cap.release()
    cv2.destroyAllWindows()

app.add_url_rule('/','webio_view',webio_view(cam), methods=['GET','POST','OPTIONS'])

app.run(debug=True)