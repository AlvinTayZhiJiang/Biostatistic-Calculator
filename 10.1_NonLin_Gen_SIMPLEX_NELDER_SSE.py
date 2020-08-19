#Author: Alvin & Shawn (Prepared on: 21/04/2020)

#Chapter 10: Non Linear regression (General multiple variable - Minimisation)
#Assuming when only 2 parameters are given -> 3 vertices
#Simplex method to minimised SSE -> obtain optimum betas
#Initial guess = [unknown parameters (beta/ sigma/ mu/ etc)] -> to get optimum parameters 

#Variables (x, y) != Parameters (beta/ sigma/ mu)

import numpy as np

###############
# Input data  #
###############
#Please go thru every single input parameter
#points = vertices

#Function given in qns
#pts: [beta 1 (xaxis),  beta 2 (yaxis)] -> Containing 2 parameters
#eg. (125.5/np.sqrt(2*np.pi*pt[0]**2))*np.exp(-(x_value-pt[1])**2/(pt[0]**2))+12.54 
def fn(pt,x):
     return (np.exp(-pt[0]*x) + pt[1])

#x and y data given -> for SSE
data_x=[1,2,3,4]
data_y=[1.5,1.75,2,2.1]
init_guess = [0,0] #If not all vertices are given, code will compute 2 additional vertices 5% away from initial guess

#If all vertices given, change -> allVertices = True
#3 points including init_guess = vertice 1
allVertices = True
point_1 = [1,1] #Given coordinates of [beta1, beta2] for vertice 2
point_2 = [2,0] #Given coordinates of [beta1, beta2] for vertice 3

#Termination criteria
max_iterations = 5 #Number of iterations stated
tolerance = 1e-8

###############
# DONT CHANGE #
###############
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

#Compute SSE for all vertices using x and y data, and [beta1, beta2]
def computeSSE(pt):
    sse = 0
    for i in range(0,len(data_x)):
        sse += (data_y[i] - fn(pt,data_x[i]))**2
    return sse;

#Compute point_1 and point_2 if vertices are not given, 5% away from initial guess
if allVertices == False:
    point_1 = [init_guess[0]*(1.05),init_guess[1]]
    point_2 = [init_guess[0],init_guess[1]*(1.05)]
   
points = [init_guess , point_1, point_2]

#Compute SSE for all points 
sse = [computeSSE(points[0]),computeSSE(points[1]),computeSSE(points[2])]
print('Before iteration and sorting:')
print('Initial (Vertice1), Vertice2, Vertice3 (unsorted):', points)
print('Initial (Vertice1), Vertice2, Vertice3  SSE (unsorted):', sse)

#Sort vertices into good, average, worst (Ascending order - smallest to biggest)
sse, points = (list(t) for t in zip(*sorted(zip(sse, points))))

#Printing of each iteration
print('------------------------------------------------------------------')
print('Good, Average, worst vertices (sorted):', points)
print('Good, Average, worst SSE (sorted):', sse, '\n')
print('##################################################################')  

for i in range (1,max_iterations+1):   
    #Assigning good, average, worst vertices coordinates to variables
    gd = points[0]
    avg = points[1]
    worst = points[2]
    
    #Assigning good, average, worst SSE to variables
    sse_gd = sse[0]
    sse_avg = sse[1]
    sse_worst=sse[2]
    
    #Compute new simplex
    print('Iteration, New simplex:', i) 
    
    #Compute midpt
    midpt = midpoint(avg,gd) 
    
    #Compute reflection and its SSE
    ref = reflection(midpt, worst)
    sse_r = computeSSE(ref)
    print('Reflect (coordinates):', ref)
    print('Reflect (SSE):', sse_r)
    print('------------------------------------------------------------------')
    
    #Flowchart to obtain new simplex (ie, points) according to SSE(r)
    if sse_r < sse_avg:
        if sse_r<sse_gd:
            ext = extend(ref,midpt)
            sse_ext = computeSSE(ext)
            
            if sse_ext < sse_r:
                points[2] = ext #Extend operation
                print('Extend (SSE):', computeSSE(points[2]))
                print('As SSE(T) < SSE(R) < SSE(G) < SSE(A),')
                print('Extend operation successful (coordinates):', points[2])
                
            else:
                points[2] = ref #Relect operation
                print('As SSE(R) < SSE(T) and SSE(G) < SSE(A),')
                print("UNSUCCESSFUL Extend operation, Reflection point taken.")
        else:
            points[2] = ref #Reflect operation
            print('As SSE(G) < SSE(R) < SSE(A),')
            print('Reflection point taken')

    else:
        c_out = contract_out(ref, midpt)
        sse_c_out = computeSSE(c_out)
        if sse_c_out < sse_avg:
            points[2] = c_out #Contract out operation
            print('Contract out (SSE):', computeSSE(points[2]))
            print('As SSE(Cout) < SSE(A) < SSE(R),')
            print('Contract out (coordinates):', points[2])
            
        else:
            points[2] = contract_in(midpt, worst) #Contract in operation
            print('Contract in (SSE):', computeSSE(points[2]))
            print('As SSE(A) < SSE(Cout) and SSE(R),')
            print('Contract in (coordinates):', points[2])
            
    #Compute SSE for all points 
    sse = [computeSSE(points[0]),computeSSE(points[1]),computeSSE(points[2])]
    
    #Sort vertices into good, average, worst (Ascending order - smallest to biggest)
    sse, points = (list(t) for t in zip(*sorted(zip(sse, points))))
    
    #Printing of each iteration
    print('------------------------------------------------------------------')
    print('Good, Average, worst vertices:', points)
    print('Good, Average, worst SSE:', sse, '\n')
    print('##################################################################')        
    if np.abs(gd[0]-avg[0])<tolerance and np.abs(gd[1]-avg[1])<tolerance:
        break #Bracket is small enough, exit the loop

#Coordinates in 'Good' vertice (NOT SSE)
print('Final beta1 (coordinate):', points[0][0]) 
print('Final beta2 (coordinate):', points[0][1])

#-End-