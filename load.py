import numpy as np
import matplotlib.pyplot as plt


class BeamLoad:
    """ Loading to be applied to beams """

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
        self.Ra = 0
        self.Rb = 0

    def reactions(self):
        """ Calculate the reactions to the beam """
        components = []
        w_loads = []
        for load in self.loads:
            if load[0] == load[1]:
                w = load[2]
                w_loads.append(w)
            else:
                w = (load[1] - load[0]) * load[2]
                w_loads.append(w)
            la = load[0] + (load[1] - load[0])/2
            components.append(la * w / self.span)
            self.Rb = sum(components)
            self.Ra = sum(w_loads) - self.Rb

    def shear_force_diagram(self):
        """ Plot the shear force diagram for the beam """
        self.reactions()
        x = np.arange(0, self.span + 0.01, 0.01)
        shear = []
        for n in x:
            shear_load = []
            for load in self.loads:
                if n > load[0] == load[1]:
                    shear_load.append(load[2])
                elif n > load[0] != load[1]:
                    shear_load.append((n-load[0])*load[2])
            shear.append(sum(shear_load) - self.Ra)

        # Plot the results
        plt.style.use('seaborn-white')
        fig, ax = plt.subplots()
        ax.plot(x, shear)
        plt.axhline(0, color='black')
        ax.fill_between(x, 0, shear)
        plt.axvline(0, color='black')
        plt.axvline(self.span, color='black')
        ax.set_xlabel('Distance (m)')
        ax.set_ylabel('Shear Force (kN)')
        ax.set_title('Shear Force Diagram')
        plt.grid()
        plt.show()

    def bending_moment_diagram(self):
        """ Plot the bending moment diagram for the beam """
        self.reactions()
        x = np.arange(0, self.span + 0.01, 0.01)
        bending_moment = []
        for n in x:
            bending_load = []
            for load in self.loads:
                if n > load[0] == load[1]:
                    bending_load.append(load[2] * (n - load[0]))
                elif n > load[0] != load[1]:
                    udl_w = (n - load[0]) * load[2]
                    udl_la = (n - load[0]) / 2
                    bending_load.append(udl_la * udl_w)
            bending_moment.append(self.Ra * n - sum(bending_load))

        # Plot the results
        plt.style.use('seaborn-white')
        fig, ax = plt.subplots()
        ax.plot(x, bending_moment, color='red')
        plt.axhline(0, color='black')
        ax.fill_between(x, 0, bending_moment, color='red')
        plt.axvline(0, color='black')
        plt.axvline(self.span, color='black')
        ax.set_xlabel('Distance (m)')
        ax.set_ylabel('Bending Moment (kNm)')
        ax.set_title('Bending Moment Diagram')
        plt.grid()
        plt.show()