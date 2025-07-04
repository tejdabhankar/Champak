import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
import random
from colors import *
from logic import handle_local_command, ask_ollama

class ChampakUI:
    def __init__(self, root):
        self.root = root
        self.root.title("🌿 Champak Chat")
        self.root.attributes('-fullscreen', True)
        self.setup_ui()

    def setup_ui(self):
        w, h = self.root.winfo_screenwidth(), self.root.winfo_screenheight()
        try:
            bg = Image.open("background.jpg").resize((w, h))
            self.bg_photo = ImageTk.PhotoImage(bg)
            tk.Label(self.root, image=self.bg_photo).place(x=0, y=0, relwidth=1, relheight=1)
        except:
            self.root.configure(bg=BACKGROUND)

        # Model Selector (Top Right)
        self.model_var = tk.StringVar(value="mistral")
        models = ["mistral", "gemma", "llama2", "qwen"]
        model_selector = ttk.Combobox(self.root, textvariable=self.model_var, values=models, state="readonly", font=("Segoe UI", 11))
        model_selector.place(relx=0.95, rely=0.03, anchor="ne", width=150)

        # Main Container
        self.container = tk.Frame(self.root, bg=HEADER_BG)
        self.container.place(relx=0.5, rely=0.5, anchor="center", width=1100, height=850)

        tk.Label(self.container, text="🌿 Champak Chat", font=("Segoe UI", 20, "bold"),
                 bg=HEADER_BG, fg=HEADER_FG).pack(pady=10)

        # Chat Area
        self.canvas = tk.Canvas(self.container, bg=BACKGROUND, highlightthickness=0)
        self.scrollbar = ttk.Scrollbar(self.container, orient="vertical", command=self.canvas.yview)
        self.scroll_frame = tk.Frame(self.canvas, bg=BACKGROUND)
        self.scroll_frame.bind("<Configure>", lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all")))
        self.canvas.create_window((0, 0), window=self.scroll_frame, anchor="nw")
        self.canvas.configure(yscrollcommand=self.scrollbar.set)

        self.canvas.pack(side="left", fill="both", expand=True, padx=(10, 0))
        self.scrollbar.pack(side="right", fill="y")

        # Input Box
        bottom = tk.Frame(self.container, bg="#ffffff")
        bottom.pack(fill="x", side="bottom", pady=8)

        self.input = tk.Entry(bottom, font=("Segoe UI", 12))
        self.input.pack(side="left", fill="x", expand=True, padx=(10, 6), ipady=8)

        tk.Button(bottom, text="Send", bg=HEADER_FG, fg="white", command=self.send,
                  font=("Segoe UI", 10, "bold"), relief=tk.FLAT).pack(side="right", padx=(6, 10))

        self.root.bind('<Return>', lambda e: self.send())

        self.append_bubble("🤖 Hello! I'm Champak. Try 'open firefox' or ask me anything!", "left")

    def append_bubble(self, text, side):
        frame = tk.Frame(self.scroll_frame, bg=BACKGROUND)
        frame.pack(anchor="center", fill=tk.X, pady=6, padx=20)

        bg_color = CHAMPAK_COLOR if side == "left" else random.choice(USER_COLORS)

        bubble = tk.Label(
            frame, text=text, bg=bg_color, fg="#000", font=("Segoe UI", 11),
            wraplength=950, justify=tk.LEFT if side == "left" else tk.RIGHT,
            padx=14, pady=10, bd=0
        )
        bubble.pack(side=side)

    def send(self):
        prompt = self.input.get().strip()
        if not prompt:
            return

        self.append_bubble("🧑 You: " + prompt, "right")
        self.input.delete(0, tk.END)

        selected_model = self.model_var.get()
        response = handle_local_command(prompt) or ask_ollama(prompt, selected_model)
        self.append_bubble("🤖 " + response, "left")
        self.canvas.yview_moveto(1)

