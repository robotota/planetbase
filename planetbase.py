# -*- encoding: utf-8 -*-

import sys
import random
import namegen
from buildings import *
from cmd import Cmd
import state
import logging

log_level = logging.DEBUG if "--debug" in sys.argv else logging.ERROR
logging.basicConfig(stream=sys.stderr, level=log_level)
state = state.State()
state.buildings = [Central(), Transport(), PowerLine()]
state.enemy_units = [combat.AngryAnt("enemy"), combat.AngryAnt("enemy")]

def startswith(start, names):
    return [name for name in names if name.startswith(start)]


def startbuilding(what):
    state.buildings.append(Building(what))
    print "building started"


def starttraining(who):
    state.buildings.append(Training(who))
    print "training started"


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

    def do_attack(self, line):
        #all current agents move to attack
        if line == "":
            for unit in state.units:
                unit.set_attacking(True)
        elif line == "stop":
            for unit in state.units:
                unit.set_attacking(False)
        else:
            print "what?!"
    def complete_attack(self, text, line, i, j):
        return startswith(text, ["stop"])

    def help_attack(self):
        print "Send living units to attack enemy"

    def do_build(self, line):
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


    def defend_base(self):
        attackers = [unit for unit in state.enemy_units if random.random() < 0.005]

        if len(attackers) >0:
            state.warning("We were attacked by " +str(len(attackers)) + " unit(s)")
            real_attackers = attackers[:]

            defenders = state.units[:]
            combat.play(defenders, real_attackers)
            for unit in attackers:
                if unit not in real_attackers:
                    state.enemy_units.remove(unit)
            for unit in state.units:
                if unit not in defenders:
                    state.badnews(unit.name + " KIA")
                    state.units.remove(unit)

            if not state.units:
                state.badnews("Enemy broke through!")
                for i in range(len(real_attackers)):
                    b = random.choice(state.buildings)
                    if random.random()<0.1:
                        state.badnews(str(b) + " was destroyed")
                        state.buildings.remove(b)

    def perform_mission(self):
        our_units = [unit for unit in state.units if unit.attacking]
        attackers = [unit for unit in state.enemy_units if random.random() < 0.01]

        if our_units and attackers:
            state.warning("Encountered " +str(len(attackers)) + " unit(s)")
            real_attackers = attackers[:]
            defenders = state.units[:]
            combat.play(our_units, real_attackers)
            for unit in attackers:
                if unit not in real_attackers:
                    state.enemy_units.remove(unit)
            for unit in state.units:
                if unit not in our_units:
                    state.badnews(unit.name + " KIA in a mission")
                    state.units.remove(unit)

    def begin_turn(self):
        state.buildings = filter(lambda x: x!=None, state.buildings)
        self.defend_base()
        if not state.buildings:
            raise Exception("YOU LOST")
        state.buildings.sort(key = lambda x: x.sortkey())
        state.printStatus()    

    def autoheal(self):
        for unit in state.units:
            if unit.wounded() and state.transport > 0 and state.mass > 0 and \
                    state.energy > 0 and state.powerline > 0:
                unit.heal()
                state.transport -= 1
                state.mass -= 1
                state.energy -= 1
                state.powerline -= 1
                state.goodnews(unit.name+" was healed")

    def tick_buildings(self):
        for building in state.buildings:
            building.tick(state)

    def tick_enemy(self):
        new_units = []
        for unit in state.enemy_units:
            r = random.random()
            if r < 0.01:
                unit.levelup()
            elif r < 0.03:
                new_units.append(combat.AngryAnt("enemy"))
            elif r < 0.5:
                unit.heal()
        state.enemy_units += new_units

    def end_turn(self):
        self.perform_mission()
        state.clear()
        self.tick_buildings()
        self.autoheal()
        self.tick_enemy()

game = PlanetBase()
game.begin_turn()
game.cmdloop()
