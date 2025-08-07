# Import necessary libraries
import streamlit as st
import requests
from io import BytesIO
import os

# -------------------------------
# SETUP SECTION
# -------------------------------

# Replace this string with your Hugging Face API token
HF_API_KEY = os.getenv("HF_API_KEY")

# This is the endpoint for the Stable Diffusion v2 model hosted by Hugging Face
API_URL = "https://api-inference.huggingface.co/models/stabilityai/stable-diffusion-xl-base-1.0"

# Set headers for the API request (Authorization and Content-Type)
headers = {
    "Authorization": f"Bearer {HF_API_KEY}"
}


# -------------------------------
# FUNCTION TO GENERATE IMAGE
# -------------------------------

def generate_image(prompt):
    """
    Sends a prompt to the Hugging Face API and returns the image bytes if successful.
    """
    # Create the request body with the prompt
    payload = {"inputs": prompt}

    # Make a POST request to the API
    response = requests.post(API_URL, headers=headers, json=payload)

    # If the request was successful (status code 200)
    if response.status_code == 200:
        return response.content  # Return the image as raw bytes
    else:
        # If error, show the error message on Streamlit UI
        st.error(f"Error {response.status_code}: {response.text}")
        return None


# -------------------------------
# STREAMLIT UI SETUP
# -------------------------------

# Set the Streamlit app title
st.title("🎨 Text to Image Generator (Stable Diffusion)")

# Optional description
st.markdown("Generate AI images from your text prompts using **Stable Diffusion v2** via Hugging Face API.")

# Create a text input box for user to enter their prompt
prompt = st.text_input("📝 Enter your image prompt", value="A futuristic city at sunset")

# Create a button labeled 'Generate Image'
if st.button("🚀 Generate Image"):
    # Show spinner while image is being generated
    with st.spinner("Generating your image..."):
        # Call the image generation function
        image_bytes = generate_image(prompt)

        # If image was successfully returned
        if image_bytes:
            # Display the image on the screen
            st.image(image_bytes, caption=f"🖼️ Generated for: '{prompt}'", use_container_width=True)

            # Convert raw bytes to a file-like object
            image_buffer = BytesIO(image_bytes)

            # Add a download button
            st.download_button(
                label="📥 Download Image",
                data=image_buffer,
                file_name="generated_image.png",
                mime="image/png"
            )
