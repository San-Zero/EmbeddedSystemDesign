import random

from django.shortcuts import render
from django.views.decorators import gzip
from django.http import StreamingHttpResponse, HttpResponse, JsonResponse
import cv2
import threading
from .api import coinDetect

data_list = []


class VideoCamera(object):
    def __init__(self):
        self.video = cv2.VideoCapture(1 + cv2.CAP_DSHOW)
        (self.grabbed, self.frame) = self.video.read()
        threading.Thread(target=self.update, args=()).start()

    def __del__(self):
        self.video.release()

    def get_frame(self):
        image = self.frame
        # 在這裡做影像處理
        global data_list

        try:
            image, data_list = coinDetect.start(image)
        except Exception as e:
            data_list = [0, 0, 0, 0]

        _, jpeg = cv2.imencode('.jpg', image)

        return jpeg.tobytes()

    def update(self):
        while True:
            (self.grabbed, self.frame) = self.video.read()


def gen(camera):
    data_list = []
    while True:
        frame = camera.get_frame()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')


@gzip.gzip_page
def showCameraImg(request):
    try:
        cam = VideoCamera()
        return StreamingHttpResponse(gen(cam), content_type="multipart/x-mixed-replace;boundary=frame")
    except:
        pass


def index(request):
    return render(request, 'index.html')


def showResult(request):
    return JsonResponse(data_list, safe=False)
