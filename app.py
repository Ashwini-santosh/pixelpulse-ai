import streamlit as st
import openai

st.set_page_config(page_title="PixelPulse AI", layout="centered")

st.title("📝 PixelPulse AI - Meeting Summarizer & Action Tracker")

# API key input (hidden in deployment via secrets)
openai.api_key = st.secrets.get("OPENAI_API_KEY", None)

uploaded_file = st.file_uploader("Upload a meeting transcript (.txt)", type=["txt"])

if uploaded_file is not None and openai.api_key:
    transcript = uploaded_file.read().decode("utf-8")
    
    with st.spinner("Summarizing and extracting action items..."):
        prompt = f"""You are an AI meeting assistant. 
        Summarize the following transcript in 5 bullet points.
        Then list clear action items with responsible persons if mentioned.
        
        Transcript:
        {transcript}
        """
        
        response = openai.ChatCompletion.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": prompt}]
        )
        
        output = response["choices"][0]["message"]["content"]
        
        st.subheader("📌 Meeting Summary & Actions")
        st.write(output)
        
        st.download_button("⬇️ Download Summary", output, file_name="meeting_summary.txt")
elif not openai.api_key:
    st.warning("⚠️ Please add your OpenAI API Key in Streamlit secrets to use this app.")
