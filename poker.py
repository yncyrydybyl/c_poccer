#!/usr/bin/python
# -*- coding: utf-8 -*-

# configure the game
# draw the basic table
# consist of playerareas containing chipfield / name / playerscards 

# collect players
# start game

import os, sys
from libavg import avg
from libavg import avg, button, Point2D, AVGApp,  anim
from libavg.AVGAppUtil import getMediaDir
from pokerengine.pokergame import PokerGameServer
g_player = avg.Player.get()              
mn = 100.0

class Game(AVGApp):
    multitouch = False
    poker_server = PokerGameServer("poker.%s.xml", ['conf', '../conf', '/etc/poker-engine']) 
    

    def init(self):
        parentnode = self._parentNode
        bgNode = g_player.createNode('image', {'href': 'media/pokertisch_bg.jpg','width':parentnode.width,'height':parentnode.height})
        parentnode.appendChild(bgNode)
        self.table = Table()
        self.startPokerMatch()
    def askForPlayerNumber(self):
        return 5

    def startPokerMatch(self):
       self.poker_server.verbose = 1 
       self.poker_server.setVariant("holdem") 
       self.poker_server.setBettingStructure("10-15-pot-limit") 
       # 
       # The serial numbers of the five players 
       # 
        
       for serial in xrange(1,self.askForPlayerNumber()+1):
          p = Player(self,serial,self.table.getFreeSeat())
          self.poker_server.addPlayer(p.id) 
          self.poker_server.payBuyIn(p.id, 1500*100) 
          self.poker_server.sit(p.id) 
          self.poker_server.autoBlindAnte(serial) 

class Player():
    def __init__(self,game,id,position):
        self.id = id
        print "player %s added" % id
        self.game = game
        self.playfield = self.drawPlayerField(position[0],position[1])
        self.drawChipCount("100000")

    def drawChipCount(self,chipcount):
        numericchipcount = g_player.createNode('words', {'text':chipcount})
        self.playfield.appendChild(numericchipcount)

    def drawPlayerField(self,x,y):
        pf = g_player.createNode('div' ,{'x': x, 'y':y})
        self.game._parentNode.appendChild(pf)
        return pf

class Table():
    def __init__(self):
        self.playerpositions = [[10,10],[10,100],[10,200],[10,300],[10,400]]
    def getFreeSeat(self):
        return self.playerpositions.pop()
                
      

if __name__=='__main__':
    Game.start(resolution=(1024,600))


