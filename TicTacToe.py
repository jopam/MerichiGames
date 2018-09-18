# -*- coding: utf-8 -*-
"""
Created on Thu Sep  6 22:40:30 2018

@author: Justin
"""


from kivy.uix.screenmanager import ScreenManager
from kivy.uix.modalview import ModalView
from kivy.properties import ObjectProperty
from kivy.properties import NumericProperty
from kivy.properties import ListProperty
from kivy.properties import StringProperty
from kivy.app import App
from kivy.factory import Factory
from kivy.clock import Clock
from kivy.config import ConfigParser
from kivy.core.audio import SoundLoader
from kivy.animation import Animation

import webcolors as wc
import random

#Game Imports
import resources as r
from settingsjson import settings_json

kv = '''
#:import WipeTransition kivy.uix.screenmanager.WipeTransition
#:import F kivy.factory.Factory
#:import SettingsWithNoMenu kivy.uix.settings.SettingsWithNoMenu

<TTTController>:
    id:tttc
    name: 'ttt'
    TTTManager:
        id: tttm
        transition: WipeTransition()
        MenuScreen:
            name: 'menu'
        SettingsScreen:
            name: 'settings'
        GameScreen:
            name: 'game'

<MenuScreen>:
    FloatLayout:
        canvas:
            Rectangle:
                source: 'assets/ttt.jpg'
                pos: self.pos
                size: self.size
        MyLabel:
            text: 'Tic Tac Toe'
            size_hint: 1,0.4
            pos_hint: {'center_x':0.5,'center_y':0.7}
            color: 1,1,1,1
        MyButton:
            on_press: root.manager.current = 'game'
            text: 'Play'
            size_hint: 0.3,0.15
            pos_hint: {'center_x':0.5,'center_y':0.4}
            background_color: 0,0,0,0
            color: 1,1,1,1
        MyButton:
            on_press: root.manager.current = 'settings'
            text: 'Settings'
            size_hint: 0.3,0.15
            pos_hint: {'center_x':0.5,'center_y':0.25}
            background_color: 0,0,0,0
            color: 1,1,1,1
<SettingsScreen>:
    mySettings: mySettings
    
    SettingsWithNoMenu:
        id: mySettings
<PlaySpot>:
    background_color: 0,0,0,0
    text: ''
    on_press: root.play()
    
<GameScreen>:
    board:board
    GridLayout:
        size_hint: 1,0.05
        pos_hint: {'center_x':0.5,'center_y':0.975}
        rows: 1
        canvas.before:
            Rectangle:
                pos: self.pos
                size: self.size
                source: 'assets/ribbon.png'
        MyLabel:
            text: 'Current Player: {}'.format(root.manager.symbol)
            size_hint: 0.7,1
            color: 0,10/255,20/255,1
        MyButton:
            text: 'Restart'
            size_hint: 0.3,0.5
            pos_hint:{'left':1,'center_y':0.5}
            background_normal: 'assets/button.png'
            on_press: root.reset()
    GridLayout:
        id:board
        rows:3
        cols:3
        size_hint: 1,0.95
        pos_hint: {'center_x':0.5,'center_y':0.475}
        canvas.before:
            Rectangle:
                pos: self.pos
                size: self.size
                source: 'assets/ttt.jpg'
        canvas:
            Color:
                rgb:1,1,1,1
            Line:
                points: 0,self.height/3,self.width,self.height/3
               
            Line:
                points: 0,self.height*2/3,self.width,self.height*2/3
                
            Line:
                points: self.width/3,0,self.width/3,self.height
                
            Line:
                points: self.width*2/3,0,self.width*2/3,self.height
            
<FinishPopup>:
    lbl:lbl
    on_touch_down: self.dismiss()
	size_hint: 0.75,0.75
	on_dismiss: app.root.tttm.current_screen.reset()
    auto_dismiss: False
    Image:
        allow_stretch: True
        keep_ratio: False
        source: 'assets/fireworks.zip'
        anim_delay: 1/20
    FloatLayout:
        MyLabel:
            id:lbl
            pos_hint: {'center_x':0.5,'center_y':0.5}
            font_size: 50
            background_color: 0,0,0,0
'''
class TTTController(r.MyScreen):
    #Cleans before leaving app
    def cleanUp(self):
        self.children[0].music.stop()
    #Starts stuff before entering app
    def introSetup(self):
        self.children[0].music.play()

