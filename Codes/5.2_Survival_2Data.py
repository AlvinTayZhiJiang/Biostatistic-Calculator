#Author: Alvin & Shawn (Prepared on: 16/04/2020)
#Function Author: Dr Alberto

#Chapter 6: Analysis of Survival Data (2 Data Comparison)

import numpy as np
from scipy import stats
import matplotlib.pyplot as plt

###############
# Input data  #
###############
#Please go thru every single input parameter
#Input data in a zigzag manner -> similar to reading a book

# If enrolment and death time are given separately #
####################################################
#1: Time of enrolment
#2: Time of event/ death
#3: Type of event (if lost to follow up/survive - 0 
#                  if event/ death - 1              ) 

# If existing time (event - enrol) are given #
##############################################
#1: Existng time/ Survival time = (event - enrol)
#2: Type of event (if lost to follow up/survive - 0 
#                  if event/ death - 1              ) 

difference_given = True #Existing time/ Survival time (event - enrol)

#Input for each individual patient, even if death occurs on the same time
data1 = [2,1,6,1,7,1,7,1,7,0,8,1,9,1,11,0,12,1,12,0]
row1 = 10 #row = number of data **account for each individual patient

#Input for each individual patient, even if death occurs on the same time
data2 = [1,1,1,1,3,0,4,1,5,1,6,1,7,1,7,0,8,1,10,1,11,0]
row2 = 11 #row = number of data, **account for each individual patient

#For hypothesis testing
confidence_lvl = 0.95 #in decimals
tail = 2

###############
# DONT CHANGE #
###############
#No. of cols depend on whether existing time was given (refer to line 15-26) - Exclude patient no.
if difference_given == True: # == Existing time (event - enrol)
    col1 = 2
    col2 = 2
else:
    col1 = 3
    col2 = 3

#This function takes in two arrays of the same length
#Each element of the array corresponds to an individual

#The first array contains the time, since the start of the study of an event related to the individual. 
#If the event is death, value in the second array is 1
#If the event is not death, value in the second array is 0
#The two arrays do not need to be sorted by time

#Given these two arrays, this function returns a list containing
#- At position 0: times of deaths in chronological order (starting from t = 0)
#- At position 1: values of Kaplan Meyer survival curve S_hat (S_hat(0) = 1)
#- At position 2: times of event (deaths/ lost to follow up/ otherwise)
#- At position 3: total number of individuals still alive just after the corresponding time in the array at position 2
#- At position 4: total number of individuals who dies at the corresponding time in the array at position 2
#- At position 5: total number of individuals who are lost to follow up at the corresponding time in the array at position 2
#- At position 6: used for plotting time versus survival in the typical "staircase" plots. Time is at this position
#- At position 7: used for plotting time versus survival in the typical "staircase" plots. Survival is at this position

def compute_survival(unsorted_time_of_events, unsorted_type_of_events):
    
    #argosrt will internally sort the array and give the original indices in order 
    indices = np.argsort(unsorted_time_of_events);
    time_of_events = np.zeros(len(indices));
    type_of_events = np.zeros(len(indices));
    for i in range (0,len(indices)):
        index = indices[i];
        time_of_events[i] =unsorted_time_of_events[index];
        if (unsorted_type_of_events[index]==1):
            type_of_events[i]=1;
        
    N = len(time_of_events)
    total_surviving = N;
    n_i = [N];
    times_of_death=[0.0];
    times_of_death_plot=[0.0];
    S_hat = [1.0];
    S_hat_plot = [1.0];
    d_i = [0];
    lost_i = [0];
    i=0;
    all_times = [0.0];
    frac_survive = [1]
    while(i<N):
        time_of_interest = time_of_events[i]
        #determine number of events at this time
        n_events = np.count_nonzero(time_of_events == time_of_interest)
        deaths_at_i=0;
        lost_at_i = 0;
        for j in range (i,i+n_events):
            if (type_of_events[j]==1):#There was a death
                deaths_at_i=deaths_at_i+1;
            else:
                lost_at_i=lost_at_i+1;
        
        if (deaths_at_i>0):            
            S_hat_plot.append(S_hat[-1]);
            times_of_death_plot.append(time_of_interest);
            new_surv_frac = float(n_i[-1]-deaths_at_i)/n_i[-1];
            frac_survive.append(new_surv_frac)
            new_value = S_hat[-1]*new_surv_frac
            S_hat.append(new_value);
            S_hat_plot.append(new_value);
            times_of_death.append(time_of_interest);
            times_of_death_plot.append(time_of_interest);
            
        all_times.append(time_of_interest);

        i=i+deaths_at_i+lost_at_i;
        
        total_surviving = total_surviving - deaths_at_i - lost_at_i;   
        n_i.append(total_surviving);
        d_i.append(deaths_at_i);
        lost_i.append(lost_at_i);
    return [times_of_death,S_hat,all_times, n_i, d_i, lost_i, times_of_death_plot, S_hat_plot, frac_survive];


#This function takes in two survival curves in the format that is returned by 
# the compute_survival functions. It goes through them and calculates the values
# of u_L and s_UL^2 that are necessary to perform the log-rank test.
# u_L and s_UL^2 are returned in a list (u_L at position 0, s_UL^2 at position 1)

