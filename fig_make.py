#!/usr/bin/env python
# -*- coding: utf-8 -*-

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import pandas as pd 
import datetime
import time

def wtemp_g(file,h_or_d,fn):
    plt.figure()
    data = pd.read_csv(file, index_col='1_Hour')
    plt.scatter(data.index, data['2_Water temp'])
    plt.ylim(15,35)
    plt.xticks(rotation=45)
    if h_or_d == "h":
        plt.xlabel("Hour")
        plt.xlim(0 ,24)
    if h_or_d == "d":
        plt.xlabel("Day")
        plt.xlim(0 ,31)
    plt.ylabel("Water temparature (C)")
    plt.savefig(str(fn)+".png")
    plt.clf()
    #plt.show()

def rtemp_g(file,h_or_d,fn):
    plt.figure()
    data = pd.read_csv(file, index_col='1_Hour')
    plt.scatter(data.index, data['3_Room temp'])
    plt.ylim(5,35)
    plt.xticks(rotation=45)
    if h_or_d == "h":
        plt.xlabel("Hour")
        plt.xlim(0 ,24)
    if h_or_d == "d":
        plt.xlabel("Day")
        plt.xlim(0 ,31)
    plt.ylabel("Room temparature (C)")
    plt.savefig(str(fn)+".png")
    plt.clf()
    #plt.show()
    
def humid_g(file,h_or_d,fn):
    plt.figure()
    data = pd.read_csv(file, index_col='1_Hour')
    plt.scatter(data.index, data['4_Humidity'])
    plt.ylim(0 ,100)
    plt.xticks(rotation=45)
    if h_or_d == "h":
        plt.xlabel("Hour")
        plt.xlim(0 ,24)
    if h_or_d == "d":
        plt.xlabel("Day")
        plt.xlim(0 ,31)
    plt.ylabel("Humidity (%)")
    plt.savefig(str(fn)+".png")
    plt.clf()
    #plt.show()

def press_g(file,h_or_d,fn):
    plt.figure()
    data = pd.read_csv(file, index_col='1_Hour')
    plt.scatter(data.index, data['5_Pressure'])
    plt.ylim(980,1030)
    plt.xticks(rotation=45)
    if h_or_d == "h":
        plt.xlabel("Hour")
        plt.xlim(0 ,24)
    if h_or_d == "d":
        plt.xlabel("Day")
        plt.xlim(0 ,31)
    plt.ylabel("Pressure (hPa)")
    plt.savefig(str(fn)+".png")
    plt.clf()
    #plt.show()

def gas_g(file,h_or_d,fn):
    plt.figure()
    data = pd.read_csv(file, index_col='1_Hour')
    plt.scatter(data.index, data['6_gas'])
    plt.ylim(15,35)
    plt.xticks(rotation=45)
    if h_or_d == "h":
        plt.xlabel("Hour")
        plt.xlim(0 ,24)
    if h_or_d == "d":
        plt.xlabel("Day")
        plt.xlim(0 ,31)
    plt.ylabel("Gas")
    plt.savefig(str(fn)+".png")
    plt.clf()
    #plt.show()

