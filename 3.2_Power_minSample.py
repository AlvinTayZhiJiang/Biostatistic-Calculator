#Author: Alvin & Shawn (Prepared on: 13/04/2020)

#Chapter 3: Power and Sample Size
#Compute minimum number (n_answer) required to achieve a certain power
#Assuming equal variance

import numpy as np
from scipy import stats

###############
# Input data  #
###############
#Please go thru every single input parameter
data = [3.9,4.5,4.0,3.4,3.9,4.1]
given_delta = 0.45 # ẟ: Difference between the 2 samples (Given by qns) 
given_sigma = 0 # σ: Standard deviation of the population (Given by qns or std)
                #If given_sigma = 0 -> std will be auto assign to given_sigma 

given_power = 0.5 #Given power to be achieved (% converted to decimals)

#For hypothesis testing
confidence_lvl = 0.95 #in decimals
tail = 2

#If need to input diff parameter like n, mean, std (line 50 -52)

###############
# DONT CHANGE #
###############
#Copmute standard parameters
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
n_given = para[0]
x_bar = para[1]
std = para[2]
print('n:', n_given)
print('x_bar:', x_bar)
print('std:', std, '\n')

if (given_sigma == 0):
    given_sigma = std #sigma for computing D

#Determine n_answer
power = 0
n_answer = 1
while power <  given_power: 
    dof = n_given + n_answer - 2
    t_crit = stats.t.ppf(1-((1-confidence_lvl)/tail), dof)
    D = given_delta/(given_sigma*np.sqrt(1/n_given + 1/n_answer))
    t_star = t_crit - D
    beta = stats.t.cdf(t_star, dof)
    power = 1.0 - beta
    n_answer += 1

print('t_star:', t_star)
print('Beta (Probability of making type II error):', beta)
print('Power (Probability of not making type II error):', power)
print('Minimum number (n_answer):', n_answer-1)

#-End-