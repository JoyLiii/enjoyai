# -*- coding: utf-8 -*-
"""
Created on Mon Mar 22 14:36:17 2021

@author: JoyWCLi
"""

import argparse #承接網頁傳回的參數
import sys
import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import time
import datetime
import pymysql.cursors
from sqlalchemy import create_engine,text
import configparser

import pandas as pd
import pandas_profiling as pdp

import plotly
import plotly.graph_objs as go
import plotly.express as px
import plotly.figure_factory as ff
from plotly.subplots import make_subplots
import plotly.io as pio
import python_config_path
config_path = python_config_path.define_python_config_path()

#sys.path.insert(1, "D:/joy/web/AutoML_web_vb_美兆_v1/python_file")
def png_to_base64_div_script(png_path_str):
    from base64 import b64encode
    # png_path_str = "C:\\inetpub\\wwwroot\\AutoML\\AutoML_user_file\\automl_experiment_file\\210918171853\\SHAP correlation_test_ipa_num_ipa_y.png"
    # 讀取圖片檔案
    fp = open(png_path_str, 'rb')
    img = fp.read()
    fp.close()
    base64_bytes = b64encode(img)
    base64_string = base64_bytes.decode('utf8')
    
    # 在網頁上呈現必須加入
    base64_string = "data:image/png;base64, " + base64_string
    
    # json_str = '{"plot":"' + base64_string + '"}'

    print("============")
    print("Done! ")
    
    return base64_string  

