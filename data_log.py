#!/usr/bin/env python
# -*- coding: utf-8 -*-

import datetime
import bme280 as bme
import i2clcda as lcd
import DS18B20
import numpy as np
import pandas as pd
import time
import picamera

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
min_log = np.zeros(num_m)
dlm = pd.DataFrame({
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
hour_log = np.zeros(num_h)
dlh = pd.DataFrame({
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
day_log = np.zeros(num_d)
dld = pd.DataFrame({
    '5_Pressure': press_log_d,
    '4_Humidity': humid_log_d,
    '3_Room temp' : rtemp_log_d,
    '2_Water temp' : wtemp_log_d,
    '1_Day': day_log
})

print "START MONITERING!!"

#　端末での水温、室温、湿度、気圧の表示用
def print_date(wtemp,temp,humid,press):
    print "###########################"

    print "Date:"+str(ts)
    print "Water temp:"+str(round(wtemp,1))+"C"
    print "Room temp:"+str(round(temp,1))+"C"
    print "Humidity:"+str(round(humid,1))+"%"
    print "Pressure:"+str(round(press,1))+"hPa"

#　データ書き込み　m：分、h：時間、d：日
def df_write(d_name,gyo,a,wtemp,temp,humid,press):
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

#　データフレーム内の平均値計算
def df_ave(d_name):
    df = d_name

    df_means = df.mean()
    wtemp_ave = round(df_means["2_Water temp"],1)
    temp_ave = round(df_means["3_Room temp"],1)
    humid_ave = round(df_means["4_Humidity"],1)
    press_ave = round(df_means["5_Pressure"],1)
    return wtemp_ave, temp_ave, humid_ave, press_ave

#　データフレームの初期化：分
def initialize_dlm():
    wtemp_log_m = np.zeros(num_m)
    rtemp_log_m = np.zeros(num_m)
    humid_log_m = np.zeros(num_m)
    press_log_m = np.zeros(num_m)
    min_log = np.zeros(num_m)

    dlm = pd.DataFrame({
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
    hour_log = np.zeros(num_h)
    dlh = pd.DataFrame({
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
    day_log = np.zeros(num_d)
    dld = pd.DataFrame({
        '5_Pressure': press_log_d,
        '4_Humidity': humid_log_d,
        '3_Room temp' : rtemp_log_d,
        '2_Water temp' : wtemp_log_d,
        '1_Day': day_log
    })
    return dld

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
    
    #　1分毎のデータログ
    if sec == 30:
        wtemp = DS18B20.main() 
        temp, humid, press = bme.Bme280(0x76, 1).get_data()
        lcd.bme(wtemp,temp,humid,press)
        df_write(dlm,gyo_m,'m',wtemp,temp,humid,press)
        gyo_m += 1
        #ライブカメラ制御
        with picamera.PiCamera() as camera:
            camera.resolution = (1024, 768)
            camera.start_preview()
            # 遅延
            time.sleep(5)
            camera.capture('/var/www/html/img/live.jpg')

        #　30分毎のデータログ
        if min == 0 or min == 30:
            dlm_a = df_ave(dlm)
            df_write(dlh,gyo_h,'h',dlm_a[0],dlm_a[1],dlm_a[2], dlm_a[3])
            #Save data log
            print "LOG DATA SAVE during Hour("+str(month)+"_"+str(day)+"_date_log.csv)"
            dlh.to_csv("./"+str(month)+"_"+str(day)+"_date_log.csv", index=False)
            gyo_m = 0
            gyo_h += 1
            dlm = initialize_dlm()
            
            #　1日毎のデータログ
            if day == next_day:
                dlh_a = df_ave(dlh)
                df_write(dld,gyo_d,'d',dlh_a[0],dlh_a[1],dlh_a[2], dlh_a[3])
                #Save data log
                print "LOG DATA SAVE during Day("+str(month)+"_"+str(day)+"_date_log.csv)"
                dld.to_csv("./"+str(month)+"_"+"date_log.csv", index=False)        
                gyo_h = 0
                gyo_d += 1
                dlh = initialize_dlh()
                next_day = day + 1
                if month == next_month:
                    next_day = 1
                    
                    #　1ヶ月のデータログ
                    if month == next_month:
                        print "LOG DATA SAVE during Month("+str(year)+"_"+str(month)+"_date_log.csv)"
                        dld.to_csv("./"+str(year)+"_"+str(month)+"_date_log.csv", index=False)
                        gyo_d = 0
                        dld = initialize_dld()
                        next_month += 1
                        if next_month == 13:
                            next_month = 1

    time.sleep(1)
  
