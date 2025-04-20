import streamlit as st
import boto3
from botocore.exceptions import BotoCoreError, ClientError

# Streamlit UI setup
st.set_page_config(page_title="Text Translator", layout="centered")
st.title("🌍 Multilingual Text Translator")

# Load AWS credentials securely from Streamlit secrets
aws_credentials = st.secrets["aws"]

# AWS Translate client
translate = boto3.client(
    service_name='translate',
    region_name=aws_credentials["region_name"],
    aws_access_key_id=aws_credentials["aws_access_key_id"],
    aws_secret_access_key=aws_credentials["aws_secret_access_key"]
)

# UI: Text input
input_text = st.text_area("Enter text to translate:")

# Language code mapping
language_options = {
    "French": "fr",
    "German": "de",
    "Spanish": "es",
    "Hindi": "hi",
    "Japanese": "ja",
    "Chinese (Simplified)": "zh",
    "Arabic": "ar"
}

# UI: Language selector
target_lang = st.selectbox("Choose target language:", list(language_options.keys()))

# Translate button
if st.button("Translate"):
    if input_text.strip():
        try:
            result = translate.translate_text(
                Text=input_text,
                SourceLanguageCode='auto',  # auto-detect source language
                TargetLanguageCode=language_options[target_lang]
            )
            st.success("Translation:")
            st.write(result.get('TranslatedText'))
        except (BotoCoreError, ClientError) as error:
            st.error(f"Translation failed: {error}")
    else:
        st.warning("Please enter some text.")