def profile_fun(web_opid_list_df,file_path,file_path_name,file_number,img_path):
    import datetime
    import pandas as pd
    starttime = datetime.datetime.now()
    
    # 將路徑中的\轉換為/img_path
    img_path  = img_path.replace('\\' , '/') #圖片存放路徑

    #將每個dataset 都建立一個profiling_data的資料夾
    file_path = file_path + "profiling_data/"
    
    i_f_path_name = file_path_name
    
    # =============================================================================
    # 繪製圖片、動態圖，並保存json
    # =============================================================================
    skew_png_path_str = '{'
    freq_plot_str = '{'
    heatmap_plot_str = '{'
        
    # =============================================================================
    #     #取得附檔名
    # =============================================================================
    web_opid_list = i_f_path_name
    web_opid_list = web_opid_list.replace('\\' , '//')
    # web_opid_list = "D:/joy/automl_upload_file/ALL_WIP_YT.xlsx"
    sub_str = web_opid_list[-3:]
    
    rows = 0
    cols = 0
    column_list_str = ""
    type_list_str = ""
    # web_opid_list_df = pd.DataFrame()
    # if sub_str == "csv":
    #     web_opid_list_df = pd.read_csv(web_opid_list)
    # elif sub_str == "lsx":
    #     web_opid_list_df = pd.read_excel(web_opid_list)
        
    # =============================================================================
    #     #加快profiling速度
    #     #特徵的結果 轉存 DB
    # =============================================================================
    profile = pdp.ProfileReport(web_opid_list_df, minimal=True)
    ds = web_opid_list_df.describe()
    profile_json_path_name = ""
    profile.to_file(file_path + file_number + "_profiling.json")
    # profile.to_file(file_path + file_number + "_profiling.html")
    profile_json_path_name = file_path + file_number + "_profiling.json"
    
    # 新增detail 的table
    
    
    creatable_sql = f"""
                    CREATE TABLE automl_file_detail_db.`{file_number}` (variable VARCHAR(500), Html_path LONGTEXT, Html_div LONGTEXT, Html_script LONGBLOB, png_script LONGBLOB, logType TEXT, dataType TEXT, Missing TEXT, Mean TEXT, Min TEXT, Max TEXT, Stdev TEXT,Unique_n TEXT, skewness TEXT, INDEX (variable));
                    """    
    #資料庫連線設定
    '''SQL Server info'''
    config = configparser.ConfigParser()
    config.read(config_path)
    server = config['database']['server']
    DBuser = config['database']['DBuser']
    password = config['database']['password']
    database = config['file_detail_database']['database']
    port = int(config['database']['port'])

    db = pymysql.connect(host=server, port=port, user=DBuser, passwd=password, db=database, charset='utf8')  
    #建立操作游標
    cursor = db.cursor()
    try:
    
        cursor.execute(creatable_sql)
        #提交修改
        db.commit()         

    except Exception as ex_create:
        print("create fail")
        print(ex_create)


   
    import json 
    import pandas as pd
    with open(profile_json_path_name) as f:
        data = json.load(f)
        
    var_df = pd.DataFrame()    
    var_dic = data['variables']
    var_df_tmp = pd.DataFrame.from_dict(var_dic, orient='index')
    
    # 重新判定類別型態
    try:
        var_df_tmp["type"][var_df_tmp.loc[:,'n_distinct'] < 3] = "Categorical"
        var_df_tmp['type'][var_df_tmp.loc[:,"type"].str.find("NUM") > -1] = "Numeric"
        var_df_tmp['type'][var_df_tmp.loc[:,"type"].str.find("CAT") > -1] = "Categorical"
        var_df_tmp['type'][var_df_tmp.loc[:,"type"].str.find("UNSUPPORTED") > -1] = "Ignore"
    except Exception:
        print("change fail")
        
    var_df["variable"] = var_df_tmp.index
    var_df["Html_path"] = ""
    var_df["Html_div"] = ""
    var_df["Html_script"] = ""    
    var_df["png_script"] = ""    
    var_df["logType"] = list(var_df_tmp["type"])
    var_df["dataType"] = ""   
    
    try:
        var_df["Missing"] = list(var_df_tmp["n_missing"])
    except Exception:
        var_df["Missing"] =""
        print("Missing fail")

    try:
        var_df["Mean"] = list(var_df_tmp["mean"])
    except Exception:
        var_df["Mean"] = ""
        print("Mean fail")
 
    try:
        var_df["Min"] = list(var_df_tmp["min"])
    except Exception:
        var_df["Min"]=""
        print("Min fail")       

    try:
        var_df["Max"] = list(var_df_tmp["max"])
    except Exception:
        var_df["Max"] = ""
        print("Max fail")        
 
    try:
        var_df["Stdev"] = list(var_df_tmp["std"])
    except Exception:
        var_df["Stdev"]= ""
        print("Stdev fail")           
  
    try:
        var_df["Unique_n"] = list(var_df_tmp["n_distinct"])
    except Exception:
        var_df["Unique_n"] =""
        print("Unique fail")     
  
    try:
        var_df["skewness"] = list(var_df_tmp["skewness"])
    except Exception:
        var_df["skewness"]=""
        print("skewness fail")    
        

    type_df = pd.DataFrame(web_opid_list_df.dtypes) 
    
    try:
        var_df["dataType"] = list(type_df[0])  
    except Exception:
        pass
    var_df = var_df.round({"Mean":3,"Min":3, "Max":3, "Stdev":3, "skewness":3})
    
    # =============================================================================
    #     # heatmap輸出html檔，並將路徑寫入資料庫存放
    # =============================================================================    
    try:
        corrdata = web_opid_list_df.corr()
        fig = go.Figure(data=go.Heatmap(z=corrdata,
                                        x=corrdata.index,
                                        y=corrdata.columns,
                                        colorscale='OrRd'))
        
        heatmap_html_path = img_path + 'heatmap.html'
        # 輸出HTML檔
        plotly.offline.plot(fig, filename = heatmap_html_path, auto_open=False,auto_play=False)
        # 輸出DIV 可直接放在網頁上繪製learning curve
        plot_div_heatmap = plotly.offline.plot(fig, include_plotlyjs = False , output_type = 'div')
        
        # plotly 切割DIV與SCRIPT
        import re
        plot_div_list_heatmap = re.split('<script type="text/javascript">|</script>',plot_div_heatmap)
        plot_div_div_heatmap = plot_div_list_heatmap[0][5:] 
        plot_div_script_heatmap = plot_div_list_heatmap[1] 
    
    
        plot_div_div_heatmap = plot_div_div_heatmap.replace('"',"'")
        plot_div_div_heatmap = plot_div_div_heatmap.replace( "'", "\\" + "'")
        plot_div_script_heatmap = plot_div_script_heatmap.replace('"',"'")
        plot_div_script_heatmap = plot_div_script_heatmap.replace( "'", "\\" + "'")
        
        heatmap_plot_str = heatmap_plot_str + "\"html_path\":" + "\"" +  heatmap_html_path + "\","
        heatmap_plot_str = heatmap_plot_str + "\"html_div\":" + "\"" +  plot_div_div_heatmap.replace("\\" + "\"", "\\" + "'") + "\","
        heatmap_plot_str = heatmap_plot_str + "\"html_script\":" + "\"" +  plot_div_script_heatmap.replace("\\" + "\"", "\\" + "'") + "\""    
    
    
    except Exception:
        
        print("heatmap fail")    

    
    
        
    # =============================================================================
    #     Skew_kurt 輸出圖檔，僅繪製連續型資料，
    #     如果有缺失值，目前採用的補0的方式。
    # =============================================================================
    
    try:
        skew = abs(web_opid_list_df.select_dtypes(include=['float64','Int64']).skew())
        skew_1 = skew[np.where(skew > 1)[0]]
        kurt = abs(web_opid_list_df.select_dtypes(include=['float64','Int64']).kurt())
        kurt_1 = kurt[np.where(skew > 1)[0]]
        var = skew_1.index.union(kurt_1.index)
        web_opid_list_df_fill = web_opid_list_df.copy()
        web_opid_list_df_fill.fillna(0,inplace=True)
        for i in var:
            skew_png_path = ""
            try:
                tmp_var =  str(i)
                group_labels = [str(i)]
                data_ot = [np.array(web_opid_list_df_fill[str(i)])]
                fig2 = ff.create_distplot(data_ot, group_labels)
                fig2.update_layout(
                # titlefont=dict(size=22, color='#7f7f7f'), #設定標題名稱、字體大小、顏色
                    title=i,
                    margin=dict(l=60,r=30,b=30,t=30,pad=0), #調整圖表的位子
                    template= "none", # 變更背景顏色及格線   
                
                
                )
                skew_png_path = img_path + 'skew_kurt_img/' + str(i) +'_skew_kurt.png'
                fig2.write_image( skew_png_path,format="png",engine="kaleido")          
               
                # png圖片轉存base64，以方便後續存放DB
                tmp_skew_base64 = png_to_base64_div_script(skew_png_path)
                
                skew_png_path_str = skew_png_path_str + f"\"{tmp_var}\":" + "\"" +  tmp_skew_base64 + "\","
    
        
            except Exception as skew_ex:
                print("skew fail")
                print(skew_ex)
                tmp_skew_base64 = "" 
        if len(skew_png_path_str) > 1:
            skew_png_path_str = skew_png_path_str[:-1]
            
        print("skew done")  
    except Exception:
        print("skew fail") 
        
        
    # =============================================================================
    #         parallel_categories 待開發
    # =============================================================================
    # import plotly.express as px
    # # fig = px.parallel_categories(web_opid_list_df)
    # fig = px.parallel_coordinates(    web_opid_list_df,
    #                              labels=list(web_opid_list_df.columns),
                                 
    #                              )
    
    # plotly.offline.plot(fig, filename = 'aaaa.html', auto_open=False,auto_play=False)

    # fig.show() 
    
    
        
    # =============================================================================
    #     # scatter_matrix輸出動態圖div文字檔，可寫入資料庫存放
    # =============================================================================

    # scatter_m = px.scatter_matrix(web_opid_list_df)
    
    # fig2 = go.Figure(scatter_m)
    # plotly.offline.plot(fig2, 'test.html', auto_open=False,auto_play=False)

    # plot_div2 = plotly.offline.plot(fig2, include_plotlyjs = False , output_type = 'div')

    # string2 = str(plot_div2)
    
    # =============================================================================
    #     pairplot輸出動態圖div文字檔，可寫入資料庫存放
    # =============================================================================
    # column1 = str(input('pairplotcolumn1(name):'))
    # column2 = str(input('pairplotcolumn2(name):'))
    # pairdata = pd.DataFrame([web_opid_list_df[column1], web_opid_list_df[column2]]).T
    # fig = px.scatter_matrix(pairdata)
    # plot_div3 = plotly.offline.plot(fig, include_plotlyjs = False , output_type = 'div')

    
    # =============================================================================
    #     # 讀取json檔案
    # =============================================================================
    # a = "210325133455_profiling.json"
    import json
    with open(file_path + file_number + "_profiling.json","r") as f:
    # with open(a,"r") as f:
        data = json.load(f)  
    # profile_json_str = json.dumps(data)
    print("profile Ok")
    
    # =============================================================================
    #     # 讀取json中低方差的資料 ，並寫入資料庫
    # =============================================================================
    message_col_str = ""
    try:
        for msg_i in data["messages"]:
            print(msg_i)
            pos = msg_i.find('[CONSTANT] warning')
            if pos >= 0:   # 有找到
                tmp_msg = msg_i.replace("[CONSTANT] warning on column ","")
                tmp_msg = tmp_msg.replace(" ","")
                message_col_str = message_col_str+ tmp_msg + "!next!" 
        if len(message_col_str) > 0:
            message_col_str = message_col_str[:-6]  
    except Exception:
        print("low_variance fail")    
    
    # =============================================================================
    #     # 繪製特徵 histogram / bar plot
    #       同時將json預測的type存放變數中    
    # =============================================================================    
    Logi_column_list = ""
    Logi_type_list = ""    
    try:
        # import matplotlib.pyplot as plot
        for col_name in list(web_opid_list_df.columns):
            data_type = data["variables"][col_name]["type"]
            
            try:
                n_unique = data["variables"][col_name]["n_distinct"]
                if (int(n_unique) < 3) and (web_opid_list_df[col_name].dtypes == "int64"):
                    data_type = "Categorical"
            except Exception:
                print("change type fail")
            
            
            Logi_type_list = Logi_type_list + str(data_type) + "!!"
            Logi_column_list = Logi_column_list + str(col_name) + "!!"
            
            tmp_feature_freq = ""
            tmp_freq_file_path = img_path + col_name + '.html'
            config = {'displayModeBar': False}
            try:
                
                # 區分類別型資料，作圖方式不同
                if data_type == "Categorical" or  data_type == "Variable.TYPE_CAT":
                    
                    
                    
                    if "value_counts_without_nan" in data["variables"][col_name].keys():
                        tmp_value = data["variables"][col_name]["value_counts_without_nan"]
                    else:
                        tmp_value = data["variables"][col_name]["value_counts"]
                    
                    
                    plt.bar(list(tmp_value.keys()),
                    list(tmp_value.values()),
                    bottom=None, 
                    align='center', 
                    # color="#054E9F", 
                    alpha=0.5)
                    plt.xticks(rotation='vertical')
                    plt.savefig(img_path + col_name + ".png")
                    plt.close("all") # 關閉所有圖片，避免圖片重疊;
                    
                    '''測試轉plotly'''
                    fig = px.bar(x=list(tmp_value.keys()),
                                 y=list(tmp_value.values()),
                                                     )
                    
      
                    fig.update_layout(
                            font=dict(
                                size=10,
                            ),
                          xaxis=dict(
                              # title='Histogram with fixed size bins (bins='+ str(bin_size) + ')',
                               # titlefont=dict(size=10),
                                                              # showticklabels = False,
                                                              # visible= False,

                          ),
                          yaxis=dict(
                               # titlefont=dict(size=10),
                                                              # showticklabels = False,
                                                              visible= False,

                          ),
                          margin=dict(l=30,r=30,b=30,t=30,pad=0), #調整圖表的位子
                          template= "none", # 變更背景顏色及格線   
                            width=210,
                            height=210,       
                            showlegend=True,
                        
                    )
                    
                    fig.update_traces(hovertemplate='%{y}') #
                    # 輸出HTML檔
                    plotly.offline.plot(fig, config={'modeBarButtonsToRemove' :[
                     'zoom2d',
                     'toggleSpikelines',
                     'select2d',
                     'lasso2d',
                     'autoScale2d',
                     'hoverClosestCartesian',
                     'hoverCompareCartesian'],"displayModeBar": False}, filename=tmp_freq_file_path, auto_open=False,auto_play=False)
                    # 輸出DIV 可直接放在網頁上繪製learning curve
                    plot_div = plotly.offline.plot(fig, config={'modeBarButtonsToRemove': [
                     'zoom2d',
                     'toggleSpikelines',
                     'select2d',
                     'lasso2d',
                     'autoScale2d',
                     'hoverClosestCartesian',
                     'hoverCompareCartesian'],"displayModeBar": False},include_plotlyjs = False , output_type = 'div')      
                else:
                    try:
                        bin_size = len(data["variables"][col_name]["histogram"]["counts"])
                        
                        plt.hist(web_opid_list_df[col_name].dropna(),bins=bin_size, alpha=0.5, 
                                 # color="#054E9F"
                                 )
                        plt.ylabel('Frequency')
                        plt.xlabel('Histogram with fixed size bins (bins='+ str(bin_size) + ')')
                        plt.savefig(img_path + col_name + ".png")
                        plt. close("all") # 關閉所有圖片，避免圖片重疊;
                        
                        
                        '''測試轉plotly'''
                        aa = web_opid_list_df[col_name].dropna()
                        fig = px.histogram(pd.DataFrame(aa), 
                                            # color="#054E9F", 
                                            # labels={'color': 'y'},
                                            nbins=bin_size,
                                            )
                    
                        
                        fig.update_layout(
                            font=dict(
                                size=10,
                            ),
                            # titlefont=dict(size=22, color='#7f7f7f'), #設定標題名稱、字體大小、顏色
                          xaxis=dict(
                              # title='Histogram with fixed size bins (bins='+ str(bin_size) + ')',
                              title='',
                               # titlefont=dict(size=10),
                                                              # showticklabels = False,
                                                              # visible= False,
                          ),
                          yaxis=dict(
                               # title='Frequency',
                               # titlefont=dict(size=10),
                                                              # showticklabels = False,
                                                              visible= False,

                          ),
                          margin=dict(l=30,r=30,b=30,t=30,pad=0), #調整圖表的位子
                          template= "none", # 變更背景顏色及格線   
                            width=210,
                            height=210,       
                            showlegend=True,
                        )
                        fig.update_traces(hovertemplate='%{y}') #
                        # 輸出HTML檔
                        plotly.offline.plot(fig, config={'modeBarButtonsToRemove' :[
                         'zoom2d',
                         'toggleSpikelines',
                         'select2d',
                         'lasso2d',
                         'autoScale2d',
                         'hoverClosestCartesian',
                         'hoverCompareCartesian'],"displayModeBar": False}, filename=tmp_freq_file_path, auto_open=False,auto_play=False)
                        # 輸出DIV 可直接放在網頁上繪製learning curve
                        plot_div = plotly.offline.plot(fig, config={'modeBarButtonsToRemove': [
                         'zoom2d',
                         'toggleSpikelines',
                         'select2d',
                         'lasso2d',
                         'autoScale2d',
                         'hoverClosestCartesian',
                         'hoverCompareCartesian'],"displayModeBar": False},include_plotlyjs = False , output_type = 'div')                                          
                    except:
                        plt.hist(web_opid_list_df[col_name].dropna(), alpha=0.5, 
                                 # color="#054E9F"
                                 )
                        plt.ylabel('Frequency')
                        plt.xlabel('Histogram with fixed size bins)')
                        plt.savefig(img_path + col_name + ".png")
                        plt. close("all") # 關閉所有圖片，避免圖片重疊;   
                        
                        '''測試轉plotly'''
                        aa = web_opid_list_df[col_name].dropna()
                        fig = px.histogram(pd.DataFrame(aa), 
                                            # color="#054E9F", 
                                            # labels={'color': 'y'},
                                            )
                    
                        
                        fig.update_layout(
                            font=dict(
                                size=10,
                            ),                            
                        # titlefont=dict(size=22, color='#7f7f7f'), #設定標題名稱、字體大小、顏色
                          xaxis=dict(
                               title='',
                               # titlefont=dict(size=10),
                                                              # showticklabels = False,
                                                              # visible= False,

                          ),
                          yaxis=dict(
                               # title='Frequency',
                               # titlefont=dict(size=10),
                                                              # showticklabels = False,
                                                              visible= False,

                          ),
                          margin=dict(l=30,r=30,b=30,t=30,pad=0), #調整圖表的位子
                          template= "none", # 變更背景顏色及格線   
                            width=210,
                            height=210,       
                            showlegend=True,
                        )
                        fig.update_traces(hovertemplate='%{y}') #
                          
                        # 輸出HTML檔
                        plotly.offline.plot(fig, config={'modeBarButtonsToRemove' :[
                         'zoom2d',
                         'toggleSpikelines',
                         'select2d',
                         'lasso2d',
                         'autoScale2d',
                         'hoverClosestCartesian',
                         'hoverCompareCartesian'],"displayModeBar": False}, filename=tmp_freq_file_path, auto_open=False,auto_play=False)
                        # 輸出DIV 可直接放在網頁上繪製learning curve
                        plot_div = plotly.offline.plot(fig, config={'modeBarButtonsToRemove': [
                         'zoom2d',
                         'toggleSpikelines',
                         'select2d',
                         'lasso2d',
                         'autoScale2d',
                         'hoverClosestCartesian',
                         'hoverCompareCartesian'],"displayModeBar": False},include_plotlyjs = False , output_type = 'div')      
                    

                # plotly 切割DIV與SCRIPT
                import re
                plot_div_list = re.split('<script type="text/javascript">|</script>',plot_div)
                plot_div_div_freq = plot_div_list[0][5:] 
                plot_div_script_freq = plot_div_list[1] 
                
                plot_div_div_freq = plot_div_div_freq.replace('"',"'")
                plot_div_div_freq = plot_div_div_freq.replace( "'", "\\" + "'")
                plot_div_script_freq = plot_div_script_freq.replace('"',"'")
                plot_div_script_freq = plot_div_script_freq.replace( "'", "\\" + "'")          
                
                
                
                # 將每一個feature json資料組起來
                
                tmp_feature_freq = tmp_feature_freq + f"\"{col_name}\":" + "{"                                
                tmp_feature_freq = tmp_feature_freq + "\"html_path\":" + "\"" +  tmp_freq_file_path + "\","
                tmp_feature_freq = tmp_feature_freq + "\"html_div\":" + "\"" +  plot_div_div_freq.replace("\\" + "\"", "\\" + "'") + "\","
                tmp_feature_freq = tmp_feature_freq + "\"html_script\":" + "\"" +  plot_div_script_freq.replace("\\" + "\"", "\\" + "'") + "\"" 
                tmp_feature_freq = tmp_feature_freq + "},"
                
                freq_plot_str = freq_plot_str + tmp_feature_freq
                
                # 將每個feature 動態圖存入 dataframe轉存 DB
                tmp_freq_file_path = tmp_freq_file_path.replace("\n"," ")
                plot_div_div_freq = plot_div_div_freq.replace("\n"," ")
                plot_div_script_freq = plot_div_script_freq.replace("\n"," ")
                
                plot_div_div_freq = plot_div_div_freq.replace("\\" + "'","'")
                plot_div_script_freq = plot_div_script_freq.replace("\\" + "'","'")

                
                var_df.loc[var_df["variable"] == col_name,'Html_path'] = tmp_freq_file_path
                var_df.loc[var_df["variable"] == col_name,'Html_div'] = plot_div_div_freq
                var_df.loc[var_df["variable"] == col_name,'Html_script'] = "<script type= text/javascript>" + plot_div_script_freq + "</script>"
                
                try:
                    # png圖片轉存base64，以方便後續存放DB
                    tmp_hist_base64 = png_to_base64_div_script(img_path + col_name + ".png")                             
                except Exception:
                    tmp_hist_base64 = ""
                var_df.loc[var_df["variable"] == col_name,'png_script'] = tmp_hist_base64
            except Exception as ex_plot_histogram:
                plot_div_div_freq = ""
                plot_div_script_freq = ""
                print(f"{col_name} histogram fail")
                print(ex_plot_histogram)
        
        if len(freq_plot_str) > 1:
            freq_plot_str = freq_plot_str[:-1]

    except Exception:
        print("histogram fail")
        
        
        
    try:
        if len(Logi_type_list) > 2:
            Logi_type_list = Logi_type_list[:-2]
            Logi_column_list = Logi_column_list[:-2]
    except:
        Logi_type_list = "fail"
        Logi_column_list = "fail"

    # =============================================================================
    # json字串結尾處理
    # =============================================================================      
    skew_png_path_str = skew_png_path_str + '}'
    freq_plot_str = freq_plot_str + '}'
    heatmap_plot_str = heatmap_plot_str + '}'

    skew_png_path_str = skew_png_path_str.replace("\n"," ")
    freq_plot_str = freq_plot_str.replace("\n"," ")
    heatmap_plot_str = heatmap_plot_str.replace("\n"," ")


    # =============================================================================
    # 將結果寫入資料庫存放
    # =============================================================================
    try:
        '''SQL Server info'''
        config = configparser.ConfigParser()
        config.read(config_path)
        server = config['database']['server']
        DBuser = config['database']['DBuser']
        password = config['database']['password']
        database = config['database']['database']
        port = int(config['database']['port'])
    
        request_table_name = "databse_info2"
    
        
        #資料庫連線設定
        db = pymysql.connect(host=server, port=port, user=DBuser, passwd=password, db=database, charset='utf8')  
        #建立操作游標
        cursor = db.cursor()
        #SQL語法
        endtime = datetime.datetime.now()
        # 執行時間
        a = str(endtime - starttime) 
        txt_date = str(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
        try:
            sql = "UPDATE " + database + "." + request_table_name + " SET Logi_column_list = '" + Logi_column_list + "' ,Logi_type_list = '" + Logi_type_list + "' ,Heatmap_svg = '" + img_path + "paircorr.html" + "' ,Profile_json = '" + profile_json_path_name + "' WHERE Dataset_number = '" + file_number + "';" 
        
            cursor.execute(sql)
            #提交修改
            db.commit()            
        except Exception as ex_sql1:
            print("sql update fail1")
            print(ex_sql1)
            
        try:
            sql = "UPDATE " + database + "." + request_table_name + " SET Low_variance_columns = '" + message_col_str + "' WHERE Dataset_number = '" + file_number + "';" 

        
            cursor.execute(sql)
            #提交修改
            db.commit()            
        except Exception as ex_sql1:
            print("sql update fail2")
            print(ex_sql1)
            
        try:
            sql = "UPDATE " + database + "." + request_table_name + " SET Skew_histogram_png = '" + skew_png_path_str + "' WHERE Dataset_number = '" + file_number + "';" 

        
            cursor.execute(sql)
            #提交修改
            db.commit()            
        except Exception as ex_sql1:
            print("sql update fail4")
            print(ex_sql1)        
            
            
        try:
            sql = "UPDATE " + database + "." + request_table_name + " SET Heatmap_plot = '" + heatmap_plot_str + "' WHERE Dataset_number = '" + file_number + "';" 

        
            cursor.execute(sql)
            #提交修改
            db.commit()            
        except Exception as ex_sql1:
            print("sql update fail5")
            print(ex_sql1)            
            
        # try:
        #     sql = "UPDATE " + database + "." + request_table_name + " SET Variable_distribution_plot = '" + freq_plot_str + "' WHERE Dataset_number = '" + file_number + "';" 

        
        #     cursor.execute(sql)
        #     #提交修改
        #     db.commit()            
        # except Exception as ex_sql1:
        #     print("sql update fail3")
        #     print(ex_sql1)
            
        
        try:
            # =============================================================================
            #     存放profile 細項的資訊
            # =============================================================================            
            data_detail = pd.DataFrame.from_dict(data['table'], orient='index')
            try:
                N_variables = str(data_detail.loc['n_var',0])
                
            except Exception:
                N_variables = "0"
                
            try:
                N_observations = str(data_detail.loc['n',0])
                
            except Exception:
                N_observations = "0"                

            try:
                N_miss = str(data_detail.loc['n_cells_missing',0])
                
            except Exception:
                N_miss = "0"

            try:
                N_duplicate = str(data_detail.loc['n_duplicates',0])
                
            except Exception:
                N_duplicate = "0"


            try:

                N_datatime = str(str(len(var_df_tmp['type'][var_df_tmp.loc[:,"type"].str.find("Date") > -1])))
                
            except Exception:
                N_datatime = "0"


            try:
                N_numeric = str(len(var_df_tmp['type'][var_df_tmp.loc[:,"type"] == "Numeric"]))
                
            except Exception:
                N_numeric = "0"

            try:
                N_category = str(len(var_df_tmp['type'][var_df_tmp.loc[:,"type"] == "Categorical"]))
                
            except Exception:
                N_category = "0"
                
            try:
                N_ignore = str(len(var_df_tmp['type'][var_df_tmp.loc[:,"type"] == "Ignore"]))
                
            except Exception:
                N_ignore = "0"
                
            sql = "UPDATE " + database + "." + request_table_name + " SET N_variables = '" + N_variables + "' ,N_observations = '" + N_observations + "' ,N_miss = '" + N_miss + "' ,N_duplicate = '" + N_duplicate + "' ,N_datatime = '" + N_datatime + "' ,N_numeric = '" + N_numeric + "' ,N_category = '" + N_category + "'  WHERE Dataset_number = '" + file_number + "';" 

        
            cursor.execute(sql)
            #提交修改
            db.commit() 
            
        except Exception as ex_sql1:
            print("sql update fail7")
            print(ex_sql1)


        try:
            sql = "UPDATE " + database + "." + request_table_name + " SET Dataset_status = '" + "OK' ,Modify_time = '" + txt_date + "' WHERE Dataset_number = '" + file_number + "';" 

        
            cursor.execute(sql)
            #提交修改
            db.commit()            
        except Exception as ex_sql1:
            print("sql update fail6")
            print(ex_sql1)           

        

            
        # 資料新增進入資料庫
        from sqlalchemy import create_engine

        engine = create_engine("mysql+pymysql://{}:{}@{}/{}".format(DBuser, password, 'localhost:3306', 'automl_file_detail_db'))
        con = engine.connect()
        
        var_df.to_sql(name=file_number, con=con, if_exists='append', index=False) 
        try:

            sql = "ALTER TABLE automl_file_detail_db.`" + file_number + "` MODIFY  Html_script LONGTEXT;"
 

        
            cursor.execute(sql)
            #提交修改
            db.commit()            
        except Exception as ex_sql1:
            print("sql update fail8")
            print(ex_sql1)     
        try:

            sql = "ALTER TABLE automl_file_detail_db.`" + file_number + "` MODIFY  png_script LONGTEXT;"
 

        
            cursor.execute(sql)
            #提交修改
            db.commit()            
        except Exception as ex_sql1:
            print("sql update fail8")
            print(ex_sql1)     
                        
        db.close()        
    except Exception as ex_sql:
        print("sql fail")
        print(ex_sql)
        


    
    return
    

# if __name__== "__main__":
    
#     import datetime
#     starttime = datetime.datetime.now()
    
#     #網頁參數
#     parser = argparse.ArgumentParser(description='')
#     parser.add_argument('--file_path', type=str, default="")
#     parser.add_argument('--file_path_name', type=str, default="")
#     args = parser.parse_args() 
#     i_f_path  = args.file_path #  檔案路徑
#     i_f_path_name  = args.file_path_name # 檔案名稱
    
#     i_f_path = "D:/joy/"
#     i_f_path_name = "D:/Pycaret/WIP_TEST/0317test/ALL_WIP_YT_bool2.xlsx"
#     i_f_number = "2103231035482"

#     a = profile_fun(i_f_path, i_f_path_name,i_f_number)
 
#     endtime = datetime.datetime.now()
#     print (endtime - starttime)






