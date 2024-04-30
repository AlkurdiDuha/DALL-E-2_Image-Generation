# -*- coding: utf-8 -*-
"""
Created on Mon Jan 16 21:22:16 2023

@author: Duha_Alkurdi
"""
 # NOW PRODUCING PermissionError: [Errno 13] Permission denied: '.\\image'
 #%%
# imports
import openai  # OpenAI Python library to make API calls
import requests  # used to download images
import os  # used to access filepaths
from PIL import Image  # used to print and edit images
from pathlib import Path

# set API key
openai.api_key = os.environ.get("OPENAI_API_KEY")
 #%%
# set a directory to save DALL-E images to
image_dir_name = "image"
image_dir = os.path.join(os.curdir, image_dir_name)

# create the directory if it doesn't yet exist
if not os.path.isdir(image_dir):
    os.mkdir(image_dir)

# print the directory to save to
print(f"{image_dir=}")



 #%%
# create an image

# set the prompt
prompt = "Driving in a rainy morning in the city with traffic"

# creating an instance of openai.Image and calls .create() on it. 
# "prompt"; passes the value of PROMPT to the prompt parameter. With that, you give DALL·E the text that it’ll use to create the image.
# "n"; passes the integer 1 to the parameter n. This parameter defines how many new images to create with the prompt. Nuber between (1,10)
# "size"; defining the dimensions of the image that DALL·E should generate. The argument needs to be a string—either "256x256", "512x512", or "1024x1024". Each string represents the dimensions in pixels of the image that you’ll receive. It defaults to the largest possible setting, 1024x1024.
# "response_format"; defining the format of the response, I beleive we can get away with not specifying this line 
generation_response = openai.Image.create(
    prompt=prompt,
    n=1,
    size="1024x1024",
    response_format="url",
) 


 #%%
# save the image
generated_image_name = "generated_image.png"  # any name you like; the filetype should be .png
generated_image_filepath = os.path.join(image_dir)
generated_image_url = generation_response["data"][0]["url"]  # extract image URL from response
generated_image = requests.get(generated_image_url).content  # download the image
   


with open(generated_image_filepath, "wb") as image_file:
    image_file.write(generated_image)  # write the image to the file
  #%%
# print the image
print(generated_image_filepath)    
#display(Image.open(generated_image_filepath))
  #%%
# create variations

# call the OpenAI API, using `create_variation` rather than `create`
variation_response = openai.Image.create_variation(
    image=generated_image,  # generated_image is the image generated above
    n=2,
    size="1024x1024",
    response_format="url",
)

# print response
print(variation_response)
  #%%
# save the images
variation_urls = [datum["url"] for datum in variation_response["data"]]  # extract URLs
variation_images = [requests.get(url).content for url in variation_urls]  # download images
variation_image_names = [f"variation_image_{i}.png" for i in range(len(variation_images))]  # create names
variation_image_filepaths = [os.path.join(image_dir, name) for name in variation_image_names]  # create filepaths
for image, filepath in zip(variation_images, variation_image_filepaths):  # loop through the variations
    with open(filepath, "wb") as image_file:  # open the file
        image_file.write(image)  # write the image to the file 
  #%%
# print the original image
print(generated_image_filepath)
#display(Image.open(generated_image_filepath))

# print the new variations
for variation_image_filepaths in variation_image_filepaths:
    print(variation_image_filepaths)
    #display(Image.open(variation_image_filepaths))    
  #%%  