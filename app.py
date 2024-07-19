import streamlit as st
import os
import dotenv
from dotenv import load_dotenv
load_dotenv()
 #loads all environment variables

import google.generativeai as genai

from youtube_transcript_api import YouTubeTranscriptApi

genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))
prompt="""You are Youtube video summarizer.You will be taking the transcript text and summarizing the entire video and providing the important summary in points within 250 words.Provide the summary of the text given here:  """

def extraxt_trascript_details(youtube_video_url):
    try:
        video_id=youtube_video_url.split("=")[1]
        transcript_text=YouTubeTranscriptApi.get_transcript(video_id)

        transcript_text=""
        for i in transcript_text:
            transcript+=" "+ i["text"]

        return transcript

    except Exception as e:
        raise e

def generate_gemini_content(transcript_text,prompt):
    model=genai.GenerativeModel("gemini-pro")
    response=model.generate_content(prompt+transcript_text)
    return response.text

st.title("YT Transcript to Detailed Notes converter ")
youtube_link=st.text_input("Enter the link: ")

if youtube_link:
    video_id=youtube_link.split("=")[1]
    st.image(f"http://img.youtube.com/vi/{video_id}/0.jpg",use_column_width=True)

if st.button("Get Notes"):
    transcript_text=extraxt_trascript_details(youtube_link)

    if transcript_text:
        summary=generate_gemini_content(transcript_text,prompt)
        st.markdown("##Detailed Notes: ")
        st.write(summary)
