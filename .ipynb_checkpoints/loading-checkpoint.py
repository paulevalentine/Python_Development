import matplotlib.pyplot as plt
import numpy as np


class Load:
    """ Loading on an element """
    # Set the general permanent loading:
    perm_loads = {
        'Decking': 0.10,
        'Joists': 0.20,
        'Ceiling': 0.20,
        'Block': 1.50,
        'Brick': 2.15,
        'Plaster': 0.20,
        'Tiles': 0.55,
        'Rafters': 0.15,
        'Felt': 0.05,
        'Battens': 0.05
    }

    var_loads = {
        'Floor': 1.50,
        'Snow': 0.60,
        'Roof': 0.60,
        'Light Access': 0.25
    }

    @staticmethod
    def print_component_loads():
        """ Print out the component loads above as a bar chart """
        perm_names = [*Load.perm_loads]
        var_names = [*Load.var_loads]
        perm_values = [*Load.perm_loads.values()]
        var_values = [*Load.var_loads.values()]
        plt.style.use('seaborn-white')
        fig, ax = plt.subplots()
        fig.set_size_inches(11,4)
        ax.bar(perm_names, perm_values, label='Permanent Unit Loads')
        ax.bar(var_names, var_values, label='Variable Unit Loads')
        ax.set_xlabel('Name of Component')
        ax.set_ylabel('Unit Load (kPa)')
        ax.set_title('Unit Loads Used')
        for i, v in enumerate(perm_values):
            plt.text(i - 0.25, v+0.05, str(v))
        for i, v in enumerate(var_values):
            plt.text(i + len(perm_values) - 0.25, v+0.05, str(v))
        plt.legend()
        plt.grid()
        plt.xticks(rotation=90)
        plt.show()



    @staticmethod
    def sum_components(data):
        """ Sum the loads from their keys for permanent loading """
        load = []
        for name in data:
            load.append(Load.perm_loads[name])
        return sum(load)
    
    @staticmethod
    def plot_elements(data):
        """Plot the element loading for the project"""
        y_value = []
        x_value = []
        for i, n in enumerate(data):
            y_value.append(data[i][0])
            x_value.append(data[i][1])
        fig, ax = plt.subplots()
        fig.set_size_inches(11, 4)
        ax.bar(x_value, y_value)
        ax.set_xlabel('Element')
        ax.set_ylabel('Area Load (kPa)')
        ax.set_title('Loads relating to elements')
        plt.grid()
        plt.show()
        

    
    def __init__(self, element, ref='Not Known'):
        """ Calculate the line loads for an element """
        self.element = element
        self.ref = ref
        self.w_perm = []
        self.w_var = []
        for n in self.element:
            self.w_perm.append(n[0] * n[2])
            self.w_var.append(n[1] * n[2])
            
        self.perm_load = sum(self.w_perm)
        self.var_load = sum(self.w_var)
        self.sls_load = self.perm_load + self.var_load
        self.uls_load = 1.35 * self.perm_load + 1.5 * self.var_load
        self.gammaf = self.uls_load / self.sls_load
 

    def plot_load_components(self):
        """Plot the components of a load on an element"""
        support = np.array([])
        perm = np.array([])
        perm_value =np.array([])
        var = np.array([])
        var_value = np.array([])
        names = []
        for n in range(len(self.element)):
            support = np.append(support, self.element[n][2])
            perm = np.append(perm, self.element[n][0])
            perm_value = np.append(perm_value, self.element[n][0] *
                                   self.element[n][2])
            var = np.append(var, self.element[n][1])
            var_value = np.append(var_value, self.element[n][1] * self.element[n][2])
            names.append(self.element[n][3])
        
        # Plot the loading data
        plt.style.use('seaborn-white')
        fig,(ax1, ax2) = plt.subplots(1,2)
        fig.suptitle(self.ref)
        fig.set_size_inches(11,4)
        ax1.scatter(support, perm, s=perm_value * 100, label='Permanent Loads',
                    color='green', alpha=0.50)
        ax1.scatter(support, var, s=var_value * 100, label='Variable Loads',
                    color='red', alpha = 0.50)
        for i, v in enumerate(names):
            ax1.text(support[i], perm[i], v)
        for i, v in enumerate(names):
            ax1.text(support[i], var[i], v)
        ax1.set_xlabel('Support Length (m)')
        ax1.set_ylabel('Load magnitude (kPa)')
        ax1.set_title('Bubble plot of loading on element (kN/m)')
        ax1.set_ylim([0,max(max(perm),max(var))+2])
        ax1.set_xlim([min(support)-1, max(support)+1])
        ax1.grid()
        ax1.legend()
        ax2.bar(names, perm)
        ax2.bar(names, var, bottom=perm)
        ax2.set_title('Unit Loads Used')
        ax2.set_xlabel('Element')
        ax2.set_ylabel('Unit Load (kPa)')
        ax2.grid()
        plt.show()
        
        # Plot the loading
        fig, (ax1, ax2, ax3) = plt.subplots(1,3)
        fig.suptitle(self.ref)
        fig.set_size_inches(11,4)
        ax1.bar(names, perm_value, color='green')
        ax1.grid()
        ax1.set_title('Permanent Loads')
        ax1.set_xlabel('Element')
        ax1.set_ylabel('Loading (kN/m)')
        ax2.bar(names, var_value, color='red')
        ax2.grid()
        ax2.set_title('Variable Loads')
        ax2.set_xlabel('Element')
        ax2.set_ylabel('Loading (kN/m)')
        loading = [self.sls_load, self.uls_load]
        ax3.bar(['SLS', 'ULS'], loading)
        for i, v in enumerate(loading):
            ax3.text(i, loading[i], f'{v:.2f}')
        ax3.grid()
        ax3.set_title('Total Loading')
        ax3.set_xlabel('Limit State Condition')
        ax3.set_ylabel('Load (kN/m)')
        plt.show()

        
