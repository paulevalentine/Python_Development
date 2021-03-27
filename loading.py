import matplotlib.pyplot as plt


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
        'Roof': 0.75,
        'Light Access': 0.25
    }

    @staticmethod
    def print_element_loads():
        """ Print out the element loads as a bar chart """
        perm_names = [*Load.perm_loads]
        var_names = [*Load.var_loads]
        perm_values = [*Load.perm_loads.values()]
        var_values = [*Load.var_loads.values()]
        plt.style.use('seaborn-white')
        fig, ax = plt.subplots()
        ax.bar(perm_names, perm_values, label='Permanent Unit Loads')
        ax.bar(var_names, var_values, label='Variable Unit Loads')
        ax.set_xlabel('Name of Element')
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
    def elements(data):
        """ Sum the loads from their keys """
        load = []
        for name in data:
            load.append(Load.perm_loads[name])
        return sum(load)

    def __init__(self, elements):
        self.elements = elements

    def sls_load(self, loads):
        " Calculate the loading on an element "
