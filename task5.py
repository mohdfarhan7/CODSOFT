import dlib
import cv2
import numpy as np
import os
from flask import Flask, request

detector = dlib.get_frontal_face_detector()
predictor = dlib.shape_predictor('shape_predictor_68_face_landmarks.dat')
face_recognizer = dlib.face_recognition_model_v1('dlib_face_recognition_resnet_model_v1.dat')
images = []
labels = []
label = 0

for dirpath, dirnames, filenames in os.walk('dataset'):
    for filename in filenames:
        image_path = os.path.join(dirpath, filename)
        image = cv2.imread(image_path)
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        faces = detector(gray)
        for face in faces:
            landmarks = predictor(gray, face)
            descriptor = face_recognizer.compute_face_descriptor(image, landmarks)
            images.append(descriptor)
            labels.append(label)
    label += 1
recognizer = cv2.face.LBPHFaceRecognizer_create()
recognizer.train(images, np.array(labels))
recognizer.save('trained_model.yml')
app = Flask(__name__)

@app.route('/face_recognition', methods=['POST'])
def face_recognition():
    image_or_video = request.files['image_or_video']
    image = cv2.imdecode(np.fromstring(image_or_video.read(), np.uint8), cv2.IMREAD_UNCHANGED)
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    faces = detector(gray)
    predictions = []
    for face in faces:
        landmarks = predictor(gray, face)
        descriptor = face_recognizer.compute_face_descriptor(image, landmarks)
        label, confidence = recognizer.predict(np.array(descriptor))
        predictions.append((label, confidence))

    return str(predictions)

if __name__ == '__main__':
    app.run()