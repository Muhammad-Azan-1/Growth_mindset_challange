
# Creating a Image background removal 

#1. Libraries Used and Their Purpose

#? 1) streamlit is a Python library used to create interactive web applications with minimal effort.
import streamlit as st  


#? 2) rembg r is a powerful Python library used for background removal from images. It uses deep learning models to remove the background and return a transparent PNG.
from rembg import remove


#? 3) Pillow (Python Imaging Library) is used for handling and processing images in Python. It allows opening, manipulating,  and saving different 
#? image formats efficiently.
#! Core Purpose of Pillow:
#? Pillow is a powerful image-processing library in Python that allows you to:
#? Open images in different formats (JPEG, PNG, BMP, etc.).
#? Edit & Manipulate images (resize, crop, rotate, filter, enhance).
#?  Convert images to different modes (grayscale, RGB, CMYK, etc.).
#? Save images in different formats (PNG, JPG, GIF, etc.).
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


#nfunction that helo the user to donwload the image they uploaded after the image background was removed
def download_image(img):
    buf = BytesIO()  # BytesIO() initializes a temporary space in memory where binary data (like images) can be stored.
 
    img.save(buf, format="PNG")  # Save the image into the buffer as PNG

    image_from_buff_memory = buf.getvalue()
    return image_from_buff_memory




# function handle the image uploaded by user
def get_uploaded_image(image):
    image = Image.open(image) 
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
    st.sidebar.download_button("Download your Image" , download_image(remove_image_bg)) #passing the background removed image to the download_image function
  






uploaded_image = st.sidebar.file_uploader("Upload your Imagex" , type = ["png" , "jpg" ,"jpeg"])
#? when we upload a image using this (st.sidebar.file_uploader)
#? it returns an UploadedFile object. This object contains metadata about the uploaded file. which shown as below


if uploaded_image is not None:

    if uploaded_image.size > max_file_size:
        st.error("The file is too large to bw uploaded . make sure you have uploaded a file of 5 MB or less.")

    else:
        get_uploaded_image(uploaded_image)
       # print("uploaded file"  , uploaded_image)


else:
    get_uploaded_image("assests/ghost.jpg")











# UploadedFile(
#     file_id='5b3ccfc1-3f7f-450d-acb9-444ce783cdef',  # Unique file ID  #? A unique identifier assigned to the uploaded file.
#     name='WhatsApp Image 2025-02-15 at 21.02.33.jpeg',  # Original file name  #? The original filename of the uploaded image.
#     type='image/jpeg',  # MIME type (JPEG format) #? The MIME type (e.g., image/jpeg, image/png).
#     size=57385,  # File size in Bytes (≈ 57 KB) #? The file size in Bytes (57385 Bytes ≈ 57 KB).
#     _file_urls=file_id: "5b3ccfc1-3f7f-450d-acb9-444ce783cdef",
#     upload_url: "/_stcore/upload_file/...",  #? The temporary upload path used internally by Streamlit.
#     delete_url: "/_stcore/upload_file/..." #? The temporary delete path for the file
# )



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