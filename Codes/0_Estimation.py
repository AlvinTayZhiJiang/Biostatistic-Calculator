#Author: Alvin & Shawn (Prepared on: 12/04/2020)

#Chapter 1: Estimation
#Compute confidence interval and plot boxplot

import numpy as np
import matplotlib.pyplot as plt
from scipy import stats
import math

###############
# Input data  #
###############
#Please go thru every single input parameter
data = [0.6254,0.5874,0.3657,0.9836,0.7812]

#For confidence interval
confidence_lvl = 0.95 #in decimals
tail = 2

#If need to change sample size, mean or std, refer to line 48-50

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

#Compute parameters for data
# In the event that any values are given, change here #
para = compute_para(data)
n = para[0]
x_bar = para[1]
std = para[2]
print('n:', n)
print('x_bar:', x_bar)
print('std:', std, '\n')

#Plot boxplot
plt.boxplot(data)

#Compute median, quartile and whiskers values
#-1 as array starts from 0
pos_median_up = math.ceil(0.5*(n+1))-1
pos_median_down = math.floor(0.5*(n+1))-1
pos_q1_up = math.ceil(0.25*(n+1))-1
pos_q1_down = math.floor(0.25*(n+1))-1
pos_q3_up = math.ceil(0.75*(n+1))-1
pos_q3_down = math.floor(0.75*(n+1))-1

if pos_q1_up == pos_q1_down:
    q1 = data[pos_q1_up]
else:
    q1 = (data[pos_q1_up] + data[pos_q1_down])/2
print('q1:', q1)

if pos_median_up == pos_median_down:
    median = data[pos_median_up]
else:
    median = (data[pos_median_up] + data[pos_median_down])/2
print('Median:', median)
    
if pos_q3_up == pos_q3_down:
    q3 = data[pos_q3_up]
else:
    q3 = (data[pos_q3_up] + data[pos_q3_down])/2 
print('q3:', q3)

min_whisker = q1 - 1.5*(q3-q1)
print('Min_whisker:', min_whisker)
if min_whisker < min(data):
    print('However, minimum data,', min(data), ',was plotted in the boxplot.')

max_whisker = q3 + 1.5*(q3-q1)
print('Max_whisker:', max_whisker)
if max_whisker > max(data):
    print('However, maximum data,', max(data), ',was plotted in the boxplot.\n')
   
#Compute confidence interval
#Compute t_crit
t_crit = stats.t.ppf(1-((1-confidence_lvl)/tail),n-1)
print('t_crit:', t_crit)

#Compute confidence interval
upper_bound = x_bar + t_crit*std/np.sqrt(n)
lower_bound = x_bar - t_crit*std/np.sqrt(n)

print('Confidence interval:', lower_bound, '< \u03BC <',upper_bound)

#-End-