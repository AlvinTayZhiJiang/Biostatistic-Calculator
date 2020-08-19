#Author: Alvin & Shawn (Prepared on: 18/04/2020)

#Chapter 7: Linear Regression (Normal)
#y(x) = beta_0 + beta_1*x
#y = mx + c

import numpy as np
import matplotlib.pyplot as plt
from scipy import stats

###############
# Input data  #
###############
#Please go thru every single input parameter
#Sample size for x and y must be the same

#Hypo test and confidence intervals are computed in all cases of true or false
#estimation = false & prediction = false -> hypo test & confidence intervals ONLY
#estimation = true & prediction = false -> mean response at a given x_h
#estimation = true & prediction = true -> prediction at a given x_pred (out of range)
estimation = False #Always false unless estimation is required
prediction = False #To compute prediction value

data_x = [10,20,40,80,100]
data_y = [48,50,52,55,65]

#For hypothesis test given value in qns: [intercept (beta0), slope (beta1)]
confidence_lvl = 0.95 #in decimals
tail = 2
expected_beta = [0,0] #Slope = 0: horizontal line, no trend
                      #Slope != 0: trend
                      #intercept = 0: line pass thru origin 
                      #intercept > 0: line pass thru given value

#For estimation
#If not required, = 0
x_h = 0
x_pred = 0 

#If need to change s_y_sq / s_y, refer to line 111-116

###############
# DONT CHANGE #
###############
#Compute standard parameters
def compute_para(data):
    #Compute length of data (Sample size)
    n = len(data)
    
    #Compute sample mean
    x_bar = np.mean(data)
    
    #Input into para array
    para = [n, x_bar]
    
    return para

#Computing regression line
#Compute parameters for x data
para_x = compute_para(data_x)
n_x = para_x[0]
x_bar = para_x[1]

#Compute parameters for y data
para_y = compute_para(data_y)
n_y = para_y[0]
y_bar = para_y[1]

#Compute beta 1
m = n_x #= n_y
sum_1 = 0 #Σ(x_i - x_bar)(y_i - y_bar)
ssx = 0 #Σ(x_i - x_bar)**2
for i in range(0,m):
    sum_1 += (data_x[i]-x_bar)*(data_y[i]-y_bar)
    ssx +=(data_x[i]-x_bar)**2

#Compute slope and intercept of the line
beta_1 = sum_1/ssx #slope of the line
beta_0 = y_bar - beta_1*x_bar #intercept of the line
print('Beta_0 (intercept):', beta_0)
print('Beta_1 (slope):', beta_1, '\n')

#Regression line of x data
regr_line = np.zeros(m)
for i in range(0,m):
    regr_line[i] = beta_0 + beta_1*data_x[i]

#Computing descriptive parameter, r
#R2 value = 1-SSE/SST -> Strength of linear regression line
sse = 0 #Σ(y_i - y_i_model)**2
sst = 0 #Σ(y_i - y_bar)**2
for i in range(0,m):
    sse += (data_y[i] - regr_line[i])**2
    sst += (data_y[i] - y_bar)**2
print('SSE:', sse)

r_square = 1-sse/sst
print('r_square (0 < r_square < 1):', r_square)

r = np.sqrt(r_square)
if(beta_1<0):    
    print('r (-1 < r < 1):', (-1)*r, '\n')
else:
    print('r (-1 < r < 1):', r, '\n')

#Hypothesis testing on the slope(beta_1) and intercept(beta_0)
#H0: slope = expected_beta0 versus  |    H1: slope != expected_beta0
#H0: intercept = 0 expected_beta1   |    H1: intercept != expected_beta1

#Compute residuals variance (square root of)
dof = m-2
s_y_sq = sse/dof
print('Residual variance, s_y_sq:', s_y_sq)

s_y = np.sqrt(s_y_sq)
print('Square root of residual variance, s_y:', s_y, '\n')

#Standard errors of parameters
s_beta_0 = s_y*np.sqrt(1/m + x_bar**2/ssx)
s_beta_1 = s_y*np.sqrt(1/ssx)
print('Standard error of beta0 (s_beta_0):', s_beta_0)
print('Standard error of beta1 (s_beta_1):', s_beta_1, '\n')

