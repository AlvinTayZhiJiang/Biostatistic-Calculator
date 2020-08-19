#Author: Alvin & Shawn (Prepared on: 14/04/2020)

#Chapter 4: Anova (Equal and unequal sample size)
#Accounted for if different sample size, n

import numpy as np
from scipy import stats

###############
# Input data  #
###############
#Please go thru every single input parameter
#n = sample size -> will be computed in the code

equal = True #Equal or unequal sample size
m = 3 #No. of grps
# if got more data grps, add another row to the data dict and update m accordingly
data = {
        0: [65.14,39.70,43.68,72.17],
        1: [70.22,75.18,66.30,73.53],
        2: [74.86,57.78,65.17,66.29],
}

#If need to input para go to line 92/137 and comment line 99/146 respectively

#For hypothesis testing
confidence_lvl = 0.95 #in decimals
t_tail = 2

###############
# DONT CHANGE #
###############
#Null hypothesis: No diff
#Alternate hypothesis: Have diff

#Multiple comparison produres
# In the event that any values are given, change here #
#True -> Bonferroni t test
#False -> Holm sidak t test
bonferroni = True

#An array to store cases that reject NUlL hypothesis during Bonferroni t test
reject = []

#Compute Bonferroni parameters
#i = position of set 1
#j = position of set 2
#para1 = n1, mean1, std1
#para2 = n2, mean2, std2
#s_sq_wit , t_crit_BONFE and t_tail are as follow
#Dfd = denominator of the dof (Equal or unequal)
def compute_bonferroni(i, j, para1, para2, s_sq_wit, t_crit_BONFE, Dfd, t_tail):
    print(i, "and", j)

    #Compute t_stat for each comparison
    t_stat = (para1[1] - para2[1])/np.sqrt((s_sq_wit/para1[0])+(s_sq_wit/para2[0]))
    print("t_stat:", t_stat)
    
    #Conclusion for each comparison
    if(np.abs(t_stat)>t_crit_BONFE):
        print("Reject the NULL hypothesis. Data support difference among the 2 groups")
    else:
        print("Unable to reject NULL hypothesis. Data failed to support difference among the 2 groups")
    
    #Compute p_value
    p_value = t_tail * (1.0 - stats.t.cdf(np.abs(t_stat),Dfd))
    print("p_value (Bonferroni):", p_value, "\n")
    
    return p_value
   
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
    sample_var = sum_sq/(n-1)
    
    #Input into para array
    para = [n, x_bar, sample_var]
    
    return para

#Compute the s_sq_wit and s_sq_bet
if(equal == True):
    para = {} #Dictionary to store [sample size, sample mean, sample var] of each group 
    j = 0
    s_sq_wit_sum = 0
    x_bar_x_bar_sum = 0
    for i in data: #Iterate thru data
        if i not in para:
            #Compute parameters for all data
            para[j] = compute_para(data[i])
            
            #Compute n sample size for Anova 
            n = para[j][0] #Equal sample size
            
            #Compute s_sq_wit_sum
            s_sq_wit_sum += para[j][2]

            #Compute x_bar_x_bar_sum
            x_bar_x_bar_sum += para[j][1]
            
            #Iterate thru para dict
            j += 1
            
            if j > m: #To prevent exceeding the number of groups (m) allowed
                break
    
    #Compute s_sq_wit and x_bar_x_bar
    s_sq_wit = s_sq_wit_sum/m
    x_bar_x_bar = x_bar_x_bar_sum/m
      
    #Compute s_sq_bet
    s_x_bar_sq_sum = 0
    for i in para:
        s_x_bar_sq_sum += (para[i][1] - x_bar_x_bar)**2
    s_x_bar_sq = s_x_bar_sq_sum / (m-1)
    
    s_sq_bet = n*s_x_bar_sq
    
    #Printing of s_sq_bet and s_sq_wit
    print("s_sq_bet:", s_sq_bet)
    print("s_sq_wit:", s_sq_wit)
    
    #Compute Dfn and Dfd
    Dfn = m-1 #numerator dof m-1
    Dfd = m*(n-1) #deonominator dof m(n-1)
    
