#Author: Alvin & Shawn (Prepared on: 21/04/2020)

#Chapter 10: Non Linear regression (General mutiple variable - Root)
#Assuming when only 2 parameters are given -> 3 vertices
#Simplex method to find minima of fxn/ minimum point of the fxn 
#Initial guess = [ variables(x/y) ] -> to find  x and y that gives the minimum z

#Variables (x, y) != Parameters (beta/ sigma/ mu)

import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits import mplot3d #just for 3D plots

###############
# Input data  #
###############
#Please go thru every single input parameter
#points = vertices

#Function given in qns
#pts: [beta 1 (xaxis),  beta 2 (yaxis)] 
#eg. 3*pt[0]*pt[0] - 3*pt[1] + pt[1]*pt[1] + 30*np.sin(pt[0])
def fn(pt):
     return 3*pt[0]*pt[0] - 3*pt[1] + pt[1]*pt[1] + 30*np.sin(pt[0])
 
init_guess = [1,1] #If not all vertices are given, code will compute 2 additional vertices 5% away from initial guess

#If all vertices given, change -> allVertices = True
#3 points including init_guess = vertice 1
allVertices = False
point_1 = [] #Given coordinates of [beta1, beta2] for vertice 2
point_2 = [] #Given coordinates of [beta1, beta2] for vertice 3

#Termination criteria
max_iterations = 5  #Number of iterations stated
tolerance = 1e-8

###############
# DONT CHANGE #
###############
#Scaling to print graph
scale = 5

#Compute midpoint, (A+G)/2
def midpoint(avg, gd):
    midpt = []
    midpt.extend( ((avg[0] + gd[0])/2, (avg[1] + gd[1])/2) )
    return midpt
    
#Compute reflection, 2M-W
def reflection(midpt, worst):
    ref = []
    ref.extend( ((2*midpt[0] - worst[0]), (2*midpt[1] - worst[1])) )
    return ref

#Compute extention, 2R-M
def extend(ref, midpt):
    ext = []
    ext.extend( ((2*ref[0] - midpt[0]), (2*ref[1] - midpt[1])) )
    return ext

#Compute contract out, (R+M)/2
def contract_out(ref,midpt):
    c_out = []
    c_out.extend( ((midpt[0] + ref[0])/2, (midpt[1] + ref[1])/2) )
    return c_out

#Compute contact in, (M+W)/2
def contract_in(midpt, worst):
    c_in = []
    c_in.extend( ((midpt[0] + worst[0])/2, (midpt[1] + worst[1])/2) )
    return c_in

#Compute point_1 and point_2 if vertices are not given, 5% away from initial guess
if allVertices == False:
    point_1 = [init_guess[0]*(1.05),init_guess[1]]
    point_2 = [init_guess[0],init_guess[1]*(1.05)]
   
points = [init_guess , point_1, point_2]

#Compute SSE for all points 
fn_values = [fn(points[0]),fn(points[1]),fn(points[2])]
print('Before iteration and sorting:')
print('Initial (Vertice1), Vertice2, Vertice3 (unsorted):', points)
print('Initial (Vertice1), Vertice2, Vertice3  fn_values (unsorted):', fn_values)

#Sort vertices into good, average, worst (Ascending order - smallest to biggest)
fn_values, points = (list(t) for t in zip(*sorted(zip(fn_values, points))))

#Printing of each iteration
print('------------------------------------------------------------------')
print('Good, Average, worst vertices:', points)
print('Good, Average, worst fn_values:', fn_values, '\n')
print('##################################################################') 

for i in range (1,max_iterations+1):    
    #Assigning good, average, worst vertices coordinates to variables
    gd = points[0]
    avg = points[1]
    worst = points[2]
    
    #Assigning good, average, worst SSE to variables
    fn_gd = fn_values[0]
    fn_avg = fn_values[1]
    fn_worst= fn_values[2]
    
    #Compute new simplex
    print('Iteration, New simplex:', i) 
    
    #Compute midpt
    midpt = midpoint(avg,gd) 
    
    #Compute reflection and its SSE
    ref = reflection(midpt, worst)
    fn_r = fn(ref)
    print('Reflect (coordinates):', ref)
    print('Reflect (fn_value):', fn_r)
    print('------------------------------------------------------------------')
    
    #Flowchart to obtain new simplex (ie, points) according to SSE(r)
    if fn_r < fn_avg:
        if fn_r<fn_gd:
            ext = extend(ref,midpt)
            fn_ext = fn(ext)
            
            if fn_ext < fn_r:
                points[2] = ext #Extend operation
                print('Extend (fn_value):', fn(points[2]))
                print('As fn(T) < fn(R) < fn(G) < fn(A),')
                print('Extend operation successful (coordinates):', points[2])
                
            else:
                points[2] = ref #Relect operation
                print('As fn(R) < fn(T) and fn(G) < fn(A),')
                print("UNSUCCESSFUL Extend operation, Reflection point taken.")
        else:
            points[2] = ref #Reflect operation
            print('As fn(G) < fn(R) < fn(A),')
            print('Reflection point taken')

    else:
        c_out = contract_out(ref, midpt)
        fn_c_out = fn(c_out)
        if fn_c_out < fn_avg:
            points[2] = c_out #Contract out operation
            print('Contract out (fn_value):', fn(points[2]))
            print('As fn(Cout) < fn(A) < fn(R),')
            print('Contract out (coordinates):', points[2])
            
        else:
            points[2] = contract_in(midpt, worst) #Contract in operation
            print('Contract in (fn_value):', fn(points[2]))
            print('As fn(A) < fn(Cout) and fn(R),')
            print('Contract in (coordinates):', points[2])
            
    #Compute SSE for all points 
    fn_values = [fn(points[0]),fn(points[1]),fn(points[2])]
    
    #Sort vertices into good, average, worst (Ascending order - smallest to biggest)
    fn_values, points = (list(t) for t in zip(*sorted(zip(fn_values, points))))
    
    #Printing of each iteration
    print('------------------------------------------------------------------')
    print('Good, Average, worst vertices:', points)
    print('Good, Average, worst fn_values:', fn_values, '\n')
    print('##################################################################')        
    
    if np.abs(gd[0]-avg[0])<tolerance and np.abs(gd[1]-avg[1])<tolerance:
        break #Bracket is small enough, exit the loop

#Coordinates in 'Good' vertice (NOT SSE)
print('Final x (coordinate):', points[0][0])
print('Final y (coordinate):', points[0][1])

#Plotting the surface in 3D
x = np.arange(-init_guess[0]*scale,init_guess[0]*scale,0.1);                   
y = np.arange(-init_guess[1]*scale,init_guess[1]*scale,0.1);                   

X, Y = np.meshgrid(x,y);
Z = fn([X, Y]);                   

ax = plt.axes(projection='3d');
ax.plot_surface(X,Y,Z,rstride=2,cstride=2,cmap='viridis',edgecolor='none');

#-End-