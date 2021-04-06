import numpy as np
import matplotlib.pyplot as plt


class Beam:
    """ Simply supported beam analysis """
    def __init__(self, span, loads):
        self.span = span
        self.loads = loads
        self.Ra = 0
        self.Rb = 0
        self.Mmax = 0
        self.Vmax = 0

    def reactions(self):
        """ Calculate the reactions to the beam """
        components = []  # list of moments about the Ra for each load
        w_loads = []  # list loads
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

    def force_diagram(self):
        """ Plot the shear force diagram for the beam """
        self.reactions()
        x = np.arange(0, self.span + 0.01, 0.01)  # intervals along the beam of the calculations
        shear = []  # list of the shear force at intervals
        bending_moment = []  # list of the bending moment at the intervals
        for n in x:
            shear_load = []  # list of the load shears (excluding reaction)
            bending_load = []  # list of the moments for the loads

            # Check whether the load is in play at the location of x
            for load in self.loads:
                if n > load[0] == load[1]:
                    shear_load.append(load[2])
                    bending_load.append(load[2] * (n - load[0]))
                elif load[1] != load[0] < n <= load[1]:
                    shear_load.append((n-load[0])*load[2])
                    udl_w = (n - load[0]) * load[2]
                    udl_la = (n - load[0]) / 2
                    bending_load.append(udl_la * udl_w)
                elif load[1] != load[0] < n > load[1]:
                    shear_load.append((load[1] - load[0])*load[2])
                    udl_w = (load[1] - load[0]) * load[2]
                    udl_la = n - (load[0] + (load[1] - load[0]) / 2)
                    bending_load.append(udl_la * udl_w)

            shear.append(sum(shear_load) - self.Ra)
            bending_moment.append(self.Ra * n - sum(bending_load))
        self.Vmax = max(max(shear), abs(min(shear)))
        self.Mmax = max(max(bending_moment), abs(min(bending_moment)))

        # Plot the bending moment and shear force diagram
        plt.style.use('seaborn-white')
        fig, ax = plt.subplots()
        ax.plot(x, shear, color='blue', label=f'Max Shear = {self.Vmax :.2f} kN')
        ax.plot(x, bending_moment, color='red', label=f'Max M = {self.Mmax :.2f} kNm')
        plt.axhline(0, color='black')
        ax.fill_between(x, 0, shear, color='blue', alpha=0.50)
        ax.fill_between(x, 0, bending_moment, color='red', alpha=0.50)
        plt.axvline(0, color='green', label=f'Ra = {self.Ra :.2f} kN')
        plt.axvline(self.span, color='yellow', label=f'Rb = {self.Rb :.2f} kN')
        ax.set_xlabel('Distance (m)')
        ax.set_ylabel('Shear Force/Bending Moment (kN/kNm)')
        ax.set_title('Shear Force & Bending Moment Diagram')
        plt.grid()
        plt.legend()
        plt.show()
