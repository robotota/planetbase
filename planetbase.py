# -*- encoding: utf-8 -*-

import combat
import random
import namegen
from buildings import *
from cmd import Cmd


def startswith(start, completes):
    return filter(lambda x: x.startswith(start), completes)


class PlanetBase(Cmd):
    def __init__(self):
        Cmd.__init__(self)
        self.prompt = "> "
        self.intro = "Planetbase sim"
    

    def do_status(self, line):
        state.printStatus()


    def help_status(self):
        print "Show current base status"
        

    def do_exit(self, line):
        exit()


    def help_exit(self):
        print "Exit simulation"
        

    def do_units(self, line):
        print state.units    


    def help_units(self):
        print "Show active units"
        

    def do_train(self, line):
        if line=="agent":
            starttraining(TrainableAgent(namegen.createName()))
        elif line == "medic":
            starttraining(TrainableMedic(namegen.createName()))
        elif line == "droid":
            starttraining(TrainableDroid())
        else:
            print "train who?"


    def complete_train(self, text, line, i, j):
        return startswith(text, ["agent", "medic", "droid"])


    def help_train(self):
        print "Start training [agent], [medic] or [droid]"
        print "train medic"
        print "train agent"
        print "train droid"


    def do_build(self,line):
        if line == "powergen":
            startbuilding(PowerGenerator())
        elif line == "massgen":
            startbuilding(MassGenerator())
        elif line == "transport":
            startbuilding(Transport())
        elif line == "powerline":
            startbuilding(PowerLine())
        else:
            print "build what?"


    def complete_build(self, text, line, i, j):
        return startswith(text, ["powergen", "massgen", "transport", "powerline"])


    def help_build(self):
        print "Start construction of new building"
        print "    build powergen"
        print "    build massgen"
        print "    build transport"
        print "    build powerline"                
        

    def do_stop(self, line):
        try:
            state.buildings[int(line)].stop()
        except:
            print "wrong argument"

    def help_stop(self):
        print "Stop active building"
        print "    stop NUMBER"        
            

    def do_start(self, line):
        try:
            state.buildings[int(line)].start()
        except:
            print "wrong argument"


    def help_start(self):
        print "Start again inactive building"
        print "    start NUMBER"            


    def default(self, line):
        print "what?!"
                

    def emptyline(self):
        self.end_turn()
        self.begin_turn()


    def begin_turn(self):
        state.buildings = filter (lambda x: x!=None, state.buildings)

        if random.random() > 0.995 ** len(state.buildings):
            count = int(round(random.random() * (len(state.units))) )
            if count <= 0:
                count = 1
            state.warning("We were attacked by " +str(count) + " unit(s)")
            enemy = [combat.AngryAnt("enemy") for i in range(count)]
            combat.play(state.units, enemy)
            if not state.units:
                state.badnews("Enemy broke through!")
                for i in range(len(enemy)):
                    b = random.choice(state.buildings)
                    if random.random()<0.1:
                        state.badnews(str(b) + " was destroyed")
                        state.buildings.remove(b)
        state.buildings.sort(key = lambda x: x.sortkey())
        state.printStatus()    

    def end_turn(self):
        state.clear()

        for building in state.buildings:
            building.tick(state)
            
        for unit in state.units:
            if unit.wounded() and state.transport >0 and state.mass > 0 and state.energy >0 and state.powerline >0:
                unit.heal()
                state.transport -= 1
                state.mass -= 1
                state.energy -= 1
                state.powerline -= 1
                state.goodnews(unit.name+" was healed")


game = PlanetBase()
game.begin_turn()
game.cmdloop()
