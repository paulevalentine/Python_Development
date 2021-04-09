import pandas as pd

class ScrewConnection:
    """ Class to model timber connections """
    
    def __init__(self, diam, diamh, grade='C16', 
                 load_duration='permanent', service_class=1):
        self.diam = diam
        self.diamh = diamh
        self.grade = grade
        self.load_duration = load_duration
        self.service_class = service_class
        
        
        # Get the general timber properties
        all_timber_materials = pd.read_csv('./data/timberProperties.csv',
                                           index_col=0)
        self.timber = all_timber_materials.loc[grade]
        
        
        # get the withdrawal load data (extract from timber manual)
        self.withdrawal_data = pd.read_csv('./data/nailwithdraw.csv', 
                                           index_col=0)
        
        # select the specific withdrawal characteristic resistance
        self.Rk = self.withdrawal_data.loc[self.diam, self.grade]
        
        # set the partial factor
        self.gamma_M = 1.3
        
        # set the kmod factor
        type='Solid'
        kmod_values = pd.read_csv('./data/kmod.csv', index_col=0)
        service_class_filter = kmod_values[kmod_values['service_class']
                                           == self.service_class]
        self.kmod =  service_class_filter.loc[type, self.load_duration]
    
    """ The below is taken from the Eurocode """
    
    def faxk(self):
        """calculate the pointside withdrawal strength"""
        faxk = 20*10**-6 * self.timber['pk']**2
        return faxk
    
    
    def fheadk(self):
        """calcaulte the headside pull through strength"""
        fheadk = 70*10**-6 * self.timber['pk']**2
        return fheadk
    
    
    def screw_withdrawal(self, tpen, t=38, number=1):
        """calculate the withdrawal load of a smooth nail"""
        a = self.faxk() * self.diam * tpen
        b = self.faxk() * self.diam * t + self.fheadk() * self.diamh**2
        F = min(a,b)
        return 4 * F * self.kmod * number / self.gamma_M
    
    """ ************************************************* """
    

    """ The below are taken from the timber designer manual """
    
    def withdrawal_nail(self, tpen=30, number=1):
        """calculate the withdrawal load of nails"""
        return tpen * number * self.kmod * self.Rk / self.gamma_M
    def withdrawal_screw(self, tpen=30, number=1):
        """calculate the withdrawal load of screws"""
        return 4 * tpen * number * self.kmod * self.Rk / self.gamma_M
    
    def nef(self, spacing='5d', number=2):
        """calculate the effective number of screws"""
        pass
    
    """ *************************************************** """

        
        
        
