import ctypes
import os
import shutil
import sys
import tempfile
import tkinter as tk
from tkinter import filedialog

import customtkinter as ctk
from PIL import Image, ImageDraw

BG = "#07111f"
CARD = "#0e1a2e"
WELL = "#08101c"
BORDER = "#1c3558"
ACCENT = "#2f7dff"
ACCENT_HOVER = "#1c64ea"
CYAN = "#3ec6ff"
TEXT = "#eef4ff"
MUTED = "#8aa0c2"
SUCCESS = "#5eead4"
DANGER = "#ff7b93"
SOFT = "#143056"
GHOST = "#10233f"
GHOST_HOVER = "#173056"

WINDOW_W = 600
WINDOW_H = 640
PREVIEW_BOX = 228
OUTPUT_SIZE = 256


def resource_path(filename):
    base = getattr(sys, "_MEIPASS", os.path.dirname(os.path.abspath(__file__)))
    return os.path.join(base, filename)


def window_icon_path(path):
    """Το iconbitmap των Windows αποτυγχάνει όταν η διαδρομή έχει ελληνικούς χαρακτήρες."""
    if not os.path.exists(path):
        return None
    try:
        path.encode("mbcs")
        return path
    except (LookupError, UnicodeEncodeError):
        safe = os.path.join(tempfile.gettempdir(), "My_convert_image2ico.ico")
        shutil.copyfile(path, safe)
        return safe


def enable_dpi():
    try:
        ctypes.windll.shcore.SetProcessDpiAwareness(1)
    except Exception:
        try:
            ctypes.windll.user32.SetProcessDPIAware()
        except Exception:
            pass


def enable_dark_title_bar(window):
    window.update_idletasks()
    hwnd = ctypes.windll.user32.GetParent(window.winfo_id())
    value = ctypes.c_int(1)
    for attribute in (20, 19):
        ctypes.windll.dwmapi.DwmSetWindowAttribute(
            hwnd, attribute, ctypes.byref(value), ctypes.sizeof(value)
        )


def shorten(name, limit=46):
    if len(name) <= limit:
        return name
    keep = limit - 1
    head = keep // 2
    tail = keep - head
    return f"{name[:head]}…{name[-tail:]}"


