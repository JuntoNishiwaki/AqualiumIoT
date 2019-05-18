#!/usr/bin/env python
# -*- coding: utf-8 -*-

import datetime
import bme280 as bme
import i2clcda as lcd
import DS18B20
import numpy as np
import pandas as pd
import wiringpi as wp
import RPi.GPIO as GPIO
import time

#while  True:
#    try:    
#　カウント用の初期パラメータ
dlm_c = 0
dlh_c = 0
dld_c = 0
gyo_m = 0
gyo_h = 0
gyo_d = 0
gyo_mt = 0

now = datetime.datetime.now()
next_day = now.day + 1
next_hour = now.hour + 1
next_month = now.month + 1
next_year = now.year + 1

# 臭気センサーの初期設定
SPI_CH = 0
PIN_BASE = 64

#　取得タイミングの設定。dm：30min毎 
dm = 30

#　ログ数
num_m = 30
num_h = 48
num_d = 31

#　30分間のログ用データフレーム
wtemp_log_m = np.zeros(num_m)
rtemp_log_m = np.zeros(num_m)
humid_log_m = np.zeros(num_m)
press_log_m = np.zeros(num_m)
gas_log_m = np.zeros(num_m)
min_log = np.zeros(num_m)
dlm = pd.DataFrame({
    '6_Gas': gas_log_m,
    '5_Pressure': press_log_m,
    '4_Humidity': humid_log_m,
    '3_Room temp' : rtemp_log_m,
    '2_Water temp' : wtemp_log_m,

    '1_Minute':min_log
})


#　30分毎のログ用データフレーム 
wtemp_log_h = np.zeros(num_h)
rtemp_log_h = np.zeros(num_h)
humid_log_h = np.zeros(num_h)
press_log_h = np.zeros(num_h)
gas_log_h = np.zeros(num_h)
hour_log = np.zeros(num_h)
dlh = pd.DataFrame({
    '6_Gas': gas_log_h,
    '5_Pressure': press_log_h,
    '4_Humidity': humid_log_h,
    '3_Room temp' : rtemp_log_h,
    '2_Water temp' : wtemp_log_h,
    '1_Hour': hour_log
})


#　1日毎のログ用データフレーム 
wtemp_log_d = np.zeros(num_d)
rtemp_log_d = np.zeros(num_d)
humid_log_d = np.zeros(num_d)
press_log_d = np.zeros(num_d)
gas_log_d = np.zeros(num_d)
day_log = np.zeros(num_d)
dld = pd.DataFrame({
    '6_Gas': gas_log_d,
    '5_Pressure': press_log_d,
    '4_Humidity': humid_log_d,
    '3_Room temp' : rtemp_log_d,
    '2_Water temp' : wtemp_log_d,
    '1_Day': day_log
})

print "START MONITERING!!"

#　端末での水温、室温、湿度、気圧の表示用
def print_date(wtemp,temp,humid,press,gas):
    print "###########################"

    print "Date:"+str(ts)
    print "Gas:"+str(round(gas,1))
    print "Water temp:"+str(round(wtemp,1))+"C"
    print "Room temp:"+str(round(temp,1))+"C"
    print "Humidity:"+str(round(humid,1))+"%"
    print "Pressure:"+str(round(press,1))+"hPa"

#　データ書き込み　m：分、h：時間、d：日
def df_write(d_name,gyo,a,wtemp,temp,humid,press,gas):
    df = d_name
    if a == 'm':
        df.iloc[gyo,0] = round(gyo*30/60,1)
    if a == 'h':
        min = now.minute
        df.iloc[gyo,0] = float(hour)+round(float(min)/60,1)
        
    if a == 'd':
        day = now.day
        df.iloc[gyo,0] = day
    
    df.iloc[gyo,1] = round(wtemp,1)
    df.iloc[gyo,2] = round(temp,1)
    df.iloc[gyo,3] = round(humid,1)
    df.iloc[gyo,4] = round(press,1)
    df.iloc[gyo,5] = round(gas,1)

