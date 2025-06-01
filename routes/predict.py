import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'
from flask import Blueprint, request, jsonify
import cv2
import mediapipe as mp
import pickle
import numpy as np
import base64

predict = Blueprint('predict', __name__)

# Load model
with open('asl_model.pkl', 'rb') as f:
    model = pickle.load(f)

# Setup
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(max_num_hands=2, min_detection_confidence=0.7)

output_file = 'output.txt'

@predict.route('/predict', methods=['POST'])
def predict_gesture():
    data = request.json
    image_data = data['image']
    is_first_frame = data.get('init', False)

    image_bytes = base64.b64decode(image_data.split(',')[1])
    np_arr = np.frombuffer(image_bytes, np.uint8)
    frame = cv2.imdecode(np_arr, cv2.IMREAD_COLOR)

    img_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    result = hands.process(img_rgb)

    prediction = ""

    if is_first_frame:
        with open(output_file, 'w') as f:
            f.write("")  # clear or create the file

    if result.multi_hand_landmarks:
        landmarks_all_hands = []
        for hand_landmarks in result.multi_hand_landmarks:
            for lm in hand_landmarks.landmark:
                landmarks_all_hands.extend([lm.x, lm.y, lm.z])

        while len(landmarks_all_hands) < 126:
            landmarks_all_hands.extend([0.0, 0.0, 0.0])

        data_np = np.array(landmarks_all_hands).reshape(1, -1)
        prediction = model.predict(data_np)[0]

        # Append letter to file
        with open(output_file, 'a') as f:
            f.write(prediction)

    return jsonify({'prediction': prediction})


@predict.route('/get_output', methods=['GET'])
def get_output():
    try:
        # Read current output
        with open('output.txt', 'r') as f:
            content = f.read().strip()
    except FileNotFoundError:
        content = ""

    # Clear the file after reading
    with open('output.txt', 'w') as f:
        f.write("")

    return jsonify({'output': content})
