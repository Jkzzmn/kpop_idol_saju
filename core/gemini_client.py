import json
import os
import re
from typing import Dict, Any

from dotenv import load_dotenv
from google import genai

load_dotenv()

try:
    import streamlit as st
    API_KEY = st.secrets.get("GOOGLE_API_KEY") or os.getenv("GOOGLE_API_KEY")
except Exception:
    API_KEY = os.getenv("GOOGLE_API_KEY")

if not API_KEY:
    raise ValueError("GOOGLE_API_KEY가 설정되지 않았습니다.")

client = genai.Client(api_key=API_KEY)


def _extract_json(text: str) -> Dict[str, Any]:
    cleaned = re.sub(r"```json|```", "", text).strip()
    return json.loads(cleaned)


def generate_interpretation(prompt: str) -> Dict[str, Any]:
    response = client.models.generate_content(
        model="gemini-2.5-flash-lite",
        contents=prompt
    )
    return _extract_json(response.text)
