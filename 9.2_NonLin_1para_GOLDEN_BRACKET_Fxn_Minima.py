#Author: Alvin & Shawn (Prepared on: 20/04/2020)

#Chapter 9: Non Linear regression (single variable - Minima of fxn)
#Bracketing method/ Golden Ratio method to find minima of fxn/ minimum point of the fxn 
#initial guess = [x (upper and lower bound] -> to get x that gives the minimum y value

import numpy as np

###############
# Input data  #
###############
#Please go thru every single input parameter

#Function given in qns
def fn(x): #eg. np.exp(x) - 25*x 
     return np.cos(2*x**2) #Change to fxn

interval = [0.8,1.6] #Initial bracket [x1, x2]

#Termination criteria
max_iterations = 100 #No. of iteration stated
tolerance = 1e-9

###############
# DONT CHANGE #
###############
#Initial bracket
a = interval[0]
b = interval[1]

#Compute beta1 and beta2
x = np.zeros(2)
r = (np.sqrt(5.0)-1)/2.0 #Golden section rule = 0.618

#The first two internal points
x[0] = (1-r)*(b-a) + a;
x[1] = r*(b-a) + a

#Compute SSE of first two internal points
f_x = np.zeros(2)
f_x[0] = fn(x[0]) #x1
f_x[1] = fn(x[1]) #x2

print("Iteration 1:")
print('a:', a)
print('b:', b)
print("x1:",x[0])
print("x2:",x[1])
print("f(x1)", f_x[0])
print("f(x2)", f_x[1], "\n")

#Iterations to determine minimum betas
for i in range(1,max_iterations+1):
    if f_x[0] > f_x[1]: #Discard the interval [a, x1]
        print('Discard [a, x1]:', [a, x[0]])
        
        a  = x[0] #x1 -> a
        x[0] = x[1] #x2 --> x1 
        f_x[0] = f_x[1] #SSE(x2) --> SSE(x1)
        x[1] = r*(b-a)+a #New x2
        f_x[1] = fn(x[1]) #SSE(new x2)
        
        print('new a:', a)
        print('new b:', b)
        print("new x1:", x[0])
        print("new x2:", x[1], "\n")
        
    else: #Discard the interval [x2, b]
        print('Discard [x2, b]:', [x[1], b])
    
        b = x[1] #x2 --> b    
        x[1] = x[0] #x1 --> x2
        f_x[1] = f_x[0] #SSE(x1) --> SSE(x2)
        x[0] = (1-r)*(b-a)+a #New x1
        f_x[0] = fn(x[0]) #SSE(new x1)
        
        print('new a:', a)
        print('new b:', b)
        print("new x1:", x[0])
        print("new x2:", x[1],"\n")
        
    if(i<max_iterations):    
        print("Iteration",i+1,":")
        print('a:', a)
        print('b:', b)
        print("x1:",x[0])
        print("x2:",x[1])
        print("f(x1)", f_x[0])
        print("f(x2)", f_x[1], "\n")
        
    if (np.abs(b-a)<tolerance):
        break #Bracket is small enough, exit the loop

#Compute final bracket
print('Final bracket, [a,b]:', [a,b])

#Compute minimum beta
minimum = (a+b)/2.0
print("min, [(a+b)/2]:", minimum)

#Obtain mimina/ minimum value of fxn
y_value = fn(minimum)
print("y_value/ minima/ minimum:", y_value);

#-End-