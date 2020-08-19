#Author: Alvin & Shawn (Prepared on: 13/04/2020)

#Chapter 3.5: Paired t test
#Analysis of data where a patient is evaluated before and after a treatment 

import numpy as np
from scipy import stats

###############
# Input data  #
###############
#Please go thru every single input parameter
data_bef = [] #If diff_array given, input diff_array here
data_aft = [] #If diff_array given, input data_aft as a array of 0  (same size as data_bef)

#For hypothesis testing
confidence_lvl = 0.95 #in decimals
given_delta = 0 #For hypothesis testing, given true mean diff between bef and after (Given by qns)
tail = 2

#If need to input diff parameter like n, mean, std (line 51 -53)

###############
# DONT CHANGE #
###############
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

#Compute mean and std of the diff
diff_array = np.zeros(len(data_bef))
for i in range(0, len(data_bef)):
    diff_array[i] = data_bef[i] - data_aft[i]

para_diff = compute_para(diff_array)
n = para_diff[0]
mean_diff = para_diff[1]
std_diff = para_diff[2]
print('n:', n)
print('mean_diff(d_bar):', mean_diff)
print('std_diff(s_d):', std_diff, '\n')

#Compute t_stat
t_stat = (mean_diff - given_delta)/(std_diff/np.sqrt(n))
print('t_stat: ', t_stat)

#Compute t_crit
t_crit = stats.t.ppf(1-((1-confidence_lvl)/tail), n-1)
print('t_crit: ', t_crit)

#Conclusion
if (np.abs(t_stat) > t_crit):
    print('Reject the NULL hypothesis. Data support a mean difference between before and after')
else:
    print('Unable to reject the NULL hypothesis. Data failed to support any difference in between before and after')
    
#Compute p value
p_value = 2.0 *(1.0 - stats.t.cdf(np.abs(t_stat), n-1));
print('p_value: ', p_value)

#-End-