#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jan 20 09:44:47 2020

@author: georgemercieca
"""

import numpy as np
import pylab as pl

class Ball:
    
    Ball_count = 0
    
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
        Ball.Ball_count += 1
        self._coll = 'False'
        if Container == 'True':
            self._c = 1
            self._v = 0
            self._m = 'Infinite'
            self._p = pl.Circle([0, 0], 10 , ec='b', fill=False, ls='solid')
            Ball.Ball_count -= 1
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
        dr = self._r - other._r
        dr2 = np.dot(dr,dr)
        dv = self._v - other._v
        dv2 = np.dot(dv,dv)
        if other._c == 1:
            dR = self._R - other._R
        elif self._c == 1:
            dR = self._R - other._R
        else:
            dR = self._R + other._R
        dR2 = dR**2
        di = ((np.dot(dr,dv)**2)-dv2*dr2+dv2*dR2) 
        if di < 0:
            return (10**10)
        else:
            dt1 = ((-1*np.dot(dr,dv)+di**0.5)/dv2)
            dt2 = ((-1*np.dot(dr,dv)-di**0.5)/dv2)
            if dt2 <=(10**-5):
                if dt1 <=(10**-5):
                    return (10**10)
                else:
                    return dt1
            elif dt1 <=(10**-5):
                return dt2
            elif dt1<dt2:
                return dt1
            else:
                return dt2

            
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
        elif other._c == 1.:
            self._v = u1per - u1par
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
                print(u1par,u2par)
                print(v1par,v2par)
                raise Exception("KE decreased")
            
    def get_patch(self):
        return self._p

        
#%%

#%%

import random as ran

class Simulation:
    
    
    def __init__(self, Balls=1, Rc=10, Rb=1, Bm=1, v1=1):
        self._Rc = Rc
        self._con = Ball(R=self._Rc, Container='True')
        self._Rb = Rb
        self._n = Balls
        if isinstance(self._n,int) != True:
            raise Exception('An integer number of balls is required')
        self._n1 = Balls
        self._Bm = Bm
        self._v1 = v1
        self._b = []
        self._dt = 0
        self._T = 0
        self._collisions = 0
        while (self._n1-self._n) < Balls:
            theta = ran.uniform(0,np.pi*2)
            self._b.append(Ball(m=self._Bm, R=self._Rb, r=[ran.uniform((self._Rc-self._Rb)*-1,(self._Rc-self._Rb)),ran.uniform((self._Rc-self._Rb)*-1,(self._Rc-self._Rb))], v=[(self._v1*np.sin(theta)),(self._v1*np.cos(theta))]))
            print (self._b[-1]._r[0])
            print (self._b[-1]._r[1])
            if (self._b[-1]._r[0]**2+self._b[-1]._r[1]**2) > ((self._Rc-self._Rb)**2):
                del self._b[-1]
            for ball in self._b:
                if (self._n1-self._n) == len(self._b):
                    pass
                elif ball == self._b[(self._n1-self._n)]:
                    pass
                else:
                    if self._b[(self._n1-self._n)].distance(ball) <= (2*self._Rb+10**-2):                 
                        del self._b[(self._n1-self._n)]
            if len(self._b) == (self._n1-self._n+1): 
                self._n -= 1


                    
    def next_collision_info(self):
        self._n = self._n1
        collisiontime = (10**10)
        collisionobjects = []
        while self._n > 0:
            for i in range(len(self._b)):
                if (i) == (self._n1-self._n):
                    pass
                else:
                    a = (self._b[(self._n1-self._n)].time_to_collision(self._b[(i)]))
                    print (a)
                    if collisiontime > a:
                        collisiontime = a
                        collisionobjects = [(self._n1-self._n+1),i+1]
                    else:
                        pass
            b=(self._b[(self._n-1)].time_to_collision(self._con))
            if collisiontime > b:
                collisiontime = b
                collisionobjects = [(self._n1-self._n+1),'container']
            self._n -= 1
        print ('time is',collisiontime)
        print ('the colliding objects are',collisionobjects)
        return [collisiontime,collisionobjects[0],collisionobjects[1]]
    
    def next_collision(self):
        info = self.next_collision_info()
        dt = info[0]
        ball_1 = info[1]
        ball_2 = info[2]
        #if dt == 10**10:
         #   print (self.balls_for_next_collision())
          #  print ('a')
           # for ball in self._b:
            #    print ('pos =',ball._r)
             #   print ('velocity =',ball._v)
            #for ball in self._b:
             #  if ball.distance(self._con) >= (self._Rc-self._Rb):
              #     ball.collide(self._con)
        for ball in self._b:
                ball.move(dt)
                self._T += dt
                self._dt = dt
        if ball_2 == 'container':
            self._b[(ball_1-1)].collide(self._con)
            self._collisions += 1
        else:
            self._b[(ball_1-1)].collide(self._b[(ball_2-1)])
            self._collisions += 1
        
        #self._n = self._n1
        #while self._n > 0:
         #   for ball in self._b:
          #      if ball == self._b[(self._n1-self._n)]:
           #         pass
            #    elif self._b[(self._n1-self._n)].distance(ball) < (2*self._Rb):
             #       print ('e')
              #      dr = self._b[(self._n1-self._n)]._r-ball._r
               #     dr1 = dr/(np.dot(dr,dr)**0.5)
                #    print ('old dr',self._b[(self._n1-self._n)].distance(ball))
                #    new_dr = dr1*(2*self._Rb+0.001)
                #    new_r = (ball._r+new_dr)
                #    self.setballposition((self._n1-self._n+1),[new_r[0],new_r[1]])
                #    print ('new dr',self._b[(self._n1-self._n)].distance(ball))
                #    if self._b[(self._n1-self._n)] == 'True':
                #        self._b[(self._n1-self._n)] == 'False'
                #    else:
                #        self._b[(self._n1-self._n)].collide(ball)
                #        ball._coll = 'True'
                #        self._collisions += 1
               # elif self._b[(self._n1-self._n)].distance(ball) >= (2*self._Rb-10**-3):
                #        if self._b[(self._n1-self._n)] == 'True':
                 #           self._b[(self._n1-self._n)] == 'False'
                  ##      else:
                    #        self._b[(self._n1-self._n)].collide(ball)
                     #ball._coll = 'True'
                      #      self._collisions += 1
         #   if ((self._b[(self._n1-self._n)]._r[0]**2)+(self._b[(self._n1-self._n)]._r[1]**2))**0.5 > (self._Rc-self._Rb):
          #      dr = self._b[(self._n1-self._n)]._r
           #     print ('old r =',dr)
            #    dr1 = dr/(np.dot(dr,dr)**0.5)
             #   new_r = dr1*(self._Rc-self._Rb-0.001)
             #   print ('new r =',new_r)
             #   self.setballposition((self._n1-self._n+1),[new_r[0],new_r[1]])
             #   self._b[(self._n1-self._n)].collide(self._con)
             #   self._collisions += 1
            #elif ((self._b[(self._n1-self._n)]._r[0]**2)+(self._b[(self._n1-self._n)]._r[1]**2))**0.5 >= (self._Rc-self._Rb-10**-3):
            #        self._b[(self._n1-self._n)].collide(self._con)
             #       self._collisions += 1
            #self._n -= 1
            
            
    def setballspeed(self,number,v):
        if isinstance(v,list):
            self._b[(number-1)]._v=np.array([v[0],v[1]])
        else:
            raise Exception('velocity needs an x and y component and must be given in list form')
            
        
    def setballposition(self,number,r):
        if isinstance(r,list):
            r_array = np.array([r[0],r[1]])
            for ball in self._b:
                if ball == self._b[(number-1)]:
                    pass
                else:
                    dr = ball._r-r_array
                    if ((dr[0]**2)+(dr[1]**2))**0.5 < 2*self._Rb:
                        raise Exception('Cannot place a ball where another one is')
            if ((r_array[0]**2)+(r_array[1]**2))**0.5 > (self._Rc-self._Rb) :
                raise Exception('Cannot place ball outside of container')
            else:
                self._b[(number-1)]._r = r_array
        else:
            raise Exception('position needs an x and y component and must be given in list form')
    
    def run(self, num_frames, animate=False):
        if animate:
            f = pl.figure()
            ax = pl.axes(xlim=(-11,11), ylim=(-11,11))
            ax.add_artist(self._con.get_patch())
            for ball in self._b:
                ax.add_patch(ball._p)
        for frame in range(num_frames):
            self.next_collision()
            if animate:
                pl.pause(0.1)
                for ball in self._b:
                   ball._p.center = [ball._r[0],ball._r[1]]
        if animate:
            pl.show()
            
    def Get_Pressure(self):
        return Simulation.Container_Collisions/Simulation.Time

#%%
S1=Simulation(1,10,1,1)
S1.setballspeed(1,[10,0])
S1.setballposition(1,[-5,0])
S1.next_collision_info()
#%%
S1.run(1000,animate=True)
#%%
S2=Simulation(1,10,1,1,1)
#%%
S2.time_to_next_collision()
#%%
S2._collisions
#%%
S2.run(100,animate=True)
#%%
S2._b[0].distance(S2._con)
#%%
S2._b[0].time_to_collision(S2._con)
#%%
S2._b[0]._v
#%%
S3=Simulation(10,10,1,1,1)
#%%
S3.run(1000,animate=True)
#%%
S3._b[0].distance(S3._b[1])
#%%
S3.time_to_next_collision()
#%%
S3._b[1]._v
#%%
S3._b[1].collide(S3._con)
#%%
S3._collisions
#%%
test=[1,2,3]
for i in range(len(test)):
    print (i)