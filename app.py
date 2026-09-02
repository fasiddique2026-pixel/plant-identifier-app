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

  prompt = """
        You are a botanical API. You MUST return ONLY a valid JSON object matching this exact schema:
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
                                " JSON."
                            ),
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
            temperature=0.1,
            max_tokens=800,
        )

        raw_content = response.choices[0].message.content.strip()
        clean_content = re.sub(
            r"<think>.*?</think>", "", raw_content, flags=re.DOTALL
        ).strip()
        data = json.loads(clean_content)

        status_str = str(data.get("health_status", "HEALTHY")).upper()
        if "HEALTH" in status_str:
          health_color = "#2e7d32"
          badge_icon = "🟢"
        elif "STRESS" in status_str:
          health_color = "#f57c00"
          badge_icon = "🟡"
        else:
          health_color = "#d32f2f"
          badge_icon = "🔴"

        card_html = f"""
                <div style="background-color: #121212; border: 1px solid #2e7d32; border-radius: 12px; padding: 18px; color: white; font-family: sans-serif; margin-top: 15px;">
                  <div style="display: flex; justify-content: space-between; align-items: center;">
                    <div>
                      <h2 style="margin: 0; color: #81c784; font-size: 22px;">🌿 {data.get('english_name', 'Unknown Plant')}</h2>
                      <p style="margin: 2px 0 0 0; font-style: italic; color: #a5d6a7; font-size: 14px;">{data.get('scientific_name', '')}</p>
                    </div>
                    <span style="background-color: {health_color}; padding: 6px 12px; border-radius: 20px; font-weight: bold; font-size: 12px; color: white;">
                      {badge_icon} {status_str}
                    </span>
                  </div>

                  <hr style="border: 0.5px solid #333; margin: 14px 0;">

                  <div style="display: grid; grid-template-columns: 1fr 1fr 1fr; gap: 10px; text-align: center; margin-bottom: 14px;">
                    <div style="background: #1e1e1e; padding: 10px; border-radius: 8px; font-size: 13px;">
                      <b>☀️ Light</b><br><span style="color: #ccc;">{data.get('light', 'N/A')}</span>
                    </div>
                    <div style="background: #1e1e1e; padding: 10px; border-radius: 8px; font-size: 13px;">
                      <b>🌡️ Temp</b><br><span style="color: #ccc;">{data.get('temp', 'N/A')}</span>
                    </div>
                    <div style="background: #1e1e1e; padding: 10px; border-radius: 8px; font-size: 13px;">
                      <b>🪴 Soil</b><br><span style="color: #ccc;">{data.get('soil', 'N/A')}</span>
                    </div>
                  </div>

                  <p style="margin: 8px 0; font-size: 14px; line-height: 1.4;"><b>🔍 Analysis:</b> {data.get('analysis', '')}</p>
                  <p style="margin: 8px 0; font-size: 14px; line-height: 1.4;"><b>📍 Location:</b> {data.get('location', '')}</p>
                  <p style="margin: 8px 0; font-size: 14px; line-height: 1.4;"><b>🩺 Diagnosis:</b> {data.get('diagnosis', '')}</p>
                </div>
                """

        st.markdown(card_html, unsafe_allow_html=True)

      except Exception as e:
        st.error(f"Error processing image: {e}")
