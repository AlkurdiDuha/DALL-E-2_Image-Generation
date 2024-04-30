# -*- coding: utf-8 -*-
"""
Created on Thu Jan 19 16:31:19 2023

@author: Duha_Alkurdi
"""

 #%%
# imports
import openai  # OpenAI Python library to make API calls
import requests  # used to download images
import os  # used to access filepaths
from PIL import Image  # used to print and edit images
import itertools  # This module works as a fast, memory-efficient tool that is used either by themselves or in combination to form iterator algebra. 
from itertools import permutations
import pandas as pd   # used to export the results to an external .xlsx file
import numpy as np

# set API key
openai.api_key = os.environ.get("OPENAI_API_KEY")
 #%%
# set a directory to save DALL-E images to
image_dir_name = "images"
image_dir = os.path.join(os.curdir, image_dir_name)

# create the directory if it doesn't yet exist
if not os.path.isdir(image_dir):
    os.mkdir(image_dir)

# print the directory to save to
print(f"{image_dir=}") 
 #%%
# generating different prompts  
weather_condition = ["clear","rainy"] # gloomy
day_time= ["morning","evening"]
area = ["city","rural"] # highway
traffic_state = ["with","without"]

# using list comprehension 
# to compute all possible permutations
all_combinations = [[i, j, k, l] for i in weather_condition
                                 for j in day_time
                                 for k in area
                                 for l in traffic_state]
print (all_combinations)

 #%%

for i,j,k,l in all_combinations:    
    print("driving in a %s weather in the %s in the %s area %s traffic"%(i,j,k,l)) 
    prompt = "driving in a %s weather in the %s in the %s area %s traffic"%(i,j,k,l)
    
    # set number of images to produce
    total_images = 4 # using this way to adjust the number of n in generation_response has highly affected the run time 

# creating an instance of openai.Image and calls .create() on it. 
# "prompt"; passes the value of PROMPT to the prompt parameter. With that, you give DALL·E the text that it’ll use to create the image.
# "n"; passes the integer 1 to the parameter n. This parameter defines how many new images to create with the prompt. Nuber between (1,10)
# "size"; defining the dimensions of the image that DALL·E should generate. The argument needs to be a string—either "256x256", "512x512", or "1024x1024". Each string represents the dimensions in pixels of the image that you’ll receive. It defaults to the largest possible setting, 1024x1024.
# "response_format"; defining the format of the response, I beleive we can get away with not specifying this line 

    generation_response = openai.Image.create(
    prompt=prompt,
    n=4,
    size="1024x1024",
    response_format="url",
    ) 

 #%%
# save the image
#generated_image_name = "generated_image.png"  # any name you like; the filetype should be .png
    generated_image_filepath = os.path.join(image_dir)



    all_urls = [datum["url"] for datum in generation_response["data"]]  # extract URLs
    all_images = [requests.get(url).content for url in all_urls]  # download images
    produced_images_names = [f"produced_image_{i}_{j}_{k}_{l}_{m}.png" for m in range(4)]  # create names
    produced_images_filepaths = [os.path.join(image_dir, name) for name in produced_images_names]  # create filepaths
    for image, filepath in zip(all_images, produced_images_filepaths):# loop through the variations
        with open(filepath, "wb") as image_file: # open the file
            image_file.write(image) 
      
        
 #%%              
# creating the .xlsx file to hold the results

# creating the Pandas DataFrame
all_images = [[i, j, k, l, m] for i in weather_condition
                              for j in day_time
                              for k in area
                              for l in traffic_state
                              for m in range (4)]
parameters = ['weather_condition', 'day_time', 'area', 'traffic_state', 'Count']
df = pd.DataFrame(all_images, columns=parameters)
print(df)

# write DataFrame to Excel file with sheet name
df.to_excel('HFES_DALLE_Driving.xlsx', sheet_name='Suggested_Parametrs', index = False) # index = False to get rid of the auto-generated numbers besides each row

 #%%