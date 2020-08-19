#Author: Alvin & Shawn (Prepared on: 19/04/2020)

#Chapter 8: Linear regression (General) (Same root fxn)
#Matrix method

import numpy as np
from scipy import stats
import matplotlib.pyplot as plt

###############
# Input data  #
###############
#Please go thru every single input parameter

#Root function, eg. x, e^x, lg(x), ln(x)
def base_fn(x):
    return np.exp(x) #x, np.exp(x), np.log10(x) = lg(x), np.log(x) = ln(x)

#Function given in qns, eg. betas[0] + betas[1]*x + betas[2]*(x**2)
def fn(betas,x):
    return betas[0] + betas[1] * np.exp(x)  #Change to fxn

power = [0,1] #Power of root function. Eg. 1 + x + x^2 --> [0,1,2]

data_x = [0,0.5,1,2]
data_y = [0.2,1,3,12]
row = 4 #m: Number of expt/ eqn/ observation
col = 2 #n: Number of parameters,ie betas

#For hypothesis test given value in qns, [beta0, beta1, beta2, ...]
expected_beta=[0,0] #Number of inputs = Number of betas
confidence_lvl = 0.95 #in decimals
tail = 2

#If need to change s_y_sq, refer to line 71

###############
# DONT CHANGE #
###############
#Compute regression line

#Compute matrix A
A = np.zeros((row,col))

for j in range (0, col):
    for i in range(0, row):
        A[i,j] = base_fn(data_x[i])**power[j]


#Compute matrix K (A^T*A)^-1 * A^T
K_matrix = np.linalg.inv(np.transpose(A).dot(A)).dot(np.transpose(A))
betas = K_matrix.dot(data_y)

print("Beta values in sequential order:",betas, '\n')

#Hypothesis testing on the parameters
#H0: beta = expected_beta
#H1: beta != expected_beta

#Compute dof
dof = row - col

#Compute sse
sse = 0
for i in range(0,row):
    sse += (data_y[i] - fn(betas, data_x[i]))**2
print('SSE:', sse)

#Compute residuals variance (square root of)
s_y_sq = sse/dof
print('Residual variance, s_y_sq:', s_y_sq)

print('Square root of residual variance, s_y:', np.sqrt(s_y_sq), '\n')

#For plotting a nice smooth curve, we get a new x axis 
x_axis = np.arange(min(data_x),max(data_x),0.01);
regr_curve = np.zeros(len(x_axis));
for i in range(0,len(x_axis)):
    regr_curve[i] = fn(betas,x_axis[i])
    
#Plot results to visualize the fit
plt.plot(data_x,data_y,'k.',x_axis,regr_curve,'r-')

#Compute all s_beta_sq for all betas
s_beta_sq = np.zeros(col)
for i in range(0,col):
    for j in range(0,row):
        s_beta_sq[i] += (K_matrix[i,j]**2)*s_y_sq
print("s_beta_sq values in sequential order:",s_beta_sq, '\n')      
  
#Compute t_crit
t_crit = stats.t.ppf(1-((1-confidence_lvl)/tail),dof);#Note m-3 dof
print("t_crit:",t_crit,'\n')

#Compute t_stat, p_value and confidence interval for all betas
for i in range(0,col):
    print('Beta', i)
    
    #Compute t_stat
    t_stat = (betas[i]-expected_beta[i])/np.sqrt(s_beta_sq[i])
    print('t_stat:', t_stat)
    
    #Conclusion for hypothesis testing
    if (np.abs(t_stat)>t_crit):
        print('Reject the NULL hypothesis.')
    else:
        print('Unable to reject the NULL hypothesis.')
    
    #Compute p value
    p_value= tail*(1.0-stats.t.cdf(abs(t_stat), dof))
    print('p_value:', p_value)
    
    #Confidence interval
    upper_bound = betas[i] + t_crit*np.sqrt(s_beta_sq[i]);
    lower_bound = betas[i] - t_crit*np.sqrt(s_beta_sq[i])
    print('Confidence interval for beta', i, ':', lower_bound, '< \u03BC <', upper_bound, '\n')

# -End-