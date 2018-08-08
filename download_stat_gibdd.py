#-------------------------------------------------------------------------------
# Name:        Downloading XML statistics report from http://stat.gibdd.ru/
#              aka "Карточки ДТП.XML"
# Author:      Alex K
#
# Created:     08.08.2018
# Copyright:   (c) Alex 2018
#-------------------------------------------------------------------------------
# -*- coding: UTF-8 -*-
import requests
import json
import os
import sys
from datetime import datetime
from datetime import timedelta
from calendar import monthrange
import zipfile

start_date = '01.01.2015'
end_date = '08.08.2018'
date_format = '%d.%m.%Y'
log_filename = 'download_stat_gibdd.log'

urlGetCook = 'http://stat.gibdd.ru/'
urlPost = 'http://stat.gibdd.ru/getCardsXML'
urlGetDown = 'http://stat.gibdd.ru/getPDFbyId?data='


def create_log():
    with open(log_filename, 'w') as f:
        pass

def write_log(text):
    timestamp = datetime.strftime(datetime.now(), '%Y-%m-%d %H:%M:%S')
    with open(log_filename, 'a') as f:
        f.write('{} {}'.format(timestamp, text))
        f.write('\n')

def build_payload(date_start, date_end):
    payload = {"data":{"date_s":"01.01.2015","date_end":"31.01.2015","ParReg":"877","order":{"type":"1","fieldName":"dat"},"reg":["7"],"ind":"1","exportType":"1"}}
    #payload = {"data":"{\"date_s\":\"01.01.2015\",\"date_end\":\"30.01.2015\",\"ParReg\":\"877\",\"order\":{\"type\":1,\"fieldName\":\"dat\"},\"reg\":[\"7\"],\"ind\":\"1\",\"exportType\":1}"}
    payload["data"]["date_s"] = str(date_start)
    payload["data"]["date_end"] = str(date_end)
    payload_json = {}
    payload_json["data"] = json.dumps(payload["data"], separators=(',', ':')).encode('utf8').decode('unicode-escape')
    return payload_json

def file_unzip(zip_file):
    zip = zipfile.ZipFile(zip_file)
    for file in zip.namelist():
        if file == "Карточки ДТП.xml":
            zip.extract(file)
            log_txt = "Unzip file: "+zip_file
            print(log_txt)
            write_log(log_txt)
            os.rename(file, ".\\XML\\"+zip_file+'.xml')
            log_txt = "Rename: "+file+" to "+zip_file+'.xml'
            print(log_txt)
            write_log(log_txt)
    zip.close()
    os.rename(zip_file, ".\\ZIP\\"+zip_file)
    log_txt = "****************************************************************"
    print(log_txt)
    write_log(log_txt)

def download(urlID, file_name):
    print(urlID)
    rec_down = requests.get(urlID)
    open(file_name, 'wb').write(rec_down.content)
    log_txt = "File download: " + file_name
    print(log_txt)
    write_log(log_txt)
    file_unzip(file_name)

def post_url(payload):
    rec_cook = requests.get(urlGetCook)
    rec_post = requests.post(urlPost, json=payload, cookies=rec_cook.cookies)
    log_txt = "Post payload: " + str(rec_post.status_code)
    print(log_txt)
    write_log(log_txt)
    if rec_post.status_code == 200:
        cont_json = (json.loads(rec_post.content))
        urlBuild = urlGetDown + cont_json["data"]
    else:
        urlBuild = "NONE"
    return urlBuild

def date_diff(d_start, d_end):
    start = datetime.strptime(d_start, date_format)
    end = datetime.strptime(d_end, date_format)
    delta = end - start
    return delta.days

def manual_period(d_start, d_end):
    log_txt = "Make period: " + d_start + "-" + d_end
    print(log_txt)
    write_log(log_txt)
    payload = build_payload(d_start, d_end)
    urlDownZIP = post_url(payload)
    if urlDownZIP != "NONE":
        f_name = d_start + "-" + d_end + '_dtp.zip'
        download(urlDownZIP, f_name)
    else:
        log_txt = "!!! Period too large."
        print(log_txt)
        write_log(log_txt)

def main():
    if not os.path.exists(log_filename):
        create_log()
    write_log("Run script...")
    days_count = date_diff(start_date, end_date)
    curr_day = 0
    curr_date = start_date
    dat = datetime.strptime(curr_date, date_format)
    log_txt = "Count days for download: " + str(days_count)
    print(log_txt)
    write_log(log_txt)
    while curr_day <= days_count:
        dat_str = datetime.strftime(dat, date_format)
        log_txt = "Make period: " + dat_str + "-" + dat_str
        print(log_txt)
        write_log(log_txt)
        payload = build_payload(dat_str, dat_str)
        urlDownZIP = post_url(payload)
        if urlDownZIP != "NONE":
            f_name = dat_str + "-" + dat_str + '_dtp.zip'
            download(urlDownZIP, f_name)
        else:
            log_txt = "! Current period statistics none."
            print(log_txt)
            write_log(log_txt)
        dat = dat + timedelta(days=1)
        curr_day += 1
        log_txt = "Days download: " + str(curr_day)+ "/" + str(days_count)
        print(log_txt)
        write_log(log_txt)

if __name__ == '__main__':
    log_text = "Загрузчик статистики <Карточки ДТП>"
    print(log_text)
    #manual_period("01.01.2015","01.01.2015")
    main()
