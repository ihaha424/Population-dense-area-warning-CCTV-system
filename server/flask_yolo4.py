from flask import Flask, request, render_template, Response, jsonify
from flask_socketio import SocketIO
from PIL import Image
import cv2
import detect_people
import base64
import io
import numpy as np
import time

app = Flask(__name__)
socketio = SocketIO(app)
num = 0
image_base64 = cv2.imread('./ready.jpg')

@app.route('/')
def index():
    return render_template('index2.html')

@app.route('/receive_image', methods=['POST'])
def receive_image():
    global image_base64
    global num
    try:
        frame = request.files['frame']
        img = Image.open(frame.stream)
        # 여기서 이미지를 모델에 전달하고 결과를 얻어옴
        # result는 이미지, num은 사람의 수(만약 -1 이면 위험)
        image_base64, num = detect_people.count_people(img, net)
        return jsonify({'num': num})

    except Exception as e:
        return jsonify({'error' : str(e)})

def generate_frames():
    global num
    global image_base64
    while True:
        time.sleep(1)

        # 여기서 이미지를 모델에 전달하고 결과를 얻어옴
        # result는 이미지, num은 사람의 수(만약 -1 이면 위험)
        

        # 이미지를 Base64로 인코딩하여 전송
        _, buffer = cv2.imencode('.jpg', image_base64)
        image_base = base64.b64encode(buffer).decode('utf-8')

        # 클라이언트에게 프레임 전송
        socketio.emit('update_frame', {'image_base64': image_base, 'num': num})

@socketio.on('connect')
def handle_connect():
    print('Client connected')
    socketio.emit('update_frame', {'image_base64': '', 'num': num})

if __name__ == '__main__':
    # YOLO 데이타 세트 로딩
    net = cv2.dnn.readNet('./yolo/yolov3.weights', './yolo/yolov3.cfg')

    # 클래스 이름 파일 로드
    with open('./yolo/coco.names', 'r') as f:
        classes = [line.strip() for line in f.readlines()]

    # 서버 실행
    socketio.start_background_task(generate_frames)
    socketio.run(app, host='0.0.0.0', debug=True, port=8000)
