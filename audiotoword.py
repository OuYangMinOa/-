  #coding:utf8
# -*- coding: UTF-8 -*-
import speech_recognition
import jieba
from pygame import mixer
from gtts import gTTS
import sys
import os
import math
import jieba.posseg
import numpy as np
import socket
import sys
import threading
import json
import requests
global ll,trans
global all_address,all_conn
global host
global port
global s
global conn_all
global add_all
host =''
port = 9998
s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
all_address=[]
all_conn=[]
def get_ip():
        try:
            ip_url = "http://jsonip.com/"
            req = requests.get(ip_url)
            ip_json = json.loads(req.text)
            return ([(s.connect(('8.8.8.8', 53)), s.getsockname()[0], s.close()) for s in [socket.socket(socket.AF_INET, socket.SOCK_DGRAM)]][0][1])
        except Exception as e:
            print('cant get ip:{}'.format(e))
def socket_create():
    try:
        global host
        global port
        global s
    except socket.error as msg:
        erro_time+=1
        ptint("socket creation error:"+str(msg)+str(erro_time))    
def socket_blind():
    try:
        global host
        global port
        global s
        print("Bind socket to port:"+str(port))
        s.bind((host, port))
        s.listen(10)
    except:
        socket_blind()
#************************** 冗言贅字 ******************************
def none_use_word():
    global trans
    trans=trans.replace('請','')
    trans=trans.replace('上','')
    trans=trans.replace('以','')
    trans=trans.replace('掉','')
    trans=trans.replace('一路','')
    trans=trans.replace('幫','')
    trans=trans.replace('我','')
    trans=trans.replace('算','')
    trans=trans.replace('出','')
    trans=trans.replace('是多','')
    trans=trans.replace('喔','')
    trans=trans.replace('多','')
    trans=trans.replace('少','')
    trans=trans.replace('诶','')
    
    trans=trans.replace('呢','')
    trans=trans.replace('阿','')
    trans=trans.replace('哈','')
    trans=trans.replace('可','')
    trans=trans.replace('話','')
    trans=trans.replace('說','')
    trans=trans.replace('所','')
def point():
    global trans, jlist
    if '點' in trans:
        
        for ji in range(trans.index('點')+1,len(trans)):
            try:
                if trans[ji]=='零':
                    trans = trans[:ji]+'0'+trans[ji+1:]
                elif not num_change(trans[ji]):
                    break
                print(trans[ji])
            except Exception as e:
                print(e)
                break
        trans=trans.replace('點','.',1)
    if '點' in trans:
        point()
#************************** 十千百 ******************************
def ten_change(ins):
     
    ins = ins.replace('0','')
    if '十' in ins:
        for ten_pos in range(0,len(ins)):
            if '十' == ins[ten_pos]:
                break
        
    else:
        ten_pos = len(ins)+1
    if '十' in ins and '百'  not in ins and '千' not in ins and ten_pos==0:
            ins = '一'+ins
            ten_pos = ten_pos +1
        
    if '百' in ins:
        for hundred_pos in range(0,len(ins)):
            if '百' == ins[hundred_pos]:
                break
    else:
        hundred_pos = len(ins)+1
        
    if '千' in ins:
        for thuasand_pos in range(0,len(ins)):
            if '千' == ins[thuasand_pos]:
                break
    else:
        thuasand_pos= len(ins)+1
    one = 0
    ans = 0
    try:
        ans +=num_change(ins[thuasand_pos-1])*1000
    except:
        pass
    try:
        ans +=num_change(ins[hundred_pos-1])*100
    except:
        pass
    try:
        ans +=num_change(ins[ten_pos-1])*10
    except:
        pass
    try:
        ans +=num_change(ins[ten_pos+1])
    except:
        pass
    return ans
#************************** 次方 ******************************
def power():
    global trans,jlist
    for i in jlist:
        if ('次' in i):
            for ji in range(trans.index(i),0,-1):
                print('ji',ji)
                if (trans[ji]=='的'):
                    trans=trans[0:ji]+'**'+trans[ji+1:]
                    break
            
            trans=trans.replace('次方','',1)
            break
        elif ('的平方' in trans):
            trans=trans.replace('的平方','**2',1)
        elif ('平方' in trans):
            trans=trans.replace('平方','**2',1)
    print(trans)
    if ('次方' in trans) or ('平方' in trans):
        power()
