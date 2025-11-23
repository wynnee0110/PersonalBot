import tkinter as tk
from tkinter import scrolledtext
from gpt4all import GPT4All
import os
import threading
import time
# --- Paths ---
MODEL_FOLDER = r"C:\Users\obial\personal-ai\models"
MODEL_FILE = "Phi-3-mini-4k-instruct-q4.gguf"  # CHANGE THIS TO YOUR PREFFERED AI MODEL
MODEL_PATH = os.path.join(MODEL_FOLDER, MODEL_FILE)

# --- Load model (local only) ---CHANGE THIS TO YOUR PREFFERED AI MODEL
model = GPT4All(model_name=MODEL_FILE, model_path=MODEL_FOLDER, allow_download=False)

# --- GUI setup ---
root = tk.Tk()
root.title("Star AI")
root.geometry("300x400")
root.resizable(False, False)

chat_window = scrolledtext.ScrolledText(root, wrap=tk.WORD, width=60, height=20, state=tk.DISABLED)
chat_window.pack(padx=10, pady=10)

user_input = tk.Entry(root, width=50)
user_input.pack( padx=(10,0), pady=(0,10))
user_input.focus()


def generate_response(user_message):

    chat_window.config(state=tk.NORMAL)
    chat_window.insert(tk.END, "Bot is typing...\n")
    chat_window.config(state=tk.DISABLED)
    chat_window.yview(tk.END)
    """Generate AI response in a separate thread."""
    response = model.generate(user_message, max_tokens=556)

        # Remove typing indicator
    chat_window.config(state=tk.NORMAL)
    chat_window.delete("end-2l", "end-1l")  # remove last line (typing...)
    chat_window.config(state=tk.DISABLED)

    chat_window.config(state=tk.NORMAL)
    chat_window.insert(tk.END, f"Bot: {response}\n\n")
    chat_window.config(state=tk.DISABLED)
    chat_window.yview(tk.END)

def send_message(event=None):
    message = user_input.get()
    if not message.strip():
        return
    chat_window.config(state=tk.NORMAL)
    chat_window.insert(tk.END, f"You: {message}\n")
    chat_window.config(state=tk.DISABLED)
    chat_window.yview(tk.END)
    user_input.delete(0, tk.END)
    

    # Generate response in a separate thread so GUI doesn't freeze
    threading.Thread(target=generate_response, args=(message,), daemon=True).start()

user_input.bind("<Return>", send_message)

send_button = tk.Button(root, text="Send", command=send_message)
send_button.pack( padx=(5,10), pady=(0,10))

root.mainloop()
