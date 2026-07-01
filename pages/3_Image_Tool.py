import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image, ImageOps

def create_layout(paper_type):
    file_path = filedialog.askopenfilename(title="Select ID Photo", filetypes=[("Image Files", "*.jpg *.jpeg *.png")])
    if not file_path:
        return

    # Constants (300 DPI is standard for high-quality print)
    DPI = 300
    id_w, id_h = int(3.5 / 2.54 * DPI), int(4.5 / 2.54 * DPI)  # 3.5x4.5 cm in pixels
    
    # Paper sizes in pixels
    paper_sizes = {
        "4x6": (int(4 * DPI), int(6 * DPI)),
        "A4": (int(8.27 * DPI), int(11.69 * DPI))
    }
    
    canvas_w, canvas_h = paper_sizes[paper_type]
    
    try:
        img = Image.open(file_path)
        # Resize photo to 3.5 x 4.5 cm
        img = ImageOps.fit(img, (id_w, id_h), Image.Resampling.LANCZOS)
        
        # Create blank white paper
        sheet = Image.new("RGB", (canvas_w, canvas_h), "white")
        
        # Calculate how many photos fit
        margin = 20
        x_offset, y_offset = margin, margin
        
        for y in range(margin, canvas_h - id_h, id_h + margin):
            for x in range(margin, canvas_w - id_w, id_w + margin):
                sheet.paste(img, (x, y))
        
        save_path = filedialog.asksaveasfilename(defaultextension=".pdf", filetypes=[("PDF", "*.pdf"), ("JPEG", "*.jpg")])
        if save_path:
            sheet.save(save_path, quality=95, dpi=(DPI, DPI))
            messagebox.showinfo("Success", f"Layout saved to {save_path}")
            
    except Exception as e:
        messagebox.showerror("Error", str(e))

# Simple GUI
root = tk.Tk()
root.title("ID Photo Tool")
root.geometry("300x200")

tk.Label(root, text="Convert ID Photo to Sheet", font=("Arial", 12, "bold")).pack(pady=10)
tk.Button(root, text="Generate 4x6 Inch Sheet", command=lambda: create_layout("4x6")).pack(pady=5)
tk.Button(root, text="Generate Full A4 Sheet", command=lambda: create_layout("A4")).pack(pady=5)

root.mainloop()
