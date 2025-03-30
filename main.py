
# Creating a Image background removal 

#1. Libraries Used and Their Purpose

#? 1) streamlit is a Python library used to create interactive web applications with minimal effort.
import streamlit as st  


#? 2) rembg r is a powerful Python library used for background removal from images. It uses deep learning models to remove the background and return a transparent PNG.
from rembg import remove


#? 3) Pillow is a Python library for image processing that converts raw binary image data into an actual image object, allowing users to open, 
#? display, edit, and save images in various formats (JPEG, PNG, BMP, etc.). It provides tools for resizing, 
 #? cropping, filtering, format conversion, and other image manipulations.

#! Core Purpose of Pillow:
#? Pillow is used to open, edit, and save images in Python.
#? ✔ Pillow converts binary image data into an actual image object that Python can process, display, and modify etc
#? ✔ It allows us to modify images (crop, resize, remove background, etc.).
#? ✔ Without it, uploaded images are just raw data that cannot be processed directly.
from PIL import Image 


#? 4) io.BytesIO The io module in Python provides an in-memory byte-stream class called BytesIO. This is used to temporarily store 
#? image data (binary data) in memory.
from io import BytesIO


#? 5)  base64 module is used for encoding binary data (like images) into text format.
#! Transmission Over Text-Based Systems:
#? Some systems (like HTML, JSON, and email) primarily handle text and may not support raw binary data.
#? Encoding allows binary files (like images) to be sent as text.
#? Storage in Text-Based Databases:
#? Some databases only store text data. Encoding allows us to store images and other binary files as strings
import base64



import pathlib

st.set_page_config(layout="wide", page_title="Image Background Remover") #? By default, Streamlit apps have a narrow layout, meaning content is displayed in a centered column with limited width.Setting layout="wide" makes the app use the full width of the screen, allowing content to stretch and making better use of available space.


# function to load Css
css_path = pathlib.Path("styles/global.css")
def load_external_css():
    """Loads an external CSS file in Streamlit"""
    if css_path.exists():  # Check if the CSS file exists
        with open(css_path, "r") as f:
            css = f.read()
            st.markdown(f"<style>{css}</style>", unsafe_allow_html=True)
    else:
        st.warning("⚠️ CSS file not found! Check the path.")

# Call the function to load the CSS
load_external_css()


st.markdown("<h2 style='text-align:center; color:black; margin-bottom:50px'>Welcome to background image removal App</h2>" , unsafe_allow_html=True)
st.sidebar.write("<h1 style='color:black'>Upload your Image ⚙️</h1>" , unsafe_allow_html=True) 



#! first we have to decide what  maximum size of file user can upload to remove the background image

max_file_size = 5 * 1024 * 1024

#? converting MB to Btyes Since 1 MB = 1024 KB, and 1KB = 1024 Bytes so we will max allow the file size to be 5MB which is 5,242,880 btyes
#? in above  max_file_size we are converting file size from MB to bytes  because computers store and process data in Bytes, not MB.
#?When handling file uploads, most programming languages (including Python & Streamlit) measure file sizes in Bytes.




col1 , col3, col2 = st.columns([1, 0.2, 1])


#function that helo the user to donwload the image they uploaded after the image background was removed
def download_image(img):
    buf = BytesIO() # BytesIO() initializes a temporary space in memory where binary data (like images) can be stored.
 
    img.save(buf, format="PNG") # Step 2: It converts the Pillow image object into binary format so that it can be saved, transferred, or downloaded.

    image_from_buff_memory = buf.getvalue() #   # Step 3: Retrieve the binary data from the buffer
    print(image_from_buff_memory)
    return image_from_buff_memory




# function handle the image uploaded by user
def get_uploaded_image(image):
    image = Image.open(image)   # Open uploaded binary image and convert it to an actual image object that python can work with
    #print(image)
    with col1:
        st.write("Original image :camera:")
        st.image(image)
  
   
    remove_image_bg = remove(image).convert("RGBA")
    #print(remove_image_bg)


    with col2:
        st.write("Image without Background :mag_right:")
        st.image(remove_image_bg)

    st.sidebar.markdown("\n")
    st.sidebar.write("<h1 style='color:black'>Download your Image ⚙️</h1>" , unsafe_allow_html=True) 
    st.sidebar.download_button("Download your Image" , 
        data=download_image(remove_image_bg), # This ensures you're passing the actual binary data, not the function.
        file_name="background_removed_image.png",  # You can specify a default filename for the image
        mime="image/png"  # MIME type for PNG images
        ) #passing the background removed image to the download_image function
  






uploaded_image = st.sidebar.file_uploader("Upload your Imagex" , type = ["png" , "jpg" ,"jpeg"])
#? when we upload a image using this (st.sidebar.file_uploader)
#? it returns an UploadedFile object. This object contains  Metadata → File name, type, size, etc. and  
 #? Binary data → The actual image content (accessed via .getvalue()).
#? The uploaded file is stored as a Streamlit UploadedFile object.


if uploaded_image is not None:
    binary_data = uploaded_image.getvalue()  # ✅ This is the actual binary data of Image  (the actual image content)
    # st.write(binary_data) 

    if uploaded_image.size > max_file_size:
        st.error("The file is too large to bw uploaded . make sure you have uploaded a file of 5 MB or less.")

    else:
        get_uploaded_image(uploaded_image)
       # print("uploaded file"  , uploaded_image)


else:
    get_uploaded_image("assests/ghost.jpg")













#! inside get_uploaded_image function

#! 1)
#? Image.open(image) is a function from the Pillow (PIL) library that opens an image file and loads it into a format 
#? that Python can work with.

#?  It reads the uploaded image file.
#?  It converts it into a Pillow Image object.
#?  You can now manipulate, edit, or display the image in Python.

#! 2)
#? col1 , col2 = st.columns(2) is a Streamlit layout function that creates two equal-width columns in your app. first colum content will be added using col1 same for col2
#? In Streamlit, col1 is likely a column created using st.columns(). It allows you to arrange elements side by side instead of 
#? stacking them vertically.

#? images are always stored as binary data, no matter the format (JPEG, PNG, BMP, etc.).




#! Python does understand binary data, but it cannot directly process or manipulate an image from raw binary data.

# Why Pillow is Needed:
# ✅ Binary image data (from file upload) is just a stream of bytes.
# ✅ Python can read binary data, but it doesn't "know" it's an image.
# ✅ Pillow converts the binary data into an actual image object that Python can work with (display, edit, modify, etc.).

# 📌 Without Pillow, Python only sees raw bytes, not an image.
# 📌 Pillow acts as a translator, making the image usable in Python.

# 🚀 So, Python understands binary, but it needs Pillow to process images! ✅



#! We convert a Pillow image object back to binary for several reasons:

# 1️⃣ To Save or Download the Image
# Python and web apps (like Streamlit) handle downloads using binary data.
# A Pillow image object cannot be downloaded directly—it must first be converted into a binary format using BytesIO().




#! img.save(buf, format="PNG") does two things:

# Converts the Pillow image object (img) into binary format (so it can be stored or transferred).
# Specifies that the binary data should be saved in the PNG format.
