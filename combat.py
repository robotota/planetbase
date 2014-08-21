import random
import namegen
loud = False

class Unit:
    speciality = ""
    def __repr__(self):
        return self.speciality +" " + self.name+" "+str(self.hp) + "/"+ str(self.maxhp) +" "+ str(self.missrate)
    def __init__(self, name):
        self.name = name
        self.level = 1
        self.exp = 0
    def heal(self):
        self.hp += 1
    def wounded(self):
        return self.hp < self.maxhp    
    def levelup(self):
        self.exp += 1
        if self.exp == self.level:
            if loud:
                print self.name, "levelup"
            self.missrate *= 0.95
            self.maxhp += 1
            self.level += 1
            self.exp = 0
    def hit(self):
        if loud:
            print self.name, "was hit!"
        if random.random()<0.1:
            if loud:
                print self.name, "critical!"
            self.hp -= 2
        else:
            self.hp -= 1    
        print self.name , " has ", self.hp, "hp left"
    def dead(self):
        return self.hp <= 0          


class Combatant(Unit):
    speciality = "agent"
    def act(self, friends, opponents):
        b = random.choice(opponents)
        self.pewpew(b)
        if b.dead():
            opponents.remove(b)

    def pewpew(self, whom):
        if loud:
            print self.name, "shoots", whom.name
        if random.random() > self.missrate:
            whom.hit()
            self.onHit(whom)
        else:
            if loud:
                print self.name, "misses"
    
    def onHit(self, whom):
        pass            

class BattleDroid(Combatant):
    speciality = "droid"
    def __init__(self, *args):
        Combatant.__init__(self, args)
        self.maxhp = 1
        self.hp = 1
        self.missrate = 0.7
                    
class Agent(Combatant):
    speciality = "agent"
    def __init__(self, *args):
        Combatant.__init__(self, args)
        self.maxhp = 3
        self.hp = 3
        self.missrate = 0.7

    def onHit(self, whom):
        if whom.dead():
            if loud:
                print whom.name, "dies"
            self.levelup()


class AngryAnt(Combatant):
    def __init__(self, name):
        Combatant.__init__(self, name)
        self.maxhp = 1
        self.hp = 1
        self.missrate = 0.7
        
class Healer(Unit):
    speciality = "medic"
    
    def __init__(self, *args):
        Unit.__init__(self, args)
        self.maxhp = 3
        self.hp = 3
        self.missrate = 0.7

    def act(self, friends, opponents):
        wounded = filter(lambda x: x.wounded(), friends)
        if wounded != []:
            b = random.choice(wounded)
            if loud:
                print self.name, "tries to heal", b.name
            if random.random()> self.missrate:
                if loud:
                    print self.name, "heals", b.name
                b.heal()
                self.levelup()
        else:
            if loud:
                print self.name, "has nothing to do"                
                
def step(A, B):
    a = random.choice(A+B)
    if a in A:
       friends = A
       opponents = B
    else:
       friends = B
       opponents = A   
    a.act(friends, opponents)
    
def status():
    print "we:", sideA
    print "they:", sideB    

def play(A, B):
    while A !=[] and B != []:
        # randomly choose player1 and 2
        step(A, B)


if __name__ == "__main__":
    loud = True
    sideA = []
    while True:
        sideB = [AngryAnt("ant") for i in range(10)] 
        while len(sideA) < 5:
            name = namegen.createName()
            if random.random()< 0.2:
                unit = Healer(name)
            else:
                unit = Combatant(name)    
            sideA.append(unit)
        print "side A is ready for next round"
        
        status()   
        while sideA !=[] and sideB != []:
            # randomly choose player1 and 2
            step(sideA, sideB)
            status()
            raw_input()
        for person in sideA:
            if person.wounded():
                person.heal()
            if person.wounded():
                person.heal()    
        