class TTTManager(ScreenManager):
    turn = NumericProperty(0)
    symbol = StringProperty()
    color = ListProperty()
    
    def __init__(self,*args,**kwargs):
        super(TTTManager,self).__init__(*args,**kwargs)
        Clock.schedule_once(lambda dt: self.setup(),0)
        
    def setup(self):
        #Background Music
        self.music = SoundLoader.load('assets/music.wav')
        self.music.loop = True
        self.music.volume = App.get_running_app().root.master_volume
        App.get_running_app().root.bind(master_volume=self.music.setter('volume'))
        
        #Save the win popup
        self._popups = Factory.FinishPopup()
        
        #Various inits for key variables
        self.frozen = False
        self.ai = ''
        self.player = {}
    
    #Update symbol/color of current player every turn
    def on_turn(self,instance,value):
        self.symbol = self.players[value%len(self.players)][0]
        self.color = self.players[value%len(self.players)][1]
class MenuScreen(r.MyScreen):
    pass
    
class GameScreen(r.MyScreen):
    board = ObjectProperty()
    
    def __init__(self,*args,**kwargs):
        super(GameScreen,self).__init__(*args,**kwargs)
        Clock.schedule_once(lambda dt: self.setup(),0)
        
    def setup(self):
        #Creates board
        for i in range(9):
            self.board.add_widget(PlaySpot())
            
        #Writing Sounds
        self.writing_sound = SoundLoader.load('assets/write.wav')
        self.writing_sound.volume = App.get_running_app().root.master_volume
        App.get_running_app().root.bind(master_volume=self.writing_sound.setter('volume'))
        
        #Winning Sounds
        self.wow_sound = SoundLoader.load('assets/wow.wav')
        self.wow_sound.volume = App.get_running_app().root.master_volume
        App.get_running_app().root.bind(master_volume=self.wow_sound.setter('volume'))
    
    #Resets board on enter
    def on_enter(self):
        self.reset()
    
    #Resets board
    def reset(self):
        for i in self.board.children:
            i.text = ''
        if self.manager.ai != 'None' and ConfigParser.get_configparser('tttconfig').get('general','ai_turn') == 'First':
            self.manager.turn = -1
            self.manager.frozen = True
            Clock.schedule_once(lambda dt:self.board.children[0]._aiMove(self.manager),0.5)
        else: 
            self.manager.turn = 0
            self.manager.frozen = False
