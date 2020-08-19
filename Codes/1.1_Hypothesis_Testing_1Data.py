#Author: Alvin & Shawn (Prepared on: 12/04/2020)

#Chapter 2: Hypothesis testing
#Hypothesis testing for 1 sample (both tails)

import numpy as np
from scipy import stats

###############
# Input data  #
###############
#Please go thru every single input parameter
data = [20.1,25.2,22.4,23.1,24.8,25.6,22.0,26.1]
expected_mean = 20 #Given value of interest (Given by qns)

#For hypothesis testing
confidence_lvl = 0.95 #in decimals
tail = 2

#If need to change sample size, mean or std, refer to line 50-52

###############
# DONT CHANGE #
###############
#Null hypothesis: data = expected_mean
#Alternate hypothesis: data != expected mean

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

#Compute parameters for data 
# In the event that any values are given, change here #
para = compute_para(data)
n = para[0]
x_bar = para[1]
std = para[2]
print('n:', n)
print('x_bar:', x_bar)
print('std:', std, '\n')

#Compute t_stat
t_stat = (x_bar - expected_mean)/(std/np.sqrt(n))
print('t_stat: ', t_stat)

#Compute t_crit
t_crit = stats.t.ppf(1-((1-confidence_lvl)/tail), n-1)
print('t_crit: ', t_crit)

#Conclusion
if (np.abs(t_stat) > t_crit):
    print('Reject NULL hypothesis. Data support a difference in mean between the two groups')
else:
    print('Unable to reject the NULl hypothesis. Data failed to support any difference in mean between the two groups')

#Compute p_value
p_value = tail*(1 - stats.t.cdf(np.abs(t_stat), n-1))
print('p_value: ', p_value)

#Confidence intervals
upper_bound = x_bar + t_crit*std/np.sqrt(n)
lower_bound = x_bar - t_crit*std/np.sqrt(n)
print('Confidence interval:', lower_bound, '< \u03BC <',upper_bound)

#-End-