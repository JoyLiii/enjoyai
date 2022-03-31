# -*- coding: utf-8 -*-
"""
Created on Tue Mar 16 16:26:21 2021

@author: JoyWCLi
取用資料夾內的資料集做切割

"""

import argparse #承接網頁傳回的參數
import sys
import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.model_selection import train_test_split
from sqlalchemy import create_engine,text
import time
import datetime
import pymysql.cursors
from profiling_function_dll import *
import configparser

import ctypes


def check_dongle():
    
    #vendor code
    vendorCode = "GCvSll31KWbbepnAAYUnaPF2Nm4OspeXvRQCHqE6QZHKb5gZkrlfFPCpzNwcyfT4dfLMRSgY7/Lbb4UY" \
        "7CvJtX0AAGVQfluR0p/OlOU6gyFO1wpiT8CfXxddohLTJKGe0KP5qaXibTtCFylm9cIyf3KBUrbsHmgm" \
        "KK7uhFvUa4WFTzncKYSgC2kGKTaWXvA9BSEG3JilyC0oLaTTOBaa3sCmus8HzjrnrIC7cG70hhvL5J8K" \
        "ZTLXzAIJn2gt8MMB5DyI5hmrB0SavaBbHgk3m0YEBv73qrdf+mwmxCMxoTGw6VrMXdEuTX0xUPuspMbI" \
        "UPTCu6W236G7OEifAT/aCuMCOCab4jrm/A7GPj+sbvPDtywPVRN+4KJxKkywutbs4VFzHQhWaoXCQHdv" \
        "guT9rDAyoNIR+9DTfV3YW0YtH2TKSTXtVCQNa2W1BFTPZUkEoE1Zl0Svbzoy+19yQRyV99+Q8SCjGNUU" \
        "ZLTEbVclChPR8qHocugxCtPIXlaWCAdxKq03OdD3Q8qw+BmWu64k/nmE9Cwe9lQLGC0YnVvIn/GQGp6M" \
        "XZfZuVOgjXcfKmjnddwZa8wKoVDJcBgjfSin6SusbZpwcctNPqiEzbjZ4gkZ0WpqSZzbf5Uo12uDY2oy" \
        "zpYBQ/ew8H2ahYxrTQMLTPCJt+PQkPt54wI72aaKySq9iZVyvVu0LjH4PVmYTHht4FrT435AdAqADJDQ" \
        "Kh1HHqOiXPTzZgo8ZPjLz1VgW72ozpKaru8LWprvkp9BCi6Gi5hynWqNDKTBx7dRP0v07ZFS35gWwqcg" \
        "fRqWDiL8vYOiTWAC7gTWpNkPWS4eC30pgyuAx7AFEo+BUAX7zpxqy4H5HKVAjYP86SVMs1Js+eDzBJJx" \
        "vvM/n/wM7jrC9FBzwkMvElFLhViO9M3TkTccascxu+JAavtncoczyzWGUTrHFMr8ZKHpSuqXoQPqYAJO" \
        "Kd81MHbcZNl4uojekW7w5A=="
    
    #轉成C、配置featureID
    pstrvendorcode = ctypes.c_char_p()
    pstrvendorcode.value = vendorCode.encode()
    handle = ctypes.c_uint32()
    intFeatureID = ctypes.c_uint32(1)
    intreturnstatus = ctypes.c_uint32()
    
    hasplib = ctypes.CDLL("hasp_windows_x64_112979.dll")
    
    #呼叫hasp
    intreturnstatus = hasplib.hasp_login(intFeatureID,pstrvendorcode,ctypes.byref(handle))
    
    return_word = ""
    if intreturnstatus == 0:
        return_word = "success"
        print("success")
    
    else:
        return_word = "dongle fail (" + str(intreturnstatus)+ ")"
        print("dongle fail")
        print("error message code",intreturnstatus)
        
    return return_word    


