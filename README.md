# 🖼️ St-ImageCaptioner

This app generates descriptive captions for images using the [BLIP model](https://huggingface.co/Salesforce/blip-image-captioning-base) and a Gradio interface.

## 🚀 Features

- Upload an image
- Generate a natural language caption using BLIP (from Hugging Face Transformers)
- Export all generated captions to CSV

## 🧠 Model

Uses: `Salesforce/blip-image-captioning-base` from Hugging Face Transformers.

## 📦 Install (for local use)

```bash
pip install -r requirements.txt
python app.py