def graph(file,h_or_d,fn):
    if h_or_d == "h":
        data = pd.read_csv(file, index_col='1_Hour')
    else:
        data = pd.read_csv(file, index_col='1_Day')        
    fig = plt.figure(figsize=(8, 6))
    
    ax1 = plt.subplot2grid((2,3), (0,0))
    ax2 = plt.subplot2grid((2,3), (0,1))
    ax3 = plt.subplot2grid((2,3), (1,0))
    ax4 = plt.subplot2grid((2,3), (1,1)) 
    ax5 = plt.subplot2grid((2,3), (2,0))   
    
    # Water temperature
    ax1.set_title('Water temperature')
    ax1.scatter(data.index, data['2_Water temp'],c='red', s=20, marker='o')
    #ax1.set_title('Water temperature')
    ax1.set_ylim(10,35)
    ax1.set_ylabel("Water temparature (C)")
    if h_or_d == "h":
        ax1.set_xlabel("Hour")
        ax1.set_xlim(0 ,24)
    
    if h_or_d == "d":
        ax1.set_xlabel("Day")
        ax1.set_xlim(0 ,31)
            
    # Room temperature
    ax2.set_title('Room temperature')
    ax2.scatter(data.index, data['3_Room temp'],c='blue', s=20, marker='o')
    #ax2.set_title('Room temperature')
    ax2.set_ylim(10,35)
    ax2.set_ylabel("Room temparature (C)")
    if h_or_d == "h":
        ax2.set_xlabel("Hour")
        ax2.set_xlim(0 ,24)
    
    if h_or_d == "d":
        ax2.set_xlabel("Day")
        ax2.set_xlim(0 ,31)

    # Humidity
    ax3.set_title('Humidity')
    ax3.scatter(data.index, data['4_Humidity'],c='green', s=20, marker='o')
    #ax3.set_title('Humidity')
    ax3.set_ylim(0 ,100)
    ax3.set_ylabel("Humidity (%)")
    if h_or_d == "h":
        ax3.set_xlabel("Hour")
        ax3.set_xlim(0 ,24)
    
    if h_or_d == "d":
        ax3.set_xlabel("Day")
        ax3.set_xlim(0 ,31)
        
    # Pressure
    ax4.set_title('Pressure')    
    ax4.scatter(data.index, data['5_Pressure'],c='orange', s=20, marker='o')
    #ax4.set_title('Pressure')    
    ax4.set_ylim(970,1040)
    ax4.set_ylabel("Pressure (hPa)")    
    if h_or_d == "h":
        ax4.set_xlabel("Hour")
        ax4.set_xlim(0 ,24)
    
    if h_or_d == "d":
        ax4.set_xlabel("Day")
        ax4.set_xlim(0 ,31)
        
    fig.subplots_adjust(left=0.075, bottom=0.05, right=0.95, top=0.95, wspace=0.3, hspace=0.40)
    plt.savefig(str(fn)+".png")
    plt.close(fig)
    #plt.show()

    # Gas
    ax4.set_title('Gas')    
    ax4.scatter(data.index, data['6_Gas'],c='orange', s=20, marker='o')
    #ax4.set_title('Pressure')    
    ax4.set_ylim(50,100)
    ax4.set_ylabel("Gas")    
    if h_or_d == "h":
        ax4.set_xlabel("Hour")
        ax4.set_xlim(0 ,24)
    
    if h_or_d == "d":
        ax4.set_xlabel("Day")
        ax4.set_xlim(0 ,31)
        
    fig.subplots_adjust(left=0.075, bottom=0.05, right=0.95, top=0.95, wspace=0.3, hspace=0.40)
    plt.savefig(str(fn)+".png")
    plt.close(fig)
    #plt.show()


now = datetime.datetime.now()
next_day = now.day + 1
next_hour = now.hour + 1
next_month = now.month + 1
next_year = now.year + 1

while True:
    
    #date
    now = datetime.datetime.now()
    sec = now.second
    min = now.minute
    hour = now.hour
    day = now.day
    month = now.month
    year = now.year
    
    fn_h = str(month)+"_"+str(day)+"_date_log.csv"
    fn_d = str(month)+"_"+"date_log.csv"
    fn_h1 = str(month)+"_"+str(day)+"_date_log_h"
    fn_d1 = str(month)+"_date_log_d"
    
    if min == 0 or min == 30:
        #For save
        time.sleep(60)
        print "Graph(Hour) save"
        graph(fn_h,"h",fn_h1)

        #HPのグラフ更新用。不要な場合はコメントアウト
        graph(fn_h,"h","/var/www/html/img/data_log_h")
    
    if day == next_day:      
        #For save
        time.sleep(60)
        print "Graph(Day) save"
        graph(fn_d,"d",fn_d1)
    
        #HPのグラフ更新用。不要な場合はコメントアウト
        graph(fn_d,"d","/var/www/html/img/data_log_d")
        
        next_day += 1

    time.sleep(1)
        
