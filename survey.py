from pywebio.input import *
from pywebio.output import *
from flask import Flask, render_template, redirect
from pywebio.platform.flask import webio_view
from deepface import DeepFace
import cv2
import threading
from pywebio.session import register_thread, defer_call

app = Flask(__name__)


def survey():

    name = input('Enter your Name to start the exam', type='text')

    t = threading.Thread(target=faceanalysis)
    register_thread(t)
    t.start()
    # time.sleep(10)

    q1 = radio('What is not a programming Language?',['Python','Java','HTML','C++'])
    q2 = radio('What is capital of India?', ['Delhi', 'Lucknow', 'Mumbai', 'Chennai'])
    q3 = radio('Who is the only captain to win all ICC trophies?', ['Dhoni', 'Ganguly', 'Kohli', 'Shastri'])
    q4 = radio('Home ground of Chelsea', ['Emirates', 'Old Trafford', 'Stamford Bridge', 'Etihad'])
    q5 = radio('Max Verstappen belongs to team ________', ['Mercedes', 'Ferrari', 'Williams', 'Redbull'])


    put_text("Thanks for the Survey!")
    put_html('<a href = "http://127.0.0.1:7777/thanks">click here</a>')



@app.route('/thanks')
def thanks():
    x = faceanalysis()
    if x.cap.isOpened():
        x.cap.release()
        x.cv2.destroyAllWindows()
    return "Thanks for the participation please press q"


def deepface():
    embeddings = DeepFace.stream(db_path="/home/webwerks/NT/FaceBiography")
    return embeddings


def faceanalysis():
    faceCascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

    cap = cv2.VideoCapture(0)
    # check if webcam is opened correctly
    if not cap.isOpened():
        cap = cv2.VideoCapture(1)
    if not cap.isOpened():
        raise IOError('Cannot open webcam')

    while True:
        ret, frame = cap.read()
        try:
            result = DeepFace.analyze(frame, actions=['emotion'])
        except:
            pass

        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        faces = faceCascade.detectMultiScale(gray, 1.1, 4)

        for (x, y, w, h) in faces:





            font = cv2.FONT_HERSHEY_SIMPLEX

            cv2.putText(frame, result['dominant_emotion'],
                        (50, 50),
                        font, 3,
                        (0, 0, 255),
                        2,
                        cv2.LINE_4)

            cv2.imshow('Original Video', frame)

            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

    cap.release()
    cv2.destroyAllWindows()



app.add_url_rule('/','webio_view',webio_view(survey), methods=['GET','POST','OPTIONS'])

if __name__ == '__main__':
    app.run(port=7777, debug=True)
