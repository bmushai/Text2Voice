import os
import asyncio
import edge_tts
from pydub import AudioSegment
import tkinter as tk
from tkinter import messagebox, scrolledtext

VOICE_MAP = {
    "Asha": "hi-IN-SwaraNeural",
    "Rahul": "hi-IN-MadhurNeural"
}

OUTPUT_DIR = "output_segments"
FINAL_AUDIO = "podcast_output.mp3"

def parse_script(text):
    lines = text.strip().splitlines()
    dialogue = []
    for line in lines:
        if ":" in line:
            speaker, content = line.strip().split(":", 1)
            dialogue.append({"speaker": speaker.strip(), "text": content.strip()})
    return dialogue

async def generate_segments(dialogue):
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    for i, line in enumerate(dialogue):
        voice = VOICE_MAP.get(line["speaker"], "hi-IN-MadhurNeural")
        output = os.path.join(OUTPUT_DIR, f"line_{i}.mp3")
        communicate = edge_tts.Communicate(text=line["text"], voice=voice)
        await communicate.save(output)

def merge_segments():
    combined = AudioSegment.empty()
    files = sorted(os.listdir(OUTPUT_DIR), key=lambda x: int(x.split("_")[1].split(".")[0]))
    for file in files:
        if file.endswith(".mp3"):
            seg = AudioSegment.from_file(os.path.join(OUTPUT_DIR, file))
            combined += seg + AudioSegment.silent(duration=700)
    combined.export(FINAL_AUDIO, format="mp3")

def generate_podcast():
    script_text = text_input.get("1.0", tk.END).strip()
    if not script_text:
        messagebox.showwarning("Input Missing", "Please enter a script.")
        return
    dialogue = parse_script(script_text)

    async def run():
        await generate_segments(dialogue)
        merge_segments()
        messagebox.showinfo("Done", f"Audio saved as {FINAL_AUDIO}")
    asyncio.run(run())

root = tk.Tk()
root.title("Text2Voice - Hindi TTS")
root.geometry("600x500")

tk.Label(root, text="🎙️ Paste your 2-speaker Hindi script below:", font=("Arial", 12)).pack(pady=10)
text_input = scrolledtext.ScrolledText(root, wrap=tk.WORD, width=70, height=20, font=("Arial", 10))
text_input.pack(padx=10)

generate_btn = tk.Button(root, text="Generate Audio", font=("Arial", 12, "bold"), bg="green", fg="white", command=generate_podcast)
generate_btn.pack(pady=20)

root.mainloop()
