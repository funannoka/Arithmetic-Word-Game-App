#!/usr/bin/env python2
__version__ = "1.0"
__metaclass__ = type
import kivy
import random
import cmd
import sys
import time
import math
import signal , os
import threading
from kivy.app import App
from kivy.base import runTouchApp
from kivy.core.window import Window
kivy.require("1.10.1")
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
from kivy.logger import Logger
from kivy.uix.screenmanager import ScreenManager, Screen, FadeTransition
from kivy.lang import Builder
#import pyttsx3
from gtts import gTTS 
from pygame import mixer
#import pyglet


#Window.clearcolor = (0.5, 0.5, 0.5, 1)
#Window.size = (800, 600) 

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

#sm =  ScreenManager()

class ScreenManagement(ScreenManager):
    pass


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

class CntrlrCls():
    def __init__(self, **kwargs):
        super(CntrlrCls,self).__init__(**kwargs)
        self.popon = 0
        self.debug = 0
        self.screenName = ""

cntr = CntrlrCls()


class Ticker(threading.Thread):
  """
  use::

    t = Ticker(1.0) # make a ticker
    t.start() # start the ticker in a new thread
    try:
      while t.evt.wait(): # hang out til the time has elapsed
        t.evt.clear() # tell the ticker to loop again
        print time.time(), "FIRING!"
    except:
      t.stop() # tell the thread to stop
      t.join() # wait til the thread actually dies

  """

  # SIGALRM based timing proved to be unreliable on various python installs,
  #a simple thread that blocks on sleep and sets a threading.Event
  # when the timer expires, it does this forever.
  def __init__(self, interval):
    super(Ticker, self).__init__()
    self.interval = interval
    self.evt = threading.Event()
    self.evt.clear()
    self.should_run = threading.Event()
    self.should_run.set()

  def stop(self):
    """Stop the this thread. call :meth:`join` immediately
    afterwards
    """
    self.should_run.clear()

  def consume(self):
    was_set = self.evt.is_set()
    if was_set:
      self.evt.clear()
    return was_set

  def run(self):
    """internal main method of this thread. Block for :attr:`interval`
    seconds before setting :attr:`Ticker.evt`

    .. warning::
      Do not call this directly!  Instead call :meth:`start`.
    """
    while self.should_run.is_set():
      time.sleep(self.interval)
      self.evt.set()


#t = Ticker(0.5)

class MyPopup(Popup):
    def __init__(self, **kwargs):
        super(MyPopup,self).__init__(**kwargs)
        Window.bind(on_key_down=self._on_keyboard_down)
    
    def _on_keyboard_down(self, instance, keyboard, keycode, text, modifiers):
        if keycode == 40:  # 40 - Enter key pressed 
            if(cntr.debug):
                print("\n[POPUP] ENTER KEY DOWN")
            self.dismiss()
            #cntr.popon =0
    pass


class WorkingScreen(Screen):
    def __init__(self, **kwargs):
        super(WorkingScreen,self).__init__(**kwargs)
        Window.bind(on_key_down=self._on_keyboard_down)
        self.screenName = ""

    def _on_keyboard_down(self, instance, keyboard, keycode, text, modifiers):
        if keycode == 40 and cntr.popon ==0:  # 40 - Enter key pressed 
            if (cntr.screenName == "work") or (self.screenName == "work"):
                if(cntr.debug):
                    print("""[WORK SCREEN] Button = {txt}\n[WORK SCREEN] ENTER KEY DOWN""".format(txt=self.ids.entr.text))
                self.ids.entr.trigger_action(duration=0.2)
                cntr.popon = 1
                self.screenName = ""
           # MyPopup.dismiss

    pass

class WorkingScreen4(Screen):
    pass
class WorkingScreen9(Screen):
    pass
class WorkingScreen16(Screen):
    pass

class DoneScreen(Screen):
    pass