#　データフレーム内の平均値計算
def df_ave(d_name):
    df = d_name

    df_means = df.mean()
    wtemp_ave = round(df_means["2_Water temp"],1)
    temp_ave = round(df_means["3_Room temp"],1)
    humid_ave = round(df_means["4_Humidity"],1)
    press_ave = round(df_means["5_Pressure"],1)
    gas_ave = round(df_means["6_Gas"],1)
    return wtemp_ave, temp_ave, humid_ave, press_ave, gas_ave

#　データフレームの初期化：分
def initialize_dlm():
    wtemp_log_m = np.zeros(num_m)
    rtemp_log_m = np.zeros(num_m)
    humid_log_m = np.zeros(num_m)
    press_log_m = np.zeros(num_m)
    gas_log_m = np.zeros(num_m)
    min_log = np.zeros(num_m)

    dlm = pd.DataFrame({
        '6_Gas': gas_log_m,
        '5_Pressure': press_log_m,
        '4_Humidity': humid_log_m,
        '3_Room temp' : rtemp_log_m,
        '2_Water temp' : wtemp_log_m,
        '1_Minute': min_log
    })
    return dlm

#　データフレームの初期化：時
def initialize_dlh():
    wtemp_log_h = np.zeros(num_h)
    rtemp_log_h = np.zeros(num_h)
    humid_log_h = np.zeros(num_h)
    press_log_h = np.zeros(num_h)
    gas_log_h = np.zeros(num_h)
    hour_log = np.zeros(num_h)
    dlh = pd.DataFrame({
        '6_Gas': gas_log_h,
        '5_Pressure': press_log_h,
        '4_Humidity': humid_log_h,
        '3_Room temp' : rtemp_log_h,
        '2_Water temp' : wtemp_log_h,
        '1_Hour': hour_log
    })
    return dlh

#　データフレームの初期化：日
def initialize_dld():
    wtemp_log_d = np.zeros(num_d)
    rtemp_log_d = np.zeros(num_d)
    humid_log_d = np.zeros(num_d)
    press_log_d = np.zeros(num_d)
    gas_log_d = np.zeros(num_d)
    day_log = np.zeros(num_d)
    dld = pd.DataFrame({
        '6_gas': gas_log_d,
        '5_Pressure': press_log_d,
        '4_Humidity': humid_log_d,
        '3_Room temp' : rtemp_log_d,
        '2_Water temp' : wtemp_log_d,
        '1_Day': day_log
    })
    return dld

#　臭気値の取得
def gas_detect(PIN_BASE,SPI_CH):
    wp.mcp3002Setup(PIN_BASE,SPI_CH)
    gas = wp.analogRead(PIN_BASE)
    return gas

#　再起動時のデータ読み込み
try:
    day = now.day
    month = now.month
    dlh = pd.read_csv("./"+str(month)+"_"+str(day)+"_date_log.csv", sep=",")
    dld = pd.read_csv("./"+str(month)+"_"+"date_log.csv", sep=",")
    s_bool = dld['1_Day'] > 0
    gyo_d = s_bool.sum()
    print "Reload date log!"
    
except:
    print "No date exist"
    pass

