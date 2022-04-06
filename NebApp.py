import imp
from multiprocessing import managers
import os
from threading import main_thread
from unicodedata import name
from kivy.app import App
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen, SlideTransition
import os
from kivy.core.window import Window
from kivy.uix.button import Button
from kivy.clock import Clock
from aiclass import gamestructure


lsb = [2,2,2,3,3,3]

player = ''



class Gamescreen(Screen):
    idd = 0
    global player
    def on_enter(self, *args):
        self.gamedata = Menuscreen().retdata()
        print(player)
        self.ids.log_id.text = "The Game has Started"
        if player == "Human":
            self.playeract()
        elif player == "Computer":
            self.comp_act()
    
    def playeract(self,val = 0):
        if not self.gamedata.chkwin():
            if val == 0:
                self.btnadder()
                self.ids.comp_id.text = str(self.gamedata.score[0])
                self.ids.hum_id.text = str(self.gamedata.score[1])
            else:
                retval = self.gamedata.gamestate(2,val)
                self.ids.bx_lyt.clear_widgets()
                if retval == 200:
                    self.comp_act()
                elif retval == 100:
                    self.ids.log_id.text = "Computer Wins the game"
                    self.ids.comp_id.text = str(self.gamedata.score[0])
                    self.ids.hum_id.text = str(self.gamedata.score[1])
                    self.gamedata.restetparm()
                elif retval == -100:
                    self.ids.log_id.text = "Human Wins the game"
                    self.ids.comp_id.text = str(self.gamedata.score[0])
                    self.ids.hum_id.text = str(self.gamedata.score[1])
                    self.gamedata.restetparm()
                elif retval == 50:
                    self.ids.log_id.text = "The game is a draw"
                    self.ids.comp_id.text = str(self.gamedata.score[0])
                    self.ids.hum_id.text = str(self.gamedata.score[1])
                    self.gamedata.restetparm()
        else:
            print("Game is finished") 
            self.gamedata.restetparm()          


    
    def comp_act(self):
        if not self.gamedata.chkwin():
            bestscore = -10
            bestnum = 0
            for num in self.gamedata.numstring:
                self.gamedata.numstring.remove(num)
                self.gamedata.score[0] = self.gamedata.score[0] - num
                score = self.gamedata.minimax(False)
                self.gamedata.numstring.append(num)
                self.gamedata.score[0] = self.gamedata.score[0] + num
                if(score > bestscore):
                    bestscore = score
                    bestnum = num
            self.ids.log_id.text = "Computer Choose " + str(bestnum)
            retval = self.gamedata.gamestate(1,bestnum)
            if retval == 200:
                self.playeract()
            elif retval == 100:
                self.ids.log_id.text = "Computer Wins the game"
                self.ids.comp_id.text = str(self.gamedata.score[0])
                self.ids.hum_id.text = str(self.gamedata.score[1])
                self.gamedata.restetparm()
            elif retval == -100:
                self.ids.log_id.text = "Human Wins the game"
                self.ids.comp_id.text = str(self.gamedata.score[0])
                self.ids.hum_id.text = str(self.gamedata.score[1])
                self.gamedata.restetparm()
            elif retval == 50:
                self.ids.log_id.text = "The game is a draw"
                self.ids.comp_id.text = str(self.gamedata.score[0])
                self.ids.hum_id.text = str(self.gamedata.score[1])
                self.gamedata.restetparm()
        else:
            print("Game is finished")
            self.gamedata.restetparm()   

    def btnadder(self):
        xax = 0.1
        for x in self.gamedata.numstring:
            xax = xax + 0.1
            button = Button(text=str(x),font_size = 12,size_hint=(0.1,0.1),pos_hint={'x': xax, 'y': 0.7},on_press= self.scorbtn)
            button.my_id = x
            self.ids.bx_lyt.add_widget(button)
    
    def restartfn(self):
        Window.clearcolor = (0, 0, 0, 0)
        self.ids.bx_lyt.clear_widgets()
        self.manager.current = 'menu'
    
    def scorbtn(self,instance):
        print(instance)
        self.playeract(instance.my_id)

    def refresh(self):
        self.idd = self.idd + 1
        print(self.idd)
        self.ids.some_d.text = str(self.idd)    
    def func(self):
        return str(self.idd)        

class Menuscreen(Screen):
    
    gamedata = gamestructure()
    def on_enter(self, *args):
        self.gamedata = gamestructure()
    
    def retdata(self):
        return self.gamedata
    
    def do_work(self,ply):
        global player
        player = ply
        self.manager.transition = SlideTransition(direction ="right")
        self.manager.current = 'Game'
        Window.clearcolor = (0.247, 0.247, 0.247, 1)
    
    def exitfn(self):
        exit()


Builder.load_string("""
<Menuscreen>:
    FloatLayout:
		cols: 1
		size: root.height, root.width
		Label:
			text: "[b][color=04ff00]Welcome to the Number Game[/color][/b]"
            pos_hint: {'x': 0, 'y': 0.4}
			markup: True
            font_size: 48
        Label:
			text: "[color=f2ff00] Who wants to play first?[/color] "
            markup: True
			font_size: 32
            pos_hint: {'x': 0, 'y': 0.3}
        Button:
            text: "Human"
            font_size: 24
            pos_hint: {'x': 0.4, 'y': 0.5}
            size_hint: 0.2, 0.2
            on_press: root.do_work("Human")
        Button:
            text: "Computer"
            font_size: 24
            pos_hint: {'x': 0.4, 'y': 0.3}
            size_hint: 0.2, 0.2
            on_press: root.do_work("Computer")
        Button:
            text: "Exit"
            font_size: 24
            size: 75,50
            background_color: (1.0, 0.0, 0.0, 1.0)
            size_hint: None,None
            on_press: root.exitfn()

<Gamescreen>:
    FloatLayout:
        id: gm_scr
		cols: 1
		size: root.height, root.width
        
		Label:
			text: "ScoreBoard"
            pos_hint: {'x': 0, 'y': 0.45}
			font_size: 24
        Label:
            text: "Computer: "
            pos_hint: {'x': -0.4, 'y': 0.35}
            font_size: 20 
        Label:
            id: comp_id
            text: "0"
            pos_hint: {'x': -0.3, 'y': 0.35}
            font_size: 20
        Label:
            text: "Human: "
            pos_hint: {'x': 0.3, 'y': 0.35}
            font_size: 20 
        Label:
            id: hum_id
            text: "0"
            pos_hint: {'x': 0.4, 'y': 0.35}
            font_size: 20
        BoxLayout:
            id: bx_lyt   
        Label:
            id: log_id
            text: "Game Has started" 
            pos_hint: {'x': 0, 'y': 0.1}
			font_size: 20 
        Button:
            text: "Restart"
            font_size: 24
            size: 75,50
            background_color: (1.0, 0.0, 0.0, 1.0)
            size_hint: None,None
            on_press: root.restartfn()
        
        
""")

Window.clearcolor = (0, 0, 0, 0)

class NebApp(App):
    def build(self):
        manager = ScreenManager()
        manager.add_widget(Menuscreen(name='menu'))
        manager.add_widget(Gamescreen(name="Game"))
        return manager

if __name__ == '__main__':
    NebApp().run()