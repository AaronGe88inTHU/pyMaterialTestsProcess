# -*- coding: utf-8 -*-
import re
import numpy as np
import pypyodbc as pyodbc
from PyQt5.QtWidgets  import QMessageBox
from xml.etree import ElementTree as ET
import gl_vars
import os

p = re.compile(u"\s+")

def is_float(value):
    try:
        float(value)
        return True
    except:
        return False

def read_txt(file_name):
    tube_sample = {}
    ybcrs = np.array([0.,0.,0.,0.])
    with open(file_name, u"rt") as f:
        for line in f:
            line_strip = line.strip()
            line_re = re.sub(p, u" ", line_strip)
            #print(line_strip)
            if line_re.startswith(u"D1"):
                line_splite = line_re.split(u"=")
                diameter = line_splite[-1]
                tube_sample[u"diameter"] = float(diameter)
                #print(u"diameter", diameter)
            elif line_re.startswith(u"MATERIAL"):
                line_splite = line_re.split(u"=")
                material = line_splite[-1]
                tube_sample[u"material"] = material
            elif line_re.startswith(u"PART_NAME"):
                line_splite = line_re.split(u"=")
                part_name = line_splite[-1]
                tube_sample[u"part_name"] = part_name
            elif line_re.startswith(u"PART_NUMBER"):
                line_splite = line_re.split(u"=")
                part_num = line_splite[-1]
                tube_sample[u"part_number"] = part_num
            elif line_re.startswith(u"WALL_THICK"):
                line_splite = line_re.split(u"=")
                wall_thick = line_splite[-1]
                tube_sample[u"wall_thick"] = wall_thick
            else:
                line_splite = line_re.split(u" ")
                #print(line_splite)
                if is_float(line_splite[0]):
                    ybcr = np.array(line_splite[1:],dtype = np.float64)
                    if float(line_splite[0]) == 1.:
                        ybcrs[:] = ybcr
                    else:
                        if ybcr.shape[0] == 1:   
                            if ybcrs.size == 4:
                                ybcr = np.array([ybcr[0], 0, 0, ybcrs[-1]])
                            else:
                                ybcr = np.array([ybcr[0], 0, 0, ybcrs[-1,-1]])
                               
                        ybcrs = np.vstack([ybcrs,ybcr])
                    
    return tube_sample, ybcrs
    
def read_xml(file_name):
    with open(file_name, u"r") as rf:
        lines = rf.readlines()
        if u"GB2312" in lines[0]:
            lines[0] = u"<?xml version=\"1.0\" encoding=\"utf-8\"?>\n"
        for ii in range(len(lines)):
            if u"<!--" in lines[ii]:
                lines[ii] = u"\n"
            
        with open(file_name, u"w") as wf:
            wf.writelines(lines)
    per=ET.parse(file_name)
    D = float(per.find(u"D1").text)
    
    thick =float(per.find(u"WALL_THICK").text) 
    R = float(per.find(u"BendingDie").text)
    mem_name =per.find(u"MEMBER_NAME").text 
    part_name = per.find(u"PART_NAME").text 
    material = per.find(u"MATERIAL").text
    tube_sample = {u"diameter": D,  u"material":material, u"part_name" : part_name,\
                        u"part_number":mem_name,  u"wall_thick":thick }
    
    root = per.getroot()
    ybcrs = np.array([0, 0, 0, 0])
    #Ys=per.findall(u"./YBC/Bend/Y")
    YBC = root.find(u"YBC")
    for node in YBC.iter(u"Bend"):
        y = float(node.find(u"Y").text)
        b = float(node.find(u"B").text)
        c = float(node.find(u"C").text)
        ybcr = np.array([y, b, c, R])
       
        ybcrs = np.vstack([ybcrs,ybcr])
    return tube_sample , ybcrs
    
    
