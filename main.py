#-*- coding:utf-8 -*- 

import sys
import copy

from random import randint
from PyQt4 import QtGui,QtCore
from PyQt4.QtCore import Qt

class CWindow(QtGui.QWidget):
	def __init__(self):
		super(CWindow,self).__init__()
		self.InitUI()
		
	def InitUI(self):
		self.setFixedSize(400,300)
		self.setWindowTitle("2048")
		self.setWindowIcon(QtGui.QIcon("res/2048.jpg"))
		self.setFocusPolicy(True)
		self.InitStartBtn()
		self.InitGameBox()
		
	def InitStartBtn(self):
		self.m_BtnStart=QtGui.QPushButton(QtGui.QIcon("res/2048.jpg"),"start",self)
		self.m_BtnStart.setGeometry(300,20,60,30)
		self.connect(self.m_BtnStart,QtCore.SIGNAL("clicked()"),OnClickStart)
		
	def InitGameBox(self):
		x,y,iSize=60,40,50
		self.m_Grid=[[QtGui.QPushButton(self) for i in range(4)] for j in range(4)]
		for i in range(4):
			for j in range(4):
				btn=self.m_Grid[i][j]
				btn.setGeometry(x+j*iSize,y+i*iSize,iSize,iSize)
				btn.setEnabled(False)
				btn.setFont(QtGui.QFont("Times",15))
				#btn.setText(str(i*4+j))
				#btn.setText(str(2048))
	
	def keyPressEvent(self,event):
		KeyPressEvent(event)
	
	def ShowNumbers(self,lstNumber):
		for i in range(4):
			for j in range(4):
				btn=self.m_Grid[i][j]
				if lstNumber[i][j]==0:
					sText=""
				else:
					sText=str(lstNumber[i][j])
				btn.setText(sText)
	
#----------------------------------------------------------
class CGame(object):
	def __init__(self):
		self.m_State=0
		self.m_Win=0
		self.m_Grid=[[0 for i in range(4)] for j in range(4)]
	
	def Start(self):
		self.m_State=1
		self.m_Win=0
		self.m_Grid=[[0 for i in range(4)] for j in range(4)]
		
		for i in (0,1):
			x,y=self.RandomEmptyPos()
			self.m_Grid[x][y]=2
	
	def Move(self,iDir):
		for i in range(4):
			tmpList=[]
			if iDir in (1,2):
				for j in range(4):
					iValue=self.m_Grid[j][i]
					if iValue:
						tmpList.append(iValue)
			else:
				for j in range(4):
					iValue=self.m_Grid[i][j]
					if iValue:
						tmpList.append(iValue)
						 
			if iDir in (2,4):
				tmpList.reverse()
			
			newList=[]
			for j in range(len(tmpList)-1):
				if tmpList[j]==tmpList[j+1]:
					tmpList[j]=tmpList[j]+tmpList[j+1]
					tmpList[j+1]=0
			
			for v in tmpList:
				if v:
					newList.append(v)
			
			newList.extend([0 for j in range(4-len(newList))])
			if iDir in (2,4):
				newList.reverse()
			
			if iDir in (1,2):
				for j in range(4):
					self.m_Grid[j][i]=newList[j]
			else:
				for j in range(4):
					self.m_Grid[i][j]=newList[j]
			
		
	def CheckEnd(self):
		iHasSame=0
		iEmpty=0
		for i in range(4):
			for j in range(4):
				iValue=self.m_Grid[i][j]
				if iValue==2048:
					self.m_Win=1
					self.m_State=2
					return
				if iValue==0:
					iEmpty=1
				if iHasSame==0:
					for dx,dy in [(0,1),(1,0)]:
						x=i+dx
						y=j+dy
						
						if 0<=x<4 and 0<=y<4 and self.m_Grid[x][y]==iValue:
							iHasSame=1
							break
		
		if not iEmpty and not iHasSame:
			self.m_Win=0
			self.m_State=2
			
		
	def IsStart(self):
		return self.m_State==1
	
	def IsEnd(self):
		return self.m_State==2
	
	def IsWin(self):
		return self.m_Win
	
	def Numbers(self):
		return self.m_Grid
		
	def RandomEmptyPos(self):
		x,y=-1,-1
		lstPos=[]
		for i in range(4):
			for j in range(4):
				if self.m_Grid[i][j]==0:
					lstPos.append((i,j))
		
		if lstPos:
			x,y=lstPos[randint(0,len(lstPos)-1)]
		return x,y
		
	

#----------------------------------------------------------
global g_window,g_game
key_table={
	Qt.Key_Up:1,
	Qt.Key_Down:2,
	Qt.Key_Left:3,
	Qt.Key_Right:4,
}

def OnClickStart():
	global g_game,g_window
	if g_game.IsStart():
		return
	g_game.Start()
	lstNumber=g_game.Numbers()
	g_window.ShowNumbers(lstNumber)



def KeyPressEvent(event):
	global g_game,g_window
	if not g_game.IsStart():
		return
	iKey=event.key()
	if not iKey in key_table:
		return
	iDir=key_table[iKey]
	old_table=copy.deepcopy(g_game.Numbers())
	g_game.Move(iDir)
	g_game.CheckEnd()
	new_table=g_game.Numbers()
	if not g_game.IsEnd() and not CheckSameTable(old_table,new_table):
		x,y=g_game.RandomEmptyPos()
		if x!=-1 and y!=-1:
			g_game.m_Grid[x][y]=2
	
	lstNumber=g_game.Numbers()
	g_window.ShowNumbers(lstNumber)
	
	if g_game.IsEnd():
		if g_game.IsWin():
			print "!!!!!!!! You Win"
		else:
			print "!!!!!!!! You Lose"
	
def CheckSameTable(tb1,tb2):
	for i in range(len(tb1)):
		for j in range(len(tb1[i])):
			if tb1[i][j]!=tb2[i][j]:
				return False
	return True
	
def Main():
	global g_window,g_game
	app=QtGui.QApplication(sys.argv)
	g_game=CGame()
	g_window=CWindow()
	g_window.show()
	sys.exit(app.exec_())
	
if __name__=="__main__":
	Main()