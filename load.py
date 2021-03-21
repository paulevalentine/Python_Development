class BeamLoad:
    """ Loading to be applied to beams """
    registry = []
    def __init__(self, load, start, finish):
        registry.append(self)
        self.load = load
        self.start = start
        self.finish = finish
        if start == finish:
            self.type = 'PL'
            self.total_load = load
        else:
            self.type = 'UDL'
            self.total_load = load * (self.finish - self.start)

        self.total_location = self.start + (self.finish - self.start) / 2


class Beam:
    """ Simply supported beam analysis """
    def __init__(self, span, loads):
        self.span = span
        self.loads = loads
        for i, load in enumerate(self.loads):
            globals()[f'load{i}'] = BeamLoad(load[i][0], load[i][1], load[i][2])

    def reactions(self):
        """ Calculate the reactions to the beam """
        components = []
        for load in BeamLoad.registry:
            components.append(load.total_location * load.load / self.span)
