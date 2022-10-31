import Simulation as S
s1=S.Simulation()
s1.run(1000,animate=True) # figure 1 in report
#%%
s1.Ideal_Gas_test_initial() # first data used in report
#%%
s1.Ideal_Gas_test_improved() # second data used in report
#%%
s2=S.Simulation(100,10**3)
s2.run(1000,animate=True) # figure 2 in report
#%%
s2.Ideal_Gas_test_improved() # third piece of data used in report
#%%
s2.Maxwell_Boltzmann_fit() # figure 3 in report
#%%
s3=S.Simulation(100,20)
s3.run(10000,animate=False) # figure 4 in report
