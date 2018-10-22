# coding: UTF-8
from picamera import PiCamera
from time import sleep

camera = PiCamera()

#カメラが画像の取得を開始する
camera.start_preview()

#5秒待つ
sleep(10)

#画像を収録して保存
camera.capture('/home/pi/script/camera/image.jpg')

#カメラが画像の取得を停止する
camera.stop_preview()