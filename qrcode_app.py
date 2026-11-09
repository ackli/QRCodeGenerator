import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from PIL import Image, ImageTk, ImageDraw
from qrcodegen import QrCode
import os


class QRCodeApp:

    BG = "#1e1e2e"
    FG = "#cdd6f4"
    ACCENT = "#89b4fa"
    SURFACE = "#313244"
    BORDER = "#45475a"
    SUCCESS = "#a6e3a1"
    ERROR = "#f38ba8"

    def __init__(self, root: tk.Tk):
        self.root = root
        self.root.title("QR Code Generator")
        self.root.configure(bg=self.BG)
        self.root.minsize(520, 620)
        self.root.resizable(True, True)

        self.qr_image: Image.Image | None = None

        self._build_ui()
        self.root.bind("<Return>", lambda _: self._generate())

    def _build_ui(self):
        style = ttk.Style()
        style.theme_use("clam")
        style.configure("App.TFrame", background=self.BG)
        style.configure("App.TLabel", background=self.BG, foreground=self.FG,
                         font=("Segoe UI", 10))
        style.configure("Title.TLabel", background=self.BG, foreground=self.FG,
                         font=("Segoe UI", 18, "bold"))
        style.configure("Sub.TLabel", background=self.BG,
                         foreground="#a6adc8", font=("Segoe UI", 9))
        style.configure("Accent.TButton", font=("Segoe UI", 11, "bold"),
                         foreground="#1e1e2e", background=self.ACCENT,
                         borderwidth=0, padding=(16, 10))
        style.map("Accent.TButton",
                   background=[("active", "#74c7ec"), ("disabled", self.BORDER)])
        style.configure("Save.TButton", font=("Segoe UI", 10),
                         foreground=self.FG, background=self.SURFACE,
                         borderwidth=0, padding=(12, 8))
        style.map("Save.TButton",
                   background=[("active", self.BORDER), ("disabled", self.SURFACE)])

        main = ttk.Frame(self.root, style="App.TFrame", padding=30)
        main.pack(fill="both", expand=True)

        ttk.Label(main, text="QR Code Generator",
                  style="Title.TLabel").pack(pady=(0, 2))
        ttk.Label(main, text="Collez un lien ou du texte, puis cliquez sur Générer",
                  style="Sub.TLabel").pack(pady=(0, 18))

        # --- URL input ---
        input_frame = ttk.Frame(main, style="App.TFrame")
        input_frame.pack(fill="x", pady=(0, 6))
        ttk.Label(input_frame, text="Lien / Texte", style="App.TLabel").pack(
            anchor="w")

        self.url_var = tk.StringVar()
        self.entry = tk.Entry(
            input_frame, textvariable=self.url_var,
            font=("Segoe UI", 12), bg=self.SURFACE, fg=self.FG,
            insertbackground=self.FG, relief="flat", bd=8,
            highlightthickness=2, highlightbackground=self.BORDER,
            highlightcolor=self.ACCENT)
        self.entry.pack(fill="x", pady=(4, 0), ipady=4)
        self.entry.focus_set()

        # --- Error correction level ---
        ecc_frame = ttk.Frame(main, style="App.TFrame")
        ecc_frame.pack(fill="x", pady=(10, 6))
        ttk.Label(ecc_frame, text="Niveau de correction d'erreur",
                  style="App.TLabel").pack(anchor="w")

        self.ecc_var = tk.StringVar(value="MEDIUM")
        ecc_options = ttk.Frame(ecc_frame, style="App.TFrame")
        ecc_options.pack(anchor="w", pady=(4, 0))
        for label, val in [("Low", "LOW"), ("Medium", "MEDIUM"),
                           ("Quartile", "QUARTILE"), ("High", "HIGH")]:
            rb = tk.Radiobutton(
                ecc_options, text=label, variable=self.ecc_var, value=val,
                font=("Segoe UI", 9), bg=self.BG, fg=self.FG,
                selectcolor=self.SURFACE, activebackground=self.BG,
                activeforeground=self.ACCENT, highlightthickness=0,
                bd=0)
            rb.pack(side="left", padx=(0, 14))

        # --- Generate button ---
        ttk.Button(main, text="Générer le QR Code",
                   style="Accent.TButton",
                   command=self._generate).pack(pady=(14, 14))

        # --- QR display area ---
        self.canvas_frame = tk.Frame(main, bg=self.SURFACE,
                                      highlightthickness=1,
                                      highlightbackground=self.BORDER)
        self.canvas_frame.pack(fill="both", expand=True)

        self.placeholder = ttk.Label(
            self.canvas_frame,
            text="Le QR Code apparaîtra ici",
            style="Sub.TLabel", background=self.SURFACE, anchor="center")
        self.placeholder.pack(fill="both", expand=True, pady=40)

        self.canvas = tk.Canvas(self.canvas_frame, bg=self.SURFACE,
                                 highlightthickness=0)

        # --- Save button ---
        self.save_btn = ttk.Button(main, text="Sauvegarder en PNG",
                                    style="Save.TButton",
                                    command=self._save, state="disabled")
        self.save_btn.pack(pady=(10, 0))

        # --- Status bar ---
        self.status_var = tk.StringVar()
        self.status_label = ttk.Label(main, textvariable=self.status_var,
                                       style="Sub.TLabel")
        self.status_label.pack(pady=(6, 0))

    def _get_ecc(self) -> QrCode.Ecc:
        mapping = {
            "LOW": QrCode.Ecc.LOW,
            "MEDIUM": QrCode.Ecc.MEDIUM,
            "QUARTILE": QrCode.Ecc.QUARTILE,
            "HIGH": QrCode.Ecc.HIGH,
        }
        return mapping[self.ecc_var.get()]

    def _generate(self):
        text = self.url_var.get().strip()
        if not text:
            self._set_status("Veuillez entrer un lien ou du texte.", error=True)
            return

        try:
            qr = QrCode.encode_text(text, self._get_ecc())
        except Exception as e:
            self._set_status(f"Erreur : {e}", error=True)
            return

        self.qr_image = self._qr_to_image(qr, scale=10, border=4,
                                            light="#ffffff", dark="#1e1e2e")
        self._display_qr()
        self.save_btn.configure(state="normal")
        size = qr.get_size()
        self._set_status(f"QR Code généré — version {qr.get_version()}, "
                         f"{size}×{size} modules")

    @staticmethod
    def _qr_to_image(qr: QrCode, scale: int = 10, border: int = 4,
                      light: str = "#ffffff", dark: str = "#000000") -> Image.Image:
        size = qr.get_size()
        img_size = (size + border * 2) * scale
        img = Image.new("RGB", (img_size, img_size), light)
        draw = ImageDraw.Draw(img)

        for y in range(size):
            for x in range(size):
                if qr.get_module(x, y):
                    x0 = (x + border) * scale
                    y0 = (y + border) * scale
                    draw.rectangle([x0, y0, x0 + scale - 1, y0 + scale - 1],
                                   fill=dark)
        return img

    def _display_qr(self):
        self.placeholder.pack_forget()
        self.canvas.pack(fill="both", expand=True)
        self.canvas.update_idletasks()

        cw = self.canvas.winfo_width() or 300
        ch = self.canvas.winfo_height() or 300
        display_size = min(cw, ch, 360)

        resized = self.qr_image.resize((display_size, display_size),
                                        Image.NEAREST)
        self._tk_img = ImageTk.PhotoImage(resized)
        self.canvas.delete("all")
        self.canvas.create_image(cw // 2, ch // 2, image=self._tk_img)

    def _save(self):
        if self.qr_image is None:
            return
        path = filedialog.asksaveasfilename(
            defaultextension=".png",
            filetypes=[("PNG", "*.png"), ("Tous les fichiers", "*.*")],
            initialfile="qrcode.png")
        if path:
            self.qr_image.save(path)
            self._set_status(f"Sauvegardé : {os.path.basename(path)}")

    def _set_status(self, msg: str, error: bool = False):
        self.status_var.set(msg)
        color = self.ERROR if error else self.SUCCESS
        self.status_label.configure(foreground=color)


if __name__ == "__main__":
    root = tk.Tk()
    app = QRCodeApp(root)
    root.mainloop()
