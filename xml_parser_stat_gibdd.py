#-------------------------------------------------------------------------------
# Name:        XML parser and loader statistics report from http://stat.gibdd.ru/
#
# Author:      Alex K
#
# Created:     08.08.2018
# Copyright:   (c) Alex 2018
#-------------------------------------------------------------------------------
# -*- coding: UTF-8 -*-
import os
import sys
import uuid
import pandas as pd
from sqlalchemy import *
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import create_session
from sqlalchemy import create_engine, event
from urllib.parse import quote_plus
from lxml import etree, objectify
from datetime import datetime

xml_dir = "C:\\temp\\gibdd\\dtp\\"

log_filename = "xml_parser_stat_gibdd.log"

mssql_ip = "127.0.0.1"
mssql_db = "DTP_KARD"
mssql_login = "sa"
mssql_pass = "123"
mssql_conn_string = "DRIVER={SQL Server Native Client 10.0};SERVER="+mssql_ip+";DATABASE="+mssql_db+";UID="+mssql_login+";PWD="+mssql_pass

sqlExecSP_Add_CardDTP   = "{CALL Add_CardDTP(?,?,?,?,?,?,?,?,?,?,?)}"
sqlExecSP_Add_InfoDTP   = "{CALL Add_InfoDTP(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)}"
sqlExecSP_Add_InfoTS   = "{CALL Add_InfoTS(?,?,?,?,?,?,?,?,?,?,?,?,?,?)}"
sqlExecSP_Add_InfoTsUchast   = "{CALL Add_InfoTsUchast(?,?,?,?,?,?,?,?,?,?,?,?,?,?)}"
sqlExecSP_Add_InfoUchast   = "{CALL Add_InfoUchast(?,?,?,?,?,?,?,?,?,?,?)}"

class C_CardDtp(object):
    def __init__(self):
        self.id_tab = ''
        self.DTPV = ''
        self.date = ''
        self.district = ''
        self.KTS = ''
        self.KUCH = ''
        self.kartId = ''
        self.POG = ''
        self.RAN = ''
        self.rowNum = ''
        self.time = ''
        self.info_dtp_list = []

class C_infoDtp(object):
    def __init__(self):
        self.id_tab = ''
        self.id_info = ''
        self.CHOM = ''
        self.COORD_L = ''
        self.COORD_W = ''
        self.dor = ''
        self.dor_k = ''
        self.dor_z = ''
        self.factor = ''
        self.house = ''
        self.k_ul = ''
        self.km = ''
        self.m = ''
        self.NP = ''
        self.ndu = ''
        self.OBJ_DTP = ''
        self.osv = ''
        self.s_dtp = ''
        self.s_pch = ''
        self.sdor = ''
        self.spog = ''
        self.street = ''
        self.ts_info_list = []
        self.uch_info_list = []

class C_ts_info(object):
    def __init__(self):
        self.id_tab = ''
        self.id_info = ''
        self.id_ts = ''
        self.color = ''
        self.f_sob = ''
        self.g_v = ''
        self.m_pov = ''
        self.m_ts = ''
        self.marka_ts = ''
        self.n_ts = ''
        self.o_pf = ''
        self.r_rul = ''
        self.t_n = ''
        self.t_ts = ''
        self.ts_s = ''
        self.ts_uch_list = []

class C_ts_uch(object):
    def __init__(self):
        self.id_tab = ''
        self.id_info = ''
        self.id_ts = ''
        self.id_uch = ''
        self.ALCO = ''
        self.INJURED_CARD_ID = ''
        self.k_UCH = ''
        self.NPDD = ''
        self.n_UCH = ''
        self.POL =''
        self.SAFETY_BELT = ''
        self.SOP_NPDD = ''
        self.s_SEAT_GROUP = ''
        self.s_SM = ''
        self.s_T = ''
        self.v_ST = ''

