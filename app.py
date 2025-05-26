import gradio as gr
from PIL import Image
from image_caption_blip import generate_caption
import datetime
import os

captions_history = []

def caption_and_save(image):
    caption = generate_caption(image)
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    captions_history.append((timestamp, caption))
    return caption

def export_captions():
    if not captions_history:
        return None
    filename = "captions_export.csv"
    with open(filename, "w", encoding="utf-8") as f:
        f.write("timestamp,caption\n")
        for ts, cap in captions_history:
            f.write(f"{ts},{cap}\n")
    return filename

with gr.Blocks() as demo:
    gr.Markdown("# 🖼️ St-ImageCaptioner")
    
    with gr.Row():
        with gr.Column():
            image_input = gr.Image(type="pil")
            caption_output = gr.Textbox(label="Generated Caption")
            generate_button = gr.Button("Generate Caption")
            export_button = gr.Button("Export Captions")
            file_output = gr.File(label="Download Exported Captions")

    generate_button.click(fn=caption_and_save, inputs=image_input, outputs=caption_output)
    export_button.click(fn=export_captions, outputs=file_output)

demo.launch()
