# -*- coding: utf-8 -*-
"""
Created on Thu Jan 19 10:25:23 2023

@author: Duha_Alkurdi
"""

 #%%
# imports
import itertools   # This module works as a fast, memory-efficient tool that is used either by themselves or in combination to form iterator algebra.   
from itertools import permutations 
 #%%
weather_condition = ["clear","rainy"]
day_time= ["morning","evening"]
area = ["city","rural"]
traffic_state = ["with","without"]

# using list comprehension 
# to compute all possible permutations
all_combinations = [[i, j, k, l] for i in weather_condition
                                 for j in day_time
                                 for k in area
                                 for l in traffic_state]
print (all_combinations)
 #%%
# for i in weather_condition:
#     for j in day_time:
#         for k in area:
#             for l in traffic_state:
#                 print("driving in a %s weather in the %s in the %s area %s traffic"%(i,j,k,l)) 
            
        
for i,j,k,l in all_combinations:    
    print("driving in a %s weather in the %s in the %s area %s traffic"%(i,j,k,l)) 