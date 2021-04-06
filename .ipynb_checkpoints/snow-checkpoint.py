class Snow:
    """ Class to assess snow loading """
    """ Calculations in accordance with BS EN 1991-1-3 and NA """
    
    
    def __init__(self, pitch=30, pitch_type='mono', sk=0.50):
        """Form and instance of the class"""
        
        self.pitch_type = pitch_type
        self.pitch = pitch
        
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
                self.mu = 0.80 + 0.40*(1.2 - 15) / 15
            elif 40 < self.pitch <= 60:
                self.mu = 1.2*(60 - self.pitch) / 30
            else:
                self.mu = 0
        else:
            self.mu = 0.80 # end conservative number
            
        self.s = self.mu * self.Ce * self.Ct
        
    def values(self):
        print(f'The snow load = {self.s :.2f}kPa')