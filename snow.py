class Snow:
    """ Class to assess snow loading """
    """ Calculations in accordance with BS EN 1991-1-3 and NA """
    
    
    def __init__(self, pitch=30, pitch_type='mono', Z=3, Alt = 100):
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
        if self.pitch_type == 'mon':
            if self.pitch <= 30:
                self.mu = 0.80
            elif 30 < self.pitch <= 60:
                self.mu = 0.80 * (60 - self.pitch) / 30
            else:
                self.mu = 0
        elif self.pitch_type == 'duo':
            if self.pitch <= 15:
                self.mu = 0.80
            elif 15 < self.pitch <= 30:
                self.mu = 0.80 + 0.40*(self.pitch - 15) / 15
            elif 40 < self.pitch <= 60:
                self.mu = 1.2*(60 - self.pitch) / 30
            else:
                self.mu = 0
        else:
            self.mu = 0.80 # end conservative number
            
        # calculate the value of the snow load on the ground 
        self.sk = (0.15 + (0.1 * self.Z + 0.05) + ((self.Alt - 100) / 525))
        
        # calculate the roof snow load
        self.s = self.mu * self.Ce * self.Ct * self.sk
    
        
    def values(self):
        print(f'The snow load = {self.s :.2f}kPa')