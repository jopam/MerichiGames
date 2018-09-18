# -*- coding: utf-8 -*-
"""
Created on Fri Sep  7 09:55:43 2018

@author: Justin
"""
from kivy.uix.screenmanager import  Screen
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.app import App
kv = '''
<MyButton>:
    text_size: self.size
    on_size: app.resizeText(self)
    on_text: app.resizeText(self)
    halign: 'center'
    valign: 'center'
<MyLabel>:
    text_size: self.size
    on_size: app.resizeText(self)
    on_text: app.resizeText(self)
    halign: 'center'
    valign: 'center'
'''

#Keeps text size constant as it is resized
@staticmethod
def resizeText(lbl):
    dummyLbl = Label(text=lbl.text,font_name=lbl.font_name,font_size = 0)
    size = lbl.size
    text_size = dummyLbl._label.get_extents(dummyLbl.text)
    while text_size[0] < size[0] and text_size[1] < size[1]:
        dummyLbl.font_size += 1
        text_size = dummyLbl._label.get_extents(dummyLbl.text)
    lbl.font_size = dummyLbl.font_size-1
    
class MyButton(Button):
    pass
class MyLabel(Label):
    pass
class MyScreen(Screen):
    #Upon leaving any screen, update screen history unless previous button is used
    def on_pre_leave(self):
        history = App.get_running_app().root.screen_history
        if len(history) == 0 or history[-1] is not None:
            App.get_running_app().root.screen_history.append(self)
        else:
            App.get_running_app().root.screen_history.pop()