#TicTacToe play locations
class PlaySpot(r.MyButton):  
    def play(self):
        tttm = App.get_running_app().root.tttm
        if self.text == '' and not tttm.frozen:
            #Plays on the location
            self.text = tttm.symbol
            self.color = tttm.color
            #Checks for a win or tie, otherwise switches turn
            check = self._checkWin()
            if check:
                if check == 'tie':
                    tttm._popups.lbl.text = 'TIE!!'
                    tttm._popups.open() 
                else:
                    highlights = [Animation(background_color = [57/255,1,20/255,1])+\
                                  Animation(background_color = [0,0,0,0]) for i in range(3)]
                    for indx,adjacent in enumerate(check):
                        highlights[indx].start(adjacent)
                    tttm._popups.lbl.text = '{} WON!!'.format(tttm.symbol)
                    Clock.schedule_once(lambda dt: tttm._popups.open(),2)
                    tttm.frozen = True
            else:
                tttm.current_screen.writing_sound.play()
                tttm.turn += 1 
                if tttm.ai != 'None' and (tttm.turn+1)%2 == 0:
                    tttm.frozen = True
                    Clock.schedule_once(lambda dt: self._aiMove(tttm),0.5)
    def _aiMove(self,tttm):
        board = list(reversed(self.parent.children))
        best = {'score': -1,'indx': -1}
        
        #AI will make terrible mistakes
        if tttm.ai == 'Easy':
            choice = 700
        #AI will make non-optimal plays
        if tttm.ai == 'Medium':
            choice = 70
        #AI will never make a mistake
        if tttm.ai == 'Hard':
            choice = 0
        #Rates each position and plays in highest rated position
        for indx,spot in enumerate(board):
            if spot.text == '':
                indx_score = self._calcAiScore(indx,board,tttm.players) + \
                            random.randint(0,choice)
                if indx_score > best['score']:
                    best = {'score': indx_score,'indx': indx}
                #Gives variety to playstyle
                elif indx_score == best['score'] and random.randint(0,1):
                    best = {'score': indx_score,'indx': indx}
        tttm.frozen = False
        board[best['indx']].play()
        
    def _calcAiScore(self,indx,board,players):
        adjacents = self._get_adjacents(indx,board)
        score = 0
        setups = 0
        counter_setups = 0
        opponent_close = 0
        for adjacent in adjacents:
            adjacent_text = [i.text for i in adjacent]
            #Empty row/col/diag, AI picks mid first and then corners
            if len(set(adjacent_text)) == 1:
                score+=1
            #One player has played here
            elif len(set(adjacent_text)) == 2:
                #Opponent played here
                if players[0][0] in adjacent_text:
                    #Opponent played here once
                    if adjacent_text.count(players[0][0]) == 1:
                        score+=0.1
                        counter_setups += 1
                        if adjacent_text == ['',players[0][0],'']:
                            opponent_close+=1
                    #Opponent played here twice
                    else:
                        score+=100
                #You played here with no opponent
                else:
                    #Youve played here once
                    if adjacent_text.count(players[1][0]) == 1:
                        setups += 1
                    #Youve played here twice
                    else:
                        score+=200
            #Both people played here
            elif len(set(adjacent_text)) == 3:
                pass
        #Capitalizes on winner setups
        if setups >= 2:
            score+=10
        #Addresses two specific scenarios
        if counter_setups >= 2 and setups == 1:
            #If you control mid
            if board[4].text == players[1][0]:
                #If opponent has played close (example: around a corner)
                if opponent_close == 2:
                    score+=10
                else:
                    score-=10
            #If opponent Controls mid
            else:
                score+=10
        return score
    def _checkWin(self):
        board = list(reversed(self.parent.children))
        indx = board.index(self)
        adjacents = self._get_adjacents(indx,board)
        for adjacent in adjacents:
            if len(set([i.text for i in adjacent])) == 1:
                return adjacent
        if len([i for i in board if i.text != '']) == 9:
            return 'tie'
        return None
    
    def _get_adjacents(self,indx,board):
        row = int(indx/3)
        col = indx%3
        rowEntries = [spot for spot in board[row*3:row*3+2+1]]
        colEntries = [spot for spot in board[col:col+6+1:3]]
        diag1 = diag2 = []
        if indx in [0,4,8]: 
            diag1 = [spot for spot in board[0:9:4]]
        if indx in [2,4,6]: 
            diag2 = [spot for spot in board[2:7:2]]
        return (rowEntries,colEntries,diag1,diag2)
            
class FinishPopup(ModalView):
    lbl = ObjectProperty()
    lbl_animation = Animation(color=[i/255 for i in wc.name_to_rgb('green')] + [1.0])+\
                    Animation(color=[i/255 for i in wc.name_to_rgb('blue')] + [1.0]) +\
                    Animation(color=[i/255 for i in wc.name_to_rgb('red')] + [1.0])
    lbl_animation.repeat = True

    def on_open(self):
        App.get_running_app().root.tttm.current_screen.wow_sound.play()
        self.lbl_animation.start(self.lbl)
class SettingsScreen(r.MyScreen):
    mySettings = ObjectProperty()
    config = ConfigParser('tttconfig')
    
    def __init__(self,*args,**kwargs):
        super(SettingsScreen,self).__init__(*args,**kwargs)
        Clock.schedule_once(lambda dt: self.setup(),0)
    
    #post init setup
    def setup(self):
        self.config.setdefaults('general',{'ai': 'None',
                                           'ai_turn':'Second',
                                           'p1_color':'Red',
                                           'p2_color':'Blue',
                                           'p1_marker':'X',
                                           'p2_marker':'O'})
        self.config.add_callback(self.update)
        self.mySettings.add_json_panel('Settings',self.config,data = settings_json)
        self.update()
        
    #updates values when settings are changed
    def update(self,*args):
        self.manager.ai = self.config.get('general','ai')
        p1_marker = self.config.get('general','p1_marker')
        p2_marker = self.config.get('general','p2_marker')
        p1_color = [i/255 for i in wc.name_to_rgb(self.config.get('general','p1_color'))] + [1]
        p2_color = [i/255 for i in wc.name_to_rgb(self.config.get('general','p2_color'))] + [1]
        self.manager.players = {0:(p1_marker,p1_color),1:(p2_marker,p2_color)}
        self.manager.symbol = p1_marker
        self.manager.color = p1_color


