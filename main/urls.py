from django.urls import path

from . import views

urlpatterns = [
    path('webcam', views.showCameraImg, name='showCameraImg'),
    path('', views.index, name='index'),
    path('result', views.showResult, name='showResult'),
]