#************************** 換數 ******************************
def num_change(ins):
    ins = ins.replace('加','')
    ins = ins.replace('0','')
    try:
        int(ins)
        print(ins,'int?')
        return int(ins)
    except:
        pass
    if ins == '零' or ins == 0:
        return 0
    if ins == '一' or ins == 1:
        return 1
    if ins == '二' or ins == 2:
        return 2
    if ins == '三' or ins == 3:
        return 3
    if ins == '四' or ins == 4:
        return 4
    if ins == '五' or ins == 5:
        return 5
    if ins == '六' or ins == 6:
        return 6
    if ins == '七' or ins == 7:
        return 7
    if ins == '八' or ins == 8 :
        return 8
    if ins == '九' or ins == 9:
        return 9
    if ('十' in ins) or ('百' in ins) or ('千' in ins):
        return ten_change(ins)
    else:
        return False
#************************** 十千百 ******************************
def num_1():
    global trans,jlist
    for i in jlist:
        if ('十' in i) or ('百' in i) or ('千' in i):
            trans=trans.replace(i,str(ten_change(i)),1)
    trans=trans.replace('零','0')
    trans=trans.replace('一','1')
    trans=trans.replace('二','2')
    trans=trans.replace('三','3')
    trans=trans.replace('四','4')
    trans=trans.replace('五','5')
    trans=trans.replace('六','6')
    trans=trans.replace('七','7')
    trans=trans.replace('八','8')
    trans=trans.replace('九','9')
    
    if ('加十' in trans) or ('+十' in trans):
        trans=trans.replace('加十','+10')
        trans=trans.replace('+十','+10')
    if ('乘十' in trans) :
        trans=trans.replace('乘十','*10')
    if ('除十' in trans) :
        trans=trans.replace('除十','/10')
    if ('減十' in trans) :
        trans=trans.replace('減十','-10')
#************************** 絕對值 ******************************       
def abs_in():
    global trans,jlist
    if('的絕對值' in trans):
        trans = trans.replace(jlist[jlist.index('的絕對值')-1],'abs('+jlist[jlist.index('的絕對值')-1],1)
        trans = trans.replace('的絕對值',')')
    if('絕對值' in trans):
        trans = trans.replace(jlist[jlist.index('絕對值')+1],jlist[jlist.index('絕對值')+1]+')',1)
        trans = trans.replace('絕對值','abs(',1)
    print(trans)
    if '絕對值' in trans:
        abs_in()
#************************** 乘 ******************************  
def x():
    global ll,trans
    trans=trans.replace('乘','*')

#************************** 除  ******************************
def x_2():
    global ll,trans
    trans=trans.replace('除','/')
#************************** 加 ******************************
def x_3():
    global ll,trans
    trans=trans.replace('加','+')
#************************** 減 ******************************
def x_4():
    global ll,trans
    trans=trans.replace('減','-')
#************************** 然後 ******************************
def naturlword_and():
    global ll,trans
    if ('然後' in trans):
        trans = trans.replace('然後','(')
        trans = trans + ')'
#************************** 括號 ******************************
def first():
    global trans
    trans = trans.replace('括號','(',1)
    trans = trans.replace('括號',')',1)
    if ('括號' in trans ):
        first()
#************************** 根號 ******************************
def sqrt_get():
    global trans,jlist
    if '開根號' not in trans:
        try:
            trans = trans.replace('根號','math.sqrt(',1)
            trans = trans.replace(jlist[jlist.index('根號')+1],jlist[jlist.index('根號')+1]+')',1)
            try:
                for ji in word_one:
                    if (ji == ''):
                        continue
                    if ji in jlist[jlist.index('根號')-1] :
                        if (jlist.index('根號') == 0):
                            break
                        print(ji,jlist[jlist.index('根號')-1] )
                        trans = trans.replace(jlist[jlist.index('根號')-1],jlist[jlist.index('根號')-1]+'*',1)
            except Exception:
                print(e)
            jlist.remove('根號')
        except Exception as e:
            print(e)
    else:
        try:
            trans = trans.replace('開根號',')',1)
            trans = trans.replace(jlist[jlist.index('開根號')-1] , 'math.sqrt('+jlist[jlist.index('開根號')-1],1)
            jlist.remove('開根號')
        except Exception as e:
            print(e)
    
    if '根號' in trans:
        sqrt_get()
#************************** 分之 ******************************
def Divide():
    global trans,jlist
    for item in jlist:
        if ('分之' in item):
            trans = trans.replace(item,item,1)
            trans = trans.replace('分之','**-1*',1)
    if ('分之' in trans):
        Divide()
    print(trans)
    if '分之' in trans:
        sqrt_get()
