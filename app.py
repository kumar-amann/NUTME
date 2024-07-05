### Nutrition Management APP 

# Loading Environment Variables

from dotenv import load_dotenv

load_dotenv() 


# importing the libraries required 

import streamlit as st
import os
import google.generativeai as genai
from PIL import Image

# genai access key configuring 

genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))


## Function to load Google Gemini Pro Vision API And get response

def get_gemini_repsonse(input,image,prompt):
     model=genai.GenerativeModel('gemini-1.5-flash')
    # model=genai.GenerativeModel('gemini-pro-vision')
    response=model.generate_content([input,image[0],prompt])
    return response.text



def input_image_setup(uploaded_file):

    # Check if a file has been uploaded

    if uploaded_file is not None:
        # Read the file into bytes
        bytes_data = uploaded_file.getvalue()

        image_parts = [
            {
                "mime_type": uploaded_file.type,  # Get the mime type of the uploaded file
                "data": bytes_data
            }
        ]
        return image_parts
    else:
        raise FileNotFoundError("No file uploaded")
    
    
##initialize our streamlit app

st.set_page_config(page_title="NutriScan App")

# Adding the Header Title of the Web app

st.header("NutriScan 🥗")

# Adding the tagline to be used 

st.write("Revitalize Your Wellness, One Bite at a Time with NutriScan!😋")

# intializing the input boxes for asking questions

input=st.text_input("Let me Check : ",key="input")

# adding the upload image button of the desired food material

uploaded_file = st.file_uploader("Choose an image...", type=["jpg", "jpeg", "png"])
image=""   
if uploaded_file is not None:
    image = Image.open(uploaded_file)
    st.image(image, caption="Uploaded Image.", use_column_width=True)


# Adding Submit button for submitting the input questions and the image 
# for further processing....
    
submit=st.button("Get Response!!")

# fine Tunning the model for acting as a Nutritionist which can analyse the food contents in the 
# image provided as input and answer the relvant question on the basis of the image....

input_prompt="""
            You are an expert in nutritionist where you need to see the food items from the image and calculate
            the quantity and then the total calories, and check whether it conatins protein or carbohydrates or fats and also tell each item is rich in which Vitamin.Also provide the details of every food items with calories intake
            is below format

               1. Item 1(quantity) - no of calories , protein/carbohydrates/fats content, Rich in Vitamin.   
               2. Item 2(quantity) - no of calories , protein/carbohydrates/fats content, Rich in Vitamin.  
               ----
               ----

        Finally you can also mention whether the food is healthy or not and also mention the
        percentage split of the ratio of carbohydrates , fats, fibers, proteins, vitamins and other important things required in our diet.


"""

## If submit button is clicked
## Display the output based on the input question and image.....

if submit:
    image_data=input_image_setup(uploaded_file)
    response=get_gemini_repsonse(input_prompt,image_data,input)
    st.subheader("The Response is")
    st.write(response)

