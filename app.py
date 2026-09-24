import streamlit as st
from textwrap import dedent
from dotenv import load_dotenv
from agno.agent import Agent
from agno.models.groq import Groq
from agno.tools.youtube import YouTubeTools

load_dotenv()

st.set_page_config(page_title="YouTube Video Analyzer", page_icon="🎬", layout="wide")

st.title("🎬 YouTube Video Analyzer Agent")
st.write("Paste a YouTube link below to extract an overview, detailed summary, timestamps, and actionable takeaways!")

# Input field for the YouTube URL
youtube_url = st.text_input("YouTube Video URL", "https://www.youtube.com/watch?v=zjkBMFhNj_g")

if st.button("Analyze Video"):
    if youtube_url:
        with st.spinner("🤖 Agent is fetching metadata and analyzing the transcript..."):
            try:
                # Initialize the agent with the active gpt-oss-120b model
                youtube_agent = Agent(
                    name="YouTube Agent",
                    model=Groq(id="openai/gpt-oss-120b"),
                    tools=[YouTubeTools()],
                    markdown=True,
                    instructions=dedent("""\
                        You are an expert YouTube content analyst. 
                        Analyze the provided video link and break it down into:
                        1. Video Overview (length, metadata, type)
                        2. Key Timestamps & Summaries ([start_time, end_time, summary])
                        3. Actionable Takeaways with Emojis
                        """),
                )

                # Run the agent and fetch response content
                response = youtube_agent.run(f"Analyze this video and provide a summary with timestamps: {youtube_url}")
                
                st.success("Analysis Complete!")
                st.markdown(response.content)

            except Exception as e:
                st.error(f"An error occurred: {e}")
    else:
        st.warning("Please enter a valid YouTube URL.")