class C_uch(object):
    def __init__(self):
        self.id_tab = ''
        self.id_info = ''
        self.id_uch = ''
        self.ALCO = ''
        self.k_UCH = ''
        self.NPDD = ''
        self.n_UCH = ''
        self.POL =''
        self.SOP_NPDD = ''
        self.s_SM = ''
        self.s_T = ''
        self.v_ST = ''

def create_log():
    with open(log_filename, 'w') as f:
        pass

def write_log(text):
    timestamp = datetime.strftime(datetime.now(), "%Y-%m-%d %H:%M:%S")
    with open(log_filename, 'a') as f:
        f.write("{} {}".format(timestamp, text))
        f.write("\n")

def build_db_engine():
    quot_str = quote_plus(mssql_conn_string)
    conn = 'mssql+pyodbc:///?odbc_connect={}'.format(quot_str)
    engine = create_engine(conn)
    return engine

def save_card_dtp(cardDTP):
    engin = build_db_engine()
    connection = engin.raw_connection()
    cursor = connection.cursor()
    AddCardParams = (cardDTP.id_tab,cardDTP.DTPV,cardDTP.date, \
        cardDTP.district,cardDTP.KTS,cardDTP.KUCH,cardDTP.kartId, \
        cardDTP.POG,cardDTP.RAN,cardDTP.rowNum,cardDTP.time)
    cursor.execute(sqlExecSP_Add_CardDTP, AddCardParams)
    for infoDTP in cardDTP.info_dtp_list:
        AddInfoDTPParams = (infoDTP.id_info, infoDTP.id_tab, infoDTP.CHOM, infoDTP.COORD_L, \
             infoDTP.COORD_W, infoDTP.dor, infoDTP.dor_k, infoDTP.dor_z, infoDTP.factor, \
             infoDTP.house, infoDTP.k_ul, infoDTP.km, infoDTP.m, infoDTP.NP, infoDTP.ndu, \
             infoDTP.OBJ_DTP, infoDTP.osv, infoDTP.s_dtp, infoDTP.s_pch, infoDTP.sdor, \
             infoDTP.spog, infoDTP.street)
        cursor.execute(sqlExecSP_Add_InfoDTP, AddInfoDTPParams)
        if len(infoDTP.uch_info_list) >0 :
            for infoUCH_dop in infoDTP.uch_info_list:
                AddUCHastParams =(infoUCH_dop.id_uch, infoUCH_dop.id_info, infoUCH_dop.ALCO, infoUCH_dop.k_UCH, \
                    infoUCH_dop.NPDD, infoUCH_dop.n_UCH, infoUCH_dop.POL, infoUCH_dop.SOP_NPDD, \
                    infoUCH_dop.s_SM, infoUCH_dop.s_T, infoUCH_dop.v_ST)
                cursor.execute(sqlExecSP_Add_InfoUchast, AddUCHastParams)
            infoDTP.uch_info_list.remove(infoUCH_dop)
        if len(infoDTP.ts_info_list) > 0:
            for infoTS in infoDTP.ts_info_list:
                AddInfoTSParams = (infoTS.id_ts, infoTS.id_info, infoTS.color, infoTS.f_sob, \
                infoTS.g_v, infoTS.m_pov, infoTS.m_ts, infoTS.marka_ts, infoTS.n_ts, infoTS.o_pf, \
                infoTS.r_rul, infoTS.t_n, infoTS.t_ts, infoTS.ts_s)
                cursor.execute(sqlExecSP_Add_InfoTS, AddInfoTSParams)
                if len(infoTS.ts_uch_list) > 0:
                    for infoUCH in infoTS.ts_uch_list:
                        AddInfoUCHParams = (infoUCH.id_uch, infoUCH.id_ts, infoUCH.ALCO, infoUCH.INJURED_CARD_ID, \
                            infoUCH.k_UCH, infoUCH.NPDD, infoUCH.n_UCH, infoUCH.POL, infoUCH.SAFETY_BELT, \
                             infoUCH.SOP_NPDD, infoUCH.s_SEAT_GROUP, infoUCH.s_SM, infoUCH.s_T, infoUCH.v_ST)
                        cursor.execute(sqlExecSP_Add_InfoTsUchast, AddInfoUCHParams)
                    infoTS.ts_uch_list.remove(infoUCH)
            infoDTP.ts_info_list.remove(infoTS)
    cardDTP.info_dtp_list.remove(infoDTP)
    cursor.close()
    connection.commit()

