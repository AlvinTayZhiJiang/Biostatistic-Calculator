#Author: Alvin & Shawn (Prepared on: 19/04/2020)

#Chapter 8: Linear regression (General) (Diff root fxn)
#Matrix method

import numpy as np
from scipy import stats

###############
# Input data  #
###############
#Please go thru every single input parameter
#Data in each variables (headers): y
data_y = [25.5,31.2,25.9,38.4,18.4,26.7,26.4,25.9,32,25.2,39.7,35.7,26.5]

#Data in each variables (headers): c0, c1, c2
data = {0:[1.74,6.32,6.22,10.52,1.19,1.22,4.1,6.32,4.08,4.15,10.15,1.72,1.7],
        1:[5.3,5.42,8.41,4.63,11.6,5.85,6.62,8.72,4.42,7.6,4.83,3.12,5.3],
        2:[10.8,9.4,7.2,8.5,9.4,9.9,8,9.1,8.7,9.2,9.4,7.6,8.2],
        }

row = 13 #m: Number of expt/ eqn/ observation
col = 3 #n: Number of parameters,ie betas

#Functions given in qns
#Add on to the functions, each  function only use one variable (a/b/c)
class fn:
    def fn1(a): #Eg. a + a**2 + 1/a
        return a + a**2 + 1/a
    def fn2(b):
        return b**3
    def fn3(c): 
        return c**2
    
fn_req = [fn.fn1, fn.fn2, fn.fn3] #Add more fxns if qns have more than 3 fxns

#For hypothesis test given value in qns, [beta0, beta1, beta2, ...]
expected_beta=[0,0,0] #Number of inputs = Number of betas
confidence_lvl = 0.99 #in decimals
tail = 2

#If need to change s_y_sq, refer to line 89

###############
# DONT CHANGE #
###############
#Compute y_model (defined fxn given)
#Eg. y = beta0*fn(A) + beta1*fxn(B) + beta2*fxn(B)
#Method: by computing each component of the eqn using the respective A, B, C values
#and summing them up to obtain y value for the eqn
#Output: an array of y_model values  
def compute_y_model(betas):
    y = np.zeros(row) #creating an array to store y_model values
    for i in range(0,row): #loop thru the datapoints of X, Y, Z
        for j in range(0,col): #Loop thru the components of the eqn
            y[i] += betas[j]*fn_req[j](data[j][i]) #Sum all components using its respective X, Y, Z 
                                                   #and betas values
    return y

#Compute regression line
#Compute matrix A
A = np.zeros((row,col))

for j in range (0, col):
    for i in range(0, row):
        A[i,j] = fn_req[j](data[j][i])


#Compute matrix K (A^T*A)^-1 * A^T
K_matrix = np.linalg.inv(np.transpose(A).dot(A)).dot(np.transpose(A));
betas = K_matrix.dot(data_y);
print("Beta values in sequential order:",betas)

#Hypothesis testing on the parameters
#H0: beta = expected_beta
#H1: beta != expected_beta

#Compute dof
dof = row - col

#Compute sse
y_model = compute_y_model(betas)
sse = 0
for i in range(0,row):
    sse += (data_y[i] - y_model[i])**2
print('SSE:', sse) 
   
#Compute residuals variance (square root of)
s_y_sq = sse/dof
print('Residual variance, s_y_sq:', s_y_sq)

print('Square root of residual variance, s_y:', np.sqrt(s_y_sq), '\n')

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