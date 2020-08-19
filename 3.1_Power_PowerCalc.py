#Author: Alvin & Shawn (Prepared on: 13/04/2020)

#Chapter 3: Power and Sample Size
#Hypothesis testing for difference between 2 means -> Compute power
#Assume equal variance
#Accounted for if different sample size

import numpy as np
from scipy import stats

###############
# Input data  #
###############
#Please go thru every single input parameter
data1 = []
data2 = []
given_delta = 5 # ẟ: Difference between the 2 samples (Given by qns) 
given_sigma = 0 # σ: Standard deviation of the population (Given by qns or sp from hypothesis testing between 2 means)
                #If given_sigma = 0 -> sp will be auto assign to given_sigma 

#For hypothesis testing
confidence_lvl = 0.95 #in decimals
tail = 2

#If need to input diff parameter like n, mean, std (line 60 -72) 

###############
# DONT CHANGE #
###############
#Null hypothesis: data1 - data2 = 0 (No diff) 
#Alternate hypothesis: data1 - data2 != 0 (Diff)

#Diff for hypothesis testing 
#Usually 0 as we want to test whether there is a diff between the 2 means, before calculating power
# In the event that any values are given, change here #
diff = 0 

#Compute standard parameters
def compute_para(data):
    #Compute length of data (Sample size)
    n = len(data)
    
    #Compute sample mean
    x_bar = np.mean(data)
    
    #Compute sample std
    sum_sq = 0
    for i in range(0,n):
        sum_sq += (data[i]-x_bar)**2
    sample_std = np.sqrt(sum_sq/(n-1))
    
    #Input into para array
    para = [n, x_bar, sample_std]
    
    return para

#Compute parameters for data 1
# In the event that any values are given, change here #
para1 = compute_para(data1)
n1 = para1[0]
x_bar1 = para1[1]
std1 = para1[2]
print('n1:', n1)
print('x_bar1:', x_bar1)
print('std1:', std1, '\n')

#Compute parameters for data 2
# In the event that any values are given, change here #
para2 = compute_para(data2)
n2 = para2[0]
x_bar2 = para2[1]
std2 = para2[2]
print('n2:', n2)
print('x_bar2:', x_bar2)
print('std2:', std2, '\n')

#Compute dof
dof = n1 + n2 - 2
    
#Compute sp
sp = np.sqrt( ((n1 - 1)*(std1**2) + (n2 - 1)*(std2**2)) / dof )
if (given_sigma == 0):
    given_sigma = sp #sigma for computing D

#Compute t_stat
t_stat = ((x_bar1 - x_bar2) - diff) / (sp * np.sqrt((1/n1)+(1/n2)))
print('t_stat: ', t_stat)

#Compute t_crit
t_crit = stats.t.ppf(1-((1-confidence_lvl)/tail), dof)
print('t_crit: ', t_crit)

#Conclusion
if (np.abs(t_stat) > t_crit):
    print('Reject NULL hypothesis. Data support a difference in mean between the two groups')
else:
    print('Unable to reject the NULl hypothesis. Data failed to support any difference in mean between the two groups.\n')

#Computing power of the test
D = given_delta/(given_sigma*np.sqrt(1/n1 + 1/n2))
t_star = t_crit - D
beta = stats.t.cdf(t_star, dof)
power = 1.0 - beta
print('t_star:', t_star)
print('Beta (Probability of making type II error)', beta)
print('Power (Probability of not making type II error):', power)

#-End-