def parse_info_uch(info_uch_tag, id_tab, id_info, id_uch):
    i_uch = C_uch()
    i_uch.id_tab = "{"+str(id_tab)+"}"
    i_uch.id_info = "{"+str(id_info)+"}"
    i_uch.id_uch = "{"+str(id_uch)+"}"
    for info_uch_child in info_uch_tag.getchildren():
        if info_uch_child.tag == 'ALCO':
            i_uch.ALCO = str(info_uch_child.text)
        if info_uch_child.tag == 'k_UCH':
            i_uch.k_UCH = str(info_uch_child.text)
        if info_uch_child.tag == 'NPDD':
            i_uch.NPDD = str(info_uch_child.text)
        if info_uch_child.tag == 'n_UCH':
            i_uch.n_UCH = str(info_uch_child.text)
        if info_uch_child.tag == 'POL':
            i_uch.POL = str(info_uch_child.text)
        if info_uch_child.tag == 'SOP_NPDD':
            i_uch.SOP_NPDD = str(info_uch_child.text)
        if info_uch_child.tag == 's_SM':
            i_uch.s_SM = str(info_uch_child.text)
        if info_uch_child.tag == 's_T':
            i_uch.s_T = str(info_uch_child.text)
        if info_uch_child.tag == 'v_ST':
            i_uch.v_ST = str(info_uch_child.text)
    return i_uch

def parse_ts_uch(ts_uch_tag, id_tab, id_info, id_ts, id_uch):
    uch = C_ts_uch()
    uch.id_tab = "{"+str(id_tab)+"}"
    uch.id_info = "{"+str(id_info)+"}"
    uch.id_ts = "{"+str(id_ts)+"}"
    uch.id_uch = "{"+str(id_uch)+"}"
    for ts_uch_child in ts_uch_tag.getchildren():
        if ts_uch_child.tag == 'ALCO':
            uch.ALCO = str(ts_uch_child.text)
        if ts_uch_child.tag == 'INJURED_CARD_ID':
            uch.INJURED_CARD_ID = str(ts_uch_child.text)
        if ts_uch_child.tag == 'k_UCH':
            uch.k_UCH = str(ts_uch_child.text)
        if ts_uch_child.tag == 'NPDD':
            uch.NPDD = str(ts_uch_child.text)
        if ts_uch_child.tag == 'n_UCH':
            uch.n_UCH = str(ts_uch_child.text)
        if ts_uch_child.tag == 'POL':
            uch.POL = str(ts_uch_child.text)
        if ts_uch_child.tag == 'SAFETY_BELT':
            uch.SAFETY_BELT = str(ts_uch_child.text)
        if ts_uch_child.tag == 'SOP_NPDD':
            uch.SOP_NPDD = str(ts_uch_child.text)
        if ts_uch_child.tag == 's_SEAT_GROUP':
            uch.s_SEAT_GROUP = str(ts_uch_child.text)
        if ts_uch_child.tag == 's_SM':
            uch.s_SM = str(ts_uch_child.text)
        if ts_uch_child.tag == 's_T':
            uch.s_T = str(ts_uch_child.text)
        if ts_uch_child.tag == 'v_ST':
            uch.v_ST = str(ts_uch_child.text)
    return uch

