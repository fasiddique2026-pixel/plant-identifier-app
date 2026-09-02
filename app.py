import base64
import json
import re
from io import BytesIO
from groq import Groq
from PIL import Image
import streamlit as st

st.set_page_config(page_title="🌿 Plant Identifier AI", layout="centered")
st.title("🌿 Quick Plant Identifier")

# Retrieve API key securely from Streamlit Secrets
if "GROQ_API_KEY" in st.secrets:
  GROQ_API_KEY = st.secrets["GROQ_API_KEY"]
else:
  st.error("GROQ_API_KEY not found in Streamlit Secrets.")
  st.stop()

uploaded_file = st.file_uploader(
    "Upload Plant Photo", type=["jpg", "jpeg", "png"]
)

if uploaded_file is not None:
  image = Image.open(uploaded_file)
  st.image(image, use_container_width=True)
  analyze_btn = st.button(
      "Identify & Analyze", type="primary", use_container_width=True
  )

if analyze_btn:
    with st.spinner("Analyzing plant details..."):
        try:
            buffered = BytesIO()
            image.save(buffered, format="JPEG")
            img_b64 = base64.b64encode(buffered.getvalue()).decode("utf-8")

            system_prompt = """
            You are a botanical API. You MUST return ONLY a valid JSON object matching this schema:
            {
                "english_name": "Single short sentence common name",
                "scientific_name": "Single short sentence botanical name",
                "health_status": "HEALTHY or STRESSED or DISEASED",
                "light": "Single short sentence light preference",
                "temp": "Single short sentence temperature range",
                "soil": "Single short sentence soil type",
                "analysis": "Single short sentence visual description",
                "location": "Single short sentence placement recommendation",
                "diagnosis": "Single short sentence health note or treatment"
            }
            Do not write internal thinking, prose, or plain key-value text.
            """

            client = Groq(api_key=GROQ_API_KEY)
            response = client.chat.completions.create(
                model="llama-3.2-11b-vision-preview",
                response_format={"type": "json_object"},
                messages=[
                    {"role": "system", "content": system_prompt},
                    {
                        "role": "user",
                        "content": [
                            {
                                "type": "text",
                                "text": "Analyze this plant and produce the requested JSON.",
                            },
                            {
                                "type": "image_url",
                                "image_url": {
                                    "url": f"data:image/jpeg;base64,{img_b64}"
                                },
                            },
                        ],
                    },
                ],
            )

            raw_json = response.choices[0].message.content
            plant_data = json.loads(raw_json)

            st.subheader(f"🌱 {plant_data.get('english_name', 'Unknown Plant')}")
            st.write(f"**Scientific Name:** {plant_data.get('scientific_name', 'N/A')}")
            st.write(f"**Health Status:** {plant_data.get('health_status', 'N/A')}")
            st.info(f"**Care & Diagnosis:** {plant_data.get('diagnosis', 'N/A')}")

        except Exception as e:
            st.error(f"Error processing image: {e}")
