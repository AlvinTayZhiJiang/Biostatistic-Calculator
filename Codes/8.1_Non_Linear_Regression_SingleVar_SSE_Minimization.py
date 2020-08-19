#Author: Alvin & Shawn (Prepared on: 20/04/2020)

#Chapter 9: Non Linear regression (single variable - SSE Minimisation)
#Bracketing method/ Golden Ratio method to minimised SSE -> obtain optimum betas
#Initial guess = [1 parameter(upper and lower bound)]

import numpy as np
import matplotlib.pyplot as plt

###############
# Input data  #
###############
#Please go thru every single input parameter

#Function given in qns
def fn(beta,x): #eg. (100.0/(1.0+(beta/x)**2))
    return np.sqrt(x + beta) #Change to fxn

data_x = [1,2,3,4]
data_y = [1.5,1.75,2,2.1]
interval = [0,10] #Initial bracket

#Termination criteria
max_iterations = 100 #Number of iterations stated
tolerance = 1e-9

###############
# DONT CHANGE #
###############
#Compute SSE
def obj_fun(beta):
    m = len(data_x);#number of experimental data points
    sse = 0;
    for i in range(0,m):
        x  = data_x[i]
        y_model = fn(beta,x)
        y_experimental = data_y[i]
        sse = sse  + (y_model - y_experimental)**2; 
    return sse;

#Initial bracket
a = interval[0]
b = interval[1]

#Compute beta1 and beta2
beta = np.zeros(2)
r = (np.sqrt(5.0)-1)/2.0 #Golden section rule = 0.618

#The first two internal points
beta[0] = (1-r)*(b-a) + a;
beta[1] = r*(b-a) + a;

#Compute SSE of first two internal points
f_beta = np.zeros(2)
f_beta[0] = obj_fun(beta[0]) #SSE_beta1
f_beta[1] = obj_fun(beta[1]) #SSE_beta2

print("Iteration 1:");
print("a:",a)
print("b:",b)
print("beta_1:",beta[0])
print("beta_2:",beta[1])
print("SSE_beta1", f_beta[0])
print("SSE_beta2", f_beta[1], "\n")

#Iterations to determine minimum betas
for i in range(1,max_iterations+1):
    if (f_beta[0] >= f_beta[1]): #Discard the interval [a, beta1]
        print('Discard [a, beta1]:', [a, beta[0]])
        
        a  = beta[0] #beta1 -> a
        beta[0] = beta[1] #beta2 --> beta1 
        f_beta[0] = f_beta[1] #SSE(beta2) --> SSE(beta1)
        beta[1] = r*(b-a)+a #New beta2
        f_beta[1] = obj_fun(beta[1]) #SSE(new beta2)
        
        print("new a:",a)
        print("new b:",b)
        print("new beta_1:",beta[0])
        print("new beta_2:",beta[1],'\n')
        
    else: #Discard the interval [beta2, b]
        print('Discard [beta2, b]:', [beta[1], b])
        
        b = beta[1] #beta2 --> b    
        beta[1] = beta[0] #beta1 --> beta2
        f_beta[1] = f_beta[0] #SSE(beta1) --> SSE(beta2)
        beta[0] = (1-r)*(b-a)+a #New beta1
        f_beta[0] = obj_fun(beta[0]) #SSE(new beta1)
        
        print("new a:",a)
        print("new b:",b)
        print("new beta_1:",beta[0])
        print("new beta_2:",beta[1],'\n')
        
    if(i<max_iterations):    
        print("Iteration",i+1,":")
        print("a:",a)
        print("b:",b)
        print("beta_1:",beta[0])
        print("beta_2:",beta[1])
        print("SSE_beta1 =",f_beta[0])
        print("SSE_beta2 =",f_beta[1], '\n')  
        
    if (np.abs(b-a)<tolerance):
        break #Bracket is small enough, exit the loop

#Compute final bracket
print('Final bracket, [a,b]:', [a,b])

#Compute minimum beta
beta_optimise = (a+b)/2.0
print("Optimum beta, [(a+b)/2]:", beta_optimise)

#Plotting results
x_axis = np.arange(min(data_x),max(data_x),0.01);
regr_curve = np.zeros(len(x_axis));
for i in range(0,len(x_axis)):
    regr_curve[i] = fn(beta_optimise,x_axis[i]);

plt.semilogx (data_x, data_y, 'k.', x_axis,regr_curve,'r-');

#-End-