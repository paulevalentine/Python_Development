class Snow:
    """ Class to assess snow loading """
    """ Calculations in accordance with BS EN 1991-1-3 and NA """
    
    
    def __init__(self, pitch=30, pitch_type='duo', Z=4, Alt = 100):
        """Form and instance of the class"""
        
        self.pitch_type = pitch_type
        self.pitch = pitch
        self.Z = Z
        self.Alt = Alt
        
        
        # set the Ce value (exposure coeff NA 2.16)
        self.Ce = 1
        
        # set the Ct value (thermal coeff NA 2.17)
        self.Ct = 1
        
        # snow load shjape coefficients
        if self.pitch_type == 'mono':
            if self.pitch <= 30:
                self.mu = 0.80
            elif 30 < self.pitch <= 60:
                self.mu = 0.80 * (60 - self.pitch) / 30
            else:
                self.mu = 0.0
        elif self.pitch_type == 'duo':
            if self.pitch <= 15:
                self.mu = 0.80
            elif 15 < self.pitch <= 30:
                self.mu = 0.80 + 0.40*(self.pitch - 15) / 15
            elif 30 < self.pitch <= 60:
                self.mu = 1.2*(60 - self.pitch) / 30
            else:
                self.mu = 0.0
        else:
            self.mu = 0.80 # end conservative number
            
        # calculate the value of the snow load on the ground 
        self.sk = (0.15 + (0.1 * self.Z + 0.05) + ((self.Alt - 100) / 525))
        
        # calculate the roof snow load
        self.s = self.mu * self.Ce * self.Ct * self.sk
        
    
    def valley(self, h=2, b1=3, b2=3, b3=9):
        """ Calculate the snow shape coeff for a valley to Annex B"""
        mua = 2 * h / self.sk
        mub = 2 * b3 / (b1+b2)
        muc = 5
        self.mu_valley = mu = min(mua, mub, muc)
        self.s_valley = self.mu_valley * self.Ce * self.Ct * self.sk
        print(f'The valley snow shape coefficient = {self.mu_valley :.2f}')
        print(f'The peak valley snow load = {self.s_valley :.2f}kPa')
    
    
    def canopy(self, h=3, b1=1):
        """ Calculate the snow load on a canopy projection """
        mu = min(5, 2 * h / self.sk)
        self.mu_canopy = mu
        self.s_canopy = self.mu_canopy * self.Ce * self.Ct * self.sk
        print(f'The canopy snow shape coeffeicient = {self.mu_canopy :.2f}')
        print(f'The peak canopy snow load = {self.s_canopy :.2f}kPa')
    
        
    def basic_loading(self):
        print(f'Snow load on the ground = {self.sk :.2f}kPa')
        print(f'The snow shape coefficient = {self.mu :.2f}')
        print(f'The snow load = {self.s :.2f}kPa')