else:
    para = {} #Dictionary to store [sample size, sample mean, sample var] of each group 
    j = 0
    s_s_wit = 0
    n_x_bar = 0
    n = 0
    n_x_bar_sq = 0
    for i in data:
        if i not in para:
            #Compute parameters for all data
            para[j] = compute_para(data[i])
            
            #Compute n sample size for Anova 
            n += para[j][0] #Unequal sample size (N) = sum of all n
            
            #Compute s_s_wit
            s_s_wit += (para[j][0]-1)*para[j][2]
            
            #Compute n_x_bar
            n_x_bar += para[j][0]*para[j][1]
            
            #Compute s_x_bar_sq
            n_x_bar_sq += para[j][0]*(para[j][1])**2
            
            #Iterate thru para dict
            j += 1
            
            if j > m: #To prevent exceeding the number of groups (m) allowed
                break
    
    #Compute s_sq_wit
    n_wit = n - m
    s_sq_wit = s_s_wit / n_wit

    #Compute s_sq_bet
    n_bet = m - 1
    s_s_bet = n_x_bar_sq - (n_x_bar)**2/ n
    s_sq_bet = s_s_bet/n_bet
    
    #Printing of s_sq_bet and s_sq_wit
    print("s_sq_bet:", s_sq_bet)
    print("s_sq_wit:", s_sq_wit)
    
    #Compute Dfn and Dfd
    Dfn = n_bet #numerator dof m-1
    Dfd = n_wit #deonominator dof N-m

#Compute F_ratio (F_stat)
F_ratio = s_sq_bet/s_sq_wit
print("F_ratio:", F_ratio, '\n')

#Compute f_crit
f_crit = stats.f.ppf(confidence_lvl,Dfn,Dfd)
print("f_crit:", f_crit)

#Conclusion
if (F_ratio>f_crit):
    print('Reject the NULL hypothesis. Data support a difference among the groups')
    
    #Compute p_value
    p_value = 1.0 - stats.f.cdf(F_ratio,Dfn,Dfd)
    print("p_value:", p_value, "\n")
    
    #Bonferroni t test
    #Compute number of comparisons
    k = int( m*(m-1)/2 )
    print('No. of comparison, k:', k)
    
    #Alpha determination
    if bonferroni == True:
        alpha_t = (1-confidence_lvl)/(k) #Bonferroni t test
    else:
        alpha_t = 1 - (1-(1-confidence_lvl))**(1/k) #Holm Sidak t test

    #Compute t_crit_BONF
    t_crit_BONFE = stats.t.ppf(1-alpha_t/t_tail, Dfd)
    print("t_crit (Bonferroni):", t_crit_BONFE, '\n')
    
    #Compute all Bonferroni p_value
    p_value_bonf = np.zeros(k)
    counter = 0
    for i in para:
        for j in para:
            if (i != j and j > i): #To prevent overlapping of case comparisons
             
                #Compute p value for all comparisons
                p_value_bonf[counter] = compute_bonferroni(i, j, para[i], para[j], s_sq_wit, t_crit_BONFE, Dfd, t_tail)
                
                #To compile cases that reject NULL hypothesis
                if p_value_bonf[counter]<alpha_t:        
                    temp = [i,j]
                    reject.insert(counter,temp)
                
                #Index the p_value_bonf
                counter += 1
                
    print('Cases that reject NULL hypothesis:', reject)  
          
else:
    print('Unable to reject the NULL hypothesis. Data failed to support any difference among the groups')
    
    #Compute p_value
    p_value = 1.0 - stats.f.cdf(F_ratio,Dfn,Dfd)
    print("p_value:", p_value, "\n")
    
#-End-