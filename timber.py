import pandas as pd
import matplotlib.pyplot as plt
import math

class TimberBeam:
    """Timber structural calculations"""
    """Must have the CSV timber propeties file to function"""
    """Must have the kmod data file"""
    
    def __init__(self, b, h, grade='C16', ksys=1, 
                 service_class=1, load_duration='permanent', ley=3000, lez=3000):
        """ Form an instance of the timber beam class """
        self.b = b
        self.h = h
        self.grade = grade
        self.kcrit = 1
        self.ksys = ksys
        self.service_class = service_class
        self.load_duration = load_duration
        self.ley= ley
        self.lez = lez
        
        
        # get all the timber materials and assign the grade passed when
        # forming the instance of the class
        all_timber_materials = pd.read_csv('./data/timberProperties.csv', index_col=0)
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
        kmod_values = pd.read_csv('./data/kmod.csv', index_col=0)
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
        
        # calculate the shear strength of the section
        self.fvd = (self.kmod * self.timber['fvk']
                     * self.ksys / self.partial_factor)
        
        # calculate the design compressive strength parallel to the grain
        self.fc0d = self.ksys * self.kmod * self.timber['fc0k'] / self.partial_factor
        
        
        def k_i(lam_rel, beta_c):
            """ Calculates the ky factor from BS EN 1995-1-1 """
            k = 0.50*(1 + beta_c * (lam_rel - 0.30) + lam_rel**2)
            return k
        
        
        def k_ci(k_i, lam_rel):
            """ Calculates the strength reduction factor for slenderness """
            k = 1 / (k_i + math.sqrt(k_i**2 - lam_rel**2))
            return k
            

        self.beta_c = 0.20 # only solid sections considered at present
        lam_y = self.ley / self.ry
        lam_z =  self.lez / self.rz
        e = self.timber['E005']
        f = self.timber['fc0k']
        lam_rely = (lam_y / math.pi * math.sqrt(f / e))
        lam_relz = (lam_z / math.pi * math.sqrt(f / e))
        k_y = k_i(lam_rely, self.beta_c)
        k_z = k_i(lam_relz, self.beta_c)
        self.k_cy = k_ci(k_y, lam_rely)
        self.k_cz = k_ci(k_z, lam_relz)
        
        # calculate the design compressive strength paralle to the grain
        # with allowance for buckling
        self.fc0dy = self.k_cy * self.fc0d
        self.fc0dz = self.k_cz * self.fc0d
        
    def capacity_check(self, M, V, F):
        """ Compare the design strength to the applied stress """
        # calculate the applied stresses
        smd = M * 10**6 / self.Zy
        td = V * 10**3 / (self.A * self.kcr) * (3/2)
        sc0d = F * 10**3 / self.A
        
        # unity checks
        km = 0.70 # for rectangular timber sections
        u1 = (smd/(self.fmd * self.kcrit))**2 + (sc0d / self.fc0dz)
        u2 = smd/(self.fmd * self.kcrit) + (sc0d / self.fc0dy)
        u3 = smd/(self.fmd * self.kcrit) * km + (sc0d / self.fc0dz)
        
        # check the status of the beam
        if u1 <= 1 and u2 <= 1 and u3 <=1:
            uls_status = 'PASS'
        else:
            uls_status = 'FAIL'
        
        # plot results
        # print('Material Properties:\n',self.timber)
        fig, (ax1, ax2) = plt.subplots(1,2)
        fig.set_size_inches(11,4)
        fig.suptitle(f'STATUS = {uls_status}')
        x_values = ['Bending', 'Shear', 'y Comp',
                    'z Comp']
        y_values = [self.fmd, self.fvd, self.fc0dy, self.fc0dz]
        colour=['red', 'green', 'orange', 'orange']
        ax1.bar(x_values, y_values, color=colour)
        ax1.set_xlabel('Design Capacities')
        ax1.set_ylabel('Stress MPa')
        ax2.bar(['U1', 'U2', 'U3'], [u1, u2, u3])
        ax1.axhline(smd, color='red', label=f'Applied bending stress { smd :.2f}MPa')
        ax1.axhline(td, color='green', label=f'Applied shear stress {td :.2f}MPa')
        ax1.axhline(sc0d, color='orange', label=f'Applied comp stress {sc0d :.2f}MPa')
        ax1.legend()
        ax1.set_title('Action Stresses')
        ax2.set_title('ULS Unity Ratio Checks')
        ax1.grid()
        ax2.grid()
        plt.show()
        