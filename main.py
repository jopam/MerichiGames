# -*- coding: utf-8 -*-
"""
Created on Sat Sep  1 10:33:16 2018

@author: Justin
"""

#Kivy Imports
from kivy.lang.builder import Builder
from kivy.uix.screenmanager import ScreenManager
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.properties import ObjectProperty
from kivy.properties import NumericProperty
from kivy.factory import Factory
from kivy.clock import Clock

#Game Imports
import resources as r
import gc

kv_string = '''
#:import FadeTransition kivy.uix.screenmanager.FadeTransition
#:import F kivy.factory.Factory
#:import Window kivy.core.window.Window

RootController:
    rm:rm
    volume_btn:volume_btn
    orientation:'vertical'
    ActionBar:
        ActionView:
            ActionButton:
                id:volume_btn
                icon: 'assets/volume.png'
                on_press: root._volume.open()
            ActionPrevious:
                app_icon: 'assets/icon.jpg'
                title:'Merichi Games'
                with_previous: True
                previous_image: 'assets/back.png'
                on_press: root.previous()
    RootManager:
        id:rm
        transition: FadeTransition()
        RootScreen:
            name: 'root'
            
<RootScreen>:
    GridLayout:
        canvas:
            Rectangle:
                pos: self.pos
                size: self.size
                source: 'assets/menu.jpg'
        rows: 3
        cols: 2
        padding: 10
        spacing: 10
        MyButton:
            background_normal: 'assets/tttbtn.png'
            text: 'Tic-Tac-Toe'
            color: 1,1,1,1
            on_press:
                if root.manager.has_screen('ttt'): root.manager.current = 'ttt'
                else: app.root.createTTT()
        MyButton:
        MyButton:
        MyButton:
        MyButton:
        MyButton:

<Volume@ModalView>:
    size_hint: 0.05,0.5
    attach_to: app.root
    pos_hint: {'right': 1,\
               'top':app.root.volume_btn.y/Window.height}
    on_dismiss: self.funbind('center', self._align_center)
    Slider:
        orientation: 'vertical'
        value_track: True
        value_track_color: [57/255,1,20/255,1]
        value: 100
        min:0
        max:100
        on_value: app.root.master_volume = self.value_normalized
    
    
'''
class RootController(BoxLayout): 
    screen_history = []
    rm = ObjectProperty()
    tttm = ObjectProperty()
    master_volume = NumericProperty(1)
    
    def __init__(self,*args,**kwargs):
        super(RootController,self).__init__(*args,**kwargs)
        Clock.schedule_once(lambda dt: self.setup(),0)
        
    def setup(self):
        self._volume = Factory.Volume()
        
    #Switches to previous screen
    def previous(self):
        if self.screen_history:
            prev = self.screen_history.pop()
            self.screen_history.append(None)
            prev.manager.current = prev.name
    
    '''
    All new apps need to be of the form:
    <Controller@MyScreen>:
        Manager@ScreenManager:
            ...
    and the controller must have two methods:
        cleanUp() and introSetup()
    '''
    
    #Creates TicTacToe App
    def createTTT(self):
        import TicTacToe as TTT
        Builder.load_string(TTT.kv)
        temp = TTT.TTTController()
        self.rm.add_widget(temp)
        self.rm.current = 'ttt'
        self.tttm = temp.ids['tttm']
class RootManager(ScreenManager):
    pass
class RootScreen(r.MyScreen):
    
    #Cleanup apps when exiting them
    def on_enter(self):
        for app in self.manager.screens:
            if app != self:
                app.cleanUp()
        gc.collect()
        
    #Intro apps when entering them
    def on_leave(self):
        self.manager.current_screen.introSetup()

class Games(App):
    resizeText = r.resizeText
    
    def build(self):
        self.icon = 'assets/icon.jpg'
        Builder.load_string(r.kv)
        return Builder.load_string(kv_string)
    
if __name__=='__main__':
    Games().run()
