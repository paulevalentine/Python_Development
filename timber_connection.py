import pandas as pd

class ScrewConnection:
    """ Class to model timber connections """
    
    def __init__(self, diam, tpen, grade='C16', 
                 load_duration='permanent', service_class=1):
        self.diam = diam
        self.tpen = tpen
        self.grade = grade
        
        self.withdrawal_data = pd.read_csv('./data/nailwithdraw.csv', index_col=0)
        
        # select the specific withdrawal characteristic resistance
        self.Rk = self.withdrawal_data.loc[self.diam, self.grade]
        
        # set the partial factor
        self.gamma_M = 1.3
        
        # set the kmod factor
        self.kmod = pd.read_csv('./data/kmod.csv', index_col=0)
        
        