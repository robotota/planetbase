import combat
from colors import *

class Turnable:
    def start(self):
        self.on = True

    def stop(self):
        self.on = False    

    def __init__(self):
        self.on = True


class Building(Turnable):
    def sortkey(self):
        return 'p';
        
    def __str__(self):
        return "Building "+ self.next.name+" m:"+str(self.next.mass_to_build) + " e:" + str(self.next.energy_to_build)

    def __init__(self, next):
        Turnable.__init__(self)
        self.next = next
        self.built = 0;

    def tick(self, state, pretend = False):
        if not self.on:
            return
        
        while self.next.mass_to_build > 0 and state.mass > 0 and state.energy >0 and state.transport >0 and state.powerline >0:
            if not pretend:
                self.next.mass_to_build -= 1
            state.mass -= 1
            state.energy -= 1
            state.transport -= 1
            state.powerline -= 1

        while self.next.energy_to_build > 0 and state.energy > 0 and state.powerline > 0:
            if not pretend:
                self.next.energy_to_build -= 1
            state.energy -= 1
            state.powerline -= 1
                        
        if self.next.mass_to_build == 0 and self.next.energy_to_build == 0:
           i = state.buildings.index(self)
           state.buildings[i] = self.next
           state.goodnews(self.next.name + " has been built")


class TrainableAgent(combat.Agent):
    def __init__(self, name):
        combat.Agent.__init__(self, name)
        self.mass_to_build = 40
        self.energy_to_build = 100
        self.name = name


class TrainableMedic(combat.Healer):
    def __init__(self, name):
        combat.Healer.__init__(self, name)
        self.mass_to_build = 20
        self.energy_to_build = 50
        self.name = name


class TrainableDroid(combat.BattleDroid):
    def __init__(self):
        combat.BattleDroid.__init__(self)
        self.mass_to_build = 5
        self.energy_to_build = 20
        self.name = "droid"        


class Training(Turnable):
    def sortkey(self):
        return 'p'
        
    def __str__(self):
        return "Training "+ self.next.name+" m:"+str(self.next.mass_to_build) + " e:" + str(self.next.energy_to_build)

    def __init__(self, next):
        Turnable.__init__(self)
        self.next = next
        self.built = 0

    def tick(self, state, pretend = False):
        if not self.on:
            return
        
        while self.next.mass_to_build > 0 and state.mass > 0 and state.energy >0 and state.transport >0 and state.powerline >0:
            if not pretend:
                self.next.mass_to_build -= 1
            state.mass -= 1
            state.energy -= 1
            state.transport -= 1
            state.powerline -= 1

        while self.next.energy_to_build > 0 and state.energy > 0 and state.powerline > 0:
            if not pretend:
                self.next.energy_to_build -= 1
            state.energy -= 1
            state.powerline -= 1
                        
        if self.next.mass_to_build == 0 and self.next.energy_to_build == 0:
           i = state.buildings.index(self)
           state.buildings[i] = None
           state.units.append(self.next)
           state.goodnews(self.next.name + " has been trained")


class Central(Turnable):

    def sortkey(self):
        return 'c';

    def __str__(self):
        return "Central"

    def tick(self, state, pretend = False):
        
        if state.powerline >0:
            state.energy += 1
            state.powerline -= 1
        if self.on:
            if state.transport > 0 and state.energy > 0 and state.powerline >0:
               state.mass += 1
               state.transport -= 1
               state.energy -= 1
               state.powerline -= 1               


class PowerGenerator(Turnable):
    def sortkey(self):
        return 'b';

    def __str__(self):
        return "Power Generator"

    def __init__(self):
        Turnable.__init__(self)
        self.mass_to_build = 5
        self.energy_to_build = 8
        self.name = "power generator"

    def tick(self, state, pretend = False):
        if self.on and state.powerline > 0:
            state.energy += 1
            state.powerline -= 1

class MassGenerator(Turnable):
    def sortkey(self):
        return 'c';

    def __str__(self):
        return "Mass Generator"

    def __init__(self):
        Turnable.__init__(self)
        self.mass_to_build = 10
        self.energy_to_build = 20
        self.name = "mass generator"

    def tick(self, state, pretend = False):
        if self.on:
            if state.energy >= 11 and state.powerline >= 11:
                state.energy -= 11
                state.powerline -= 11
                state.mass += 1
                state.transport -= 1
            else:
                state.warning("no energy for mass generator")          


class Transport(Turnable):
    def sortkey(self):
        return 'a';

    def __str__(self):
        return "Transportation droid"

    def __init__(self):
        Turnable.__init__(self)
        self.mass_to_build = 10
        self.energy_to_build = 40    
        self.name = "transport"

    def tick(self, state, pretend = False):
        state.transport += 1
        state.transport_capacity += 1


class PowerLine(Turnable):
    def sortkey(self):
        return 'a';

    def __str__(self):
        return "Power line"

    def __init__(self):
        Turnable.__init__(self)    
        self.mass_to_build = 10
        self.energy_to_build = 5
        self.name = "powerline"

    def tick(self, state, pretend = False):
        state.powerline += 5
        state.powerline_capacity += 5
           





