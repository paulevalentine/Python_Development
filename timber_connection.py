import pandas as pd
import math

class ScrewConnection:
    """ Class to model timber connections """
    """ Initialise with the general prarameters for the connection """
    """ Number of fixings is considered as an instance parameter """

    def __init__(self, diam, diamh, grade='C16',
                 load_duration='permanent', service_class=1, alpha=90):
        self.diam = diam
        self.diamh = diamh
        self.grade = grade
        self.load_duration = load_duration
        self.service_class = service_class
        self.alpha = alpha * math.pi / 180


        # Get the general timber properties from the data CSV file
        all_timber_materials = pd.read_csv('./data/timberProperties.csv',
                                           index_col=0)
        self.timber = all_timber_materials.loc[grade]

        # set the value of gamma M to the maximum - future work to make selection
        self.gamma_M = 1.3

        # set the kmod factor
        type='Solid'
        kmod_values = pd.read_csv('./data/kmod.csv', index_col=0)
        service_class_filter = kmod_values[kmod_values['service_class']
                                           == self.service_class]
        self.kmod =  service_class_filter.loc[type, self.load_duration]

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
        # todo - this needs to be modified to account for the angle of the
        # fixing to the grain
        a = self.alpha
        kd = min(1, self.diam / 8)

        f = (self.nef_axial(n) * self.faxk_screw(tpen)  * self.diam * tpen * kd /
                (1.2 * math.cos(a)**2 + math.sin(a)**2))
        return f 

    def screw_pullthrough(self, n=1, fheadk=0):
        if fheadk == 0:
            fheadk = self.fheadk_nail()

        return self.nef_axial(n) * fheadk * self.diamh**2 # nail fheadk used here 


    def screw_axial(self, tpen, n=1, fheadk=0):
        """ the min of withdrawl and pull through """
        """ calcualest the axial capacity of the screw """
        return min(self.screw_withdrawal(tpen, n), self.screw_pullthrough(n, fheadk)) * self.kmod / self.gamma_M


    """ This section deals with shear capacity of screws """

    def splitting(self, b=38, h=100, he=50):
        """ characeristic splitting capacity of the connection """
        F90Rk = 14 * b * math.sqrt(he / (1 - he/h))
        F90Rd = F90Rk * self.kmod / self.gamma_M
        return F90Rd 


    def fhk(self, drill='predrilled'):
        """ calculate the characteristic embedment strengths """
        if drill == 'predrilled':
            fhk = 0.082 * (1-0.01 * self.diam) * self.timber['pk']
        else:
            fhk = 0.082 * self.timber['pk'] * self.diam**(-0.30)
        return fhk 

    
    def myrk(self, fu=540):
        """ calculate the characteristic value for the yield moment """
        # only applicable for round nails / screws
        return 0.30 * fu * self.diam**2.6


    def Fvrk(self, t1=38, t2=38, drill='predrilled', fu=540, tpen=30):
        """ calculate the characteristic shear capacity of a fixing in single shear """
        m = self.myrk(fu)
        d = self.diam
        a1 = self.fhk(drill)
        a2 = self.fhk(drill)
        b = a1 / a2
        a3 = self.screw_axial(tpen, 1) / 4

        # Selection criteria from (8.6) 
        f1 = a1 * t1 * self.diam
        f2 = a2 * t2 * self.diam
        f3 = f1/(1+b)*(math.sqrt(b+2*b**2*(1+(t2/t1)+(t2/t1)**2)+b**3*(t2/t1)**2) - b*(1+(t2/t1))) + a3
        f4 = 1.05 * f1 / (2+b) * (math.sqrt(2*b*(1+b) + (4*b*(2+b)*m)/(a1*self.diam*t1**2)) - b) + a3
        f5 = 1.05 * f2 / (1+2*b) * (math.sqrt(2*b**2*(1+b) + (4*b*(1+2*b)*m / (a1 * self.diam * t2**2))) - b) + a3
        f6 = 1.15 * math.sqrt(2*b/(1+b)) * math.sqrt(2*m*a1*self.diam) + a3 
        answer = [f1, f2, f3, f4, f5, f6]
        return min(answer)


    def screw_lateral(self, t1=38, t2=38, drill='predrilled', fu=540, tpen=30, n=1, spacing='10d'):
        """ calculate the design lateral load resistance of a screw """
        # get the value of nef for teh connection
        nef = self.nef(spacing, drill, n)

        # get the charactoristic lateral capacity
        f = self.Fvrk(t1, t2, drill, fu, tpen)

        # calc the design value
        fd = nef * self.kmod * f / self.gamma_M
        return fd


    def unity_check(self, F, V, t1=38, t2=38, drill='predrilled', fu=540, tpen=30, n=1, spacing='10d'):
        """ calculate the (8,28) unit check for combined lateral and axial capacity """
        ax = self.screw_axial(tpen, n)
        vx = self.screw_lateral(t1, t2, drill, fu, tpen, n, spacing)
        uax = F/ax
        uvx = V/vx
        u = (F/ax)**2 + (V/vx)**2

        if uax < 1 and uvx < 1 and u < 1:
            status = 'The connectoin is adequate'
        else:
            status = 'FAIL'

        print(f'The design axial capacity of the connection = {vx :.2f}N')
        print(f'The design lateral capacity of the connection = {ax :.2f}N')
        print(f'The axial unity check = {uax :.2f}')
        print(f'The lateral unity check = {uvx :.2f}')
        print(f'The combined unity check = {u :.2f}')
        print(status)
