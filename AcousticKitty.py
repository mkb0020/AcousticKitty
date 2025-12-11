import tkinter as tk
from tkinter import filedialog, messagebox, ttk
import os
import math
from PIL import Image

# ------------------------------------------------------------
# CONVERT HEX
# ------------------------------------------------------------
def hex_to_rgb(hex_color):
    hex_color = hex_color.strip().lstrip("#")
    if len(hex_color) != 6:
        raise ValueError("Invalid hex color: " + hex_color)
    r = int(hex_color[0:2], 16)
    g = int(hex_color[2:4], 16)
    b = int(hex_color[4:6], 16)
    return (r, g, b)

# ------------------------------------------------------------
# TAB 1: SPRITE SHEET BUILDER
# ------------------------------------------------------------
def build_sheet():
    folder = folder_var.get().strip()
    output = sheet_output_var.get().strip()
    cols = int(cols_var.get())
    padding = int(padding_var.get())

    if not folder or not os.path.isdir(folder):
        messagebox.showerror("Error", "Please select a valid folder.")
        return

    if not output:
        messagebox.showerror("Error", "Please enter an output filename.")
        return

    files = sorted([
        f for f in os.listdir(folder)
        if f.lower().endswith(".png") and f != output
    ])

    if not files:
        messagebox.showerror("Error", "No PNGs found in selected folder.")
        return

    # FIRST FRAME WILL BE BASE SIZE
    first_img = Image.open(os.path.join(folder, files[0])).convert("RGBA")
    w, h = first_img.size

    w_with_pad = w + padding
    h_with_pad = h + padding

    rows = math.ceil(len(files) / cols)
    sheet_width = w_with_pad * cols
    sheet_height = h_with_pad * rows

    sheet = Image.new("RGBA", (sheet_width, sheet_height), (0, 0, 0, 0))

    for i, filename in enumerate(files):
        frame = Image.open(os.path.join(folder, filename)).convert("RGBA")
        x = (i % cols) * w_with_pad
        y = (i // cols) * h_with_pad
        sheet.paste(frame, (x, y))

    if not output.lower().endswith(".png"):
        output += ".png"

    sheet.save(os.path.join(folder, output))

    messagebox.showinfo("Done", f"Sprite sheet created:\n{output}")

# ------------------------------------------------------------
# TAB 2: RECOLOR A SINGLE SPRITE SHEET
# ------------------------------------------------------------
def recolor_image():
    input_path = recolor_input_var.get().strip()
    output_path = recolor_output_var.get().strip()

    if not input_path or not os.path.exists(input_path):
        messagebox.showerror("Error", "Please select a valid input image.")
        return

    if not output_path:
        messagebox.showerror("Error", "Please enter an output filename.")
        return

    # GET PALETTE FROM TEXT BOXES
    palette_hex = [
        recolor_color1.get(),
        recolor_color2.get(),
        recolor_color3.get(),
        recolor_color4.get(),
        recolor_color5.get()
    ]

    try:
        palette = [hex_to_rgb(c) for c in palette_hex]
    except ValueError as e:
        messagebox.showerror("Error", str(e))
        return


    # BUILD SPRITE SHEET USING THESE COLORS
    MASTER_COLORS = [
        (255,255,255),
        (124,124,125),
        (167,167,168),
        (180,180,180),
        (0,0,0)
    ]

    img = Image.open(input_path).convert("RGBA")
    pixels = img.load()
    w, h = img.size

    for y in range(h):
        for x in range(w):
            r, g, b, a = pixels[x, y]
            if a == 0:
                continue
            for i, master in enumerate(MASTER_COLORS):
                if (r, g, b) == master:
                    new_r, new_g, new_b = palette[i]
                    pixels[x, y] = (new_r, new_g, new_b, a)
                    break

    if not output_path.lower().endswith(".png"):
        output_path += ".png"

    out_full = os.path.join(os.path.dirname(input_path), output_path)
    img.save(out_full)
    messagebox.showinfo("Done", f"Recolored sheet saved as:\n{output_path}")

# ------------------------------------------------------------
# TAB 3: BATCH RE-COLOR
# ------------------------------------------------------------
def batch_recolor():
    folder = batch_folder_var.get().strip()

    if not folder or not os.path.isdir(folder):
        messagebox.showerror("Error", "Select a valid folder.")
        return

    # PALETTE TEXT FIELDS
    palette_hex = [
        batch_color1.get(),
        batch_color2.get(),
        batch_color3.get(),
        batch_color4.get(),
        batch_color5.get()
    ]

    try:
        palette = [hex_to_rgb(c) for c in palette_hex]
    except ValueError as e:
        messagebox.showerror("Error", str(e))
        return

    MASTER_COLORS = [
        (255,255,255),
        (124,124,125),
        (167,167,168),
        (180,180,180),
        (0,0,0)
    ]

    pngs = [f for f in os.listdir(folder) if f.lower().endswith(".png")]

    if not pngs:
        messagebox.showerror("Error", "No PNG files found in folder!")
        return

    for filename in pngs:
        path = os.path.join(folder, filename)
        img = Image.open(path).convert("RGBA")
        pixels = img.load()
        w, h = img.size

        for y in range(h):
            for x in range(w):
                r, g, b, a = pixels[x, y]
                if a == 0:
                    continue

                for i, master in enumerate(MASTER_COLORS):
                    if (r, g, b) == master:
                        new_r, new_g, new_b = palette[i]
                        pixels[x, y] = (new_r, new_g, new_b, a)
                        break

        new_name = f"recolor_{filename}"
        img.save(os.path.join(folder, new_name))

    messagebox.showinfo("Done", "Batch recolor complete!")

# ------------------------------------------------------------
# GUI SETUP 
# ------------------------------------------------------------

root = tk.Tk()
root.title("Acoustic Kitty Sprite Tool")
root.geometry("650x650")
root.resizable(False, False)

BG = "#15191C"
FG = "#00FFFF"
ACCENT = "#A55AFF"
TAB_BG = "#830CDE"
INPUT_BG = "#DBE2E9"
TIP = "#ffffff"

root.configure(bg=BG)

style = ttk.Style()
style.theme_use("default")

# NOTEBOOK THEME
style.configure(
    "TNotebook",
    background=BG,
    borderwidth=5,
)

style.configure(
    "TNotebook.Tab",
    background=TAB_BG,
    foreground=FG,
    padding=[10, 5],
    font=("Arial bold", 12),
)

style.map(
    "TNotebook.Tab",
    background=[("selected", "#00FFFF")],
    foreground=[("selected", "#37025A")],
)

style.configure("TFrame", background=BG)
style.configure("TLabel", background=BG, foreground=FG, font=("arial", 14))
style.configure("TButton", background='#830CDE', foreground=FG, padding=6, font=("arial bold", 12))

notebook = ttk.Notebook(root)
notebook.pack(fill="both", expand=True, padx=20, pady=20)

# ------------------------------------------------------------
# LABELS
# ------------------------------------------------------------
def section_title(parent, text):
    ttk.Label(parent, text=text, font=("arial", 14, "bold")).pack(anchor="w", padx=20, pady=(20, 2))

def tip(parent, text):
    ttk.Label(parent, text=text, font=("arial", 12), foreground=TIP).pack(anchor="w", padx=20, pady=(10, 2))

# ============================================================
# TAB 1 — SPRITE SHEET BUILDER
# ============================================================
tab1 = ttk.Frame(notebook)
notebook.add(tab1, text="BUILD")

section_title(tab1, "SPRITE SHEET BUILDER")
tip(tab1, "Combine multiple frames into one sheet. Make sure all frames are the same size!")

folder_var = tk.StringVar()
sheet_output_var = tk.StringVar(value="spritesheet.png")
cols_var = tk.StringVar(value="1")
padding_var = tk.StringVar(value="0")

ttk.Label(tab1, text="Frame Folder:").pack(anchor="w", padx=20, pady=(10,0))
ttk.Entry(tab1, textvariable=folder_var).pack(anchor="w", padx=20, fill="x")
ttk.Button(tab1, text="Browse", command=lambda: folder_var.set(filedialog.askdirectory())).pack(anchor="w", padx=20, pady=10)

ttk.Label(tab1, text="Columns:").pack(anchor="w", padx=20, pady=(10,0))
ttk.Entry(tab1, textvariable=cols_var, width=8).pack(anchor="w", padx=20)

ttk.Label(tab1, text="Padding (px):").pack(anchor="w", padx=20, pady=(10,0))
ttk.Entry(tab1, textvariable=padding_var, width=8).pack(anchor="w", padx=20)

ttk.Label(tab1, text="Output Filename:").pack(anchor="w", padx=20, pady=(10,0))
ttk.Entry(tab1, textvariable=sheet_output_var).pack(anchor="w", padx=20, fill="x")
tip(tab1, "Output file will be saved in the input folder.")


ttk.Button(tab1, text="BUILD SPRITE SHEET", command=build_sheet).pack(pady=30)

# ============================================================
# TAB 2 — SINGLE SHEET RECOLOR
# ============================================================
tab2 = ttk.Frame(notebook)
notebook.add(tab2, text="COLOR x1")

section_title(tab2, "RECOLOR ONE SPRITE SHEET")
tip(tab2, "When you make your sprite sheet, use the greyscale palette below.  Then change the hex codes below to the colors you want to recolor your sprite sheet(s) to.")

recolor_input_var = tk.StringVar()
recolor_output_var = tk.StringVar(value="recolor.png")

ttk.Label(tab2, text="Sprite Sheet to recolor:").pack(anchor="w", padx=20)
ttk.Entry(tab2, textvariable=recolor_input_var).pack(anchor="w", padx=20, fill="x")
ttk.Button(tab2, text="Browse", command=lambda: recolor_input_var.set(filedialog.askopenfilename(filetypes=[("PNG files",".png")]))).pack(anchor="w", padx=20, pady=10)

section_title(tab2, "Output Palette (Hex Colors)")
tip(tab2, "Each grayscale shade will be replaced with your selected colors.")

recolor_color1 = ttk.Entry(tab2); recolor_color1.insert(0, "#FFFFFF")
recolor_color2 = ttk.Entry(tab2); recolor_color2.insert(0, "#7C7C7D")
recolor_color3 = ttk.Entry(tab2); recolor_color3.insert(0, "#A7A7A8")
recolor_color4 = ttk.Entry(tab2); recolor_color4.insert(0, "#B4B4B4")
recolor_color5 = ttk.Entry(tab2); recolor_color5.insert(0, "#000000")

for e in [recolor_color1, recolor_color2, recolor_color3, recolor_color4, recolor_color5]:
    e.pack(anchor="w", padx=20, fill="x", pady=1)

ttk.Label(tab2, text="Output Filename:").pack(anchor="w", padx=20, pady=(10,0))
ttk.Entry(tab2, textvariable=recolor_output_var).pack(anchor="w", padx=20, fill="x")
tip(tab2, "Output file will be saved in the same folder as the input.")


ttk.Button(tab2, text="COLOR!", command=recolor_image).pack(pady=20)

# ============================================================
# TAB 3 — BATCH RECOLOR
# ============================================================
tab3 = ttk.Frame(notebook)
notebook.add(tab3, text="BATCH COLOR")

section_title(tab3, "RECOLOR MULTIPLE SPRITE SHEETS")
tip(tab3, "All PNGs in the selected folder will be recolored in a batch using your palette.")

batch_folder_var = tk.StringVar()

ttk.Label(tab3, text="Folder containing PNGs:").pack(anchor="w", padx=20)
ttk.Entry(tab3, textvariable=batch_folder_var).pack(anchor="w", padx=20, fill="x")
ttk.Button(tab3, text="Browse", command=lambda: batch_folder_var.set(filedialog.askdirectory())).pack(anchor="w", padx=20, pady=10)

section_title(tab3, "Palette Colors")
batch_color1 = ttk.Entry(tab3); batch_color1.insert(0, "#FFFFFF")
batch_color2 = ttk.Entry(tab3); batch_color2.insert(0, "#7C7C7D")
batch_color3 = ttk.Entry(tab3); batch_color3.insert(0, "#A7A7A8")
batch_color4 = ttk.Entry(tab3); batch_color4.insert(0, "#B4B4B4")
batch_color5 = ttk.Entry(tab3); batch_color5.insert(0, "#000000")

for e in [batch_color1, batch_color2, batch_color3, batch_color4, batch_color5]:
    e.pack(anchor="w", padx=20, fill="x", pady=5)

tip(tab3, "Output file will be saved in the input folder.")

ttk.Button(tab3, text="COLOR All!", command=batch_recolor).pack(pady=30)

# ------------------------------------------------------------
# RUN IT!
# ------------------------------------------------------------
root.mainloop()
