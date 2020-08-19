#Author: Alvin & Shawn (Prepared on: 15/04/2020)

#Chapter 5: Nominal
#Accounted for 2x2 table and other table sizes

import numpy as np
from scipy import stats

###############
# Input data  #
###############
#Please go thru every single input parameter
#Input data in a left to right manner -> similar to reading a book
row = 4 #DO NOT INCLUDE THE TOTAL ROW
col = 2 #DO NOT INCLUDE THE TOTAL COL
percentage = False #Eg. National average (in %)
data = [46238,91,38667,118,8464,33,14152,56] #If percentage given, input values in % form, ie 43%

#For hypothesis testing
confidence_lvl = 0.95 #in decimals 
                      #Chi_sq distribution always 1 tail

###############
# DONT CHANGE #
###############
#An array to store cases that reject NUlL hypothesis during Bonferroni t test
reject = []

#Compute Bonferroni parameters
#row1 = position of set 1
#row2 = position of set 2
#Observed table and chi_sq_crit_BONFE are as follow
def compute_bonferroni(row1, row2, observed_table, chi_sq_crit_BONFE):
    print(row1, "and", row2)
    
    #Split table into 2x2 observed contingency table for Bonferroni 
    table_2x2 = observed_table[[row1,row2],:]
    print(table_2x2)
    
    #Compute sum of row
    if percentage == False:
        table_2x2_row_sum = np.zeros(2)
        for i in range(0, 2):
            for j in range(0,2):
                table_2x2_row_sum[i] += table_2x2[i,j]
                
    #Compute sum of col
    table_2x2_col_sum = np.zeros(2)        
    for j in range(0, 2):
        for i in range(0, 2):
            table_2x2_col_sum[j] += table_2x2[i,j]
    
    #Compute total population in table
    total_2x2 = 0
    for i in range(0, 2):
        if percentage == False:
            total_2x2 += table_2x2_col_sum[i]
        else:
            total_2x2 = table_2x2_col_sum[1]
     
    #Compute expected contingency table
    if percentage == False:
        expected_table_2x2 = np.zeros((2,2))
        for i in range(0, 2):
            for j in range(0, 2):
                expected_table_2x2[i,j] = (table_2x2_row_sum[i] * table_2x2_col_sum[j])/total_2x2
    
        print(expected_table_2x2)
    
    #Compute chi_sq_stat
    chi_sq_stat_BONF = 0
    for i in range(0, 2):
        if percentage == True:
              chi_sq_stat_BONF += ((np.abs(table_2x2[i,1] - ((table_2x2[i,0]/table_2x2_col_sum[0])*total_2x2)) - 0.5)**2)/((table_2x2[i,0]/table_2x2_col_sum[0])*total_2x2)
        else:
            for j in range(0, 2):
                chi_sq_stat_BONF += ((np.abs(table_2x2[i,j]-expected_table_2x2[i,j]) - 0.5)**2)/expected_table_2x2[i,j]
                
    print('chi_sq_stat_BONF:', chi_sq_stat_BONF)

    #Conclusion for each comparison
    if(chi_sq_stat_BONF>chi_sq_crit_BONFE):
        print("Reject the NULL hypothesis. Data support difference among the 2 groups")
    else:
        print("Unable to reject NULL hypothesis. Data failed to support difference among the 2 groups")
    
    #Compute p_value
    p_value = 1.0 - stats.chi2.cdf(chi_sq_stat_BONF,1)
    print("p_value (Bonferroni):", p_value, "\n")
    
    return p_value

#Input data into observed contingency table
table = np.zeros((row,col))
counter = 0
for i in range(0,row):
    for j in range(0,col):
        table[i,j] = data[counter]
        counter += 1
        
#Compute dof
dof = (row-1) * (col-1)

#Compute sum of row
if percentage == False:
    table_row_sum = np.zeros(row)
    for i in range(0, row):
        for j in range(0,col):
            table_row_sum[i] += table[i,j]
        
#Compute sum of col
table_col_sum = np.zeros(col)        
for j in range(0, col):
    for i in range(0, row):
        table_col_sum[j] += table[i,j]

#Compute total population in table
total = 0
if percentage == False:
    for i in range(0, col):
        total += table_col_sum[i]
else:
    total = table_col_sum[1]
 
#Compute expected contingency table
if percentage == False:
    expected_table = np.zeros((row,col))
    for i in range(0, row):
        for j in range(0, col):
            expected_table[i,j] = (table_row_sum[i] * table_col_sum[j])/total

#Compute chi_sq_stat
chi_sq_stat = 0
for i in range(0, row):
    if percentage == True:
        if row == 2 and col == 2: 
            chi_sq_stat += ((np.abs(table[i,1] - ((table[i,0]/100.0)*total)) - 0.5)**2)/((table[i,0]/100.0)*total) 
        else:
            chi_sq_stat += ((table[i,1] - ((table[i,0]/100.0)*total))**2)/((table[i,0]/100.0)*total) 
    else:
        for j in range(0, col):
            if row == 2 and col == 2: 
                chi_sq_stat += ((np.abs(table[i,j]-expected_table[i,j]) - 0.5)**2)/expected_table[i,j] 
            else:
                chi_sq_stat += ((table[i,j]-expected_table[i,j])**2)/expected_table[i,j]
                
print('chi_sq_stat:', chi_sq_stat)

#Compute chi_sq_crit        
chi_sq_crit = stats.chi2.ppf(confidence_lvl, dof)
print('chi_sq_crit:', chi_sq_crit)

#Conclusion
if(chi_sq_stat>chi_sq_crit):
    print('Reject the NULL Hypothesis. Data support a difference in the in the results between the', row,' groups.')
   
    #Compute p_value
    p_value = 1.0 - stats.chi2.cdf(chi_sq_stat,dof)
    print('p_value:', p_value,'\n')
    
    #Bonferroni t test
    #Compute number of comparisons
    k = int(row*(row - 1)/2)
    print('No. of comparison, k:', k)
    
    #Compute t_crit_BONF
    chi_sq_crit_BONFE = stats.chi2.ppf(1-(1-confidence_lvl)/k, 1)
    print("chi_sq_crit (Bonferroni):", chi_sq_crit_BONFE, '\n')
    
    #Compute all Bonferroni p_value
    p_value_bonf = np.zeros(k)
    counter = 0
    for i in range(0,row):
        for j in range(0,row):
            if (i != j and j > i): #To prevent overlapping of case comparisons
                
                #Compute p value for all comparisons
                p_value_bonf[counter] = compute_bonferroni(i, j, table, chi_sq_crit_BONFE)
                
                #To compile cases that reject NULL hypothesis
                if p_value_bonf[counter]<((1-confidence_lvl)/k):        
                    temp = [i,j]
                    reject.insert(counter,temp)
                
                #Index the p_value_bonf
                counter += 1
                
    print('Cases that reject NULL hypothesis:', reject)  
    
else:
    print('Do not reject the NULL Hypothesis. Data failed to support a difference in the results between the', row,' groups.\n')
    
    #Compute p_value
    p_value = 1.0 - stats.chi2.cdf(chi_sq_stat,dof)
    print('p_value:', p_value)

#-End-