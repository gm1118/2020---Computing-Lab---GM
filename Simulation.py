from GM1118_Code import Ball as B
import numpy as np
import pylab as pl
import random as ran
Kb = 1.38064852*(10**-23)

class Simulation:
    """
    A class containing a set amount of identical balls 
    within a single container ball. It is able to move
    its entire system forward in time to subsequent 
    collisions while simultaneously animating it.
    If its balls are considered to be gas particles
    it can be used to model a thermodynamic system
    and obtain the physical data of such a system.
    """
    
    def __init__(self, Balls=20, Rc=10, Rb=1, Bm=1, v1=1):
        self._Rc = Rc
        self._con = B.Ball(R=self._Rc, Container='True')
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
        self._momentumtransferred = 0
        while (self._n1-self._n) < Balls:
            theta = ran.uniform(0,np.pi*2)
            self._b.append(B.Ball(m=self._Bm, R=self._Rb, r=[ran.uniform((self._Rc-self._Rb)*-1,(self._Rc-self._Rb)),ran.uniform((self._Rc-self._Rb)*-1,(self._Rc-self._Rb))], v=[(self._v1*np.sin(theta)),(self._v1*np.cos(theta))]))
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
                    if collisiontime > a > 0.00001:
                        collisiontime = a
                        collisionobjects = [(self._n1-self._n+1),i+1]
                    else:
                        pass
            b=(self._b[(self._n1-self._n)].time_to_collision(self._con))
            if collisiontime > b > 0.00001:
                collisiontime = b
                collisionobjects = [(self._n1-self._n+1),'container']
            self._n -= 1
        return [collisiontime,collisionobjects[0],collisionobjects[1]]
    
    def time_to_collision(self):
        a = self.next_collision_info()
        return a[0]
    
    def balls_for_next_collision(self):
        a = self.next_collision_info()
        return [a[1],a[2]]
    
    def next_collision(self):
        info = self.next_collision_info()
        dt = info[0]
        ball_1 = info[1]
        ball_2 = info[2]
        for ball in self._b:
                ball.move(dt)
        self._T += dt
        self._dt = dt
        if ball_2 == 'container':
            self._b[(ball_1-1)].collide(self._con)
            dr = self._b[(ball_1-1)]._r
            dr1 = dr/(np.dot(dr,dr)**0.5)
            new_r = dr1*(self._Rc-self._Rb-0.00001)
            self.setballposition((ball_1),[new_r[0],new_r[1]])
            self._momentumtransferred += self._b[(ball_1-1)]._mom
        else:
            self._b[(ball_1-1)].collide(self._b[(ball_2-1)])
            
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
    
    def run(self, num_collisions, animate=False):
        if animate:
            pl.figure()
            ax = pl.axes(xlim=(-self._Rc,self._Rc), ylim=(-self._Rc,self._Rc))
            ax.add_artist(self._con.get_patch())
            for ball in self._b:
                ax.add_patch(ball._p)
        for collision in range(num_collisions):
            self.next_collision()
            if animate:
                pl.pause(0.1)
                for ball in self._b:
                   ball._p.center = [ball._r[0],ball._r[1]]
        if animate:
            pl.show()
            
    def Get_Pressure(self):
        return self._momentumtransferred/(self._T*2*np.pi*self._Rc)
    
    def Get_Temp(self):
        KE = 0
        for ball in self._b:
            KE += 0.5*ball._m*(np.dot(ball._v,ball._v))
        return (KE)/(Kb*self._n1)
    
    def Ideal_Gas_test_initial(self):
        return self.Get_Pressure()*(np.pi*(self._Rc)**2)-(self._n1*Kb*self.Get_Temp())

    def Ideal_Gas_test_improved(self):
        return self.Get_Pressure()*(np.pi*(self._Rc)**2-self._n1*np.pi*(self._Rb)**2)-(self._n1*Kb*self.Get_Temp())
    
    def Origin_Distance_Histogram(self, bars = 25):
        distances = []
        for ball in self._b:
            distances.append(np.dot(ball._r,ball._r)**0.5)
        pl.figure
        pl.hist(distances, bars, fc='b')
        pl.xlabel('Distance from Origin')
        pl.ylabel('Frequency multiplied by 2')
        pl.title('Histogram of Ball Distances from the Origin')
        pl.show()
        
    
    def Ball_Distance_Histogram(self, bars = 25):
        distances = []
        self._n = self._n1
        while self._n > 0:
            for i in range(len(self._b)):
                if (i) == (self._n1-self._n):
                    pass
                else:
                    dr = self._b[(self._n1-self._n)].distance(self._b[(i)])
                    distances.append(dr)
            self._n -= 1      
        pl.figure
        pl.hist(distances, bars, fc='b')
        pl.xlabel('Distance from Other Ball')
        pl.ylabel('Frequency')
        pl.title('Histogram of Ball Distances from Other Balls')
        pl.show()
        
    def Ball_Velocity_Histogram(self, bars = 25, subfigure = 'False'):
        velocities = []
        for ball in self._b:
            velocities.append(np.dot(ball._v,ball._v)**0.5)
        if subfigure == 'False':            
            pl.figure
            pl.hist(velocities, bars, fc='b')
            pl.xlabel('Speed')
            pl.ylabel('Frequency')
            pl.title('Histogram of Ball Distances from the Origin')
            pl.show()
        else:
            return(velocities, bars)
        
    def Maxwell_Boltzmann_fit(self, adj = 0.2):
        x = np.arange(0, 2.5, 0.025)
        MBfit = adj*self._n1*x*np.exp(-0.5*self._Bm*(x**2)/(Kb*self.Get_Temp()))
        v, b =self.Ball_Velocity_Histogram(subfigure = 'True')
        pl.figure()
        pl.hist(v, b, fc='b')
        pl.plot(x,MBfit, label = 'Maxwell-Boltzmann distribution')
        pl.title('Comparing the velocity distribution with the Maxwell-Boltzmann Distribution')
        pl.xlabel('Speed')
        pl.ylabel('Frequency')
        pl.show()