def status_change(change_number, update_status):
    '''SQL Server info'''
    config = configparser.ConfigParser()
    config.read(config_path)
    server = config['database']['server']
    DBuser = config['database']['DBuser']
    password = config['database']['password']
    database = config['database']['database']
    port = int(config['database']['port'])

    
    #資料庫連線設定
    db = pymysql.connect(host=server, port=port, user=DBuser, passwd=password, db=database, charset='utf8')       
    #建立操作游標
    cursor = db.cursor()
    #SQL語法
    sql = f" UPDATE automl_db.databse_info2 SET Dataset_status='{update_status}' WHERE Dataset_number='{change_number}';"                 
    cursor.execute(sql)
    #提交修改
    cursor.close()
    db.commit()         
    db.close()


def row_col_f(data_path_name,data_number, splitted_data):
    
    # data_path_name = "D:/joy/automl_upload_file/2103191441582/2103191441582_out2.xlsx"
    # data_path_name = r"D:\joy\automl_upload_file\210420085925\MVA2_M270HAN1C.XLSX"
    i_data_path_name = data_path_name.replace('\\' , '//')
    sub_str = i_data_path_name[-3:]
    
    rows = 0
    cols = 0
    column_list_str = ""
    type_list_str = ""
    web_opid_list_df = pd.DataFrame()
    web_opid_list_df = splitted_data
    rows = web_opid_list_df.shape[0]
    cols = web_opid_list_df.shape[1]    
    # if sub_str == "csv":
        
    #     try:
    #         web_opid_list_df = pd.read_csv(i_data_path_name,encoding='utf-8')
    #         rows = web_opid_list_df.shape[0]
    #         cols = web_opid_list_df.shape[1]
    #     except Exception:
    #         web_opid_list_df = pd.read_csv(i_data_path_name,encoding='big5')
    #         rows = web_opid_list_df.shape[0]
    #         cols = web_opid_list_df.shape[1]
    # elif sub_str == "lsx":
    #     web_opid_list_df = pd.read_excel(i_data_path_name)
    #     rows = web_opid_list_df.shape[0]
    #     cols = web_opid_list_df.shape[1]
        
    type_df = pd.DataFrame(web_opid_list_df.dtypes)
    type_df[0] = type_df[0].apply(lambda _: str(_))
    column_list = pd.Series(type_df.index)
    type_list = pd.Series(type_df[0])
    
    column_list_str = column_list.str.cat(sep='!!')
    type_list_str = type_list.str.cat(sep='!!')
    

    dataset_name = "1"
    column_list = str(column_list_str)
    type_list = str(type_list_str)
    upload_filename = str(i_data_path_name)
    size_f_upload = str(os.path.getsize(i_data_path_name))
    txt_date = str(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    r=str(rows)
    c=str(cols)
    file_size = str(os.path.getsize(i_data_path_name))


    '''SQL Server info'''
    config = configparser.ConfigParser()
    config.read(config_path)    
    server = config['database']['server']
    DBuser = config['database']['DBuser']
    password = config['database']['password']
    database = config['database']['database']
    request_table_name = "databse_info2"
    port = int(config['database']['port'])

    # server = '10.96.48.148' #IP:port
    # DBuser = 'automl'
    # password = 'automl$0'
    # database = 'automl_db'
    # request_table_name = "databse_info2"
    # port = 3306
    
    i_data_path_name_array = i_data_path_name.split("/")
    dataset_real_path = i_data_path_name_array[len(i_data_path_name_array)-1]      
        
    #資料庫連線設定
    db = pymysql.connect(host=server, port=3306, user=DBuser, passwd=password, db=database, charset='utf8')
    #建立操作游標
    cursor = db.cursor()
    #SQL語法
    # sql2 = "INSERT INTO " + database + "." + request_table_name + " ( Dataset_number,Dataset_name,Row_no, Column_no,Column_list,Type_list,Dataset_status,Dataset_path,Dataset_size,Upload_time ) VALUES ('" + i_dataset_number + "','" + dataset_name + "', " + r + " , " + c + " ,'" + column_list + "' ,'" + type_list + "' ,'資料集上傳111','" + upload_filename + "','" + size_f_upload + "','" + txt_date + "');"
    
    txt_date = str(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    sql = "UPDATE " + database + "." + request_table_name + " SET Row_no =  " + r + " , Column_no = " + c + "  ,Column_list = '" + column_list + "' ,Type_list =  '" + type_list + "' ,Dataset_status = '資料繪製中' ,Dataset_size = '" + file_size + "' ,Dataset_path = '" + dataset_real_path + "' ,Modify_time = '" + txt_date + "' WHERE Dataset_number = '" + data_number + "';" 
    
   

    cursor.execute(sql)
    #提交修改
    db.commit()
    db.close()

    return("success update sql")
    
    #輸出：success

def main(py_config_path):       
    global engine
    global config_path
    global tmp_train_number
    global tmp_test_number
    config_path = py_config_path
    
    '''SQL Server info'''
    config = configparser.ConfigParser()
    config.read(config_path)
    server = config['database']['server']
    DBuser = config['database']['DBuser']
    password = config['database']['password']
    database = config['database']['database']
    file_db = config['database']['file_db']
    port = int(config['database']['port'])

    engine = create_engine(f"mysql+pymysql://{DBuser}:{password}@localhost:{port}/{database}")
    file_engine = create_engine(f"mysql+pymysql://{DBuser}:{password}@localhost:{port}/{file_db}")


    parser = argparse.ArgumentParser(description='')
    parser.add_argument('--original_f_number', type=str, default="")
    parser.add_argument('--train_f_name', type=str, default="")
    parser.add_argument('--test_f_name', type=str, default="")
    parser.add_argument('--path_train', type=str, default="")
    parser.add_argument('--path_test', type=str, default="")
    parser.add_argument('--original_f_path', type=str, default="")
    
    parser.add_argument('--target', type=str, default="")
    parser.add_argument('--random_seed', type=str, default="")
    parser.add_argument('--datashuffle', type=str, default="")
    parser.add_argument('--timecolumn', type=str, default="")
    parser.add_argument('--train_ratio', type=str, default="")
    
    parser.add_argument('--img_train_path', type=str, default="")
    parser.add_argument('--img_test_path', type=str, default="")
    args = parser.parse_args()         
    
    i_original_f_number = args.original_f_number        
    i_train_f_name  = args.train_f_name # train 檔案名稱
    i_test_f_name  = args.test_f_name # test 檔案名稱
    i_path_train  = args.path_train #train 檔案資料夾路徑
    i_path_test  = args.path_test #test 檔案資料夾路徑
    i_original_f_path  = args.original_f_path #train 檔案資料夾路徑
    i_img_train_path  = args.img_train_path #train 圖片檔案資料夾路徑
    i_img_test_path  = args.img_test_path #test 圖片檔案資料夾路徑
    
    
    i_target = args.target #target
    i_random_seed  = args.random_seed #random_seed
    i_datashuffle  = args.datashuffle #datashuffle
    i_timecolumn  = args.timecolumn #timecolumn
    i_train_ratio  = args.train_ratio #train_ratio

    
    '''joy test'''
    # i_original_f_number = "220316112934"
    # i_train_f_name  = "220316114117_out1" # train 檔案名稱
    # i_test_f_name  = "2203161141172_out2" # test 檔案名稱
    # i_path_train  = "D:/joy/automl_upload_file/220316114117/" #train 檔案資料夾路徑
    # i_path_test  = "D:/joy/automl_upload_file/2203161141172/" #test 檔案資料夾路徑
    
    # i_original_f_path  = "D:/joy/automl_upload_file/220316112934/" #train 檔案資料夾路徑
    # i_img_train_path  = r"D:\joy\web\AutoML_web_vb\upload_file_img/220316114117/profiling_data/" #train 圖片檔案資料夾路徑
    # i_img_test_path  = r"D:\joy\web\AutoML_web_vb\upload_file_img/2203161141172/profiling_data/" #test 圖片檔案資料夾路徑
    
    
    # i_target = "y" #target
    # i_random_seed  = "3" #random_seed
    # i_datashuffle  = "True" #datashuffle
    # i_timecolumn  = "NO_NEED" #timecolumn
    # i_train_ratio  = "50" #train_ratio
    
    '''取得 train / test 的 ID'''
    
    tmp_train_number_array = i_path_train.split("/")
    tmp_train_number = tmp_train_number_array[len(tmp_train_number_array)-2]
    tmp_test_number_array = i_path_test.split("/")
    tmp_test_number = tmp_test_number_array[len(tmp_test_number_array)-2]
        
    try:        

        '''執行dongle驗證，驗證失敗，強制結束'''
        dongle_status = check_dongle()
        if dongle_status == "success":
            status_change(tmp_train_number, "dongle success")
            status_change(tmp_test_number, "dongle success")
        else:
            status_change(tmp_train_number, dongle_status)
            status_change(tmp_test_number, dongle_status)
            print(dongle_status)
            sys.exit(0)

        if i_train_ratio == "NO_NEED":
            i_train_ratio_int = 0
        else:
            i_train_ratio_int = int(i_train_ratio) / 100
            
        # =============================================================================
        #         讀取要切割的完整資料集
        # =============================================================================
        # 查詢語句，選出train表中的所有數據 
        sql = f''' 
            select * FROM automl_file_db.`{i_original_f_number}`;    
        ''' 
        original_db = pd.read_sql_query(sql, engine)    
        web_opid_list_df = original_db
        # =============================================================================
        #           刪除target欄位中 為空的資料  
        # =============================================================================
        web_opid_list_df.dropna(subset=[i_target],inplace= True)
        y = web_opid_list_df[i_target]
        
        # # data_path_name = r"D:\joy\automl_upload_file\210420085925\MVA2_M270HAN1C.XLSX"       
        # flag = 0
        # #取得網頁OPID_LIST
        # web_opid_list = i_original_f_path
        # # web_opid_list = "D:/joy/automl_upload_file/23_ALL_WIP_YT2.xlsx"
        # web_opid_list = web_opid_list.replace('\\' , '/')
        # sub_str = web_opid_list[-3:]
        
        # if sub_str.lower() == "csv":
        #     flag = 0
        #     web_opid_list_df = pd.read_csv(web_opid_list)
        #     # =============================================================================
        #     #           刪除target欄位中 為空的資料  
        #     # =============================================================================
        #     web_opid_list_df.dropna(subset=[i_target],inplace= True)
            
        #     y = web_opid_list_df[i_target]
        
        # elif sub_str.lower() == "lsx":
        #     if sub_str == "LSX":
        #         upper_flag = 1
        #     else:
        #         upper_flag = 0
        #     flag = 1
        #     web_opid_list_df = pd.read_excel(web_opid_list)
        #     # =============================================================================
        #     #           刪除target欄位中 為空的資料  
        #     # =============================================================================
        #     web_opid_list_df.dropna(subset=[i_target],inplace= True)
            
        #     y = web_opid_list_df[i_target]
        


        
        if i_train_ratio == "NO NEED" and i_datashuffle == "True":
            # create training and testing vars
            X_train, X_test, y_train, y_test = train_test_split(web_opid_list_df, y, shuffle=True, random_state = int(i_random_seed), stratify=y)
        elif i_train_ratio == "NO NEED" and i_datashuffle == "False":
            X_train, X_test, y_train, y_test = train_test_split(web_opid_list_df, y, shuffle=False, random_state = int(i_random_seed))
        elif ~(i_train_ratio == "NO NEED") and i_datashuffle == "False":
            X_train, X_test, y_train, y_test = train_test_split(web_opid_list_df, y, train_size=i_train_ratio_int, shuffle=False, random_state = int(i_random_seed))
        elif ~(i_train_ratio == "NO NEED") and i_datashuffle == "True":
            X_train, X_test, y_train, y_test = train_test_split(web_opid_list_df, y, train_size=i_train_ratio_int, shuffle=True, random_state = int(i_random_seed), stratify=y)
            
        X_train_all = X_train
        X_test_all = X_test
        # X_train_all = pd.concat([X_train, pd.DataFrame(y_train)]) 
        # X_test_all = pd.concat([X_test, pd.DataFrame(y_test)]) 
            
        train_final_path_name = ""
        train_final_path = i_path_train
        train_final_number = ""
        
        test_final_path_name = ""
        test_final_path = i_path_test
        test_final_number = ""
        train_final_path_name = i_path_train + i_train_f_name + ".xlsx"
        test_final_path_name = i_path_test + i_test_f_name + ".xlsx"
        
        a = pd.DataFrame(X_train_all).to_excel(train_final_path_name , index=False)
        b = pd.DataFrame(X_test_all).to_excel(test_final_path_name , index=False)
        train_number_array = i_path_train.split("/")
        train_number = train_number_array[len(train_number_array)-2]
        
        update_sql = ""
        update_sql = row_col_f(train_final_path_name, train_number, X_train_all)
        
        test_number_array = i_path_test.split("/")
        test_number = test_number_array[len(test_number_array)-2]
        
        update_sql_test = ""
        update_sql_test = row_col_f(test_final_path_name, test_number, X_test_all)
        
        train_final_number = train_number
        test_final_number = test_number        
        # if flag == 0:
        #     #work for .csv
        #     train_final_path_name = i_path_train + i_train_f_name + ".csv"
        #     test_final_path_name = i_path_test + i_test_f_name + ".csv"

            
        #     a = pd.DataFrame(X_train).to_csv(train_final_path_name , index=False)
        #     b = pd.DataFrame(X_test).to_csv(test_final_path_name , index=False)
        #     train_number_array = i_path_train.split("/")
        #     train_number = train_number_array[len(train_number_array)-2]
            
        #     update_sql = ""
        #     update_sql = row_col_f(train_final_path_name, train_number)
            
            
        #     test_number_array = i_path_test.split("/")
        #     test_number = test_number_array[len(test_number_array)-2]
            
        #     update_sql_test = ""
        #     update_sql_test = row_col_f(test_final_path_name, test_number)
            
        #     train_final_number = train_number
        #     test_final_number = test_number
        # elif flag == 1:
        #     #work for .xlsx
        #     if upper_flag == 1:
        #         train_final_path_name = i_path_train + i_train_f_name + ".xlsx"
        #         test_final_path_name = i_path_test + i_test_f_name + ".xlsx"
        #     else:
        #         train_final_path_name = i_path_train + i_train_f_name + ".xlsx"
        #         test_final_path_name = i_path_test + i_test_f_name + ".xlsx"
            
        #         train_final_path_name = i_path_train + i_train_f_name + ".xlsx"
        #         test_final_path_name = i_path_test + i_test_f_name + ".xlsx"
            
        #     a = pd.DataFrame(X_train).to_excel(train_final_path_name , index=False)
        #     b = pd.DataFrame(X_test).to_excel(test_final_path_name , index=False)
        #     train_number_array = i_path_train.split("/")
        #     train_number = train_number_array[len(train_number_array)-2]
            
        #     update_sql = ""
        #     update_sql = row_col_f(train_final_path_name, train_number)
            
        #     test_number_array = i_path_test.split("/")
        #     test_number = test_number_array[len(test_number_array)-2]
            
        #     update_sql_test = ""
        #     update_sql_test = row_col_f(test_final_path_name, test_number)
            
        #     train_final_number = train_number
        #     test_final_number = test_number
            
        # 資料新增進入資料庫
        con = file_engine.connect()
        pd.DataFrame(X_train_all).to_sql(name=train_final_number, con=con, if_exists='replace', index=False)
        pd.DataFrame(X_test_all).to_sql(name=test_final_number, con=con, if_exists='replace', index=False)
        
        status_change(train_final_number, "split done")
        status_change(test_final_number, "split done")

        # 繪製heatmap / histogram / bar plot
        # i_f_path = "D:/joy/"
        # i_f_path_name = "D:/joy/ALL_WIP_YT.xlsx"
        # i_f_number = "123456"
        i_f_path = train_final_path
        i_f_number = train_final_number
        i_f_path_name  = train_final_path_name
        a = profile_fun(X_train_all,i_f_path, i_f_path_name,i_f_number,i_img_train_path)
        

        
        i_f_path = test_final_path
        i_f_number = test_final_number
        i_f_path_name  = test_final_path_name
        a = profile_fun(X_test_all,i_f_path, i_f_path_name,i_f_number,i_img_test_path)
        

        print("split done.")
    except Exception as ex:
        status_change(tmp_train_number, "split fail")
        status_change(tmp_test_number, "split fail")
        print("split fail." + str(ex))



    