#************************** 加到 ******************************
def plus_to():
    global trans,jlist
    try:
        jj = jlist[jlist.index('加到')-1]+ '加到'+jlist[jlist.index('加到')+1]
        ans=0      
        for i in range( min(num_change(jlist[jlist.index('加到')-1]) , num_change(jlist[jlist.index('加到')+1]) ) ,\
                        max(num_change(jlist[jlist.index('加到')-1]) , num_change(jlist[jlist.index('加到')+1]) ) +1):
            ans +=i
        trans = trans.replace('加到',str('+('+str(ans-num_change(jlist[jlist.index('加到')-1])-\
                                               num_change(jlist[jlist.index('加到')+1]))
                                               +')+'),1)
    except Exception as e:
        print(e)
#************************** 負 ******************************
def minus():
    global trans,jlist
    trans = trans.replace('負的','(-1)*',1)
    trans = trans.replace('負','(-1)*',1)
    if '負' in trans :
        minus()

    
jieba.load_userdict('word.txt')
##jieba.load_userdict('word_2.txt')
word_one =['','零','一','二','三','四','五','六','七','八','九'
           ,'負零','負一','負二','負三','負四','負五','負六','負七','負八','負九']

def cut_word():
    global jlist,trans
    jjj = jieba.cut(trans)
    jlist=[]
    for item in jjj:
        print(item)
        jlist.append(item)
ll=1
r = speech_recognition.Recognizer()
print('IP: {}'.format(get_ip()))
socket_create()
socket_blind()
global conn
conn,address = s.accept()
conn_all =[]
add_all = []
def send_file(word):
    global host
    global port
    global s
    global conn
    global address
    global conn_all
    global add_all
    try:
        conn.sendall(word)
        print(conn,address)
    except Exception as e:
        conn,address = s.accept()
        send_file(word)
        print(e)


while 1 :#int(input('輸入1以繼續聽讀 輸入0以結束\n(目前接受算符:加減乘除 分之 次方 根號 加到 負 括號 絕對值 小數 分數)\n輸入~:')):
    print('start:')
##    with speech_recognition.Microphone() as source: #錄製
##        audio = r.listen(source)
##    with open("microphone-results.wav", "wb") as f: #輸出
##        f.write(audio.get_wav_data())

    ##with speech_recognition.AudioFile('microphone-results.wav') as source: #讀檔案
    ##    audio = r.record(source)
    ##    
##    print("audio get")
##    trans =r.recognize_google(audio,language='zh-TW')
##    try:
##        print('trans',trans)
##        print("Transalate finish")
##        jjj = jieba.cut(trans)
##        for item in jjj:
##            print(jjj)
##    except Exception as e:
##        print(e)
    trans=input() #直接輸入
    start_trans = trans
    point() #小數點
    trans = trans.replace('零','')
    print(trans)
    none_use_word()#冗言贅字
    cut_word()
    flag = 0 
    try:
        abs_in()#絕對值 的
        power() #次方 的
        minus()#負號 的
        trans = trans.replace('的','')
        cut_word()
        sqrt_get() #根號
        Divide()#幾分之幾 
        plus_to()# 等差
        print(trans)
        x() #加
        x_2()#減
        x_3()#乘
        x_4()#除
        naturlword_and()#然後
        first()#括號
        print(trans)
        num_1() #必須最後 (換數字)
        print(trans)
    except Exception as e:
        print(e)
    if flag == 0:
        try:
            print(eval(trans))
            trans_ans ='None'
            trans_ans=eval(trans)
            print(str(start_trans)+'計算的結果是'+str(trans_ans))#計算
            tts = gTTS(text=str(str(start_trans)+'計算的結果是'+str(trans_ans)),lang='zh-tw')      
        except Exception as e:
            print('無法計算的文字',start_trans,e)
            tts = gTTS(text=str('很抱歉我無法幫您計算'+str(start_trans)+'....請確定是否有講對'),lang='zh-tw')
        finally:
##            tts.save('ans.mp3')
##            mixer.init()
##            mixer.music.load('ans.mp3')
##            mixer.music.play()
            try:
##                thread1= threading.Thread(target=send_file(str.encode(str(start_trans)+'答案:'+str(trans_ans))))
##                thread1.start()
                send_file(str.encode('接受>'+str(start_trans)+' 答案: '+str(trans_ans)+'\n'))
            except Exception as e:
                send_file(str.encode('接受>'+str(start_trans)+' 答案: '+str(trans_ans)+'\n'))
                print(e)
            
print('end')
        








