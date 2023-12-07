from flask import Flask, render_template, jsonify
from threading import Thread
import pygame
import cv2
import base64
import json
import requests
import time


# OpenCV 카메라 초기화
# Define VideoStream class to handle streaming of video from webcam in separate processing thread
class VideoStream:
    """Camera object that controls video streaming from the Picamera"""
    def __init__(self,resolution=(640,480),framerate=30):
        # Initialize the PiCamera and the camera image stream
        #breakpoint()
        
        self.stream = cv2.VideoCapture(0)
        print("Camera initiated.")
        ret = self.stream.set(cv2.CAP_PROP_FOURCC, cv2.VideoWriter_fourcc(*'MJPG'))
        ret = self.stream.set(3,resolution[0])
        ret = self.stream.set(4,resolution[1])
            
        # Read first frame from the stream
        (self.grabbed, self.frame) = self.stream.read()

    # Variable to control when the camera is stopped
        self.stopped = False

    def start(self):
    # Start the thread that reads frames from the video stream
        Thread(target=self.update,args=()).start()
        return self

    def update(self):
        # Keep looping indefinitely until the thread is stopped
        while True:
            # If the camera is stopped, stop the thread
            if self.stopped:
                # Close camera resources
                self.stream.release()
                return

            # Otherwise, grab the next frame from the stream
            (self.grabbed, self.frame) = self.stream.read()

    def read(self):
    # Return the most recent frame
        return self.frame

    def stop(self):
    # Indicate that the camera and thread should be stopped
        self.stopped = True

pygame.mixer.init()
pygame.mixer.music.load("./warning.ogg")
videostream = VideoStream(resolution=(640,480),framerate=30).start()
time.sleep(1)

while True:
    try:
        #time.sleep(1)
        frame = videostream.read()
        ret, buffer = cv2.imencode('.jpg', frame)
        frame_bytes = buffer.tobytes()
        files = {'frame': ('frame.jpg', frame_bytes, 'image/jpeg')}
        response = requests.post('http://10.19.207.0:8000/receive_image', files=files)
        data = response.json()
        if response.status_code == 200:
            print('Image sent successfully!')
        else:
            print('Error in sending image. Status code: {}'.format(response.status_code))
        if data['num'] == -1:
            pygame.mixer.music.play()

    except Exception as e:
        print('Error: {}'.format(str(e)))
