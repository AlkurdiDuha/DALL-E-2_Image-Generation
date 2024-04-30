# -*- coding: utf-8 -*-
"""
Created on Thu Jan 19 10:25:23 2023

@author: Duha_Alkurdi
"""

 #%%
# imports
import openai  # OpenAI Python library to make API calls
import requests  # used to download images
import os  # used to access filepaths
from PIL import Image  # used to print and edit images
import itertools   # This module works as a fast, memory-efficient tool that is used either by themselves or in combination to form iterator algebra. 
from itertools import permutations

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
weather_condition = ["clear","rainy"]
day_time= ["morning","evening"]
# area = ["city","rural"]
# traffic_state = ["with","without"]

# create empty list to store the
# combinations
unique_combinations = []

# Getting all permutations of list_1
# with length of list_2
permut = itertools.permutations(weather_condition, len(day_time))

# zip() is called to pair each permutation
# and shorter list element into combination
for comb in permut:
	zipped = zip(comb,day_time)
	unique_combinations.append(list(zipped))

# printing unique_combination list
print(unique_combinations)
 #%% 
# trying to access the different combinations 
for i,j in unique_combinations:
    print(i,j)

 #%%

for k in range(len(unique_combinations)):
    for (i,j) in unique_combinations[k]:
        print("driving in a %s weather in the %s"%(i,j))
        prompt = ("driving in a %s weather in the %s"%(i,j))
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
        produced_images_names = [f"produced_image_{k}_{i}_{j}.png" for k in range(4)]  # create names
        produced_images_filepaths = [os.path.join(image_dir, name) for name in produced_images_names]  # create filepaths
        for image, filepath in zip(all_images, produced_images_filepaths):  # loop through the variations
         with open(filepath, "wb") as image_file:  # open the file
            image_file.write(image) 
 #%%              
              