# class ScreenManager(ScreenManager):
#     pass
#tools_path = os.path.dirname(__file__)
#icons_path = os.path.join(tools_path, 'NanumSquareL.ttfs')

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
    timeExceedTag = "You exceeded the time limit!\n"
    invalidEntryTag ="Invalid entry."
    enterAlphaTag ="Enter a string of alphabets."
    enterIntTag = "Enter an integer."
    drvdSumTag = "Your Sums:  "
    drvdWrdTag = "Word Bank: "
    jckptHeadTag = "Congratulations you've hit a jackpot!"
    jckptDefTag = "Your Bonus Point is 50 !"
    strmksentence ='click to make four-word sentences'
    questionkvString = StringProperty()
    selSentenString = StringProperty()
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

    btn1Text = StringProperty()
    btn2Text = StringProperty()
    btn3Text = StringProperty()
    btn4Text = StringProperty()
    btn5Text = StringProperty()
    btn6Text = StringProperty()
    btn7Text = StringProperty()
    btn8Text = StringProperty()
    btn9Text = StringProperty()
    btn10Text = StringProperty()
    btn11Text = StringProperty()
    btn12Text = StringProperty()
    btn13Text = StringProperty()
    btn14Text = StringProperty()
    btn15Text = StringProperty()
    btn16Text = StringProperty()

    
    def __init__(self, **kwargs):
        super(GameApp,self).__init__(**kwargs)
        #Window.bind(on_key_down=self._on_keyboard_down)
        self.gridsize = 4
        self.currGrid=1
        self.questionsList = [[]]
        self.randLineList = []
        self.randLineList2 = []
        self.randLineListWspace =[]
        self.equivSumList = [[]]
        self.fnGridImageList = []
        self.fnGridImArr = []
        self.questionkvString = ""
        self.sqPoints = 0 
        self.totalPoints=0
        self.qpos = 0
        self.errMsg = ""
        self.errDef = ""
        self.numSentence=0
        self.reqNumSentence = 0
        self.sumTxt =  self.drvdSumTag
        self.wrdTxt =  self.drvdWrdTag
        self.ansWord = False
        self.screenName = ""#self.workScreenName
        cntr.screenName = self.screenName
        self.selGridScreen =""
        self.pointLabelTxt = "Total points: 0"
        self.sStruct = ("subject","verb","determ","noun")
        self.selSentenString = ""
        self.debug = cntr.debug
        self.endsq = 0
        self.set_all_btn_Disabled(False)
        self.set_all_bck_color([1,1,1,1])
        self.fnGridImageList = ['']*16
        self.wrdDict = dict(init="init")
        self.initAllBtnTxt()
        self.mkSenten = False
        self.foundSentences = []
        self.numTries = 0
        self.firstQuest =1
        self.mp3cnt =0
        #self.initTTSpyttsx()
        self.initgTTS()
        #self.del_all_mp3_files()
        self.tinterval = time.time()
       
    # def initTTSpyttsx(self):
    #     self.engine = pyttsx3.init()
    #     self.rate = self.engine.getProperty('rate')
    #     self.engine.setProperty('rate', self.rate-80)
       
       
    # def textToSpeech(self):
    #     self.engine.say(self.questionkvString)
    #     self.engine.runAndWait()

    def initgTTS (self):
        #mytext = 'Welcome'
        #pygame.init()
        mixer.init()
        self.language = 'en'
        #self.myobj = gTTS(text=mytext, lang=self.language, slow=False)  
        #self.myobj.save("gTTSspeech.mp3") 
        #os.system("gTTSspeech.mp3") 
    
    def textToSpeechgTTS(self):
        #self.initgTTS()
        if(self.questionkvString != ""):
            #if self.cnt !=0:
                #p = subprocess.Popen(['mixer.music', "gTTSspeech"+str(self.cnt-1)+".mp3"])
                #self.kill_by_process_name_shell("gTTSspeech"+str(self.cnt-1)+".mp3")
                #p.kill()
                #os.remove("gTTSspeech"+str(self.cnt-1)+".mp3")  #gTTSspeech.mp3
            self.myobj = gTTS(text=self.questionkvString, lang=self.language, slow=False)  
            self.myobj.save("gTTSspeech"+str(self.mp3cnt)+".mp3") 
            #os.system("gTTSspeech.mp3") #os.system("mpg321 gTTSspeech.mp3 -quiet")
            mixer.music.load("gTTSspeech"+str(self.mp3cnt)+".mp3")
            mixer.music.play()
            #speech = pyglet.resource.media("gTTSspeech"+str(self.mp3cnt)+".wav",streaming=False)
            #speech.play()
            #pyglet.app.run()
            self.mp3cnt +=1
            
    
    # def kill_by_process_name_shell(self):
	# 	#os.system("Taskkill /IM "+name+" /F")
    #     #mixer.quit()
    #     for i in range(self.mp3cnt-1):
    #         try:
    #             os.remove("gTTSspeech"+str(i)+".mp3")
    #         except:
    #             self.errMsg= "Delete Error"
    #             self.errDef= "Error while deleting file "+ "gTTSspeech"+str(i)+".mp3"
    #             if(self.debug):
    #                 print("Error while deleting file ", "gTTSspeech"+str(i)+".mp3")
    #         #os.remove("gTTSspeech"+str(i)+".mp3")
    #     self.mp3cnt = 0
    
    def del_all_mp3_files(self):
        for fname in os.listdir('.'):
            if fname.endswith('.mp3'):
                if(self.debug):
                    print(fname)
                try:
                    os.remove(fname)
                except:
                    self.errMsg= "Delete Error"
                    self.errDef= "Error while deleting file "
                    if(self.debug):
                        print("Error while deleting file ", fname)
                else:
                	Logger.info('File removed: '+fname)

    def collectGridImages(self):
        self.fnGridImageList = []
        self.fnGridImArr = []
        randTheme = self.random_line(self.imageThemeFile)
        dirRandTheme = 'images/'+randTheme+'/'
        #for g in range(self.gridsize):
        while (len(self.fnGridImageList) < self.gridsize):
            fnGridImage = self.random_line_no_rep(dirRandTheme+randTheme+'.txt',self.fnGridImArr)
            self.fnGridImArr.append(fnGridImage)
            self.fnGridImageList.append(dirRandTheme+fnGridImage) #[g] = dirRandTheme+fnGridImage
            if(self.debug):
                g = len(self.fnGridImageList) 
                print(self.fnGridImageList[g-1])   #debug  [g]
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
    
    def collectQuestionsPlus_deprc(self):
        self.questionsList = [[]]
        self.randLineListWspace = []
        self.randLineList = []
        self.equivSumList = [[]]
        self.randSentenceList = []
        self.wrdDict.clear()
        #self.sStruct = ("subject","verb","determ","noun")
        #self.wrdTxt =  self.drvdWrdTag
        self.sqPoints = 0 
        self.qpos = 0
        self.cnt = 0
        if(self.debug):
            print(self.gridsize)  #debug
        self.jackSq = 0
        if self.gridsize > 4:
            self.jackSq = random.randint(1, self.gridsize)
            if (self.gridsize > 9):
                self.rept = 3
            else:
                self.rept = 2
        else:
            self.rept = 1
        for n in range (self.rept):
        #while (len(self.randSentenceList) < self.rept):
            self.randSentenceList.append(self.randSentenceGenerator().split()) #not necessary
        #for n in range (self.rept):
            for i in range (len(self.randSentenceList[n])):
               #self.randLineList2.append(self.randSentenceList[n][i])
                self.randLineListWspace.append(self.randSentenceList[n][i])
                self.wrdDict [self.randLineListWspace[i+(n*4)]] = self.sStruct[i]  
        if(self.debug):
            print(self.randLineListWspace)  #debug
            print(self.wrdDict)

        while (len(self.randLineListWspace) < self.gridsize):
            self.randLineListWspace.append(' ')
        if(self.debug):
                print(self.randLineListWspace)
        random.shuffle(self.randLineListWspace)
        if(self.debug):
                print("after shuffle: "+str(self.randLineListWspace))
        for i in range (self.gridsize):
            if(self.randLineListWspace[i] == ' '):
                randLine = self.random_line(self.singleWordFileName)
                self.randLineList.append(randLine)
            else:
                self.randLineList.append(self.randLineListWspace[i])
            equivSum = self.mapLine(self.randLineList[i])
            numSeq = self.pack_rand_vals_of_sum(equivSum)
            questions = self.get_all_quests_in_square(numSeq)
            if(self.debug):
                print(questions)  #debug
                print(self.randLineList[i])
            self.questionsList.append(questions)
            self.equivSumList.append(equivSum)
        if(self.debug):
            print("filled in: "+str(self.randLineList))
        self.questionsList=self.questionsList[1:]
        self.equivSumList=self.equivSumList[1:]
        self.numSquareDone =0
        self.startGrid = time.time()
            
    def randSentenceGenerator(self):
        randVerb = self.random_line('words/verb.txt')
        randNoun = self.random_line('words/'+randVerb+'-nouns.txt')
        randSubject = self.random_line('words/subject.txt')
        randDeterminer = self.random_line('words/determiner.txt')
        randSentence =  randSubject+" "+randVerb+" "+randDeterminer+" "+randNoun
        return randSentence
    
    def collectQuestionsPlus(self):
        self.questionsList = [[]]
        self.wrdTxt =  self.drvdWrdTag
        self.randLineListWspace = []
        self.randLineList = []
        self.equivSumList = [[]]
        self.randSentenceList = []
        self.wrdDict.clear()
        self.sqPoints = 0 
        self.qpos = 0
        self.cnt = 0
        if(self.debug):
            print(self.gridsize)  #debug
        self.jackSq = 0
        if self.gridsize > 4:
            self.jackSq = random.randint(1, self.gridsize)
        self.randLineListWspace = self.collectWrdsRandSentenceGen()
        if(self.debug):
            print(self.randLineListWspace)  #debug
            print(self.wrdDict)
        while (len(self.randLineListWspace) < self.gridsize):
            self.randLineListWspace.append(' ')
        if(self.debug):
                print(self.randLineListWspace)
        random.shuffle(self.randLineListWspace)
        if(self.debug):
                print("after shuffle: "+str(self.randLineListWspace))
        for i in range (self.gridsize):
            if(self.randLineListWspace[i] == ' '):
                randLine = self.random_line(self.singleWordFileName)
                self.randLineList.append(randLine)
            else:
                self.randLineList.append(self.randLineListWspace[i])
            equivSum = self.mapLine(self.randLineList[i])
            numSeq = self.pack_rand_vals_of_sum(equivSum)
            questions = self.get_all_quests_in_square(numSeq)
            if(self.debug):
                print(questions)  #debug
                print(self.randLineList[i])
            self.questionsList.append(questions)
            self.equivSumList.append(equivSum)
        if(self.debug):
            print("filled in: "+str(self.randLineList))
        self.questionsList=self.questionsList[1:]
        self.equivSumList=self.equivSumList[1:]
        self.numSquareDone =0
        self.initgTTS()
        self.startGrid = time.time()

    def collectWrdsRandSentenceGen(self):
        randVerbList = []
        randNounList = []
        randDetList = []
        randSubList = []
        sentenceWrdArr = []
        randtheme = self.random_line('words/theme.txt')
        if (self.gridsize > 9):
            cnt = 6
            cnt2 = 2
        elif (self.gridsize > 4):
            cnt = 3
            cnt2 = 1
        else:
            cnt = 1
            cnt2 = 1
        for i in range (cnt):
            randVerbList.append(self.random_line_no_rep('words/'+randtheme+'-verbs.txt',randVerbList))
            randNounList.append(self.random_line_no_rep('words/'+randtheme+'-nouns.txt',randNounList))
            self.wrdDict[randVerbList[i]] = self.sStruct[1] 
            self.wrdDict[randNounList[i]] = self.sStruct[3]  
        for i in range (cnt2):
            randDetList.append(self.random_line_no_rep('words/determiner.txt',randDetList))
            randSubList.append(self.random_line_no_rep('words/subject.txt',randSubList))
            self.wrdDict[randDetList[i]] = self.sStruct[2] 
            self.wrdDict[randSubList[i]] = self.sStruct[0]  
        for i in range(len(randVerbList)):
            sentenceWrdArr.append(randVerbList[i])
            sentenceWrdArr.append(randNounList[i])
        for i in range(len(randDetList)):
            sentenceWrdArr.append(randDetList[i])
            sentenceWrdArr.append(randSubList[i])
        return sentenceWrdArr
            
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
       # for g in range(self.gridsize):
        while (len(self.randLineList) < self.gridsize):
            randLine = self.random_line_no_rep(self.singleWordFileName,self.randLineList)
            equivSum = self.mapLine(randLine)
            numSeq = self.pack_rand_vals_of_sum(equivSum)
            questions = self.get_all_quests_in_square(numSeq)
            if(self.debug):
                print(questions)  #debug
                print(randLine)
            self.questionsList.append(questions)
            self.randLineList.append(randLine)
            self.equivSumList.append(equivSum)
        self.questionsList=self.questionsList[1:]
        self.equivSumList=self.equivSumList[1:]
        self.numSquareDone =0
        #self.collectQuestionsPlus()
        self.startGrid = time.time()
        #self.collectOneQuestion()

    def collectOneQuestion (self):
        if(self.debug):
            print(self.currGrid)    #debug
            print(self.qpos)       #debug
        if(self.questionsList == [[]]):
            self.questionkvString = "Init"
        else:
            self.questionkvString = self.questionsList[self.currGrid-1][self.qpos]
        if self.firstQuest == 1: #if self.currGrid == 1 and self.qpos == 0:
            if(self.debug):
                print(self.questionkvString)  #debug
            self.start = time.time()
            self.firstQuest =0
            return self.questionkvString
        else:
            if (self.endsq == 1):
                if(self.debug):
                    print(self.questionkvString)  #debug
                self.endsq = 0
                self.start = time.time()

    def returnQuestion(self):
        if(self.debug):
            print(self.questionkvString)  #debug
        #cntr.popon =0
        self.start = time.time()
        #mixer.quit()
        return self.questionkvString,self.textToSpeechgTTS(),self.chngCntr(0.3) #self.textToSpeechgTTS(), 
	
	#works on macOS
    # def handler(self, signum, frame):
    #     if (self.debug):
    #         print ('Signal handler called with signal', signum)
    #     cntr.popon = 0

    #Windows OS
    def handler(self):
        time.sleep(self.tinterval)
        cntr.popon = 0
        #self.tinterval = time.time()
        #return self.done

    def chngCntr(self,s):
        #cntr.popon = 0
        ##works on macOS
        #signal.signal(signal.SIGALRM, self.handler)
        #signal.alarm(t)
        ##Windows OS
        self.tinterval = s
        t = threading.Thread(target=self.handler)
        t.start() # start ticker in a new thread
        
    def showBtnTxt (self,index):
        self.btnText[index-1] = self.randLineList[index-1]
        self.setAllBtnTxt()
    
    def setAllBtnTxt(self):
        self.btn1Text = self.btnText[0]
        self.btn2Text = self.btnText[1]
        self.btn3Text = self.btnText[2]
        self.btn4Text = self.btnText[3]
        self.btn5Text = self.btnText[4]
        self.btn6Text = self.btnText[5]
        self.btn7Text = self.btnText[6]
        self.btn8Text = self.btnText[7]
        self.btn9Text = self.btnText[8]
        self.btn10Text = self.btnText[9]
        self.btn11Text = self.btnText[10]
        self.btn12Text = self.btnText[11]
        self.btn13Text = self.btnText[12]
        self.btn14Text = self.btnText[13]
        self.btn15Text = self.btnText[14]
        self.btn16Text = self.btnText[15]

    def initAllBtnTxt(self):
        self.btnText = ['']*16
        self.setAllBtnTxt()

    def collectAns(self):
        self.screenName = self.workScreenName
        cntr.screenName = self.screenName
        self.timeElapsed = 0
        self.timeElapsed = time.time() - self.start
        
        if (self.ansWord):
            try:
                ans = str(self.ans_ent)
            except(TypeError):
                self.errMsg= self.invalidEntryTag
                self.errDef= self.enterAlphaTag
            except(ValueError):
                self.errMsg=self.invalidEntryTag
                self.errDef=self.enterAlphaTag
            else:
                try:
                    ansSum = self.mapLine(ans)
                except(KeyError):
                    self.errMsg=self.invalidEntryTag
                    self.errDef= self.enterAlphaTag
                else:
                    if ans == "":
                        self.errMsg=self.invalidEntryTag
                        self.errDef=self.enterAlphaTag
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
            self.errMsg = self.incorrectTag 
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
        if(self.mkSenten == True):
            if((self.numSentence >= self.gridsize)|
            ((self.numSentence == 1)&(self.gridsize == 4))): #self.reqNumSentence
                #self.endGrid = time.time()
                self.foundSentences = []
                self.endGame()
        elif (self.ansWord == True):
            self.numSquareDone +=1
            self.endSquare()
        else:
            self.screenName = self.workScreenName
            cntr.screenName = self.screenName
            self.sumTxt +=  "  "+str(self.equivSumList[self.currGrid-1][self.qpos-1])
            if (self.qpos not in range(len(self.questionsList[self.currGrid-1]))):
                self.askWord()
            else:
                self.collectOneQuestion()
            #self.textToSpeech()

    def askWord(self):
        self.ansWord = True
        self.questionkvString = "Enter the word that matches the sums below:"
        self.start = time.time()
  
    def endSquare(self):
        self.ansWord = False
        self.cnt +=1
        if (self.cnt > 5):
            self.wrdTxt += "\n                     "
            self.cnt = 1
        self.wrdTxt +=  "  "+self.randLineList[self.currGrid-1]
        self.sumTxt = self.drvdSumTag
        self.questionkvString = ""
        if (self.numSquareDone == self.gridsize):
            #self.endGrid = time.time()
            for i in range(len(self.randLineListWspace)):
                self.btnText[i] = self.randLineListWspace[i]
            self.setAllBtnTxt()
            #self.randLineList = self.randLineListWspace[i]
            self.screenName = self.wrkScreen
            cntr.screenName = self.screenName
            self.mkSenten = True
            #self.endGame()
        else:
            self.screenName = self.selGridScreen 
            cntr.screenName = self.screenName
            self.endsq = 1
            self.qpos =0
            self.sqPoints = 0

    def checkSentence(self):
        if(self.selSentenString in self.foundSentences): 
            self.errMsg = "Sorry!"
            self.errDef = "That sentence has already been found!"
        else:
            arrSentence = []
            arrSentence = self.selSentenString.split() 
            self.numSentence += 1
            self.numTries += 1
            for i in range(len(arrSentence)):
                if(self.wrdDict[arrSentence[i]] != self.sStruct[i]):
                    self.errMsg = self.incorrectTag
                    self.errDef = "That is not a correct sentence!"
                    self.numSentence -= 1
                    break
                else:
                    self.errMsg = self.correctTag
                    self.errDef = "That is a correct sentence!"
            if(self.errMsg == self.correctTag):
                self.foundSentences.append(self.selSentenString)
                self.sqPoints = 200/self.numTries
                self.numTries = 0
                self.reportSummary()
        self.selSentenString = ""
        
        # if(self.numSentence >= self.reqNumSentence):
        #     #self.endGrid = time.time()
        #     self.foundSentences = []
        #     self.endGame()
        
    def endGame(self):
        self.endGrid = time.time()
        self.firstQuest = 1
        self.mkSenten = False
        self.screenName = self.doneScreenName 
        cntr.screenName = self.screenName
        self.ansWord = False
        if (self.questionkvString == "1"):
            self.questionkvString = "You were almost there!\nCompletion Time: "+str(int((self.endGrid-self.startGrid)/60))+"mins\nPoints Earned: " +str(self.totalPoints)+"."
        elif (self.numSquareDone == self.gridsize):
            self.questionkvString = "Congratulations! You're All Done!\nCompletion Time: "+str(int((self.endGrid-self.startGrid)/60))+"mins\nPoints Earned: " +str(self.totalPoints)+"."
        else:
            self.questionkvString = "Incomplete Grid!\nPoints Earned: " +str(self.totalPoints)+"."

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
        self.selSentenString = ""
        self.foundSentences = []
        self.numSentence = 0
        self.totalPoints = 0
        self.sqPoints = 0 
        self.qpos = 0
        self.ansWord = False
        self.questionkvString = "Solve: "
        self.wrdTxt =  self.drvdWrdTag
        self.sumTxt = self.drvdSumTag
        self.pointLabelTxt = "Total Points: 0"
        mixer.quit()
        self.del_all_mp3_files()
        #self.kill_by_process_name_shell() 

    # def makeMapTable(self):
    #     for i in range (13):
    #         self.tblRow1 += alphaTuple[i] + "   "
    #     self.tblRow1 += "\n"
    #     for i in range (13):
    #          self.tblRow1 += str(i)+ "   "
    #     self.tblRow1 += "\n"
    #     for i in range (13,26):
    #         self.tblRow1 += alphaTuple[i] + "    "
    #     self.tblRow1 += "\n"
    #     for i in range (13,26):
    #          self.tblRow1 += str(i)+ "   "
        
    def random_line(self,fn):
        fp = open(fn).read().splitlines()
        return random.choice(fp)

    def random_line_no_rep(self,fn,workArr):
        fp = open(fn).read().splitlines()
        randChoice = random.choice(fp)
        while (randChoice in workArr):
            randChoice = random.choice(fp)
        return randChoice

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

    def on_stop(self):
        mixer.quit()
        #pygame.quit()
        self.del_all_mp3_files()
        #Logger.critical('Goodbye')

    def build(self):
        self.presentation = Builder.load_file("wordGame.kv")
        return self.presentation





if __name__ == "__main__":
    GameApp().run()
    #mixer.quit()
