# -*- coding: utf-8 -*-
"""
Created on Wed Aug 29 12:10:28 2018

@author: Justin
"""

import json

settings_json = json.dumps([
        {'type': 'options',
         'title':'AI',
         'section': 'general',
         'key':'ai',
         'options': ['None','Easy','Medium','Hard']},
         {'type': 'options',
         'title':'AI Turn Start',
         'desc': 'If AI Enabled',
         'section': 'general',
         'key':'ai_turn',
         'options': ['First','Second']},
         {'type': 'title',
          'title':'Player 1 (Human Player If AI Enabled)'},
         {'type': 'options',
          'title': 'Color',
          'desc': '',
          'section': 'general',
          'key': 'p1_color',
          'options': ['Blue','Red','Green','Purple','Yellow','Black','Pink']},
         {'type':'string',
            'title':'Marker',
            'desc':'',
            'section':'general',
            'key':'p1_marker'},
         {'type': 'title',
          'title':'Player 2 (AI Player If AI Enabled)'},
          {'type': 'options',
           'title':'Color',
           'desc': '',
           'section':'general',
           'key':'p2_color',
           'options':['Blue','Red','Green','Purple','Yellow','Black','Pink']},
           {'type':'string',
            'title':'Marker',
            'desc':'',
            'section':'general',
            'key':'p2_marker'}])
