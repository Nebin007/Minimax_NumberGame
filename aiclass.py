import random
from itertools import repeat
class gamestructure:
    numstring = []
    score = []
    #class core
    def __init__(self):
        self.numstring.clear()
        for x in range(7): self.numstring.append(random.randint(1,7))
        self.score.clear()
        k = sum(self.numstring) - random.randint(4,6)
        for x in range(2): self.score.append(k)
    
    def __str__(self):
        return '[Comp: '+str(self.score[0])+', '+str(self.numstring)+', Player: '+str(self.score[1])
    
    def restetparm(self):
        self.numstring.clear()
        for x in range(7): self.numstring.append(random.randint(1,7))
        self.score.clear()
        k = sum(self.numstring) - random.randint(4,6)
        for x in range(2): self.score.append(k)
    
    #Member functions
    def printdet(self):
        self.numstring.sort()
        print("Computer: "+str(self.score[0])+","+str(self.numstring)+","+"Player: "+str(self.score[1]))
        print("\n")
    
    def chkwin(self):
        if len(self.numstring) == 1:
            return True
        else:
            return False
            
    def whowon(self,player):
        plin = player - 1
        if len(self.numstring) == 1:
            if self.score[plin] == max(self.score):
                return True
            else:
                return False
        else:
            return False
    
    def drawcheck(self):
        if len(self.numstring) == 1:
            if self.score[0] == self.score[1]:
                return True
            else:
                return False
        else:
            return False
    
    def gamestate(self, player,num):
        plinp = player - 1
        if num in self.numstring:
            self.numstring.remove(num)
            self.score[plinp] = self.score[plinp] - num
            self.numstring.sort()
            if self.chkwin():
                if self.score[0] > self.score[1]:
                    print("Bot win")
                    return 100
                elif self.score[0] < self.score[1]:
                    print("Human Wins")
                    return -100
                else:
                    print("Draw")
                    return 50
            return 200
        else:
            print("Invalid Input! Insert again")
            num = int(input("Choose 2 or 3: "))
            self.gamestate(player,num)
    
    def minimax(self, isMaxi):
        
        print(self)
        if self.whowon(1):
            return 1
        elif self.whowon(2):
            return -1
        elif self.drawcheck():
            return 0
        
        if(isMaxi):
            bestscore = -10
            for num in self.numstring:
                self.numstring.remove(num)
                self.score[0] = self.score[0] - num
                score = self.minimax(False)
                self.numstring.append(num)
                self.score[0] = self.score[0] + num
                if(score > bestscore):
                    bestscore = score
            print("The current level is: "+str(bestscore))
            return bestscore
        else:
            bestscore = 10
            for num in self.numstring:
                self.numstring.remove(num)
                self.score[1] = self.score[1] - num
                score = self.minimax(True)
                self.numstring.append(num)
                self.score[1] = self.score[1] + num
                if(score > bestscore):
                    bestscore = score
            print("The current level is: "+str(bestscore))
            return bestscore
