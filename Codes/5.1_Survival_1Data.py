#Author: Alvin & Shawn (Prepared on: 16/04/2020)
#Function Author: Dr Alberto

#Chapter 6: Analysis of Survival Data (1 Data)

import numpy as np
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
data = [2,1,6,1,7,1,7,1,7,0,8,1,9,1,11,0,12,1,12,0] 
row = 10 #row = number of data, **account for each individual patient

###############
# DONT CHANGE #
###############
#No. of cols depend on whether existing time was given (refer to line 15-26) - Exclude patient no.
if difference_given == True: # == Existing time (event - enrol)
    col = 2
else:
    col = 3

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

#Input data into observed contingency table
table = np.zeros((row,col))
counter = 0
for i in range(0,row):
    for j in range(0,col):
        table[i,j] = data[counter]
        counter += 1   
                
if difference_given == True:
    time = table[:,0]
    event_type = table[:,1]

else:
    time = table[:,1] - table[:,0]
    event_type = table[:,2]

survival = compute_survival(time,event_type)

plt.figure(1);
plt.plot(survival[6],survival[7], 'b-')

#Print S_hat(t) table
print('Survival_time Frac_survive S_hat(t)')
array = np.zeros((len(survival[0]),3))
array[:,0] = survival[0]
array[:,1] = survival[8]
array[:,2] = survival[1]
print(array)
print('**Note: excluding lost to follow up.\n')

#Median survival times
t_deaths = survival[0]
s_hat = survival[1]
median = 0
for i in range(0,len(t_deaths)):
    if (s_hat[i]<0.5):
        median = t_deaths[i]
        break
    
print('Median survival time for data is ',median, '(time unit).')
    
#-End-