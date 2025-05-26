import gradio as gr
from PIL import Image
from image_caption_blip import generate_caption
import datetime

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

# Simple JS to toggle dark/light CSS variables
toggle_js = """
() => {
  const root = document.documentElement;
  const current = root.style.getPropertyValue('--bg-color');
  if (current === 'white' || current === '') {
    root.style.setProperty('--bg-color', '#121212');
    root.style.setProperty('--text-color', '#e0e0e0');
    root.style.setProperty('--btn-bg', '#333');
    root.style.setProperty('--btn-text', 'white');
  } else {
    root.style.setProperty('--bg-color', 'white');
    root.style.setProperty('--text-color', '#111');
    root.style.setProperty('--btn-bg', '#ddd');
    root.style.setProperty('--btn-text', '#111');
  }
}
"""

custom_css = """
:root {
  --bg-color: white;
  --text-color: #111;
  --btn-bg: #ddd;
  --btn-text: #111;
}
body {
  background-color: var(--bg-color);
  color: var(--text-color);
  font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Oxygen,
    Ubuntu, Cantarell, "Open Sans", "Helvetica Neue", sans-serif;
  margin: 0;
  padding: 0;
}
.gradio-container {
  max-width: 600px;
  margin: 2rem auto;
  padding: 2rem;
  border-radius: 12px;
  box-shadow: 0 0 15px rgb(0 0 0 / 0.1);
  background-color: var(--bg-color);
}
.gr-button {
  background-color: var(--btn-bg);
  color: var(--btn-text);
  border: none;
  padding: 0.6rem 1.2rem;
  font-weight: 600;
  border-radius: 8px;
  transition: background-color 0.3s ease;
  cursor: pointer;
}
.gr-button:hover {
  background-color: var(--btn-bg-hover, #bbb);
}
.gr-textbox {
  font-size: 1.1rem;
  border-radius: 8px;
}
.gr-image {
  border-radius: 12px;
  box-shadow: 0 2px 10px rgb(0 0 0 / 0.1);
}
"""

with gr.Blocks(css=custom_css) as demo:
    gr.Markdown(
        """
        <h1 style="text-align:center; font-weight: 700;">🖼️ St-ImageCaptioner</h1>
        <p style="text-align:center; color: var(--text-color); font-weight: 400;">
        Upload an image or take a photo with your camera.
        </p>
        """
    )

    with gr.Row():
        with gr.Column(scale=1):
            image_input = gr.Image(label="Take a photo or upload", type="pil", source="camera")
            generate_button = gr.Button("✨ Generate Caption", elem_classes=["gr-button"])
            export_button = gr.Button("📤 Export Captions", elem_classes=["gr-button"])
            dark_toggle = gr.Button("🌓 Toggle Light/Dark Mode", elem_classes=["gr-button"])

        with gr.Column(scale=1):
            caption_output = gr.Textbox(
                label="Generated Caption", lines=3, interactive=False, elem_classes=["gr-textbox"]
            )
            file_output = gr.File(label="Download Exported Captions")

    generate_button.click(fn=caption_and_save, inputs=image_input, outputs=caption_output)
    export_button.click(fn=export_captions, outputs=file_output)
    dark_toggle.click(fn=None, js=toggle_js)


demo.launch()
