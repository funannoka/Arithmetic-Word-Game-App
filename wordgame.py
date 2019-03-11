#!/usr/bin/env python3

#import kivy
import random
import cmd
import sys
import time
import math
import os
from kivy.app import App
from kivy.base import runTouchApp
#kivy.require("1.8.0")
from kivy.properties import StringProperty, AliasProperty, BooleanProperty,ListProperty
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.widget import Widget
from kivy.graphics import Line
from kivy.uix.textinput import TextInput
from kivy.uix.behaviors.button import ButtonBehavior
from kivy.uix.popup import Popup
from kivy.uix.scrollview import ScrollView
#from kivy.logger import Logger
from kivy.uix.screenmanager import ScreenManager, Screen, FadeTransition
from kivy.lang import Builder

alphaDict = {
  "A":0,"a":0,
  "B":1,"b":1,
  "C":2,"c":2,
  "D":3,"d":3,
  "E":4,"e":4,
  "F":5,"f":5,
  "G":6,"g":6,
  "H":7,"h":7,
  "I":8,"i":8,
  "J":9,"j":9,
  "K":10,"k":10,
  "L":11,"l":11,
  "M":12,"m":12,
  "N":13,"n":13,
  "O":14,"o":14,
  "P":15,"p":15,
  "Q":16,"q":16,
  "R":17,"r":17,
  "S":18,"s":18,
  "T":19,"t":19,
  "U":20,"u":20,
  "V":21,"v":21,
  "W":22,"w":22,
  "X":23,"x":23,
  "Y":24,"y":24,
  "Z":25,"z":25,
}

alphaTuple = ("a","b","c","d","e","f","g","h","i","j","k",
              "l","m","n","o","p","q","r","s","t","u","v",
              "w","x","y","z")


class StartScreen(Screen):
    pass

class SelLevelScreen(Screen):
    pass

class SelGridScreen(Screen):
    pass

class SelGrid9Screen(Screen):
    pass

class SelGrid16Screen(Screen):
    pass

class WorkingScreen(Screen):
    # def __init__(self, **kwargs):
    #     super(WorkingScreen,self).__init__(**kwargs)

    pass

class DoneScreen(Screen):
    pass

class ScreenManagement(ScreenManager):
    pass

# class TotalPointsLabel(Label):
#     def __init__(self, **kwargs):
#         super(TotalPointsLabel,self).__init__(**kwargs)
#         #self.totalPoints=0
#         self.offset=100




