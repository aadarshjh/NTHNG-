import streamlit as st 
import os
from PIL import Image
import google.generativeai as genai

model = genai.GenerativeModel('gemini-1.5-flash')

genai.configure(api_key = "AIzaSyCLgJyAj-H8tJKG8c4bptHy1jHvi6-Vu2s")

def get_gemini_response(input_text, image_data, prompt):
    safety_settings = [
        {
            "category": "HARM_CATEGORY_DANGEROUS_CONTENT",
            "threshold": "BLOCK_NONE",
        },
    ]
    response = model.generate_content(
        [input_text, image_data[0], prompt],
        safety_settings=safety_settings,
        generation_config={"temperature": 0.8, "top_p": 1, "top_k": 32}
    )
    return response.text

def input_image_details(uploaded_file):
    if uploaded_file is not None:
        bytes_data = uploaded_file.getvalue()
        image_parts = [
            {
                "mime_type" : uploaded_file.type,
                "data" : bytes_data
            }
        ]
        return image_parts
    else:
        raise FileNotFoundError("No file was uploaded")
    
st.set_page_config(page_title = "RythRec")
st.sidebar.header("Mood's Recommendation")
st.sidebar.write("Lassgooo")
st.sidebar.warning("Note: Don't use this too much otherwise you'll fall for this.")
st.header("Mood's Recommendation")
st.subheader("Check your mood and I'll suggest songs")
input = st.text_input("Ask me to suggest?",key = "input")
uploaded_file = st.file_uploader("Choose an image",type = ["jpg","jpeg","png"])
image = ""
if uploaded_file is not None:
    image = Image.open(uploaded_file)
    st.image(image,caption = "Uploaded",use_column_width = True)

ssubmit = st.button("Submit")

input_prompt = """
You are an advanced AI music expert with the following capabilities:
🎵 Musical Expertise:
Comprehensive knowledge of various music genres, artists, and styles
Understanding of music theory and composition
Ability to analyze and interpret musical elements
🖼️ Image Analysis:
Advanced facial emotion recognition technology
Capability to detect mood and sentiment from user-uploaded images
🎧 Personalized Recommendations:
Skill in matching emotional states to appropriate music
Ability to suggest songs, playlists, or genres based on detected mood
💡 Interaction Approach:
Provide friendly and empathetic responses
Offer brief explanations for music suggestions
Respect user privacy and emotional state
When a user uploads an image, analyze their facial expression to determine their emotional state. 
Then, provide music recommendations tailored to their current mood, explaining briefly why each suggestion might resonate with them emotionally.
For each song recommendation, provide both YouTube and Spotify links.
Format your response as follows:
1. Song Title - Artist
   - Reason for recommendation
   - YouTube link: [insert link]
   - Spotify link: [insert link]
"""

if ssubmit:
    image_data = input_image_details(uploaded_file)
    response = get_gemini_response(input_prompt,image_data,input)
    st.subheader("Here you go!")
    st.write(response)
