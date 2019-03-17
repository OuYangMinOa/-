# -*- coding: utf8 -*-
from kivy.app import App
#:kivy 1.10.0
import kivy
from kivy.uix.label import Label
from kivy.uix.popup import Popup
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.textinput import TextInput
from kivy.properties import NumericProperty, ReferenceListProperty,\
    ObjectProperty
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager , Screen , FadeTransition
from kivy.uix.widget import Widget
from kivy.core.image import Image as CoreImage
from kivy.core.window import Window
from kivy.clock import Clock
from kivy.core.audio import SoundLoader
from kivy.core.window import Window
from functools import partial
import random
import time
import socket
import threading
#********************* global **********************************#
global pop_how,design_mode,design_blue
global host
global port
global s
s=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
port = 9998
pop_how = 0
design_mode = 0
design_blue = 0
s.settimeout(1/61)
class connect_start(Screen):
    def __init__(self,**kw):
        super(connect_start,self).__init__(**kw)
        Clock.schedule_once(self.button_name, -1)
    def button_name(self, dt):
        self.ids.name.text=u'給我去上正字班'
        self.ids.name.font_name='DroidSansFallback.ttf'
        self.ids.name.font_size=75

        self.ids.say_ok.font_name='DroidSansFallback.ttf'
        self.ids.say_ok.font_size=50
        
##        self.ids.start.text=u'重新整理'
##        self.ids.start.font_name='DroidSansFallback.ttf'
##        self.ids.start.font_size=50
        hi_2=((Button(text=str('重新整理'),
                            font_size=50,
                            size_hint=(0.4,0.2),
                            pos=(Window.size[0]*0.3,Window.size[1]*0.151),
                            font_name='DroidSansFallback.ttf',
                            background_normal="buttonn.png",
                            background_down='buttonn.png'
                    )
                     )
                    )
        self.add_widget(hi_2)
        hi_2.bind(on_release=self.update)

        
        hi_3=((Button(text=str('隨機生成'),
                            font_size=50,
                            size_hint=(0.4,0.2),
                            pos=(Window.size[0]*0.3,Window.size[1]*0.001),
                            font_name='DroidSansFallback.ttf',
                            background_normal="buttonn.png",
                            background_down='buttonn.png'
                    )
                     )
                    )
        self.add_widget(hi_3)
        hi_3.bind(on_release=self.gerator)
        
        clear_screen=((Button(text=str('清除'),
                            font_size=50,
                            size_hint=(0.3,0.4),
                            pos=(Window.size[0]*0.7,Window.size[1]*0.001),
                            font_name='DroidSansFallback.ttf',
                            background_normal="buttonn.png",
                            background_down='buttonn.png'
                    )
                     )
                    )
        self.add_widget(clear_screen)
        clear_screen.bind(on_release=self.clearscreen)
    def clearscreen(self,*args):
         self.ids.say_ok.text=''
        
    def gerator(self,*args):
        get_num=str(random.randint(1,50))+str(random.choice(['+','-','*','/']))+str(random.randint(1,50))
        data = '生成>'+get_num + ' 答案: '+str('{:.2f}'.format(eval(get_num)))
        self.ids.say_ok.text=str(self.ids.say_ok.text+ data+'\n')
    
        
    def update(self,*args):
        def callback():
            print('')
##        popup = Popup(title=u'查看伺服器數據中...',title_font='DroidSansFallback.ttf',
##                                  content=Label(text='請稍後',font_name='DroidSansFallback.ttf'),
##                                  pos_hint={'x':0.1,'y':0.3},size_hint=(0.8,0.4),auto_dismiss=False)
##        popup.open()
        threading.Thread(target=self.get_word(callback)).start()
    def get_word(self,callback):
        global host
        global port
        global s
        s.settimeout(1/61)
        if (design_mode==0):
            try:
                print('等待數據')
                data = s.recv(20480).decode('utf-8')
                print(data)
                self.ids.say_ok.text=str(self.ids.say_ok.text+ data)
                with open('data.txt','a') as f:
                    f.write(data)
            except Exception as e:
                pass
        
##                try:
##                    s.close()
##                    s.connect((host, port))
##                except:
##                    self.parent.current='input_name'
##                    popup = Popup(title=u'無法連線IP:',title_font='DroidSansFallback.ttf',
##                                      content=Label(text='請確定是否連線正確?\n'+str(e),font_name='DroidSansFallback.ttf'),
##                                      pos_hint={'x':0.1,'y':0.3},size_hint=(0.8,0.4),auto_dismiss=True)
##                    popup.open()
##                print('重新開始連線{}'.format(e))
        elif(design_mode==1):
            try:
                print('等待數據')
                data = s.recv(20480).decode('utf-8')
                print(data)
                self.ids.say_ok.text=str(self.ids.say_ok.text+ data)
                with open('data.txt','a') as f:
                    f.write(data)
            except:
                pass
        callback()
class connect_ok(Screen):
    def __init__(self,**kw):
        super(connect_ok,self).__init__(**kw)
        Clock.schedule_once(self.button_name, -1)
        Clock.schedule_interval(self.check_blue,0.1)
    def button_name(self, dt):
        self.ids.name.text=u'歡迎光臨志明的第一個家'
        self.ids.name.font_name='DroidSansFallback.ttf'
        self.ids.name.font_size=50
        hi=((Button(text=str('確定'),
                            font_size=50,
                            size_hint=(0.7,0.3),
                            pos=(Window.size[0]*0.15,Window.size[1]*0.15),
                            font_name='DroidSansFallback.ttf',
                            background_normal="buttonn.png",
                            background_down='buttonn.png'
                    )
                     )
                    )
        self.add_widget(hi)
        hi.bind(on_press=self.change_frame)
    def check_blue(self,dt):
        if (design_blue==0):
            self.ids.say_ok.text=u'連線成功^_^'
            self.ids.say_ok.font_name='DroidSansFallback.ttf'
            self.ids.say_ok.font_size=50
            
        elif(design_blue==1):
            self.ids.say_ok.text=u'連線失敗OAQ..\n志明:你在跟我作對嗎?'
            self.ids.say_ok.font_name='DroidSansFallback.ttf'
            self.ids.say_ok.font_size=50

       
    def change_frame(self,*args):
        if (design_blue==0 or design_mode == 1):
            self.parent.current='connect_start'
        