class GameApp(App):
    title = "Arithmetic Word Game App"
    icon = 'images/one2oneMap.png'
    normThemeButton = "button"
    singleWordFileName = "words.txt"
    imageThemeFile = "ImageTheme.txt"
    workScreenName = "work"
    doneScreenName = "done"
    correctTag =  "Correct"
    incorrectTag =  "Incorrect"
    corrAnsTag = "Correct Answer: "
    ansTag = "Answer: "
    tblRow1 = ""
    tblrow2 = ""
    timeExceedTag = "You exceeded the time Limit!\n"
    invalidEntryTag ="Invalid entry."
    enterAlphaTag ="Enter a string of alphabets."
    enterIntTag = "Enter an integer."
    drvdSumTag = "Derived Sums:   "
    drvdWrdTag = "Derived Words: "
    jckptHeadTag = "Congratulations you hit a jackpot!"
    jckptDefTag = "Extra Points Gained = 50 points!"
    questionkvString = StringProperty()
    errMsg = StringProperty()
    errDef = StringProperty()
    screenName = StringProperty()
    selGridScreen = StringProperty()
    pointLabelTxt = StringProperty()
    sumTxt =StringProperty()
    wrdTxt =StringProperty()

    fnGridImage0 = StringProperty()
    fnGridImage1 = StringProperty()
    fnGridImage2 = StringProperty()
    fnGridImage3 = StringProperty()
    fnGridImage4 = StringProperty()
    fnGridImage5 = StringProperty()
    fnGridImage6 = StringProperty()
    fnGridImage7 = StringProperty()
    fnGridImage8 = StringProperty()
    fnGridImage9 = StringProperty()
    fnGridImage10 = StringProperty()
    fnGridImage11 = StringProperty()
    fnGridImage12 = StringProperty()
    fnGridImage13 = StringProperty()
    fnGridImage14 = StringProperty()
    fnGridImage15 = StringProperty()
   
    btnDisabled =  BooleanProperty()
    btn2Disabled = BooleanProperty()
    btn3Disabled = BooleanProperty()
    btn4Disabled = BooleanProperty()
    btn5Disabled = BooleanProperty()
    btn6Disabled = BooleanProperty()
    btn7Disabled = BooleanProperty()
    btn8Disabled = BooleanProperty()
    btn9Disabled = BooleanProperty()
    btn10Disabled = BooleanProperty()
    btn11Disabled = BooleanProperty()
    btn12Disabled = BooleanProperty()
    btn13Disabled = BooleanProperty()
    btn14Disabled = BooleanProperty()
    btn15Disabled = BooleanProperty()
    btn16Disabled = BooleanProperty()  

    bck_color  = ListProperty()
    bck2_color  = ListProperty()
    bck3_color  = ListProperty()
    bck4_color  = ListProperty()
    bck5_color  = ListProperty()
    bck6_color  = ListProperty()
    bck7_color  = ListProperty()
    bck8_color  = ListProperty()
    bck9_color  = ListProperty()
    bck10_color  = ListProperty()
    bck11_color  = ListProperty()
    bck12_color  = ListProperty()
    bck13_color  = ListProperty()
    bck14_color  = ListProperty()
    bck15_color  = ListProperty()
    bck16_color  = ListProperty()

    
    def __init__(self, **kwargs):
        super(GameApp,self).__init__(**kwargs)
        self.gridsize = 4
        self.currGrid=1
        self.questionsList = [[]]
        self.randLineList = []
        self.equivSumList = [[]]
        self.fnGridImageList = []
        self.questionkvString = ""
        self.sqPoints = 0 
        self.totalPoints=0
        self.qpos = 0
        self.errMsg = ""
        self.errDef = ""
        self.sumTxt =  self.drvdSumTag
        self.wrdTxt =  self.drvdWrdTag
        self.ansWord = False
        self.screenName = self.workScreenName
        self.selGridScreen =""
        self.pointLabelTxt = "Total points: 0"
        self.debug = 0
       # self.appwidth = 0  #debug
        #self.appheight=0   #debug
        #self.makeMapTable()
        self.set_all_btn_Disabled(False)
        self.set_all_bck_color([1,1,1,1])
        self.fnGridImageList = ['']*16
       

    def collectGridImages(self):
        #self.fnGridImageList = []
        randTheme = self.random_line(self.imageThemeFile)
        dirRandTheme = 'images/'+randTheme+'/'
        for g in range(self.gridsize):
            fnGridImage = self.random_line(dirRandTheme+randTheme+'.txt')
            self.fnGridImageList[g] = dirRandTheme+fnGridImage#.append(dirRandTheme+fnGridImage)
            if(self.debug):
                print(self.fnGridImageList[g])   #debug
        self.fnGridImage0 = self.fnGridImageList[0]
        self.fnGridImage1 = self.fnGridImageList[1]
        self.fnGridImage2 = self.fnGridImageList[2]
        self.fnGridImage3 = self.fnGridImageList[3]
        if (self.gridsize > 4):
            self.fnGridImage4 = self.fnGridImageList[4]
            self.fnGridImage5 = self.fnGridImageList[5]
            self.fnGridImage6 = self.fnGridImageList[6]
            self.fnGridImage7 = self.fnGridImageList[7]
            self.fnGridImage8 = self.fnGridImageList[8]
        if (self.gridsize > 9):
            self.fnGridImage9 = self.fnGridImageList[9]
            self.fnGridImage10 = self.fnGridImageList[10]
            self.fnGridImage11 = self.fnGridImageList[11]
            self.fnGridImage12 = self.fnGridImageList[12]
            self.fnGridImage13 = self.fnGridImageList[13]
            self.fnGridImage14 = self.fnGridImageList[14]
            self.fnGridImage15 = self.fnGridImageList[15]
    
    def collectQuestions(self):
        self.questionsList = [[]]
        self.randLineList = []
        self.equivSumList = [[]]
        #self.wrdTxt =  self.drvdWrdTag
        self.sqPoints = 0 
        self.qpos = 0
        self.cnt = 0
        if(self.debug):
            print(self.gridsize)  #debug
        self.jackSq = 0
        if self.gridsize > 4:
            self.jackSq = random.randint(1, self.gridsize)
        for g in range(self.gridsize):
            randLine = self.random_line(self.singleWordFileName)
            equivSum = self.mapLine(randLine)
            numSeq = self.pack_rand_vals_of_sum(equivSum)
            questions = self.get_all_quests_in_square(numSeq)
            if(self.debug):
                print(questions)  #debug
            self.questionsList.append(questions)
            self.randLineList.append(randLine)
            self.equivSumList.append(equivSum)
        self.questionsList=self.questionsList[1:]
        self.equivSumList=self.equivSumList[1:]
        self.numSquareDone =0
        #self.collectOneQuestion()

    def collectOneQuestion (self):
        if(self.debug):
            print(self.currGrid)    #debug
            print(self.qpos)       #debug
        if(self.questionsList == [[]]):
            self.questionkvString = "Init"
        else:
            self.questionkvString = self.questionsList[self.currGrid-1][self.qpos]
        if(self.debug):
            print(self.questionkvString)  #debug
        self.start = time.time()
        return self.questionkvString


    def collectAns(self):
        self.screenName = self.workScreenName
        self.timeElapsed = 0
        self.timeElapsed = time.time() - self.start
        #print("width = "+str(self.appwidth))   #debug
        #print("height = "+str(self.appheight))  #debug
        if (self.ansWord):
            try:
                ans = str(self.ans_ent)
            except(TypeError):
                self.errMsg= self.invalidEntryTag
                self.errDef= self.enterAlphaTag
            else:
                try:
                    ansSum = self.mapLine(ans)
                except(KeyError):
                    self.errMsg=self.invalidEntryTag
                    self.errDef= self.enterAlphaTag
                else:
                    if(self.debug):
                        print("YAY" + str(ans))   #debug
                    self.checkAns(ansSum)
        else:
            try:
                ans = int(self.ans_ent)
            except(ValueError):
                self.errMsg=self.invalidEntryTag
                self.errDef=self.enterIntTag
            else:
                if(self.debug):
                    print("YAY" + str(ans))   #debug
                self.checkAns(ans)

    def checkAns(self,ans):
        self.sqPoints = 0  #20*len(questions)
        maxTime = 30 #6seconds
        maxWTime = 35 #5
        if (self.ansWord)and(self.timeElapsed > maxWTime)and(ans != self.equivSumList[self.currGrid-1]):
            self.errMsg = self.incorrectTag
            self.errDef =self.timeExceedTag+self.ansTag+self.randLineList[self.currGrid-1]
            self.sqPoints -= 20 
        elif (self.ansWord)and(self.timeElapsed > maxWTime):
            self.errMsg = self.correctTag
            self.errDef = self.timeExceedTag+self.ansTag+self.randLineList[self.currGrid-1]
            self.sqPoints -= 5 
        elif (self.ansWord)and(ans != self.equivSumList[self.currGrid-1]):
            self.errMsg = self.incorrectTag
            self.errDef = self.corrAnsTag+self.randLineList[self.currGrid-1]
            self.sqPoints -= 15
        elif (self.ansWord):
            if(self.currGrid == self.jackSq):
                self.errMsg = self.jckptHeadTag
                self.errDef = self.jckptDefTag
                self.sqPoints += 60
            else:
                self.errMsg = self.correctTag
                self.errDef = self.ansTag+self.randLineList[self.currGrid-1]
                self.sqPoints += 10
        elif (self.timeElapsed > (maxTime))and(ans != self.equivSumList[self.currGrid-1][self.qpos]): 
            self.errMsg = self.correctTag 
            self.errDef = self.timeExceedTag+self.ansTag+str(self.equivSumList[self.currGrid-1][self.qpos]) 
        elif (self.timeElapsed > (maxTime)):
            self.errMsg = self.correctTag
            self.errDef = self.timeExceedTag+self.ansTag+str(self.equivSumList[self.currGrid-1][self.qpos])
            self.sqPoints += 10
        elif (ans != self.equivSumList[self.currGrid-1][self.qpos]):
            self.sqPoints += 5
            self.errMsg = self.incorrectTag
            self.errDef = self.corrAnsTag+str(self.equivSumList[self.currGrid-1][self.qpos])
        else:
            self.sqPoints += 20
            self.errMsg = self.correctTag
            self.errDef = self.ansTag+str(self.equivSumList[self.currGrid-1][self.qpos])
        self.qpos +=1
        self.reportSummary()
        return

    def reportSummary(self):
        self.totalPoints += self.sqPoints
        self.pointLabelTxt = "Total points: "+str(self.totalPoints)        
        if (self.ansWord == True):
            self.numSquareDone +=1
            self.endSquare()
        else:
            self.screenName = self.workScreenName
            self.sumTxt +=  "  "+str(self.equivSumList[self.currGrid-1][self.qpos-1])
            if (self.qpos not in range(len(self.questionsList[self.currGrid-1]))):
                self.askWord()
            else:
                self.collectOneQuestion()

    def askWord(self):
        self.ansWord = True
        self.questionkvString = "Enter the word that matches the sums below:"
        self.start = time.time()
  
    def endSquare(self):
        self.ansWord = False
        self.cnt +=1
        if (self.cnt > 5):
            self.wrdTxt += "\n                            "
            self.cnt = 1
        self.wrdTxt +=  "  "+self.randLineList[self.currGrid-1]
        self.sumTxt = self.drvdSumTag
        if (self.numSquareDone == self.gridsize):
            self.endGame()
        else:
            self.screenName = self.selGridScreen 
            self.qpos =0
            self.sqPoints = 0

    def endGame(self):
        self.screenName = self.doneScreenName 
        self.questionkvString = """You're All Done!\nTotal Points Earned is """ +str(self.totalPoints)+"."

    def set_all_btn_Disabled(self,stvalue):
        self.btnDisabled = stvalue
        self.btn2Disabled = stvalue
        self.btn3Disabled = stvalue
        self.btn4Disabled = stvalue
        self.btn5Disabled = stvalue
        self.btn6Disabled = stvalue
        self.btn7Disabled = stvalue
        self.btn8Disabled = stvalue
        self.btn9Disabled = stvalue
        self.btn10Disabled = stvalue
        self.btn11Disabled = stvalue
        self.btn12Disabled = stvalue
        self.btn13Disabled = stvalue
        self.btn14Disabled = stvalue
        self.btn15Disabled = stvalue
        self.btn16Disabled = stvalue
        #print(self.btnDisabled)
        
    def set_all_bck_color(self,val):
        self.bck_color  = val
        self.bck2_color  = val
        self.bck3_color  = val
        self.bck4_color  = val
        self.bck5_color  = val
        self.bck6_color  = val
        self.bck7_color  = val
        self.bck8_color  = val
        self.bck9_color  = val
        self.bck10_color  = val
        self.bck11_color  = val
        self.bck12_color  = val
        self.bck13_color  = val
        self.bck14_color  = val
        self.bck15_color  = val
        self.bck16_color  = val
        


    def restart(self):
        self.questionsList = [[]]
        self.randLineList = []
        self.equivSumList = [[]]
        self.totalPoints=0
        self.sqPoints = 0 
        self.qpos = 0
        self.questionkvString = "Solve: "
        self.wrdTxt =  self.drvdWrdTag
        self.sumTxt = self.drvdSumTag
        self.pointLabelTxt = "Total Points: 0"

    def makeMapTable(self):
        for i in range (13):
            self.tblRow1 += alphaTuple[i] + "   "
        self.tblRow1 += "\n"
        for i in range (13):
             self.tblRow1 += str(i)+ "   "
        self.tblRow1 += "\n"
        for i in range (13,26):
            self.tblRow1 += alphaTuple[i] + "    "
        self.tblRow1 += "\n"
        for i in range (13,26):
             self.tblRow1 += str(i)+ "   "
        
    def random_line(self,fn):
        fp = open(fn).read().splitlines()
        return random.choice(fp)

    def mapLine(self,oneLine):
        #fp = open("words.txt","r")
        sum = []
        for a in oneLine:
            sum.append(alphaDict[a])
        return sum

    def random_ints_with_sum(self,n):
        cnt =0
        while n > 0:
            r = random.randint(1, n)
            yield r
            n -= r
            cnt +=1
        if cnt < 2:
            r = 0
            yield r
        if cnt < 1:
            r = 0
            yield r

    def pack_rand_vals_of_sum(self,sumList):
        val = [[]]
        for i in range(len(sumList)):
            val.append(list(self.random_ints_with_sum(sumList[i])))
        val = val[1:]
        return val

    def get_all_quests_in_square(self,nums):
        numStrList = [""]
        for i in nums:
            numStr = ""
            numStr = "Solve: " + str(i[0])
            i=i[1:]
            for j in i:
                numStr +=(" + "+str(j))
            numStrList.append(numStr)
        numStrList = numStrList[1:]
        return numStrList

    
    def build(self):
        presentation = Builder.load_file("wordGame.kv")

        return presentation





if __name__ == "__main__":
    GameApp().run()
