#-*- coding:utf-8 -*-
import cv2
import numpy as np
import random
import sys
import datetime
import picamera
import time

#保存ディレクトリ指定
pic_dir= '/var/www/html/img/'
#オリジナルファイル名
org_name = 'live.jpg'

#現時点の日時
now = datetime.datetime.now()

while  True:

    try:
        sec = datetime.datetime.now().second
        hour = datetime.datetime.now().hour
        day = datetime.datetime.now().day
        month = datetime.datetime.now().month
        

        if 16 <= hour <= 23 and sec == 50: #1分ごとに取得

            #ライブカメラ制御
            with picamera.PiCamera() as camera:
                camera.resolution = (800, 600)
                camera.start_preview()
                # 遅延
                time.sleep(10)
                #オリジナル保存先
                camera.capture(pic_dir+org_name)

                #別途保存先が必要な場合は指定
                if min == 0 and hour == 22:
                    file_name = str(month)+'_'+str(day)
                    camera.capture('/home/pi/img/'+file_name+'.jpg')

                # オリジナルをロード
                img_org = cv2.imread(pic_dir+org_name)

                # 処理対象をロード
                img = cv2.imread(pic_dir+org_name)

                #γ調整
                gamma = 0.5

                # ガンマ値を使って Look up tableを作成。エビ頭部の赤色を検出
                lookUpTable = np.empty((1,256), np.uint8)
                for i in range(256):
                    lookUpTable[0,i] = np.clip(pow(i / 255.0, gamma) * 255.0, 0, 255)
                
                # Look up tableを使って画像の輝度値を変更
                img = cv2.LUT(img, lookUpTable)
                hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV_FULL)
                h = hsv[:, :, 0]
                s = hsv[:, :, 1]

                mask = np.zeros(h.shape, dtype=np.uint8)
                mask[((h < 25) | (h >180)) & (s > 220)] = 255

                # 前処理
                #img = cv2.GaussianBlur(img,(3,3),0)
                #img = cv2.bilateralFilter(img,3,75,75)
                #img = cv2.blur(img,(5,5))

                # 輪郭1の出力  
                img_dst, contours, hierarchy = cv2.findContours(mask, cv2.CHAIN_APPROX_NONE, cv2.CHAIN_APPROX_SIMPLE)

                # 輪郭2の出力
                # 輪郭1を膨張させて、エビの位置を取得する。
                kernel = np.ones((3,3),np.uint8)
                #img_dst = cv2.erode(img_dst,kernel,iterations = 1)
                img_dst = cv2.dilate(img_dst,kernel,iterations = 13)
                img_dst, contours, hierarchy = cv2.findContours(img_dst, 2, 1)

                # ラベリング処理
                ret, markers = cv2.connectedComponents(img_dst)

                # ラベリング結果書き出し準備
                color_src = cv2.cvtColor(img_dst, cv2.COLOR_GRAY2BGR)
                height, width = img_dst.shape[:2]
                colors = []

                for i in range(1, ret + 1):
                    colors.append(np.array([random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)]))

                # ラベリング処理
                label = cv2.connectedComponentsWithStats(img_dst)

                # オブジェクト情報を項目別に抽出
                n = label[0] - 1
                data = np.delete(label[2], 0, 0)
                center = np.delete(label[3], 0, 0)

                # オブジェクト情報を利用してラベリング結果を画面に表示
                for i in range(n):

                    # 各オブジェクトの外接矩形を赤枠で表示
                    x0 = data[i][0]
                    y0 = data[i][1]
                    x1 = data[i][0] + data[i][2]
                    y1 = data[i][1] + data[i][3]
                    #cv2.rectangle(img_org, (x0, y0), (x1, y1), (0, 0, 255))

                    # 各オブジェクトのラベル番号と面積に黄文字で表示
                    cv2.putText(img_org, "EBI: " +str(i + 1), (x1 - 20, y1 + 15), cv2.FONT_HERSHEY_PLAIN, 1, (255, 255, 255))
                    #cv2.putText(img_org, "S: " +str(data[i][4]), (x1 - 20, y1 + 30), cv2.FONT_HERSHEY_PLAIN, 1, (0, 255, 255))
                    cv2.putText(img_org, "Total: "+str(ret - 1), (20, 580), cv2.FONT_HERSHEY_PLAIN, 3, (255, 255, 255),3)
                    """
                    # 各オブジェクトの重心座標をに黄文字で表示
                    cv2.putText(img_org, "X: " + str(int(center[i][0])), (x1 - 30, y1 + 15), cv2.FONT_HERSHEY_PLAIN, 1, (0, 255, 255))
                    cv2.putText(img_org, "Y: " + str(int(center[i][1])), (x1 - 30, y1 + 30), cv2.FONT_HERSHEY_PLAIN, 1, (0, 255, 255))
                    """

                #　写真上に輪郭をプロット
                Result = cv2.drawContours(img_org, contours, -1, (0,255,0), 3)

                # 表示
                cv2.imwrite(pic_dir+"ebi_count_result.jpg", Result)
        
        else:
            pass             
                
    except:
        print('Error! Restart after 1min')
        time.sleep(5)