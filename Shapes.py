#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jan 14 16:21:18 2020

@author: georgemercieca
"""

import numpy as np

class Shape:
    """
    Class for different shapes with
    colours that can be modified
    """
    Red_count = 0
    
    def __init__(self, colour='Blue'):
        self._c = colour
        if self._c == 'Red':
            Shape.Red_count += 1
            
    def set(self, new_colour):
        if self._c == 'Red':
            Shape.Red_count -=1
        self._c = new_colour
        if self._c == 'Red':
            Shape.Red_count += 1
        return self
    
    def colour(self):
        return self._c
    
    
#%%
s = Shape()
s.set('Red')
s.colour()
#%%
s.set('Red').set('Yellow').colour()
#%%
import numpy as np

class Square(Shape):
    """
    Derived Shape class specified 
    for a square
    """
    
    def __init__(self, length=1):
        self._l = length
        Shape.__init__(self, colour='Blue')
    
    def setl(self, new_l):
        self._l = new_l
    
    def area(self):
        return self._l**2

class Triangle(Shape):
    """
    Derived Shape class specified 
    for a triangle
    """
    
    def __init__(self, base=1, height=1):
        self._b = base
        self._h = height
        Shape.__init__(self, colour='Blue')
        
    def setb(self, new_b):
        self._b = new_b
        
    def seth(self, new_h):
        self._h = new_h
        
    def area(self):
        return 0.5*self._b*self._h
    
class Circle(Shape):
    """
    Derived Shape class specified 
    for a triangle
    """
    
    def __init__(self, radius=1):
        self._r = radius
        Shape.__init__(self, colour='Blue')
        
    def setr(self, new_r):
        self._r = new_r
        
    def area(self):
        return np.pi*(self._r**2)
    
    def circumference(self):
        return np.pi*self._r*2
    
#%%
a = Square()
a.set('Red')
a.colour()
#%%
a.setl(2)
a.area()
#%%
b = Triangle()
b.set('Yellow')
b.colour()  
#%%
b.setb(3)
b.seth(5)
b.area()
#%%
c = Circle()
c.set('Green')
c.colour()
#%%
c.setr(2)
c.area()
#%%
c.circumference()
#%%
isinstance(c,Circle)
isinstance(c,Shape)
#%%
isinstance('hello',Shape)
isinstance(10,Shape)
#%%
if isinstance('hello', Shape) != True:
    print ('hello is not a shape')
#%%
def Red(a):
    if not isinstance(a,Shape):
        raise TypeError("a needs to be an instance of Shape")
    a._c='Red'

Red(c)
c.colour()
#%%
Shape.Red_count
#%%
b.set('Red')
Shape.Red_count
#%%
b.set('Yellow')
Shape.Red_count