def write_database(file_name):
    if file_name.endswith(u"txt"):
        tube_sample, ybcrs = read_txt(file_name)
    else:
        tube_sample,  ybcrs = read_xml(file_name)
    try:
        id = os.path.basename(file_name).split(u".")[0]
        sample_ID = u"".join([u"'",id,u"'"])
        
    except KeyError as e:
        QMessageBox.critical (None,  u"Error", u"txt文件读取失败！")
    else:
        try:
            path = os.getenv(u"TBS_DIR")
            path = os.path.join(path, u"导管弯曲.mdb")
            #path = u"导管弯曲.mdb"
            print(path)
            conn = pyodbc.win_connect_mdb(path)
        except pyodbc.Error as e:
            QMessageBox.critical(None, u"错误", u"数据库连接错误"+"\n" +str(e))
            return
        cur = conn.cursor()
        uni_sql = u"select * from SAMPLE_BASIC_INFO where SAMPLE_ID = {0}".format(sample_ID)
        cur.execute(uni_sql)
        row = cur.fetchone()
        if not row:
            try:
                bend_R = ybcrs[-1,-1]
                radius = tube_sample[u"diameter"] / 2
                thick = tube_sample[u"wall_thick"]
                pro_num = ybcrs.shape[0]
                material = u"".join(["'", tube_sample[u"material"],"'"])
                
                uni_sql = u"insert into SAMPLE_BASIC_INFO (SAMPLE_ID,SAMPLE_BEND_RADIUS,SAMPLE_RADIUS,SAMPLE_THICKNESS,SAMPLE_PROCESSNum,SAMPLE_MATER, SAMPLE_DIAMETER) values ({0}, {1}, {2}, {3}, {4}, {5}, {6})".format(\
                            sample_ID, bend_R, radius, thick, pro_num, material, radius*2)
                
                cur.execute(uni_sql)
                conn.commit()
                for ii, ybcr in enumerate(ybcrs): 
                    
                    uni_sql = u"insert into YBC_INFO (SAMPLE_ID,Bend_N, Y, B, C,BEND_R) values ({0}, {1}, {2}, {3}, {4}, {5})".format(\
                                sample_ID, ii + 1, ybcr[0], ybcr[1], ybcr[2], ybcr[3])
                    cur.execute(uni_sql)
                    conn.commit()
                
                    uni_sql = u"insert into MANU_INFO (SAMPLE_ID,Bend_N, Y, B, C,BEND_R) values ({0}, {1}, {2}, {3}, {4}, {5})".format(\
                                sample_ID, ii + 1, ybcr[0], ybcr[1], ybcr[2], ybcr[3])
                    cur.execute(uni_sql)
                    conn.commit()
                    
                
                """
                Add for the defect initiation in 20/8/2019
                """
                for ii,_ in enumerate(ybcrs): 
                    
                    uni_sql = u"insert into SAMPLE_QUALITY_DATA (SAMPLE_ID,Bend_N, WRINKLE, WALL_REDUCE, ELLIPSE) values ({0}, {1}, {2}, {3}, {4})".format(\
                                sample_ID, ii + 1, 0, thick, 0)
                    cur.execute(uni_sql)
                    conn.commit()
                   
                    
            except pyodbc.ProgrammingError as e:
                QMessageBox.critical (None, u"Error", u"插入信息失败"+str(e))
            except KeyError as e:
                QMessageBox.critical (None, u"Error", u"txt文件读取失败")    
            
                
            else:
                QMessageBox.information(None, u"成功", u"添加成功！")
                uni_sql = u"update INTEGRATION_NEW set SAMPLE_ID = {0}".format(sample_ID)
                cur.execute(uni_sql)
                conn.commit()
                gl_vars.SAMPLE_ID = sample_ID[1:-1]
        else:  QMessageBox.critical(None, u"Error", u"导管编号重复！")
    
        conn.commit()
        conn.close()
"""            
if __name__== '__main__':
    import sys
    if len(sys.argv) > 1:
        write_database(sys.argv[1])
    else:
        messagebox.showerror (u"Error", u"参数错误！")
"""
    
