from GM1118_Code import Ball as B
from GM1118_Code import Simulation as S
"""
Task 1:
This is solved within the time_to_collision() method of Ball
which takes r, v and R from the two balls, using R1-R2 for 
a container-ball collision, and R1+R2 for ball-ball collisions
"""
"""
Task 2:
Ball is defined with all of the necessary variables and methods
"""
"""
Task 3:
Simulation is defined with all of the necessary variables and methods
"""
#%%
"""
Task 4:
The following code finds that the time to collision is 14 as expected,
with the following collisions using next_collisions producing the
expected results
"""
s1=S.Simulation()
s1.setballspeed(1,[1,0])
s1.setballposition(1,[-5,0])
print(s1.time_to_collision())
s1.next_collision()
print(s1._b[0]._v)
s1.next_collision()
print(s1._b[0]._v)
print(s1._b[0]._r)
#%%
s2=S.Simulation()
s2.setballspeed(1,[1,1])
s2.setballposition(1,[0,0])
print(s2.time_to_collision())
s2.next_collision()
print(s2._b[0]._v)
s2.next_collision()
print(s2._b[0]._v)
print(s2._b[0]._r)
#%%
"""
Task 5:
The Simulation class has a run method, and the following code
shows an example of it in action, with the previous simulation
of s1
"""
s1=S.Simulation()
s1.setballspeed(1,[1,0])
s1.setballposition(1,[-5,0])
s1.run(100,animate=True)
"""
Task 6:
The Ball class's collide function contains code to raise an error
if Kinetic Energy of Momentum are not conserved. The Simulation class
has a method Get_Pressure() to obtain the pressure on the container
after a passage of time
"""
"""
Task 7:
The Simulation class is already designed for multiple balls
"""
"""
Task 8:
The Simulation is designed to systematically place the balls in random
positions, but not where they can overlap with each other
"""
#%%
"""
Task 9:
The following code creates the first histogram, and then use the subsequent
code to create the seconf one. These histograms appear as expected, with
the majority of balls being near the edges as they take up the greatest
area of the distances, however amongst themselves they form a gaussian
distribution. With more balls these histograms would show this more
evidently, however s3 only contains 20 balls.
"""
s3=S.Simulation()
s3.run(100)
s3.Origin_Distance_Histogram()
#%%
s3.Ball_Distance_Histogram()
"""
Task 10:
The total KE of the system is directly proportional to the gas's 
temperature. Momentum is also conserved. If all the velocities are doubled
the temperature and pressure would both quadruple as they are 
directly proportional to each other, and temperature is proportional to
the average velocity squared. The animation would not change as it is not
affected by increased particle velocities.
"""
"""
Task 11:
The Ball classes are coded to raise an error if the conservation laws 
are not obeyed, the pressure can be calculated using the method
Get_Pressure() and it depends on T due to the ideal gas equation as
these particle act like ideal gas particles. T does not change with the
volume or the number of balls as the particles are all set up with the 
same initial speed. P is inversely proportional to the radius of the
container, and thus will decrease with the volume, but will increase with
more balls in the container.
"""
"""
Task 12:
The results can be compared to the ideal gas law using the 
Ideal_Gas_test_initial() method, however the larger the balls, the greater
the disparity between the simulation and the law. The
Ideal_Gas_test_improved() method can reduce the effect, but not remove it.
"""
"""
Task 13:
The velocities can be compared with the Maxwell_Boltzmann_fit() method
"""