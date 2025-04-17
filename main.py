import streamlit as st
import os
from dotenv import load_dotenv
from frameworks import frameworks
from openai import OpenAI

# Load environment variables
load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# Streamlit app config
st.set_page_config(page_title="LinkedIn Post Generator", layout="centered")
st.title("🧠 LinkedIn Post Generator")

# UI inputs
idea = st.text_area("What's the idea?", height=150)
framework_names = [f["name"] for f in frameworks]
selected_framework = st.selectbox("Choose a format", framework_names)

# Generate post button
if st.button("Generate Post"):
    if not idea:
        st.warning("Please enter an idea.")
    else:
        # Create prompt from selected framework
        framework = next(f for f in frameworks if f["name"] == selected_framework)
        prompt = framework["prompt_template"].format(idea=idea)

        # Call OpenAI with the updated API method
        with st.spinner("Writing your post..."):
            response = client.chat.completions.create(
                model="gpt-4",
                messages=[
                    {"role": "system", "content": "You are a skilled B2B marketer."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.7,
                max_tokens=800
            )

            output = response.choices[0].message.content
            st.subheader("Generated Post")
            st.write(output)
