# Author: Swastik Nayak
import os
import streamlit as st
import requests


# Set page configuration for better appearance
st.set_page_config(page_title="KICKFLIP", layout="centered")

# Apply custom CSS for full dark mode with magenta title
st.markdown(
    """
    <style>
        /* Set full page background to black */
        body, .stApp {
            background-color: black !important;
            color: white !important;
        }

        /* Ensure all text appears in white */
        h2, h3, h4, h5, h6, p, div, span, label {
            color: white !important;
        }

        /* Kickflip title (logo text) in magenta */
        .magenta-title {
            color: magenta !important;
            font-size: 36px;
            font-weight: bold;
            text-align: center;
        }

        /* Input box text color */
        .stTextInput > div > div > input {
            color: white !important;
            background-color: #222 !important; /* Dark input box */
            border: 1px solid magenta !important;
        }

        /* Button styling */
        div.stButton > button {
            background-color: magenta !important;
            color: white !important;
            border-radius: 10px;
            font-size: 16px;
            font-weight: bold;
            padding: 10px;
            border: none;
        }

        div.stButton > button:hover {
            background-color: #d600a7 !important; /* Darker magenta on hover */
        }

        /* Ensure response texts are white */
        .stMarkdown, .stMarkdown p {
            color: white !important;
        }
    </style>
    """,
    unsafe_allow_html=True
)

# App UI
st.markdown("<h1 class='magenta-title'>KICKFLIP</h1>", unsafe_allow_html=True)  # Magenta Title
st.write("Ask a question related to Experiences")

query = st.text_input("Enter your question")

if st.button("Get Answer"):
    if query:
        try:
            response = requests.get("http://127.0.0.1:8000/answer", params={"query": query})#sending query to the server 
            #st.markdown(response.text)
            if response.status_code == 200:
                data = response.json()
                if "answer" in data:
                    st.markdown(f"**Answer:** <span style='color: white;'>{data['answer']}</span>", unsafe_allow_html=True)
                else:
                    st.markdown("<span style='color: white;'>Error: Unable to fetch the answer</span>", unsafe_allow_html=True)

        except Exception as e:
            st.markdown(f"<span style='color: white;'>Error: {e}</span>", unsafe_allow_html=True)

        try:
            response = requests.get("http://127.0.0.1:8000/retrieve", params={"query": query})
            
            if response.status_code == 200:
                data = response.json()
                #st.markdown(data)
                if "error" in data:
                    st.markdown(f"<span style='color: white;'>Error: {data['error']}</span>", unsafe_allow_html=True)
                elif "video_path" in data:
                  
                    # Display caption if available
                    caption = data.get("caption", "No caption available.")
                    st.markdown(f"<span style='color: white; font-size: 16px;'>**Best Match Caption:** {caption}</span>", unsafe_allow_html=True)

                    video_path_modified = os.path.join("/Users/kaustuvdash/Desktop/KickFlip/kickflipvenv/python_project_rag/", data['video_path'])
                    # Display video
                    #st.markdown(video_path_modified)
                    #print(video_path_modified)
                    print("in the videos")
                    st.video(video_path_modified)
                else:
                    st.markdown("<span style='color: white;'>Error: Unable to fetch the video</span>", unsafe_allow_html=True)
            else:
                st.markdown(f"<span style='color: white;'>Error: API request failed with status code {response.status_code}</span>", unsafe_allow_html=True)

        except Exception as e:
            st.markdown(f"<span style='color: white;'>Error: {e}</span>", unsafe_allow_html=True)



































# #Author:Swastik Nayak
# import os
# import streamlit as st
# import requests

# st.title("KICKFLIP")
# st.write("Ask a question related to Experiences")

# query = st.text_input("Enter your question")

# if st.button("Get Answer"):
#     if query:
#         try:
#             response =requests.get("http://127.0.0.1:8000/answer", params ={"query": query})
#             if response.status_code== 200 :
#                 data=response.json()
#                 if "answer" in data:
#                     st.write(f"**Answer:**{data['answer']}")
#                 else:
#                     st.write("Error:Unable to fetch the answer")

#         except Exception as e:
#             st.write(f"Error: {e}")

#     else:
#         st.write("Please enter a question.")