def parse_ts_info(ts_info_tag, id_tab, id_info, id_ts):
    ts_inf = C_ts_info()
    ts_inf.id_tab = "{"+str(id_tab)+"}"
    ts_inf.id_info = "{"+str(id_info)+"}"
    ts_inf.id_ts = "{"+str(id_ts)+"}"
    for ts_info_child in ts_info_tag.getchildren():
        if ts_info_child.tag == 'color':
            ts_inf.color = str(ts_info_child.text)
        if ts_info_child.tag == 'f_sob':
            ts_inf.f_sob = str(ts_info_child.text)
        if ts_info_child.tag == 'g_v':
            ts_inf.g_v = str(ts_info_child.text)
        if ts_info_child.tag == 'm_pov':
            ts_inf.m_pov = str(ts_info_child.text)
        if ts_info_child.tag == 'm_ts':
            ts_inf.m_ts = str(ts_info_child.text)
        if ts_info_child.tag == 'marka_ts':
            ts_inf.marka_ts = str(ts_info_child.text)
        if ts_info_child.tag == 'n_ts':
            ts_inf.n_ts = str(ts_info_child.text)
        if ts_info_child.tag == 'o_pf':
            ts_inf.o_pf = str(ts_info_child.text)
        if ts_info_child.tag == 'r_rul':
            ts_inf.r_rul = str(ts_info_child.text)
        if ts_info_child.tag == 't_n':
            ts_inf.t_n = str(ts_info_child.text)
        if ts_info_child.tag == 't_ts':
            ts_inf.t_ts = str(ts_info_child.text)
        if ts_info_child.tag == 'ts_s':
            ts_inf.ts_s = str(ts_info_child.text)
        if ts_info_child.tag == 'ts_uch':
            id_uch = uuid.uuid1()
            uch = parse_ts_uch(ts_info_child, id_tab, id_info, id_ts, id_uch)
            ts_inf.ts_uch_list.append(uch)
    return ts_inf

def parse_infoDtp(infoDtp_tag,id_tab,id_info):
    info_dtp = C_infoDtp()
    info_dtp.id_tab = "{"+str(id_tab)+"}"
    info_dtp.id_info = "{"+str(id_info)+"}"
    ndu = ''
    for infoDtp_child in infoDtp_tag.getchildren():
        if infoDtp_child.tag == 'CHOM':
            info_dtp.CHOM = str(infoDtp_child.text)
        if infoDtp_child.tag == 'COORD_L':
            info_dtp.COORD_L = str(infoDtp_child.text)
        if infoDtp_child.tag == 'COORD_W':
            info_dtp.COORD_W = str(infoDtp_child.text)
        if infoDtp_child.tag == 'dor':
            info_dtp.dor = str(infoDtp_child.text)
        if infoDtp_child.tag == 'dor_k':
            info_dtp.dor_k = str(infoDtp_child.text)
        if infoDtp_child.tag == 'dor_z':
            info_dtp.dor_z = str(infoDtp_child.text)
        if infoDtp_child.tag == 'factor':
            info_dtp.factor = str(infoDtp_child.text)
        if infoDtp_child.tag == 'house':
            info_dtp.house = str(infoDtp_child.text)
        if infoDtp_child.tag == 'k_ul':
            info_dtp.k_ul = str(infoDtp_child.text)
        if infoDtp_child.tag == 'km':
            info_dtp.km = str(infoDtp_child.text)
        if infoDtp_child.tag == 'm':
            info_dtp.m = str(infoDtp_child.text)
        if infoDtp_child.tag == 'NP':
            info_dtp.NP = str(infoDtp_child.text)
        if infoDtp_child.tag == 'ndu':
            ndu = ndu + str(infoDtp_child.text)+" | "
        if infoDtp_child.tag == 'OBJ_DTP':
            info_dtp.OBJ_DTP = str(infoDtp_child.text)
        if infoDtp_child.tag == 'osv':
            info_dtp.osv = str(infoDtp_child.text)
        if infoDtp_child.tag == 's_dtp':
            info_dtp.s_dtp = str(infoDtp_child.text)
        if infoDtp_child.tag == 's_pch':
            info_dtp.s_pch = str(infoDtp_child.text)
        if infoDtp_child.tag == 'sdor':
            info_dtp.sdor = str(infoDtp_child.text)
        if infoDtp_child.tag == 'spog':
            info_dtp.spog = str(infoDtp_child.text)
        if infoDtp_child.tag == 'street':
            info_dtp.street = str(infoDtp_child.text)
        if infoDtp_child.tag == 'ts_info':
           id_ts = uuid.uuid1()
           it_info_p = parse_ts_info(infoDtp_child,id_tab, id_info, id_ts)
           info_dtp.ndu = ndu
           info_dtp.ts_info_list.append(it_info_p)
        if infoDtp_child.tag == 'uchInfo':
           id_uch = uuid.uuid1()
           uch_info_p = parse_info_uch(infoDtp_child,id_tab, id_info, id_uch)
           info_dtp.uch_info_list.append(uch_info_p)
    return info_dtp

