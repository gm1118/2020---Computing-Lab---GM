
import numpy as np
import pylab as pl

class Ball:
    """
    A class which creates 2D circles with a mass, size, 
    position and velocity that can move forward in time 
    and collide with each other. A ball can also be 
    designated as a container, affecting its interactions
    with other balls.
    """
    
    def __init__(self, m=1, R=1, r=[0.0,0.0], v=[0.0,0.0], Container='False'):
        self._m = m
        if self._m <= 0:
            raise Exception("Ball has negative or 0 mass")
        self._R = R
        if self._R <= 0:
            raise Exception("Balls has negative or 0 radius")
        self._r = np.array([ r[0], r[1]])
        self._v = np.array([ v[0], v[1]])
        self._p = pl.Circle([self._r[0],self._r[1]], self._R, fc='r')
        self._mom = 0
        if Container == 'True':
            self._c = 1 
            self._v = [0,0]
            self._m = 'Infinite'
            self._p = pl.Circle([0, 0], R , ec='b', fill=False, ls='solid')
        else:
            self._c = 0

    def pos(self):
        return self._r
    
    def vel(self):
        return self._v
    
    def move(self, dt):
        r2 = self._r + self._v*dt 
        self._r = r2
        
    def distance (self, other):
        dr = self._r - other._r
        return (((dr[0]**2)+(dr[1]**2))**0.5)
        
    def time_to_collision(self, other):
        dr = (self._r - other._r)
        dr2 = np.dot(dr,dr)
        dv = (self._v - other._v)
        dv2 = np.dot(dv,dv)
        if other._c == 1:
            c=1
            dR = other._R - self._R
        elif self._c == 1:
            c=1
            dR = self._R - other._R
        else:
            c=0
            dR = self._R + other._R
        dR2 = dR**2
        di = ((np.dot(dr,dv)**2)-(dv2*dr2)+(dv2*dR2)) 
        if di < 0:
            return (10**10) 
        else:
            dt1 = ((-1*np.dot(dr,dv)+di**0.5)/dv2)
            dt2 = ((-1*np.dot(dr,dv)-di**0.5)/dv2)
            if c==1:
                return (dt1-0.0001) 
            elif dt2 <=(0.00001):
                if dt1 <=(0.00001):
                    return 10**10
                else:
                    return (dt1-(0.0001))
            elif dt1 <=(0.00001):
                return (dt2-(0.0001))
            elif dt1<dt2:
                return (dt1-(0.0001))
            else:
                return (dt2-(0.0001))

            
    def collide(self,other):
        u1 = self._v
        u2 = other._v
        dr = self._r - other._r
        dr1 = dr/(np.dot(dr,dr)**0.5)
        u1par = dr1*(np.dot(self._v,dr1))
        u2par = dr1*(np.dot(other._v,dr1))
        u1per = self._v - u1par
        u2per = other._v - u2par
        if self._c == 1:
            other._v = u2per - u2par
            other._mom = 2*other._m*(np.dot(u2par,u2par)**0.5)
        elif other._c == 1:
            self._v = u1per - u1par
            self._mom = 2*self._m*(np.dot(u1par,u1par)**0.5)
        else:
            v1par = (u1par*(self._m-other._m)+2*other._m*u2par)/(self._m+other._m)
            v2par = ((u1par*2*self._m + u2par*(other._m-self._m))/(self._m+other._m))
            self._v = u1per + v1par
            other._v = u2per + v2par
            if (self._m*(np.dot(u1,u1))+other._m*(np.dot(u2,u2))) > ((self._m*(np.dot(self._v,self._v))+other._m*(np.dot(other._v,other._v)))+10**-5):
                print(u1,u2)
                print(self._v,other._v)
                raise Exception("KE increased")
            elif (self._m*(np.dot(u1,u1))+other._m*(np.dot(u2,u2))) < ((self._m*(np.dot(self._v,self._v))+other._m*(np.dot(other._v,other._v)))-10**-5):
                print(u1,u2)
                print(self._v,other._v)
                raise Exception("KE decreased")
            elif (self._m*np.dot(u1,u1)+other._m*np.dot(u2,u2)) > (self._m*np.dot(self._v,self._v)+(other._m*np.dot(other._v,other._v))+10**-5):
                print(u1,u2)
                print(self._v,other._v)
                raise Exception("Momentum increased")
            elif (self._m*np.dot(u1,u1)+other._m*np.dot(u2,u2)) < (self._m*np.dot(self._v,self._v)+(other._m*np.dot(other._v,other._v))-10**-5):
                print(u1,u2)
                print(self._v,other._v)
                raise Exception("Momentum decreased") # checks to ensure KE and Momentum are conserved in collisions
                
    def get_patch(self):
        return self._p
