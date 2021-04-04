import pandas as pd
import matplotlib.pyplot as plt
import math

class TimberBeam:
    """Timber structural calculations"""
    """Must have the CSV timber propeties file to function"""
    """Must have the kmod data file"""
    
    def __init__(self, b, h, grade='C16', ksys=1, 
                 service_class=1, load_duration='permanent', ley=3000, lez=2000):
        """ Form an instance of the timber beam class """
        self.b = b
        self.h = h
        self.grade = grade
        self.kcrit = 1
        self.ksys = ksys
        self.service_class = service_class
        self.load_duration = load_duration
        self.ley= lex
        self.lez = lez
        
        
        # get all the timber materials and assign the grade passed when
        # forming the instance of the class
        all_timber_materials = pd.read_csv('timberProperties.csv', index_col=0)
        self.timber = all_timber_materials.loc[grade]
        
        # set the partial factor on material
        if self.timber['Type'] == 'Solid':
            self.partial_factor = 1.3
        elif self.timber['Type'] == 'Glulam':
            self.partial_factor = 1.25
        else:
            self.partial_factor = 1.20
        # set the kcr factor for shear to allow for splitting
        self.kcr = 0.67
        
        # set the kh value
        if self.h < 150:
            self.kh = min(1.3, (150/self.h)**0.20)
        else:
            self.kh = 1
        
        # set the kmod value
        type = self.timber['Type']
        kmod_values = pd.read_csv('kmod.csv', index_col=0)
        service_class_filter = kmod_values[kmod_values['service_class']
                                           == self.service_class]
        self.kmod =  service_class_filter.loc[type, self.load_duration]
        
        # calculate the design bending strength
        self.fmd = (self.kcrit * self.ksys * self.kh * self.kmod * 
                    self.timber['fmk']
                    / self.partial_factor)
        
        # calculate the geometric properties of the section
        self.A = self.b * self.h
        self.Zy = self.b * self.h**2 / 6
        self.Iy = self.b * self.h**3 / 12
        self.Iz = self.h * self.b**3 / 12
        self.ry = math.sqrt(self.Iy / self.A)
        self.rz = math.sqrt(self.Iz / self.A)
        
        # calculate the bending capacity of the section  
        self.Mcap = self.Zy * self.fmd
        
        # calculate the shear capacity of the section
        self.Vcap = (self.kmod * self.timber['fvk']
                     * self.A * self.ksys * self.kcr * (2/3) /
                     self.partial_factor)
        
        # properties for axial capacity
        self.beta_c = 0.20 # only solid sections considered at present
        lam_y = self.ley / self.ry
        lam_z =  self.lez / self.rz
        e = self.timber['E005']
        f = self.timber['fc0k']
        lam_rely = (lam_y / math.pi()) * math.sqrt(f / e)
        lam_relz = (lam_z / math.pi()) * math.sqrt(f / e)
        
        
    def print_capacities(self, M, V):
        """ Print the capacities for the timber beam """
        if self.Mcap*10**-6 >= M and self.Vcap*10**-3 >= V:
            uls_status = 'Pass'
        else:
            uls_status = 'Fail'
        fig, ax = plt.subplots()
        fig.set_size_inches(5,4)
        fig.suptitle(f'Beam status = {uls_status}')
        x_values = ['Moment Capacity', 'Shear Capacity']
        y_values = [self.Mcap*10**-6, self.Vcap*10**-3]
        ax.bar(x_values, y_values, color='grey')
        ax.set_xlabel('Force Effect')
        ax.set_ylabel('Force / Moment (kN/kNm)')
        plt.axhline(M, color='red', label=f'Applied Moment { M :.2f}kNm')
        plt.axhline(V, color='green', label=f'Applied Shear {V :.2f}kN')
        plt.legend()
        plt.grid()
        plt.show()
        