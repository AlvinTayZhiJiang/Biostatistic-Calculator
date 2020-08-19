#Author: Alvin & Shawn (Prepared on: 12/04/2020)

#Chapter 2: Hypothesis testing
#Hypothesis testing for difference between 2 means (Equal/Unequal variance)
#Accounted for if different sample size

import numpy as np
from scipy import stats

###############
# Input data  #
###############
#Please go thru every single input parameter
data1 = [70.00,62.00,80.00,81.00]
data2 = [47.00,51.00,85.00,88.00,80.00]
equal = True #Equal/ Unequal variance

#For hypothesis testing
confidence_lvl = 0.95 #in decimals
given_diff = 0 #Given diff for hypothesis testing (Given by qns)
tail = 2

#If need to change sample size, mean or std, refer to line 53-65

###############
# DONT CHANGE #
###############
#Null hypothesis: data1 - data2 = given_diff 
#Alternate hypothesis: data1 - data2 != given_diff

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

#Compute dof, t_stat
if equal == True:
    #Assume equal variance
    #Compute dof
    dof = n1 + n2 - 2
        
    #Compute sp
    sp = np.sqrt( ((n1 - 1)*(std1**2) + (n2 - 1)*(std2**2)) / dof )
    print('sp (pool variance): ', sp)
    
    #Compute t_stat
    t_stat = ((x_bar1 - x_bar2) - given_diff) / (sp * np.sqrt((1/n1)+(1/n2)))
    print('t_stat: ', t_stat)

else:
    #Assume unequal variance
    #Compute dof
    dof = round(  ((std1**2/n1 + std2**2/n2)**2)\
                 / ((std1**2/n1)**2 / (n1-1) +\
                    (std2**2/n2)**2 / (n2-1)) )
    
    #Compute t_stat
    t_stat = ((x_bar1 - x_bar2) - given_diff) / np.sqrt((std1**2/n1)+(std2**2/n2))
    print('t_stat: ', t_stat)

#Compute t_crit
t_crit = stats.t.ppf(1-((1-confidence_lvl)/tail), dof)
print('t_crit: ', t_crit)

#Conclusion
if (np.abs(t_stat) > t_crit):
    print('Reject NULL hypothesis. Data support a difference in mean between the two groups')
else:
    print('Unable to reject the NULl hypothesis. Data failed to support any difference in mean between the two groups')

#Compute p_value
p_value = tail*(1 - stats.t.cdf(np.abs(t_stat), dof))
print('p_value: ', p_value)

#-End-