def parse_tab(tab_tag,id_tab):
    card_dtp = C_CardDtp()
    card_dtp.id_tab = "{"+str(id_tab)+"}"
    for tab_child in tab_tag.getchildren():
        if tab_child.tag == 'DTPV':
            card_dtp.DTPV = str(tab_child.text)
        if tab_child.tag == 'date':
            card_dtp.date = str(tab_child.text)
        if tab_child.tag == 'district':
            card_dtp.district = str(tab_child.text)
        if tab_child.tag == 'KTS':
            card_dtp.KTS = str(tab_child.text)
        if tab_child.tag == 'KUCH':
            card_dtp.KUCH = str(tab_child.text)
        if tab_child.tag == 'kartId':
            card_dtp.kartId = str(tab_child.text)
        if tab_child.tag == 'POG':
            card_dtp.POG = str(tab_child.text)
        if tab_child.tag == 'RAN':
            card_dtp.RAN = str(tab_child.text)
        if tab_child.tag == 'rowNum':
            card_dtp.rowNum = str(tab_child.text)
        if tab_child.tag == 'time':
            card_dtp.time = str(tab_child.text)
        if tab_child.tag == 'infoDtp':
            id_info = uuid.uuid1()
            inf_dtp = parse_infoDtp(tab_child,id_tab,id_info)
            card_dtp.info_dtp_list.append(inf_dtp)
    save_card_dtp(card_dtp)

def replase_xml_text(file_src):
    with open(file_src,'rb') as input:
        with open(file_src+".bak",'wb') as output:
            for line in input:
                if not b"encoding=\"UTF-8\"" in line:
                    output.write(line)
    os.remove(file_src)
    os.rename(file_src+".bak", file_src)
    return file_src

def open_xml(file_xml):
    replase_xml_text(file_xml)
    with open(file_xml, 'rb') as f:
        xml = f.read()
    return xml

def parse_xml(xml_data):
    data = xml_data.decode('utf-8')
    root = objectify.fromstring(data)
    for tag_all in root.getchildren():
        if tag_all.tag == 'tab':
            id_tab = uuid.uuid1()
            parse_tab(tag_all, id_tab)

def rename_after_save(file_name):
    os.rename(file_name, file_name+".saved")

def main():
    write_log("Run script...")
    xml_files = [f for f in os.listdir(xml_dir) if f.endswith('.xml')]
    f_cou_all = len(xml_files)
    log_txt = "Find XML files: " + str(f_cou_all)
    print(log_txt)
    write_log(log_txt)
    file_proc = 0
    for f_name in xml_files:
        log_txt = "File satart save: " + f_name
        print(log_txt)
        write_log(log_txt)
        xml_f = open_xml(xml_dir+f_name)
        parse_xml(xml_f)
        rename_after_save(xml_dir+f_name)
        log_txt = "File saved OK."
        file_proc += 1
        print(log_txt)
        write_log(log_txt)
        log_txt = "File processed: "+str(file_proc)+"/"+str(f_cou_all)
        print(log_txt)
        write_log(log_txt)
        log_txt = "*************************************************"
        print(log_txt)
        write_log(log_txt)

if __name__ == '__main__':
    log_text = "Загрузчик XML файлов <Карточки ДТП> в БД"
    print(log_text)
    main()