#　メイン
while  True:
    #日時取得
    now = datetime.datetime.now()
    sec = now.second
    min = now.minute
    hour = now.hour
    day = now.day
    month = now.month
    year = now.year
    """
    #　1ヶ月のデータログ
    if month == next_month:
        print "LOG DATA SAVE during Month("+str(year)+"_"+str(month)+"_date_log.csv)"
        dld.to_csv("./"+str(year)+"_"+str(month)+"_date_log.csv", index=False)
        gyo_d = 0
        dld = initialize_dld()
        next_month += 1
        if next_month == 13:
            next_month = 1
        """
    #　1分毎のデータログ
    if sec == 10:
        # 水温の取得
        wtemp = DS18B20.main() 
        # 室温、湿度、気圧の取得
        temp, humid, press = bme.Bme280(0x76, 1).get_data()
        # 臭気の取得
        gas = gas_detect(PIN_BASE,SPI_CH)
        if 60 > gas:
            gas_state = "良好"
        elif 150 > gas >= 60:
            gas_state = "そろそろ水換え"
        else:
            gas_state = "要水換え"
        
        # 水換えタイミングの出力（LED）
        LED_list = [16, 20, 21]
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(LED_list, GPIO.OUT)

        #扇風機制御
        fan = 0

        #エアコン制御
        airc = 0
        
        # 扇風機の動作確認
        if fan == 1:
            fan_state = "ON"
        else fan == 0:
            fan_state = "OFF"
        
        # エアコンの動作確認
        if airc == 1:
            airc_state = "ON"
        else airc == 0:
            airc_state = "OFF"
        
        #html編集
        path = '//var/www/html/index.txt'
        new_path = '//var/www/html/index.html'
        with open(path, "r", encoding="utf-8") as f:
            fdata = f.read()
            fdata = fdata.replace("wtwtwt", wtemp)
            fdata = fdata.replace("rtrtrt", temp)
            fdata = fdata.replace("pppp", press)
            fdata = fdata.replace("hhhh", humid)
            fdata = fdata.replace("eeee", gas_state)
            fdata = fdata.replace("ffff", fan_state)
            fdata = fdata.replace("aaaa", airc_state)        

        with open(new_path, "w", encoding="utf-8") as f:
            f.write(fdata)

        # 基準値
        GOOD = 60
        BAD = 150
        # 良好
        if GOOD >= gas:
            GPIO.output(LED_list[0], GPIO.HIGH)
            GPIO.output(LED_list[1], GPIO.LOW)
            GPIO.output(LED_list[2], GPIO.LOW)
        # そろそろ水換え
        elif BAD >= gas > GOOD:
            GPIO.output(LED_list[0], GPIO.LOW)
            GPIO.output(LED_list[1], GPIO.HIGH)
            GPIO.output(LED_list[2], GPIO.LOW)
        # 要水換え
        else: 
            GPIO.output(LED_list[0], GPIO.LOW)
            GPIO.output(LED_list[1], GPIO.LOW)
            GPIO.output(LED_list[2], GPIO.HIGH)

        # LCDへの出力
        lcd.bme(wtemp,temp,humid,press,gas)
        df_write(dlm,gyo_m,'m',wtemp,temp,humid,press,gas)
        gyo_m += 1
        PIN_BASE += 2
        """
        #ライブカメラ制御
        with picamera.PiCamera() as camera:
            camera.resolution = (800, 600)
            camera.start_preview()
            # 遅延
            time.sleep(5)
            camera.capture('/var/www/html/img/live.jpg')
            if min == 0 and hour == 22:
                file_name = str(month)+'_'+str(day)
                camera.capture('/home/pi/img/'+file_name+'.jpg')
        """
        #　30分毎のデータログ
        if min == 0 or min == 30:
            dlm_a = df_ave(dlm)
            df_write(dlh,gyo_h,'h',dlm_a[0],dlm_a[1],dlm_a[2], dlm_a[3], dlm_a[4])
            #Save data log
            print "LOG DATA SAVE during Hour("+str(month)+"_"+str(day)+"_date_log.csv)"
            dlh.to_csv("./"+str(month)+"_"+str(day)+"_date_log.csv", index=False)
            gyo_m = 0
            gyo_h += 1
            dlm = initialize_dlm()
        
            #　1日毎のデータログ
            if day == next_day:
                dlh_a = df_ave(dlh)
                df_write(dld,gyo_d,'d',dlh_a[0],dlh_a[1],dlh_a[2], dlh_a[3], dlh_a[4])
                #Save data log
                print "LOG DATA SAVE during Day("+str(month)+"_"+str(day)+"_date_log.csv)"
                dld.to_csv("./"+str(month)+"_"+"date_log.csv", index=False)        
                gyo_h = 0
                gyo_d += 1
                dlh = initialize_dlh()
                next_day = day + 1
        
        # html編集
        path = '//var/www/html/index.html'
        f = open(path, 'w')
        with open(path, mode = 'r', encoding = 'utf-8') as f:
            line = f.readline()
            while line:
                print(line)
                line = f.readline()

        new_1st = "<p>室温：" + str(temp) + "℃         水温：" + str(wtemp) + "℃</p>"
        new_2nd = "<p>気圧：" + str(press) + "hPa      湿度：" + str(humid) + "％</p>"
        new_3rd = "<p>水質：" + eval + "</p>"
        new_4th = "<p>扇風機：" + Fan+"       エアコン：" + Airc + "</p>"

    time.sleep(1)
   
    #except:
        #print('Error! Restart after 1min')
        #time.sleep(60)
