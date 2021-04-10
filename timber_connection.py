import pandas as pd
import math

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

        self.gamma_M = 1.3

        # set the kmod factor
        type='Solid'
        kmod_values = pd.read_csv('./data/kmod.csv', index_col=0)
        service_class_filter = kmod_values[kmod_values['service_class']
                                           == self.service_class]
        self.kmod =  service_class_filter.loc[type, self.load_duration]

    """ The below is taken from the Eurocode """
    """ This section deals with axial withdrawal and pull through """

    def faxk_nail(self):
        """calculate the pointside withdrawal strength for a screw"""
        faxk = 20*10**-6 * self.timber['pk']**2
        return faxk

    def faxk_screw(self, tpen):
        """Calculate the pointside withdrawal strength of a screw"""
        faxk = (0.52 * self.diam**(-0.50) * tpen**(-0.10) *
        self.timber['pk']**0.80)
        return faxk


    def fheadk_nail(self):
        """calcaulte the headside pull through strength for a nail"""
        fheadk = 70*10**-6 * self.timber['pk']**2
        return fheadk


    def nail_withdrawal(self, tpen, t=38, number=1):
        """calculate the withdrawal load of a smooth nail"""
        a = self.faxk_nail() * self.diam * tpen
        b = (self.faxk_nail() * self.diam * t + self.fheadk_nail() 
                * self.diamh**2)
        F = min(a,b)
        return F * self.kmod * number / self.gamma_M


    def nef(self, spacing='10d', drill='predrilled', n=1):
        """calculate the effective fixing number factor"""
        df = pd.read_csv('./data/kef.csv')
        kef = df[df['spacing']==spacing].loc[:,drill].values[0]
        nef = n**kef  
        return nef


    def nef_axial(Self, n=1):
        """ effective fixing number for axially loaded fixings """
        return n**0.90


    def screw_withdrawal(self, tpen, n=1):
        """calculate the withdrawal capacity of a screw"""
        # note that the force angle is not considere here
        kd = min(1, self.diam / 8)
        f = (self.nef_axial(n) * self.faxk_screw(tpen) * self.diam *
                tpen * kd / 1.2)
        return f

    def screw_pullthrough(self, n=1):
        return self.nef_axial(n) * self.fheadk_nail() * self.diamh**2 # nail fheadk used here 


    def screw_axial(self, tpen, n=1):
        """ the min of withdrawl and pull through """
        """ calcualest the axial capacity of the screw """
        return min(self.screw_withdrawal(tpen, n), self.screw_pullthrough(n)) * self.kmod / self.gamma_M


    """ This section deals with shear capacity of screws """

    def splitting(b=38, h=100, he=50):
        """ characeristic splitting capacity of the connection """
        return 14 * b * math.sqrt(he / (1 - he/h))


    def fhk(drill='predrilled'):
        """ calculate the characteristic embedment strengths """
        if drill == 'predrilled':
            fhk = 0.082 * (1-0.01 * self.diam) self.timber['pk']
        else:
            fhk = 0.082 * self.timber['pk'] self.diam**(-0.30)
        return fhk 

    
    def myrk(fu=400):
        """ calculate the characteristic value for the yield moment """
        # only applicable for round nails / screws
        return 0.30 * fu * self.d**2.6


    def Fvrk(t1=38, t2=38, drill='predrilled', fu=400, tpen=30):
        """ calculate the characteristic shear capacity of a fixing in single shear """
        f1 = fhk(drill)
        f2 = fhk(drill)
        b = f1 / f2
        m = myrk(fu)
        d = self.diam

        a1 = f1*t1*d
        a2 = f2*t2*d
        c = screw_axial(n=1, tpen)/4

        f3 = f1/(1+b)
        """ THIS IS NOT FINISHED """
