#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jan 13 11:37:48 2020

@author: georgemercieca
"""
import numpy as np

class FourVector:
    """
    Class for a Fourvector containing a
    timelike component and 3 spacelike
    ones within an array
    """
    def __init__(self, ct=0.0, r=[0.0,0.0,0.0]):
        self._rl=r
        if  len(self._rl)>3:
            raise Exception("FourVector parameter r has incorrect size")
        if  len(self._rl)<3:
            raise Exception("FourVector parameter r has incorrect size")
        self._r = np.array([ r[0], r[1], r[2]])
        self._ct=ct
        self._a = [self._ct,self._r]
        
    def __repr__(self):
        return "FourVector(ct=%g,r=array(%s)" % (self._ct, self._r)
    
    def __str__(self):
        return "(%g, %g, %g, %g)" % (self._ct, self._r[0], self._r[1], self._r[2])
   
    def ct(self):
        return self._ct
    
    def r(self):
        return self._r
    
    def setr(self, new_r):
        self._r = np.array([ new_r[0], new_r[1], new_r[2]])
    
    def setct(self, new_ct):
        self._ct = new_ct
        
    def copy(self):
        return FourVector(self._ct, self._rl)
    
    def __add__(self, other):
        return FourVector(self._ct + other._ct, [self._r[0]+other._r[0],self._r[1]+other._r[1],self._r[2]+other._r[2]])
    
    def __iadd__(self, other):
        self._ct += other._ct
        self._r[0] += other._r[0]
        self._r[1] += other._r[1]
        self._r[2] += other._r[2]
        self._a = [self._ct,self._r]
        return self
    
    def __sub__(self, other):
        return FourVector(self._ct - other._ct, [self._r[0]-other._r[0],self._r[1]-other._r[1],self._r[2]-other._r[2]])
    
    def __isub__(self, other):
        self._ct -= other._ct
        self._r[0] -= other._r[0]
        self._r[1] -= other._r[1]
        self._r[2] -= other._r[2]
        self._a = [self._ct,self._r]
        return self
    
    def inner(self, other):
        return (self._ct*other._ct)-self._r[0]*other._r[0]-self._r[1]*other._r[1]-self._r[2]*other._r[2]
    
    def magsquare(self):
        return self.inner(self)
    
    def boost(self, beta):
        gamma = (1-beta**2)**(-0.5)
        return FourVector((gamma*self._ct-gamma*beta*self._r[2]), [self._r[0], self._r[1],(gamma*self._r[2]-gamma*beta*self._ct) ])
            
#%%
P0=FourVector()
P0._a
#%%
v = FourVector(ct=99, r=[1.0, 2.0, 3.0])
print (v)
#%%
v = FourVector(ct=99, r=[1.0, 2.0, 3.0])
v
#%%
v1 = FourVector(ct=100, r=[1,1,1])
v1
#%%
v2=v1.copy()
v2
#%%
v2.setr(new_r=[1,2,3])
v2
#%%
v3 = v1-v2
v3
#%%
v3 -= v1
v3
#%%
v1.inner(v2)
#%%
v1.magsquare()
#%%
v4=v1.boost(0.5)
v4
#%%
v4.magsquare()
#%%
v5 = FourVector(ct=99, r=[1.0, 2.0, 3.0, 4.0])
#%%