#Compute t_crit
t_crit = stats.t.ppf(1-((1-confidence_lvl)/tail), dof)

#Compute t_stat for beta 0
print('Hypothesis testing for Beta_0 (intercept)')
t_stat_beta_0 = (beta_0-expected_beta[0])/s_beta_0
print('t_stat:', t_stat_beta_0)
if (np.abs(t_stat_beta_0)>t_crit):
    print('Reject the NULL hypothesis. Data support a change in y associated with a change in x')

else:
    print('Unable to reject the NULL hypothesis. Data failed to support any association between x and y')

#Compute p value for beta 0
p_value_beta_0 = tail*(1.0-stats.t.cdf(abs(t_stat_beta_0), dof))
print('p_value:', p_value_beta_0, '\n')

#Compute t_stat for beta 1
print('Hypothesis testing for Beta_1 (slope)')
t_stat_beta_1 = (beta_1-expected_beta[1])/s_beta_1
print('t_stat:', t_stat_beta_1)
if (np.abs(t_stat_beta_1)>t_crit):
    print('Reject the NULL hypothesis. Data support a change in y associated with a change in x')

else:
    print('Unable to reject the NULL hypothesis. Data failed to support any association between x and y')

#Compute p value for beta 1
p_value_beta_1 = tail*(1.0-stats.t.cdf(abs(t_stat_beta_1), dof))
print('p_value:', p_value_beta_1, '\n')

#Compute confidence intervals for regression parameters
upp_int  = beta_0 + t_crit*s_beta_0
low_int  = beta_0 - t_crit*s_beta_0
print('Confidence interval for intercept (Beta0):', low_int, '< \u03BC <', upp_int)

upp_slope = beta_1 + t_crit*s_beta_1
low_slope = beta_1 - t_crit*s_beta_1
print('Confidence interval for slope (Beta1):', low_slope, '< \u03BC <', upp_slope, '\n')

#Plot the regression line and the data points in one plot
plt.figure(0)
plt.plot(data_x, data_y,'k.', data_x, regr_line,'r-')

if estimation == True and prediction == False:
    #Compute mean response y_h for a given x_h
    y_h = beta_0 + beta_1*x_h
    s_y_h = s_y*np.sqrt(1/m + (x_h-x_bar)**2/ssx)
    upp_conf_est = y_h + t_crit*s_y_h
    low_conf_est = y_h - t_crit*s_y_h
    
    print('Confidence interval for estimated value at given (x_h =', x_h, '):', low_conf_est, '< \u03BC <', upp_conf_est)
    
    #Compute confidence bands
    upp_conf_band = np.zeros(m)
    low_conf_band = np.zeros(m)
    x_axis = np.sort(data_x) #x axis is a sorted version of ages
    for i in range (0,m):
        x_h_band = x_axis[i]
        y_h_band = beta_0 + beta_1*x_h_band
        s_y_h_band = s_y*np.sqrt(1/m + (x_h_band-x_bar)**2/ssx)
        upp_conf_band[i] = y_h_band + t_crit*s_y_h_band
        low_conf_band[i] = y_h_band - t_crit*s_y_h_band
        
    #Plot the regression line and the data points in one plot
    plt.figure(1)
    plt.plot(data_x, data_y,'k.', data_x, regr_line,'r-',\
             x_axis,upp_conf_band,'g-',x_axis,low_conf_band,'g-')

elif estimation == True and prediction == True:
    #Compute estimation of an individual prediction y_pred at a given x_pred
    y_pred = beta_0 + beta_1*x_pred
    s_y_pred = s_y*np.sqrt(1 + (1/m) + (x_pred-x_bar)**2/ssx)
    upp_conf_pred = y_pred + t_crit*s_y_pred
    low_conf_pred = y_pred - t_crit*s_y_pred

    print('Confidence interval for predicted value at given (x_pred =', x_pred, '):', low_conf_pred, '< \u03BC <', upp_conf_pred)

# -End-