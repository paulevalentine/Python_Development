class Wind:
    """ module to calculate wind loading """
    def __initi__(self, Cdir, Cs, Cp, A, vmap, z):
        """ initiate and instance of wind """
        self.Cdir = Cdir
        self.Cs = Cs 
        self.Cp = Cp
        self.A = A 
        self.vmap = vmap
        self.z = z

        # calculate the altitude factor
        if z <= 10:
            self.Ca = 1 + 0.001 * self.A
        else:
            self.Ca = 1 + 0.001 * self.A * (10/self.z)**0.20

        self.vb = self.Cdir * self.Cs * self.Cp * self.Ca * vmap
        self.qb = self.vp**2 * 0.613 * 10**-3

    def qp(self, Cez, CeT):
        return self.qp * Cez * ceT
