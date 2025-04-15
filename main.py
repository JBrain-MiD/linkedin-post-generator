import streamlit as st
import openai
import os
from dotenv import load_dotenv
from frameworks import frameworks

load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

st.set_page_config(page_title="LinkedIn Post Generator", layout="centered")

st.title("🧠 LinkedIn Post Generator")

idea = st.text_area("What's the idea?", height=150)

framework_names = [f["name"] for f in frameworks]
selected_framework = st.selectbox("Choose a format", framework_names)

if st.button("Generate Post"):
    if not idea:
        st.warning("Please enter an idea.")
    else:
        # Find the matching framework
        framework = next(f for f in frameworks if f["name"] == selected_framework)
        prompt = framework["prompt_template"].format(idea=idea)

        # Call OpenAI
        with st.spinner("Writing your post..."):
            response = openai.ChatCompletion.create(
                model="gpt-4",
                messages=[
                    {"role": "system", "content": "You are a skilled B2B marketer."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.7,
                max_tokens=800
            )

            output = response["choices"][0]["message"]["content"]
            st.subheader("Generated Post")
            st.write(output)
            st.code(output, language='markdown')