class input_name(Screen):
    def __init__(self,**kw):
        super(input_name,self).__init__(**kw)
        Clock.schedule_once(self.button_name, -1)
    def button_name(self, dt):
        self.ids.name_in.text=u'請輸入伺服器IP'
        self.ids.name_in.font_name='DroidSansFallback.ttf'
        self.ids.name_in.font_size=50

        self.ids.accept.text=u'確定'
        self.ids.accept.font_name='DroidSansFallback.ttf'
        self.ids.accept.font_size=50

        self.ids.port_how.text=u'Port?'
        self.ids.port_how.font_name='DroidSansFallback.ttf'
        self.ids.port_how.font_size=50     
    def check(self,*args):
        global popup,pop_how,design_blue
        global host
        global port
        global s
        pop_how = 0
        ip = self.ids.port_in.text
        if(ip==''):
            ip='127.0.0.1'
        host = ip
        if (design_mode == 0):  # 非開發者
            try:  
                print('connect to '+str(host))
                s.connect((host, port))
                s.sendall(str.encode('try'))
                self.parent.current='connect_ok'
                design_blue = 0
            except  Exception as e:
                popup = Popup(title=u'無法連線IP:'+str(ip),title_font='DroidSansFallback.ttf',
                                  content=Label(text='請確定是否連線正確?\n'+str(e),font_name='DroidSansFallback.ttf'),
                                  pos_hint={'x':0.1,'y':0.3},size_hint=(0.8,0.4),auto_dismiss=True)
                popup.open()
                pop_how = 1
                design_blue = 1
        elif(design_mode == 1): # 開發者
            try:
                print('connect to '+str(host))
                s.connect((host, port))
                s.sendall(str.encode('try'))
                design_blue = 0
                self.parent.current='connect_ok'
            except  Exception as e:
                self.parent.current='connect_ok'
                design_blue = 1
                print(e)
    def HOW(self,*args):
        global popup,pop_how
        popup = Popup(title=u'如何找到連線IP?',title_font='DroidSansFallback.ttf',
                              content=Label(text='IP都不知道那妳可以關掉這程式了',font_name='DroidSansFallback.ttf'),
                              pos_hint={'x':0.1,'y':0.3},size_hint=(0.8,0.4),auto_dismiss=True)
        popup.open()
        pop_how = 1
class MainScreen(Screen):
    def __init__(self,**kw):
        super(MainScreen,self).__init__(**kw)
        Clock.schedule_once(self.button_name, -1)
    def button_name(self, dt):
        self.ids.name.text=u'志明與他的小夥伴們'
        self.ids.name.font_name='DroidSansFallback.ttf'
        self.ids.name.font_size=50
        self.ids.start.text=u'開始'
        self.ids.start.font_name='DroidSansFallback.ttf'
        self.ids.start.font_size=50

        self.ids.design.text=u'開發者模式'
        self.ids.design.font_name='DroidSansFallback.ttf'
        self.ids.design.font_size=50

    def design_mode(self,*args):
        global popup,pop_how,design_mode
        if (design_mode == 0):
            popup = Popup(title=u'已進入開發者模式',title_font='DroidSansFallback.ttf',
                                  content=Label(text='爾後將會無視所有錯誤\n若要關閉請重開此程式',font_name='DroidSansFallback.ttf'),
                                  pos_hint={'x':0.1,'y':0.3},size_hint=(0.8,0.4),auto_dismiss=True)
            popup.open()
            design_mode = 1
            pop_how = 1
        else:
            popup = Popup(title=u'已進入開發者模式過',title_font='DroidSansFallback.ttf',
                                  content=Label(text='您已經是開發者模式\n我已經失去作用了\n別再傷害我了OAQ\n若要關閉請重開此程式',font_name='DroidSansFallback.ttf'),
                                  pos_hint={'x':0.1,'y':0.3},size_hint=(0.8,0.4),auto_dismiss=True)
            popup.open()
            design_mode = 1
            pop_how = 1
class ScreenManagement(ScreenManager):
    pass
presentation = Builder.load_file("main.kv")
class GminApp(App):
    def __init__(self,**kw):
        super(GminApp,self).__init__(**kw)
        Window.bind(on_key_down=self.Android_back_click)
    def Android_back_click(self,window,key,*args):
        global popup,pop_how
        if key in  (1000,27):
            if pop_how==1:
                try:
                    popup.dismiss()
                    pop_how = 0
                    return True
                except Exception as e:
                    print(e)
            else:
                try:
                    if self.root.current =='MainScreen':
                        return False
                    if self.root.current =='input_name':
                        self.root.current ='MainScreen'
                        return True
                    if self.root.current =='connect_ok':
                        self.root.current ='input_name'
                        return True
                    if self.root.current =='connect_start':
                        self.root.current ='connect_ok'
                        return True
                except:
                    pass
    def build(self):
        return presentation
if __name__ == '__main__':
    GminApp().run()









