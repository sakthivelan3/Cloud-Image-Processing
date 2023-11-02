import streamlit as st

import cv2
import numpy as np
from streamlit_option_menu import option_menu
from PIL import Image
import base64
st.set_page_config(page_title="Image Wizard", layout="wide")

# -- use local CSS
def local_css(file_name):
      with open(file_name) as f:
            st.markdown(f"<style>{f.read()}</style>",unsafe_allow_html=True)


local_css("styles/styles.css")

# --------- Header Section -------
with st.container():
      left_column, right_column = st.columns(2)
      with left_column:
            st.subheader("Image Wizard")
            st.title("Welcome to ImageWizard - Your Ultimate Image Enhancement and Editing Platform")
            st.write("Are you looking to transform your ordinary photos into extraordinary masterpieces? Look no further! ImageWizard is your one-stop solution for all your image enhancement and editing needs. Whether you're a photography enthusiast, a professional photographer, or just someone who wants to make your images pop, we've got you covered.")

      with right_column:
            file_ = open("./images/desktop_computer.gif", "rb")
            contents = file_.read()
            data_url = base64.b64encode(contents).decode("utf-8")
            file_.close()

            st.markdown(
            f'<img src="data:image/gif;base64,{data_url}" alt="cat gif">',
            unsafe_allow_html=True,
            )

      st.write("---")
      st.write("Upload an image for processing.")
      # Upload an image using st.file_uploader
      uploaded_image = st.file_uploader("Choose an image...", type=["jpg", "png", "jpeg"])
      # ****************************** image enhancement *************************
      if uploaded_image is not None:
      
            # Display the uploaded image
            left_column, rigth_column = st.columns(2)
            with left_column: 
                  st.image(uploaded_image, use_column_width=True, caption="Original Image")
            with rigth_column:
                  st.empty()
            # Perform color image enhancement on the uploaded image
            if st.button("Enhance Image"):
                  # Read and process the uploaded image
                  image = cv2.imdecode(np.fromstring(uploaded_image.read(), np.uint8), 1)

                  l, a, b = cv2.split(image)

                  # Apply CLAHE to the L channel (luminance)
                  clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8, 8))
                  enhanced_l = clahe.apply(l)

                  # Merge the enhanced L channel with the original A and B channels
                  enhanced_lab = cv2.merge((enhanced_l, a, b))
                        
                  # Convert the LAB image back to BGR color space
                  enhanced_image = cv2.cvtColor(enhanced_lab, cv2.COLOR_BGR2RGB)

                  enhanced_image = Image.fromarray(enhanced_image)
                  # Display the enhanced image
                  left_column, right_column = st.columns(2)
                  with left_column:
                        st.image(enhanced_image, use_column_width=True, caption="Enhanced Image")
                  with right_column:
                        st.empty()
       
            # ****************************** image sharpening *************************

            # Perform color image sharpening on the uploaded image
            if st.button("Sharpen Image"):
                  # Read and process the uploaded image
                  image = cv2.imdecode(np.fromstring(uploaded_image.read(), np.uint8), 1)

                  # Convert the image to a float32 format
                  image = image.astype(np.float32) / 255.0

                  # Apply image sharpening using the Laplacian filter
                  sharpened_image = cv2.filter2D(image, -1, kernel=np.array([[-1, -1, -1], [-1, 9, -1], [-1, -1, -1]]))

                  # Clip pixel values to ensure they remain in the valid range
                  sharpened_image = np.clip(sharpened_image * 255, 0, 255).astype(np.uint8)

                  sharpened_image=cv2.cvtColor(sharpened_image, cv2.COLOR_BGR2RGB)

                  # Display the sharpened image
                  left_column, right_column = st.columns(2)
                  with left_column:
                        st.image(sharpened_image, use_column_width=True, caption="Sharpened Image")
                  with right_column:
                        st.empty()

            # ****************************** image saturation *************************

            # Perform saturation adjustment on the uploaded image
            if st.button("Adjust Saturation"):
                  # Read and process the uploaded image
                  image = cv2.imdecode(np.fromstring(uploaded_image.read(), np.uint8), 1)

                  # Convert the image to the HSV color space
                  hsv_image = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

                  # Adjust the saturation (increase or decrease) by modifying the S channel
                  saturation_factor = 1.5  # Increase saturation (1.0 for no change, values < 1.0 decrease saturation)
                  hsv_image[:, :, 1] = np.clip(hsv_image[:, :, 1] * saturation_factor, 0, 255)

                  # Convert the HSV image back to the BGR color space
                  adjusted_image = cv2.cvtColor(hsv_image, cv2.COLOR_HSV2RGB)

                  # Display the adjusted image
                  left_column, right_column = st.columns(2)
                  with left_column:
                        st.image(adjusted_image, use_column_width=True, caption="Adjusted Saturation Image", channels='RGB')
                  with right_column:
                        st.empty()

            # Image smoothing
            if st.button("Image Smooth"):
                  image=cv2.imdecode(np.fromstring(uploaded_image.read(), np.uint8), 1)
                  simple_average_kernel = np.array([[1,1,1],[1,1,1],[1,1,1]]) * 1/9
                  simple_average_image = cv2.filter2D(src=image,ddepth=-1,kernel=simple_average_kernel)
                  smoothened_image = cv2.cvtColor(simple_average_image, cv2.COLOR_BGR2RGB)

                  #Displaying smooothned image 
                  left_column, right_column = st.columns(2)
                  with left_column:
                        st.image(smoothened_image,use_column_width=True, caption="Smoothened Image", channels='RGB')
                  with right_column:
                        st.empty()

      # ---------- What We Provide ------

      with st.container():
            st.write("---")
            st.title("What we Offer")
            left_column, right_column = st.columns(2)
            with left_column:
                  st.markdown("<h3 style='text-align: center;'>Image Enhancement</h3>", unsafe_allow_html=True)
                  st.write("Our cutting-edge image enhancement technology will breathe life into your photos. Say goodbye to dull and lifeless images! Our team of expert editors and powerful algorithms work together to enhance the color, contrast, and overall quality of your images.")
                  image = Image.open("./images/enhancement.jpg")
                  st.image(image,use_column_width=True)
            with right_column:
                  st.markdown("<h3 style='text-align: center;'>Image Filtering</h3>", unsafe_allow_html=True)
                  st.write("Create unique and artistic effects with our diverse range of image filters. From vintage and sepia tones to modern, high-contrast looks, you can apply filters that match your style and vision. Customize the filter intensity to achieve the perfect result.")
                  image = Image.open("./images/dog.png")
                  st.image(image,use_column_width=True)
            left_column, right_column = st.columns(2)
            with left_column:
                  st.markdown("<h3 style='text-align: center;'>Image Saturation</h3>", unsafe_allow_html=True)
                  st.write("Fine-tune the vibrancy and color intensity of your images with our image saturation adjustment tool. Whether you want to make colors pop or create a soft, pastel effect, our tools give you full control over image saturation.")
                  image = Image.open("./images/saturation.png")
                  st.image(image,use_column_width=True)
            with right_column:
                  st.markdown("<h3 style='text-align: center;'>Image Sharpening</h3>", unsafe_allow_html=True)
                  st.write("Ensure every detail in your images is crisp and clear with our image sharpening tools. Perfect for bringing out intricate details in landscapes, portraits, and more. You'll be amazed at how sharp and professional your images can look.")
                  image = Image.open("./images/sharpening.png")
                  st.image(image,use_column_width=True)

      # ---------- Contact US --------

      with st.container():
            st.write("---")
            st.header("Get in Touch with me")
            st.write('##')

            # https://formsubmit.co/
            contact_form = """
                  <form action="https://formsubmit.co/kumaresansakthi007@gmail.com" method="POST">
                        <input type="text" name="name" placeholder = "Your Name" required>
                        <input type="email" name="email" placeholder = "Your email" required>
                        <textarea name="message" placeholder="Your message here" required></textarea>
                        <button type="submit">Send</button>
                  </form>
                  """
            left_column, right_column = st.columns(2)
            with left_column:
                  st.markdown(contact_form, unsafe_allow_html=True)
            with right_column:
                  st.empty()
      
