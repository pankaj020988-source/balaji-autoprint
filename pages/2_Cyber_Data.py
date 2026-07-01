import tkinter as tk
from tkinter import messagebox
import webbrowser
from urllib.parse import quote
import os

# --- Function to format the receipt text ---
def get_formatted_text():
    c_name = entry_name.get()
    c_phone = entry_phone.get()
    f_purpose = entry_purpose.get()
    f_id = entry_id.get()
    f_pass = entry_pass.get()
    f_site = entry_site.get()

    # The Receipt Format
    text = f"""
*************************************
      BALAJI CYBER POINT
*************************************
Customer: {c_name}
Phone: {c_phone}
-------------------------------------
Form Details:
Purpose: {f_purpose}
Website: {f_site}

Login ID: {f_id}
Password: {f_pass}
-------------------------------------
Thank you for visiting!
*************************************
"""
    return text, c_phone

# --- Function to Save and Open for Printing ---
def save_and_print():
    receipt_text, _ = get_formatted_text()
    
    # Save to a text file
    filename = "Customer_Receipt.txt"
    with open(filename, "w", encoding="utf-8") as f:
        f.write(receipt_text)
    
    # Open the file automatically (usually opens in Notepad)
    os.startfile(filename) 

# --- Function to Send via WhatsApp ---
def send_whatsapp():
    receipt_text, phone = get_formatted_text()
    
    if not phone:
        messagebox.showerror("Error", "Please enter a Phone Number to WhatsApp.")
        return

    # Encode the message for the URL
    encoded_message = quote(receipt_text)
    
    # Create the WhatsApp Web link
    # Note: Phone number should usually include country code (e.g., 91 for India)
    whatsapp_url = f"https://web.whatsapp.com/send?phone=91{phone}&text={encoded_message}"
    
    # Open browser
    webbrowser.open(whatsapp_url)

# --- GUI Setup (The Window) ---
root = tk.Tk()
root.title("Balaji Cyber Point - Manager")
root.geometry("400x550")

# Heading
lbl_title = tk.Label(root, text="BALAJI CYBER POINT", font=("Arial", 16, "bold"), bg="orange", fg="white")
lbl_title.pack(fill="x", pady=10)

# Input Fields
frame_inputs = tk.Frame(root, padx=20, pady=10)
frame_inputs.pack(fill="both", expand=True)

tk.Label(frame_inputs, text="Customer Name:").pack(anchor="w")
entry_name = tk.Entry(frame_inputs)
entry_name.pack(fill="x", pady=5)

tk.Label(frame_inputs, text="Phone Number (10 digits):").pack(anchor="w")
entry_phone = tk.Entry(frame_inputs)
entry_phone.pack(fill="x", pady=5)

tk.Label(frame_inputs, text="Form Name / Purpose:").pack(anchor="w")
entry_purpose = tk.Entry(frame_inputs)
entry_purpose.pack(fill="x", pady=5)

tk.Label(frame_inputs, text="Website Used:").pack(anchor="w")
entry_site = tk.Entry(frame_inputs)
entry_site.pack(fill="x", pady=5)

tk.Label(frame_inputs, text="Login / User ID:").pack(anchor="w")
entry_id = tk.Entry(frame_inputs)
entry_id.pack(fill="x", pady=5)

tk.Label(frame_inputs, text="Password:").pack(anchor="w")
entry_pass = tk.Entry(frame_inputs)
entry_pass.pack(fill="x", pady=5)

# Buttons
btn_print = tk.Button(root, text="📄 Save & Print Receipt", bg="lightblue", font=("Arial", 10, "bold"), command=save_and_print)
btn_print.pack(fill="x", padx=20, pady=5)

btn_wa = tk.Button(root, text="📱 Send via WhatsApp", bg="lightgreen", font=("Arial", 10, "bold"), command=send_whatsapp)
btn_wa.pack(fill="x", padx=20, pady=10)

# Start the App
root.mainloop()