def compare_survivals(survival_1, survival_2):
    
    #First, obtain, from the two, all the times where we need to do something
    to_be_added = [];
    for i in range(0, len(survival_2[2])):
        position = np.where(np.isclose(survival_1[2],survival_2[2][i],1e-4));
        if (len(position[0])==0):#if not there, we add it
            to_be_added.append(survival_2[2][i]);
    
    all_times = survival_1[2] + to_be_added;
    all_times.sort();
    
    u_l=0.0;
    s_2_UL=0.0;
    n_1_i = survival_1[3][0];
    n_2_i = survival_2[3][0];
    d_1_i = 0;
    d_2_i = 0;
    lost_1_i = 0;
    lost_2_i = 0;
    for i in range(1,len(all_times)):#Note we ignore t=0.
        #Check whether this time in the first, second or both
        pos_2 = np.where(np.isclose(survival_2[2],all_times[i],1e-4))
        pos_1 = np.where(np.isclose(survival_1[2],all_times[i],1e-4))
        if len(pos_2[0])>0 :
            d_2_i  = survival_2[4][pos_2[0][0]];
            n_2_i  = survival_2[3][pos_2[0][0]-1];
            lost_2_i = survival_2[5][pos_2[0][0]];
        else:
            n_2_i = n_2_i - d_2_i - lost_2_i;
            d_2_i = 0;
            lost_2_i =0;
                
        if len(pos_1[0])>0 :
            d_1_i  = survival_1[4][pos_1[0][0]];
            n_1_i  = survival_1[3][pos_1[0][0]-1];
            lost_1_i  = survival_1[5][pos_1[0][0]];
        else:
            n_1_i = n_1_i - d_1_i - lost_1_i;
            d_1_i  = 0;
            lost_1_i  = 0;
    
        if (d_2_i>0 or d_1_i>0):#u_L is computed only when there is a death
            d_total_i = d_2_i + d_1_i;
            n_total_i = n_2_i + n_1_i;
            f_i = float(d_total_i)/n_total_i;#float is key otherwise it may do an integer division
            e_i = n_2_i*f_i;
            o_minus_e = d_2_i - e_i;
            u_l = u_l + o_minus_e;
            if (n_total_i>1):
                s_2_UL = s_2_UL + (float(n_1_i)*n_2_i*d_total_i*(n_total_i-d_total_i))/(n_total_i*n_total_i*(n_total_i-1));
                
    return [u_l, s_2_UL];

#Input data into observed contingency table
table1 = np.zeros((row1,col1))
counter = 0
for i in range(0,row1):
    for j in range(0,col1):
        table1[i,j] = data1[counter] #IndexError: list index out of range -> REMEMBER TO CHANGE DIfFERENCE_GIVEN OR ROW
        counter += 1
        
table2 = np.zeros((row2,col2))
counter = 0
for i in range(0,row2):
    for j in range(0,col2):
        table2[i,j] = data2[counter]
        counter += 1
                
if difference_given == True:
    time1 = table1[:,0]
    type1 = table1[:,1]
    
    time2 = table2[:,0]
    type2 = table2[:,1]
else:
    time1 = table1[:,1] - table1[:,0]
    type1 = table1[:,2]
    
    time2 = table2[:,1] - table2[:,0]
    type2 = table2[:,2]

survival1 = compute_survival(time1,type1)
survival2 = compute_survival(time2,type2)

plt.figure(1);
plt.plot(survival1[6],survival1[7], 'b-', survival2[6],survival2[7], 'r-')

#Print S_hat(t) table for data 1
print('Survival_time Frac_survive S_hat(t)')
array1 = np.zeros((len(survival1[0]),3))
array1[:,0] = survival1[0]
array1[:,1] = survival1[8]
array1[:,2] = survival1[1]
print(array1)
print('**Note: excluding lost to follow up.')

#Compute Median survival times for data 1
t_deaths1 = survival1[0]
s_hat1 = survival1[1]
median1 = 0
for i in range(0,len(t_deaths1)):
    if (s_hat1[i]<0.5):
        median1 = t_deaths1[i]
        break
print ('Median survival time for data 1 is ',median1, '(time unit).\n')

#Print S_hat(t) table for data 2
print('Survival_time Frac_survive S_hat(t)')
array2 = np.zeros((len(survival2[0]),3))
array2[:,0] = survival2[0]
array2[:,1] = survival2[8]
array2[:,2] = survival2[1]
print(array2)
print('**Note: excluding lost to follow up.')

t_deaths2 = survival2[0]
s_hat2 = survival2[1]
median2 = 0
for i in range(0,len(t_deaths2)):
    if (s_hat2[i]<0.5):
        median2 = t_deaths2[i]
        break
print ('Median survival time for data 2 is ',median2, '(time unit).\n')

#Log rank test
result = compare_survivals(survival1, survival2)
u_L = result[0]
print("U_L =", u_L)
s_2_UL = result[1]
print("s_2_UL =", s_2_UL)

z_stat = u_L/np.sqrt(s_2_UL)
print("z_stat =", z_stat)
z_crit = stats.norm.ppf(1-((1-confidence_lvl)/tail))
print("z_crit =", z_crit)
if (abs(z_stat)>z_crit):
    print('Reject the NULL hypothesis. Data support a difference in survival outcome between the 2 groups')

else:
    print('Unable to reject the NULL hypothesis. Data failed to support any difference in survival outcome between the 2 groups')

#Adter rejecting the NULL hypothesis, we know p<0.05
p_value = 2.0*(1.0 - stats.norm.cdf(abs(z_stat)));
print("p_value =", p_value)

#-End-