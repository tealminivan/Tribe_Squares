import sys
from PyQt5.QtGui import QPainter, QColor, QFont, QPen, QBrush
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QWidget, QApplication
import itertools
import simpleaudio as sa



# Be sure to put your (corrected) Score class in the same directory.
from Score import Score

#Variables
square_width=75
filler_width=55



class TribeSquares(QWidget):

  def __init__(self):
    super().__init__() 
    #Gameboard
    self.grid=[[i]*8 for i in range(8)]
    self.setGeometry(400,400,650,800)
    self.setWindowTitle('Fire vs Water')
    #Variables
    self.player_turn=0
    self.inside=False
    self.player1_move=[]
    self.player2_move=[]
    self.refresh1=True
    self.refresh2=False
    self.gamefinish=False
    self.player1=Score("player1")
    self.player2=Score("player2")
    self.squarecountplayer1=0
    self.squarecountholdplayer1=0
    self.multiplierplayer1=1
    self.squarecountplayer2=0
    self.squarecountholdplayer2=0
    self.multiplierplayer2=1
    self.scoreplayer1=0
    self.scoreplayer2=0
    self.scorelistplayer1=[]
    self.scorelistplayer2=[]
    self.sound=True
    self.addscoreplayer1=False
    self.addscoreplayer2=False
    player1sound=sa.WaveObject.from_wave_file("player1sound.wav")
    playplayer1sound=player1sound.play()
    self.show()

  def paintEvent(self, event):
    #Draw grid
    x=25
    y=25
    qp = QPainter()
    qp.begin(self)
    blackPen=QPen(QBrush(Qt.black),2)
    qp.setPen(blackPen)
    for row in self.grid:
      for col in row:
        square=qp.drawRect(x,y,square_width,square_width)
        x=x+square_width
      y=y+square_width
      x=25
    #Draw player 1 square
    for o in self.player1_move:
      l=o.split("-")
      current_x=int(l[0])
      current_y=int(l[1])
      redRect=QPen(QBrush(Qt.red),3)
      qp.setPen(redRect)
      recx=25+current_x*square_width+10
      recy=25+current_y*square_width+10
      qp.fillRect(recx,recy,filler_width,filler_width,Qt.red)
    #Draw player 2 square
    for o in self.player2_move:
      l=o.split("-")
      current_x=int(l[0])
      current_y=int(l[1])
      blueRect=QPen(QBrush(Qt.blue),3)
      qp.setPen(blueRect)
      recx=25+current_x*square_width+10
      recy=25+current_y*square_width+10
      qp.fillRect(recx,recy,filler_width,filler_width,Qt.blue )
    
    #player 1 stuff
    if (len(self.player1_move)>=4):
      player1combination=list(itertools.combinations(self.player1_move,4)) 
      player1combination=set(player1combination)
      #Increment multiplier and add points 
      if (self.addscoreplayer1==True):
        for i in range(self.multiplierplayer1-1):
          self.player1.increment_multiplier()
        self.player1.add_points(self.scoreplayer1)
      #draw the line 
      for i in player1combination:
        index=1
        for m in i:
          a=m.split("-")
          if (index==1):
            x1=int(a[0])
            y1=int(a[1])
          if (index==2):
            x2=int(a[0])
            y2=int(a[1])
          if (index==3):
            x3=int(a[0])
            y3=int(a[1])
          if (index==4):
            x4=int(a[0])
            y4=int(a[1])
          index=index+1  
        if (self.__issquare(x1,y1,x2,y2,x3,y3,x4,y4)==True):
          minx=self.__minimum_x(x1,x2,x3,x4)
          maxx=self.__maximum_x(x1,x2,x3,x4)
          miny=self.__minimum_y(y1,y2,y3,y4)
          maxy=self.__maximum_y(y1,y2,y3,y4)
          if (self.__isrotatedsquare(i,str(maxx)+"-"+str(maxy))==True): 
            dist1_2=((x1-x2)**2+(y1-y2)**2)**1/2
            dist1_3=((x1-x3)**2+(y1-y3)**2)**1/2
            dist1_4=((x1-x4)**2+(y1-y4)**2)**1/2
            redPen = QPen(QBrush(Qt.red),3)
            qp.setPen(redPen)
            if (dist1_2 == dist1_3):
              qp.drawLine(37.5+25+x1*75,37.5+25+y1*75,37.5+25+x2*75,37.5+25+y2*75)
              qp.drawLine(37.5+25+x1*75,37.5+25+y1*75,37.5+25+x3*75,37.5+25+y3*75)
              qp.drawLine(37.5+25+x2*75,37.5+25+y2*75,37.5+25+x4*75,37.5+25+y4*75)
              qp.drawLine(37.5+25+x3*75,37.5+25+y3*75,37.5+25+x4*75,37.5+25+y4*75)
            if (dist1_2 == dist1_4):
              qp.drawLine(37.5+25+x1*75,37.5+25+y1*75,37.5+25+x2*75,37.5+25+y2*75)
              qp.drawLine(37.5+25+x1*75,37.5+25+y1*75,37.5+25+x4*75,37.5+25+y4*75)
              qp.drawLine(37.5+25+x2*75,37.5+25+y2*75,37.5+25+x3*75,37.5+25+y3*75)
              qp.drawLine(37.5+25+x3*75,37.5+25+y3*75,37.5+25+x4*75,37.5+25+y4*75)
            if (dist1_3 == dist1_4):
              qp.drawLine(37.5+25+x1*75,37.5+25+y1*75,37.5+25+x3*75,37.5+25+y3*75)
              qp.drawLine(37.5+25+x1*75,37.5+25+y1*75,37.5+25+x4*75,37.5+25+y4*75)
              qp.drawLine(37.5+25+x2*75,37.5+25+y2*75,37.5+25+x3*75,37.5+25+y3*75)
              qp.drawLine(37.5+25+x2*75,37.5+25+y2*75,37.5+25+x4*75,37.5+25+y4*75)
          else:
            redPen = QPen(QBrush(Qt.red),3)
            qp.setPen(redPen)
            qp.drawRect(37.5+25+minx*75,37.5+25+miny*75,(maxx-minx)*75,(maxy-miny)*75)
            
            
    #player 2 stuff   
    if (len(self.player2_move)>=4):
      player2combination=list(itertools.combinations(self.player2_move,4))
      player2combination=set(player2combination)
      #Increment multiplier and add points
      if (self.addscoreplayer2==True):
        for i in range(self.multiplierplayer2-1):
          self.player2.increment_multiplier()
        self.player2.add_points(self.scoreplayer2)
      #draw the line 
      for i in player2combination:
        index=1
        for m in i:
          a=m.split("-")
          if (index==1):
            x1=int(a[0])
            y1=int(a[1])
          if (index==2):
            x2=int(a[0])
            y2=int(a[1])
          if (index==3):
            x3=int(a[0])
            y3=int(a[1])
          if (index==4):
            x4=int(a[0])
            y4=int(a[1])
          index=index+1
        if (self.__issquare(x1,y1,x2,y2,x3,y3,x4,y4)==True):
          minx=self.__minimum_x(x1,x2,x3,x4)
          maxx=self.__maximum_x(x1,x2,x3,x4)
          miny=self.__minimum_y(y1,y2,y3,y4)
          maxy=self.__maximum_y(y1,y2,y3,y4)
          if (self.__isrotatedsquare(i,str(maxx)+"-"+str(maxy))==True):
            dist1_2=((x1-x2)**2+(y1-y2)**2)**1/2
            dist1_3=((x1-x3)**2+(y1-y3)**2)**1/2
            dist1_4=((x1-x4)**2+(y1-y4)**2)**1/2
            bluePen = QPen(QBrush(Qt.blue),3)
            qp.setPen(bluePen)
            if (dist1_2 == dist1_3):
              qp.drawLine(37.5+25+x1*75,37.5+25+y1*75,37.5+25+x2*75,37.5+25+y2*75)
              qp.drawLine(37.5+25+x1*75,37.5+25+y1*75,37.5+25+x3*75,37.5+25+y3*75)
              qp.drawLine(37.5+25+x2*75,37.5+25+y2*75,37.5+25+x4*75,37.5+25+y4*75)
              qp.drawLine(37.5+25+x3*75,37.5+25+y3*75,37.5+25+x4*75,37.5+25+y4*75)
            if (dist1_2 == dist1_4):
              qp.drawLine(37.5+25+x1*75,37.5+25+y1*75,37.5+25+x2*75,37.5+25+y2*75)
              qp.drawLine(37.5+25+x1*75,37.5+25+y1*75,37.5+25+x4*75,37.5+25+y4*75)
              qp.drawLine(37.5+25+x2*75,37.5+25+y2*75,37.5+25+x3*75,37.5+25+y3*75)
              qp.drawLine(37.5+25+x3*75,37.5+25+y3*75,37.5+25+x4*75,37.5+25+y4*75)
            if (dist1_3 == dist1_4):
              qp.drawLine(37.5+25+x1*75,37.5+25+y1*75,37.5+25+x3*75,37.5+25+y3*75)
              qp.drawLine(37.5+25+x1*75,37.5+25+y1*75,37.5+25+x4*75,37.5+25+y4*75)
              qp.drawLine(37.5+25+x2*75,37.5+25+y2*75,37.5+25+x3*75,37.5+25+y3*75)
              qp.drawLine(37.5+25+x2*75,37.5+25+y2*75,37.5+25+x4*75,37.5+25+y4*75)
          else:
            bluePen = QPen(QBrush(Qt.blue),3)
            qp.setPen(bluePen)
            qp.drawRect(37.5+25+minx*75,37.5+25+miny*75,(maxx-minx)*75,(maxy-miny)*75)
    
    #Check if the game ends
    if (len(self.player1_move)+len(self.player2_move)==64):
      self.gamefinish=True
        
    #Display player turn
    if (self.player_turn%2==0 and self.refresh1==True and self.gamefinish==False):
      textPen = QPen(QBrush(Qt.red),4)
      qp.setPen(textPen)
      qp.drawText(150, 665,"PLAYER 1 TURN")
      qp.fillRect(400, 640, 100,100,Qt.red)
    if (self.player_turn%2!=0 and self.refresh2==True and self.gamefinish==False):
      textPen = QPen(QBrush(Qt.blue),4)
      qp.setPen(textPen)
      qp.drawText(150, 715,"PLAYER 2 TURN")
      qp.fillRect(400, 640, 100, 100,Qt.blue) 
      
     
    #Display score and multiplier    
    
    textPen = QPen(QBrush(Qt.red),4)
    qp.setPen(textPen)
    qp.drawText(25, 665,str(self.player1.get_score()))
    qp.drawText(100, 665,"X "+str(self.player1.get_multiplier()))
    print("multiplier draw:"+str(self.player1.get_multiplier()))    
    textPen = QPen(QBrush(Qt.blue),4)
    qp.setPen(textPen)
    qp.drawText(25, 715,str(self.player2.get_score()))
    qp.drawText(100, 715,"X "+str(self.player2.get_multiplier()))
    qp.drawText(25, 715,str(self.player2.get_score()))   
    
    #Result screen
    if (self.gamefinish==True):
      if (self.player1.get_score()==self.player2.get_score()):
        textPen=QPen(QBrush(Qt.magenta),5)
        qp.setPen(textPen)
        qp.drawText(400, 685,"TIE GAME")
        #sound if tie
        if (self.sound==True):
          tiesound=sa.WaveObject.from_wave_file("tiesound.wav")
          playtiesound=tiesound.play()
          self.sound=False
      if (self.player1.get_score()>self.player2.get_score()):
        textPen=QPen(QBrush(Qt.red),5)
        qp.setPen(textPen)
        qp.drawText(400, 685,"PLAYER 1 WINS")
        #sound if win
        if (self.sound==True):
          winnersound=sa.WaveObject.from_wave_file("winnersound.wav")
          playwinnersound=winnersound.play()
          self.sound=False
      if (self.player2.get_score()>self.player1.get_score()):
        textPen=QPen(QBrush(Qt.blue),5)
        qp.setPen(textPen)
        qp.drawText(400, 685,"PLAYER 2 WINS") 
        #sound if win
        if (self.sound==True): 
          winnersound=sa.WaveObject.from_wave_file("winnersound.wav")
          playwinnersound=winnersound.play()
          self.sound=False

    qp.end()
  
  #useful functions
  def __issquare(self,x1,y1,x2,y2,x3,y3,x4,y4):
    centerx=(x1+x2+x3+x4)/4
    centery=(y1+y2+y3+y4)/4
    distance1=((centerx-x1)**2+(centery-y1)**2)**1/2 
    distance2=((centerx-x2)**2+(centery-y2)**2)**1/2 
    distance3=((centerx-x3)**2+(centery-y3)**2)**1/2 
    distance4=((centerx-x4)**2+(centery-y4)**2)**1/2 
    dist1_2=((x1-x2)**2+(y1-y2)**2)**1/2
    dist1_3=((x1-x3)**2+(y1-y3)**2)**1/2
    dist1_4=((x1-x4)**2+(y1-y4)**2)**1/2
    if (distance1==distance2 and distance1==distance3 and distance1==distance4):
      if (dist1_2==dist1_3 or dist1_2==dist1_4 or dist1_3==dist1_4):
        return True
      else:
        return False
    else:
      return False
  
  def __isrotatedsquare(self,list,point):
    hasrec=False
    for i in list:
      if (i==point):
        hasrec=True
    if (hasrec==False):
      return True
    else:
      return False
      
  def __minimum_x(self,x1,x2,x3,x4):
    minx=x1
    if (minx>x2):
      minx=x2
    if (minx>x3):
      minx=x3
    if (minx>x4):
      minx=x4
    return minx
    
  def __minimum_y(self,y1,y2,y3,y4):
    miny=y1    
    if (miny>y2):
      miny=y2
    if (miny>y3):
      miny=y3
    if (miny>y4):
      miny=y4
    return miny
  
  def __maximum_x(self,x1,x2,x3,x4):
    maxx=x1
    if (maxx<x2):
      maxx=x2
    if (maxx<x3):
      maxx=x3
    if (maxx<x4):
      maxx=x4
    return maxx
  
  def __maximum_y(self,y1,y2,y3,y4):
    maxy=y1
    if (maxy<y2):
      maxy=y2
    if (maxy<y3):
      maxy=y3
    if (maxy<y4):
      maxy=y4
    return maxy
    
  def __hasvalue(self,list,value):
    hasvalue=False
    for i in list:
      if (i==value):
        hasvalue=True
    return hasvalue
    
  def __getplayerscore(self,list):
    score=0
    for i in list:
      s=i.split("-")
      score=score+int(s[0])
    return score
        
  def mousePressEvent(self, event):
    #Check if click is outside the grid
    is_valid=True
    if ((event.x()-25)//square_width<0 or (event.x()-25)//square_width>7):
      is_valid=False
    if ((event.y()-25)//square_width<0 or (event.y()-25)//square_width>7):
      is_valid=False
    #append player 1 move and checks the player turn and calculates score and multiplier
    self.addscoreplayer1=False
    self.addscoreplayer2=False
    if (is_valid==True):
      has_value=False
      if (self.player_turn%2==0):
        player2occupy=False
        #checks if player 2 move is occupied in a square
        for o in self.player2_move:
           if (o==str((event.x()-25)//square_width) + '-' + str((event.y()-25)//square_width)):
              player2occupy=True
        if (player2occupy==False):
        #checks if player 1 move is occupied in a square
          for o in self.player1_move:
            if (o==str((event.x()-25)//square_width) + '-' + str((event.y()-25)//square_width)):
              has_value=True
          if (has_value==False):
            #announces the next player's turn after click
            if (self.player_turn<63):
              player2sound=sa.WaveObject.from_wave_file("player2sound.wav")
              playplayer2sound=player2sound.play()
            self.player1_move.append(str((event.x()-25)//square_width) + '-' + str((event.y()-25)//square_width))
            self.player_turn=self.player_turn+1
            self.refresh2=True
            self.refresh1=False
            if (len(self.player1_move)>=4):
              player1combination=list(itertools.combinations(self.player1_move,4)) 
              player1combination=set(player1combination)
              self.scoreplayer1=0
              for i in player1combination:
                index=1
                for m in i:
                  a=m.split("-")
                  if (index==1):
                    x1=int(a[0])
                    y1=int(a[1])
                  if (index==2):
                    x2=int(a[0])
                    y2=int(a[1])
                  if (index==3):
                    x3=int(a[0])
                    y3=int(a[1])
                  if (index==4):
                    x4=int(a[0])
                    y4=int(a[1])
                  index=index+1  
                if (self.__issquare(x1,y1,x2,y2,x3,y3,x4,y4)==True): 
                  self.squarecountplayer1=self.squarecountplayer1+1
                  minx=self.__minimum_x(x1,x2,x3,x4)
                  maxx=self.__maximum_x(x1,x2,x3,x4)
                  miny=self.__minimum_y(y1,y2,y3,y4)
                  maxy=self.__maximum_y(y1,y2,y3,y4)
                  if (self.__isrotatedsquare(i,str(maxx)+"-"+str(maxy))==True): 
                    dist1_2=((x1-x2)**2+(y1-y2)**2)**1/2
                    dist1_3=((x1-x3)**2+(y1-y3)**2)**1/2
                    dist1_4=((x1-x4)**2+(y1-y4)**2)**1/2
                    if (dist1_2 == dist1_3):
                      if (self.__hasvalue(self.scorelistplayer1,i)==False):
                        self.scoreplayer1=self.scoreplayer1+int((dist1_2+1)*(dist1_3+1))
                        self.scorelistplayer1.append(i)
                    if (dist1_2 == dist1_4):
                      if (self.__hasvalue(self.scorelistplayer1,i)==False):
                        self.scoreplayer1=self.scoreplayer1+int((dist1_2+1)*(dist1_4+1))
                        self.scorelistplayer1.append(i)
                    if (dist1_3 == dist1_4):
                      if (self.__hasvalue(self.scorelistplayer1,i)==False):
                        self.scoreplayer1=self.scoreplayer1+int((dist1_4+1)*(dist1_3+1))
                        self.scorelistplayer1.append(i)
                  else:
                    if (self.__hasvalue(self.scorelistplayer1,i)==False):
                      self.scoreplayer1=self.scoreplayer1+(maxx-minx+1)*(maxy-miny+1)
                      self.scorelistplayer1.append(i)
              if (self.scoreplayer1>0):
                self.addscoreplayer1=True
              if (self.squarecountplayer1 != self.squarecountholdplayer1):
                self.squarecountholdplayer1=self.squarecountplayer1
                if (self.squarecountplayer1 > 1):
                  self.multiplierplayer1=self.squarecountplayer1 
                self.squarecountplayer1=0
              else:
                self.multiplierplayer1=1
                self.squarecountplayer1=0
                self.squarecountholdplayer1=0  
                self.player1.subtract_points(0) 
            
      #append player 2 move and checks the player turn
      else:
        player1occupy=False
        #checks if player 1 move is occupied in a square
        for o in self.player1_move:
           if (o==str((event.x()-25)//square_width) + '-' + str((event.y()-25)//square_width)):
              player1occupy=True
        if (player1occupy==False):
          #checks if player 2 move is occupied in a square and calculates the points and multiplier 
          for o in self.player2_move:
            if (o==str((event.x()-25)//square_width) + '-' + str((event.y()-25)//square_width)):
              has_value=True
          if (has_value==False):
            #announces the next player's turn after the click
            if (self.player_turn<63):
              player1sound=sa.WaveObject.from_wave_file("player1sound.wav")
              playplayer1sound=player1sound.play()
            self.player2_move.append(str((event.x()-25)//square_width) + '-' + str((event.y()-25)//square_width))
            self.player_turn=self.player_turn+1
            self.refresh1=True
            self.refresh2=False
            if (len(self.player2_move)>=4):
              player2combination=list(itertools.combinations(self.player2_move,4)) 
              player2combination=set(player2combination)
              self.scoreplayer2=0
              for i in player2combination:
                index=1
                for m in i:
                  a=m.split("-")
                  if (index==1):
                    x1=int(a[0])
                    y1=int(a[1])
                  if (index==2):
                    x2=int(a[0])
                    y2=int(a[1])
                  if (index==3):
                    x3=int(a[0])
                    y3=int(a[1])
                  if (index==4):
                    x4=int(a[0])
                    y4=int(a[1])
                  index=index+1  
                if (self.__issquare(x1,y1,x2,y2,x3,y3,x4,y4)==True):  
                  self.squarecountplayer2=self.squarecountplayer2+1
                  minx=self.__minimum_x(x1,x2,x3,x4)
                  maxx=self.__maximum_x(x1,x2,x3,x4)
                  miny=self.__minimum_y(y1,y2,y3,y4)
                  maxy=self.__maximum_y(y1,y2,y3,y4)
                  if (self.__isrotatedsquare(i,str(maxx)+"-"+str(maxy))==True): 
                    dist1_2=((x1-x2)**2+(y1-y2)**2)**1/2
                    dist1_3=((x1-x3)**2+(y1-y3)**2)**1/2
                    dist1_4=((x1-x4)**2+(y1-y4)**2)**1/2
                    if (dist1_2 == dist1_3):
                      if (self.__hasvalue(self.scorelistplayer2,i)==False):
                        self.scoreplayer2=self.scoreplayer2+int((dist1_2+1)*(dist1_3+1))
                        self.scorelistplayer2.append(i)
                    if (dist1_2 == dist1_4):
                      if (self.__hasvalue(self.scorelistplayer2,i)==False):
                        self.scoreplayer2=self.scoreplayer2+int((dist1_2+1)*(dist1_4+1))
                        self.scorelistplayer2.append(i)
                    if (dist1_3 == dist1_4):
                      if (self.__hasvalue(self.scorelistplayer2,i)==False):
                        self.scoreplayer2=self.scoreplayer2+int((dist1_4+1)*(dist1_3+1))
                        self.scorelistplayer2.append(i)
                  else:
                    if (self.__hasvalue(self.scorelistplayer2,i)==False):
                      self.scoreplayer2=self.scoreplayer2+(maxx-minx+1)*(maxy-miny+1)
                      self.scorelistplayer2.append(i)
              if (self.scoreplayer2>0):
                self.addscoreplayer2=True
              if (self.squarecountplayer2 != self.squarecountholdplayer2):
                self.squarecountholdplayer2=self.squarecountplayer2
                if (self.squarecountplayer2 > 1):
                  self.multiplierplayer2=self.squarecountplayer2
                self.squarecountplayer2=0
              else:
                self.multiplierplayer2=1
                self.squarecountplayer2=0
                self.squarecountholdplayer2=0 
                self.player2.subtract_points(0)  
    self.update()

if __name__ == '__main__':
  app = QApplication(sys.argv)
  ex = TribeSquares()
  sys.exit(app.exec_())
  