class App(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.file_path = None
        self.output_folder = None
        self.preview_image = None

        self.title("Μετατροπή σε εικονίδιο")
        self.geometry(f"{WINDOW_W}x{WINDOW_H}")
        self.minsize(WINDOW_W, WINDOW_H)
        self.resizable(False, False)
        self.configure(fg_color=BG)

        icon = window_icon_path(resource_path("My_convert_image2ico.ico"))
        if icon:
            try:
                self.iconbitmap(default=icon)
            except tk.TclError:
                pass

        self._build()
        self._center()
        self.after(30, self._draw_accent)
        self.after(50, lambda: enable_dark_title_bar(self))

    def _center(self):
        self.update_idletasks()
        x = max((self.winfo_screenwidth() - WINDOW_W) // 2, 0)
        y = max((self.winfo_screenheight() - WINDOW_H) // 2 - 12, 16)
        self.geometry(f"{WINDOW_W}x{WINDOW_H}+{x}+{y}")

    def _draw_accent(self):
        width = max(self.winfo_width(), WINDOW_W)
        self.accent.delete("all")
        for x in range(width):
            blend = x / max(width - 1, 1)
            red = int(0x2F + (0x3E - 0x2F) * blend)
            green = int(0x7D + (0xC6 - 0x7D) * blend)
            blue = 0xFF
            self.accent.create_line(x, 0, x, 5, fill=f"#{red:02x}{green:02x}{blue:02x}")

    def _build(self):
        self.accent = tk.Canvas(
            self, height=4, highlightthickness=0, bd=0, bg=BG, cursor="arrow"
        )
        self.accent.pack(fill="x")

        header = ctk.CTkFrame(self, fg_color="transparent")
        header.pack(fill="x", padx=26, pady=(14, 2))

        self.logo_image = self._logo_image()
        ctk.CTkLabel(header, text="", image=self.logo_image).pack(side="left", padx=(0, 14))

        titles = ctk.CTkFrame(header, fg_color="transparent")
        titles.pack(side="left", fill="x", expand=True)
        ctk.CTkLabel(
            titles,
            text="Μετατροπή σε εικονίδιο",
            font=ctk.CTkFont(family="Segoe UI", size=24, weight="bold"),
            text_color=TEXT,
            anchor="w",
        ).pack(anchor="w")
        ctk.CTkLabel(
            titles,
            text="Από εικόνα σε αρχείο .ico για τα Windows",
            font=ctk.CTkFont(family="Segoe UI", size=13),
            text_color=MUTED,
            anchor="w",
        ).pack(anchor="w", pady=(2, 0))

        card = ctk.CTkFrame(
            self,
            fg_color=CARD,
            corner_radius=22,
            border_width=1,
            border_color=BORDER,
        )
        card.pack(fill="both", expand=True, padx=22, pady=(10, 16))

        self.stage = ctk.CTkFrame(
            card,
            fg_color=WELL,
            corner_radius=18,
            border_width=1,
            border_color=BORDER,
            width=PREVIEW_BOX + 36,
            height=PREVIEW_BOX + 8,
        )
        self.stage.pack(padx=20, pady=(16, 6))
        self.stage.pack_propagate(False)

        self.empty_frame = ctk.CTkFrame(self.stage, fg_color="transparent")
        self.empty_frame.place(relx=0.5, rely=0.5, anchor="center")
        ctk.CTkLabel(
            self.empty_frame,
            text="ICO",
            font=ctk.CTkFont(family="Segoe UI", size=28, weight="bold"),
            text_color=CYAN,
        ).pack()
        ctk.CTkLabel(
            self.empty_frame,
            text="Επίλεξε εικόνα",
            font=ctk.CTkFont(family="Segoe UI", size=16, weight="bold"),
            text_color=TEXT,
        ).pack(pady=(6, 0))
        ctk.CTkLabel(
            self.empty_frame,
            text="PNG, JPG, WEBP ή BMP",
            font=ctk.CTkFont(family="Segoe UI", size=13),
            text_color=MUTED,
        ).pack(pady=(2, 0))

        self.preview_label = ctk.CTkLabel(self.stage, text="")
        self._bind_choose(self.stage)
        self._bind_choose(self.empty_frame)
        for child in self.empty_frame.winfo_children():
            self._bind_choose(child)

        self.stage.bind("<Enter>", lambda _e: self.stage.configure(border_color=ACCENT))
        self.stage.bind("<Leave>", lambda _e: self.stage.configure(border_color=BORDER))

        info = ctk.CTkFrame(card, fg_color="transparent")
        info.pack(fill="x", padx=26, pady=(8, 0))
        self.name_label = ctk.CTkLabel(
            info,
            text="Καμία εικόνα",
            font=ctk.CTkFont(family="Segoe UI", size=14, weight="bold"),
            text_color=TEXT,
            anchor="w",
        )
        self.name_label.pack(side="left")
        self.size_label = ctk.CTkLabel(
            info,
            text="Έξοδος  256 × 256",
            font=ctk.CTkFont(family="Segoe UI", size=12, weight="bold"),
            text_color=CYAN,
            fg_color=SOFT,
            corner_radius=12,
            width=150,
            height=28,
        )
        self.size_label.pack(side="right")

        self.detail_label = ctk.CTkLabel(
            card,
            text="Πάτα την περιοχή από πάνω ή το κουμπί επιλογής.",
            font=ctk.CTkFont(family="Segoe UI", size=12),
            text_color=MUTED,
            anchor="w",
        )
        self.detail_label.pack(fill="x", padx=26, pady=(4, 12))

        actions = ctk.CTkFrame(card, fg_color="transparent")
        actions.pack(fill="x", padx=22, pady=(0, 8))
        actions.grid_columnconfigure(0, weight=1)
        actions.grid_columnconfigure(1, weight=2)

        self.choose_button = ctk.CTkButton(
            actions,
            text="Επιλογή εικόνας",
            height=46,
            corner_radius=12,
            font=ctk.CTkFont(family="Segoe UI", size=14, weight="bold"),
            fg_color=GHOST,
            hover_color=GHOST_HOVER,
            border_width=1,
            border_color=ACCENT,
            text_color=TEXT,
            command=self.choose_file,
        )
        self.choose_button.grid(row=0, column=0, sticky="ew", padx=(0, 10))

        self.convert_button = ctk.CTkButton(
            actions,
            text="Μετατροπή σε ICO",
            height=46,
            corner_radius=12,
            font=ctk.CTkFont(family="Segoe UI", size=14, weight="bold"),
            fg_color=ACCENT,
            hover_color=ACCENT_HOVER,
            text_color="#ffffff",
            text_color_disabled="#7f93b3",
            state="disabled",
            command=self.convert,
        )
        self.convert_button.grid(row=0, column=1, sticky="ew")
        self._set_ready(False)

        ctk.CTkLabel(
            card,
            text="Το αρχείο αποθηκεύεται στον φάκελο  icon_output,  δίπλα στην εικόνα.",
            font=ctk.CTkFont(family="Segoe UI", size=12),
            text_color=MUTED,
            anchor="w",
        ).pack(fill="x", padx=26, pady=(8, 0))

        footer = ctk.CTkFrame(card, fg_color="#0b1628", corner_radius=14)
        footer.pack(fill="x", padx=18, pady=(14, 18))
        footer.grid_columnconfigure(0, weight=1)
        self.status_label = ctk.CTkLabel(
            footer,
            text="Διάλεξε μια εικόνα για να ξεκινήσεις.",
            font=ctk.CTkFont(family="Segoe UI", size=13),
            text_color=MUTED,
            anchor="w",
            justify="left",
            wraplength=300,
        )
        self.status_label.grid(row=0, column=0, sticky="ew", padx=(14, 8), pady=12)

        self.open_button = ctk.CTkButton(
            footer,
            text="Άνοιγμα φακέλου",
            width=176,
            height=36,
            corner_radius=10,
            font=ctk.CTkFont(family="Segoe UI", size=13, weight="bold"),
            fg_color=SOFT,
            hover_color=GHOST_HOVER,
            border_width=1,
            border_color=ACCENT,
            text_color=TEXT,
            command=self.open_output,
        )
        self.open_button.grid(row=0, column=1, sticky="e", padx=(0, 12), pady=12)
        self.open_button.grid_remove()

    def _logo_image(self):
        path = resource_path("My_convert_image2ico.ico")
        if os.path.exists(path):
            image = Image.open(path).convert("RGBA")
            image = image.resize((48, 48), Image.Resampling.LANCZOS)
        else:
            image = Image.new("RGBA", (48, 48), (0, 0, 0, 0))
            draw = ImageDraw.Draw(image)
            draw.rounded_rectangle((2, 2, 46, 46), radius=12, fill=ACCENT)
        return ctk.CTkImage(light_image=image, dark_image=image, size=(48, 48))

    def _bind_choose(self, widget):
        widget.bind("<Button-1>", lambda _event: self.choose_file())
        widget.configure(cursor="hand2")

    def _set_status(self, text, color=MUTED):
        self.status_label.configure(text=text, text_color=color)

    def _set_ready(self, ready):
        if ready:
            self.convert_button.configure(
                state="normal",
                fg_color=ACCENT,
                hover_color=ACCENT_HOVER,
                text_color="#ffffff",
            )
        else:
            self.convert_button.configure(
                state="disabled",
                fg_color="#16345c",
                text_color_disabled="#7f93b3",
            )

    def choose_file(self):
        path = filedialog.askopenfilename(
            parent=self,
            title="Επιλογή εικόνας",
            filetypes=[
                ("Εικόνες", "*.png *.jpg *.jpeg *.webp *.bmp"),
                ("PNG", "*.png"),
                ("Όλα τα αρχεία", "*.*"),
            ],
        )
        if path:
            self._load_file(path)

    def _load_file(self, path):
        try:
            image = Image.open(path)
            image.load()
        except Exception as error:
            self._set_status(f"Δεν άνοιξε η εικόνα. {error}", DANGER)
            return

        self.file_path = path
        self.output_folder = None
        self.open_button.grid_remove()

        preview = image.convert("RGBA")
        preview.thumbnail((PREVIEW_BOX - 24, PREVIEW_BOX - 24), Image.Resampling.LANCZOS)
        self.preview_image = ctk.CTkImage(
            light_image=preview, dark_image=preview, size=preview.size
        )
        self.empty_frame.place_forget()
        self.preview_label.configure(image=self.preview_image, text="")
        self.preview_label.place(relx=0.5, rely=0.5, anchor="center")
        self._bind_choose(self.preview_label)

        self.name_label.configure(text=shorten(os.path.basename(path)))
        width, height = image.size
        self.detail_label.configure(text=f"Αρχικό μέγεθος  {width} × {height} px")
        self._set_ready(True)
        self._set_status("Έτοιμο. Η μετατροπή θα δημιουργήσει εικονίδιο 256 × 256.", CYAN)

    def convert(self):
        if not self.file_path:
            return

        folder = os.path.dirname(self.file_path)
        name = os.path.splitext(os.path.basename(self.file_path))[0]
        output_folder = os.path.join(folder, "icon_output")
        output_path = os.path.join(output_folder, f"{name}.ico")

        try:
            os.makedirs(output_folder, exist_ok=True)
            image = Image.open(self.file_path).convert("RGBA")
            image.save(output_path, format="ICO", sizes=[(OUTPUT_SIZE, OUTPUT_SIZE)])
        except Exception as error:
            self.output_folder = None
            self.open_button.grid_remove()
            self._set_status(f"Σφάλμα κατά τη μετατροπή. {error}", DANGER)
            return

        self.output_folder = output_folder
        self.open_button.grid()
        self._set_status("Το εικονίδιο αποθηκεύτηκε.", SUCCESS)

    def open_output(self):
        if self.output_folder and os.path.isdir(self.output_folder):
            os.startfile(self.output_folder)


def main():
    enable_dpi()
    ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID("MyConvertImage2Ico.App")
    ctk.set_appearance_mode("dark")
    ctk.set_default_color_theme("dark-blue")
    app = App()
    app.mainloop()


if __name__ == "__main__":
    main()
