import colors

class State:
    def __init__(self):
        self.energy = 0
        self.mass = 0
        self.energy_capacity = 0
        self.mass_capacity = 0
        self.transport = 0
        self.powerline = 0
        self.transport_capacity = 0
        self.powerline_capacity = 0

        self.units = []
        self.enemy_units = []
        self.log = []

    def printStatus(self):
        planned_state = self.copy()
        planned_state.clear()
        for building in planned_state.buildings:
            building.tick(planned_state, pretend = True)
        i = 0
        for building in planned_state.buildings:
            print i, ")", building, {False: colors.red("Off"), True: colors.green("On")}[building.on]
            i += 1

        print "Energy:", self.energy
        print "Mass:", self.mass
        print "Transport: %d / %d" %(planned_state.transport, planned_state.transport_capacity)
        print "Powerline: %d / %d"%(planned_state.powerline, planned_state.powerline_capacity)

        print "\n".join(self.log)

        print "Enemy units:", len(self.enemy_units)
        self.log = []

    def message(self, string):
        self.log.append(colors.color(colors.USUAL, colors.BLUE) + string + colors.RESET)

    def warning(self, string):
        self.log.append(colors.color(colors.USUAL, colors.YELLOW) + string + colors.RESET)

    def goodnews(self, string):
        self.log.append(colors.color(colors.USUAL, colors.GREEN) + string + colors.RESET)

    def badnews(self, string):
        self.log.append(colors.color(colors.USUAL, colors.RED) + string + colors.RESET)

    def copy(self):
        result = State()
        fields  = [key for (key, value) in self.__dict__.items() if not callable(value) and not key.startswith('__')]
        for field in fields:
            setattr(result, field, getattr(self, field))
        return result

    def clear(self):
        self.transport = 0
        self.transport_capacity = 0
        self.powerline = 0
        self.powerline_capacity = 0
