import tkinter as tk
from tkinter import messagebox, ttk
import os
import subprocess
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from datetime import datetime

# जागतिक लिस्ट एकाधिक आयटम साठवण्यासाठी
added_items = []

# ==========================================
# गुगल SHEET जोडणी (Google Sheet Connection)
# ==========================================
def get_next_bill_number_and_save(row_data_without_no):
    try:
        scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
        creds = ServiceAccountCredentials.from_json_keyfile_name("credentials.json", scope)
        client = gspread.authorize(creds)
        spreadsheet = client.open("बालाजी सायबर पॉइंट हिशोब")
        
        try:
            sheet = spreadsheet.worksheet("बिल डेटा")
        except gspread.exceptions.WorksheetNotFound:
            sheet = spreadsheet.add_worksheet(title="बिल डेटा", rows="1000", cols="10")
            sheet.append_row(["तारीख/वेळ", "बिल नंबर", "ग्राहक नाव", "मोबाईल नंबर", "कामाचा प्रकार", "एकूण रक्कम"])
        
        all_records = sheet.get_all_values()
        next_serial = 101
        if len(all_records) > 1:
            last_row = all_records[-1]
            last_bill_no = last_row[1]
            try:
                last_num = int(last_bill_no.split('-')[1])
                next_serial = last_num + 1
            except:
                next_serial = 101 + (len(all_records) - 1)

        final_bill_no = f"BCP-{next_serial}"
        full_row_data = [row_data_without_no[0], final_bill_no, row_data_without_no[1], row_data_without_no[2], row_data_without_no[3], row_data_without_no[4]]
        sheet.append_row(full_row_data)
        return True, final_bill_no
    except Exception as e:
        print(f"Google Sheet Error: {e}")
        return False, f"BCP-{datetime.now().strftime('%H%M%S')}"

# ==========================================
# ऑटो-कॅल्क्युलेटर लॉजिक (Smart Pricing)
# ==========================================
def on_service_change(event):
    service = combo_item.get()
    
    frame_xerox_calc.pack_forget()
    frame_photo_calc.pack_forget()
    frame_custom_service.pack_forget()
    
    if "Xerox" in service:
        frame_xerox_calc.pack(fill=tk.X, pady=5)
        entry_rate.delete(0, tk.END)
        entry_rate.insert(0, "5") 
        calculate_xerox()
        
    elif "Color Printout" in service:
        frame_xerox_calc.pack(fill=tk.X, pady=5)
        entry_rate.delete(0, tk.END)
        entry_rate.insert(0, "10") 
        calculate_xerox()
        
    elif "Lamination" in service:
        frame_xerox_calc.pack(fill=tk.X, pady=5)
        entry_rate.delete(0, tk.END)
        entry_rate.insert(0, "50") 
        calculate_xerox()
        
    elif "Passport Photo" in service:
        frame_photo_calc.pack(fill=tk.X, pady=5)
        combo_photo_type.set("4X6 - 9 Photo (₹ 60)")
        update_photo_price()
        
    elif "Other" in service:
        frame_custom_service.pack(fill=tk.X, pady=5)
        entry_custom_name.delete(0, tk.END)
        entry_amount.delete(0, tk.END)
        
    else:
        entry_amount.delete(0, tk.END)

def calculate_xerox(*args):
    try:
        pages = int(entry_pages.get() if entry_pages.get() else 1)
        copies = int(entry_copies.get() if entry_copies.get() else 1)
        rate = float(entry_rate.get() if entry_rate.get() else 0)
        total = pages * copies * rate
        entry_amount.delete(0, tk.END)
        entry_amount.insert(0, f"{total:.2f}")
    except ValueError:
        pass

def update_photo_price(*args):
    p_type = combo_photo_type.get()
    entry_amount.delete(0, tk.END)
    if "60" in p_type:
        entry_amount.insert(0, "60.00")
    else:
        entry_amount.insert(0, "150.00")

def add_item_to_list():
    service = combo_item.get()
    amt = entry_amount.get().strip()
    
    if service == "निवडा..." or not amt:
        messagebox.showerror("Error", "कृपया सेवा आणि रक्कम आधी भरा!")
        return
        
    if "Other" in service:
        custom_name = entry_custom_name.get().strip()
        if not custom_name:
            messagebox.showerror("Error", "कृपया कामाचे नाव टाईप करा!")
            return
        service = custom_name
        
    elif "Xerox" in service or "Color Printout" in service or "Lamination" in service:
        pages = entry_pages.get() if entry_pages.get() else "1"
        copies = entry_copies.get() if entry_copies.get() else "1"
        service = f"{service} ({pages} Pg x {copies} Copy)"
        
    elif "Passport Photo" in service:
        service = f"Passport Photo ({combo_photo_type.get().split(' (')[0]})"

    try:
        amt_val = float(amt)
    except ValueError:
        messagebox.showerror("Error", "रक्कम फक्त आकड्यात टाका!")
        return
        
    added_items.append((service, amt_val))
    listbox_summary.insert(tk.END, f" {len(added_items)}. {service} -> ₹ {amt_val}/-")
    
    combo_item.set("निवडा...")
    entry_amount.delete(0, tk.END)
    frame_xerox_calc.pack_forget()
    frame_photo_calc.pack_forget()
    frame_custom_service.pack_forget()

def clear_all_items():
    global added_items
    added_items = []
    listbox_summary.delete(0, tk.END)

def generate_and_print_all():
    global added_items
    cust_name = entry_cust_name.get().strip()
    cust_phone = entry_cust_phone.get().strip()
    current_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    wa_date = datetime.now().strftime("%Y-%m-%d %H:%M")
    
    if not cust_name:
        messagebox.showerror("Error", "कृपया ग्राहकाचे नाव आधी भरा!")
        return
    if not added_items:
        messagebox.showerror("Error", "बिलामध्ये किमान एक काम जोडणे आवश्यक आहे!")
        return
        
    total_amount = sum(item[1] for item in added_items)
    all_services_text = ", ".join(item[0] for item in added_items)
    
    sheet_success, bill_no = get_next_bill_number_and_save([current_date, cust_name, cust_phone, all_services_text, total_amount])
    
    table_rows_html = ""
    for idx, item in enumerate(added_items, start=1):
        table_rows_html += f"""
        <tr>
            <td style="text-align: center; border-bottom: 1px solid #ddd; padding: 10px;">{idx}</td>
            <td style="text-align: left; border-bottom: 1px solid #ddd; padding: 10px;"><b>{item[0]}</b></td>
            <td style="text-align: right; border-bottom: 1px solid #ddd; padding: 10px; font-weight: bold; white-space: nowrap;">₹ {item[1]:.2f}/-</td>
        </tr>
        """
    
    html_bill = f"""<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8">
    <style>
        @page {{ size: A5 portrait; margin: 0; }}
        body {{ font-family: 'Segoe UI', Arial, sans-serif; margin: 0; padding: 0; color: #333; -webkit-print-color-adjust: exact; print-color-adjust: exact; background-color: #f0f2f5; }}
        
        /* 📋 प्रिंटसाठी पाने (A5 Portrait) */
        .page-front {{ width: 138mm; height: 200mm; padding: 8mm; box-sizing: border-box; background-color: #ffffff; page-break-after: always; }}
        .page-back {{ width: 138mm; height: 198mm; padding: 10mm; box-sizing: border-box; background-color: #ffffff; page-break-after: always; }}
        
        .bill-box {{ border: 2.5px solid #0056b3; padding: 15px; border-radius: 8px; background-color: #ffffff; height: 100%; box-sizing: border-box; display: flex; flex-direction: column; justify-content: space-between; }}
        .header-table {{ width: 100%; border-bottom: 3.5px solid #0056b3; padding-bottom: 6px; }}
        .shop-name {{ color: #0056b3; font-size: 24px; font-weight: bold; margin: 0; }}
        .address {{ font-size: 11px; color: #555; margin: 2px 0; }}
        .contacts {{ font-size: 11px; font-weight: bold; color: #111; }}
        .bill-details {{ width: 100%; margin-top: 10px; font-size: 13px; border-collapse: collapse; }}
        .items-table {{ width: 100%; border-collapse: collapse; margin-top: 10px; font-size: 14px; table-layout: fixed; }}
        .items-table th {{ background-color: #0056b3; color: white; padding: 8px; font-weight: bold; }}
        .bottom-container {{ width: 100%; margin-top: 15px; border-collapse: collapse; }}
        .total-section {{ font-size: 16px; font-weight: bold; color: #0056b3; text-align: left; }}
        .stamp-box {{ border: 3px dashed #cc0000; color: #cc0000; font-size: 14px; font-weight: bold; text-align: center; padding: 4px 10px; width: 130px; border-radius: 5px; transform: rotate(-4deg); background-color: #fff5f5; font-weight: 900; line-height: 1.2; }}
        .services-box {{ border: 1.5px solid #0056b3; border-radius: 6px; background-color: #f4f8ff; padding: 10px; margin-top: 15px; }}
        .services-title {{ font-size: 12px; font-weight: bold; color: #0056b3; margin: 0 0 6px 0; border-bottom: 1.5px solid #0056b3; padding-bottom: 3px; text-align: center; }}
        .services-list {{ width: 100%; font-size: 11px; color: #111; font-weight: bold; border-collapse: collapse; }}
        .services-list td {{ padding: 3px 5px; width: 50%; }}
        .footer {{ text-align: center; font-size: 11px; color: #555; border-top: 1px dashed #ccc; padding-top: 6px; font-weight: bold; margin-top: 10px; }}
        
        .adv-box {{ border: 4px double #ff6600; padding: 15px; border-radius: 12px; text-align: center; height: 100%; box-sizing: border-box; display: flex; flex-direction: column; justify-content: space-between; }}
        .adv-title {{ font-size: 28px; font-weight: bold; color: #ff6600; margin: 0; }}
        .adv-subtitle {{ font-size: 14px; color: #555; margin: 3px 0 15px 0; font-weight: bold; border-bottom: 2.5px solid #ff6600; padding-bottom: 8px; letter-spacing: 0.5px; }}
        .adv-heading {{ font-size: 16px; font-weight: bold; color: #111; margin: 10px 0 6px 0; background: #ffe6d5; padding: 6px; border-radius: 5px; text-align: center; border-left: 5px solid #ff6600; }}
        .adv-table {{ width: 100%; font-size: 13px; text-align: left; border-collapse: collapse; font-weight: bold; margin-bottom: 2px; }}
        .adv-table td {{ padding: 6px 8px; color: #222; width: 50%; }}
        .adv-features {{ display: flex; justify-content: space-around; background: #fdfaf6; padding: 8px; border-radius: 6px; border: 1px dashed #ff6600; margin-top: 8px; }}
        .feature-item {{ font-size: 12px; font-weight: bold; color: #555; }}
        .adv-footer {{ font-size: 14px; font-weight: bold; color: #ff6600; background: #fff0e6; padding: 10px; border-radius: 6px; margin-top: 10px; line-height: 1.5; border: 1px solid #ff6600; }}

        /* 👑 स्क्रीनशॉटसाठी कडक व्हॉट्सॲप मेसेज बॉक्स डिझाईन (फक्त स्क्रीनवर दिसेल, प्रिंट होणार नाही) */
        .screenshot-container {{
            max-width: 420px;
            margin: 30px auto;
            padding: 15px;
            background-color: #eae6df; /* WhatsApp Background */
            border-radius: 10px;
            box-shadow: 0 4px 10px rgba(0,0,0,0.15);
        }}
        .wa-chat-bubble {{
            background-color: #d9fdd3; /* WhatsApp Light Green Message */
            padding: 14px;
            border-radius: 8px;
            font-family: 'Segoe UI', Arial, sans-serif;
            font-size: 14px;
            line-height: 1.5;
            color: #111b21;
            white-space: pre-wrap;
            border-bottom: 1px solid #e1e1e1;
            box-shadow: 0 1px 2px rgba(0,0,0,0.1);
        }}
        .wa-header-label {{
            text-align: center;
            font-size: 12px;
            font-weight: bold;
            color: #667781;
            margin-bottom: 10px;
            text-transform: uppercase;
        }}

        /* 🖨️ प्रिंट करताना स्क्रीनशॉटचा बॉक्स लपवण्यासाठी मॅजिक CSS */
        @media print {{
            .screenshot-container {{ display: none !important; }}
        }}
    </style>
</head>
<body>
    <!-- १. बिलाची पुढची बाजू -->
    <div class="page-front">
        <div class="bill-box">
            <div>
                <table class="header-table">
                    <tr>
                        <td>
                            <div class="shop-name">BALAJI CYBER POINT</div>
                            <div class="address">Mangaon, Raigad, Maharashtra</div>
                            <div class="contacts">📞 Call: 8007365051 | 💬 WA: 8806789013</div>
                        </td>
                        <td style="text-align: right; vertical-align: top;">
                            <h2 style="margin: 0; color: #0056b3; font-size: 18px;">INVOICE</h2>
                        </td>
                    </tr>
                </table>
                <table class="bill-details">
                    <tr><td><b>बिल क्र:</b> {bill_no}</td><td style="text-align: right;"><b>तारीख/वेळ:</b> {current_date}</td></tr>
                    <tr><td><b>ग्राहक नाव:</b> {cust_name}</td><td style="text-align: right;"><b>मोबाईल नं:</b> {cust_phone if cust_phone else '-'}</td></tr>
                </table>
                <table class="items-table">
                    <thead>
                        <tr>
                            <th style="width: 12%; text-align: center;">क्र.</th>
                            <th style="width: 63%; text-align: left;">कामाचा तपशील / सेवा प्रकार</th>
                            <th style="width: 25%; text-align: right;">रक्कम</th>
                        </tr>
                    </thead>
                    <tbody>{table_rows_html}</tbody>
                </table>
            </div>
            <div>
                <table class="bottom-container">
                    <tr>
                        <td class="total-section" style="vertical-align: middle;">एकूण देय रक्कम: ₹ {total_amount:.2f}/-</td>
                        <td style="text-align: right; width: 140px;">
                            <div class="stamp-box">PAID<br><span style="font-size:8px; font-weight:bold;">BALAJI CYBER POINT</span></div>
                        </td>
                    </tr>
                </table>
                <div class="services-box">
                    <div class="services-title">⚡ आमच्याकडील प्रमुख सेवा Center ⚡</div>
                    <table class="services-list">
                        <tr><td>• On-line सर्व सरकारी फॉर्म</td><td>• नवीन पॅन कार्ड / दुरुस्ती</td></tr>
                        <tr><td>• मतदार कार्ड (Voter ID) कामे</td><td>• लाईट बिल भरणे केंद्र</td></tr>
                        <tr><td>• पासपोर्ट व ड्रायव्हिंग लायसन्स</td><td>• गॅझेट गॅरंटी (नाव बदलणे)</td></tr>
                        <tr><td>• डोमासिएल / उत्पन्न दाखला</td><td>• कलर PRINTING व लॅमिनेशन</td></tr>
                    </table>
                </div>
                <div class="footer">🙏 धन्यवाद! पुन्हा भेट द्या! 🙏</div>
            </div>
        </div>
    </div>
    
    <!-- २. बिलाची मागची बाजू (जाहिरात) -->
    <div class="page-back">
        <div class="adv-box">
            <div>
                <div class="adv-title">BALAJI CYBER POINT</div>
                <div class="adv-subtitle">डिजिटल क्रांती आणि शासकीय सेवा केंद्र</div>
                <div class="adv-heading">🎯 सर्व ऑनलाईन सेवा एकाच छताखाली!</div>
                <table class="adv-table">
                    <tr><td>✅ महा-ई-सेवा केंद्र कामे</td><td>✅ नवीन पॅन कार्ड / दुरुस्ती</td></tr>
                    <tr><td>✅ मतदार कार्ड आणि आधार लिंक</td><td>✅ लाईट बिल पेमेंट सुविधा Center</td></tr>
                    <tr><td>✅ गॅझेट गॅरंटी (नाव/धर्म बदलणे)</td><td>✅ पासपोर्ट आणि लायसन्स अर्ज</td></tr>
                    <tr><td>✅ डोमासिएल, उत्पन्न व जातीचे दाखले</td><td>✅ सर्व प्रकारचे ऑनलाईन जॉब फॉर्म</td></tr>
                </table>
                <div class="adv-heading">🖨️ स्पेशल प्रिंटिंग आणि बुकिंग सेवा</div>
                <table class="adv-table">
                    <tr><td>🚀 A3 हाय-क्वालिटी प्रिंटिंग</td><td>🔥 A3 आणि A4 कडक लॅमिनेशन</td></tr>
                    <tr><td>✈️ फ्लाईट बुकिंग (Flight Tickets)</td><td>📸 पासपोर्ट साईझ फोटो</td></tr>
                    <tr><td>🗂️  कलर झेरॉक्स आणि स्कॅनिंग</td><td>👮 पोलीस व्हेरिफिकेशन (Police Verification)</td></tr>
                </table>
                <div class="adv-features">
                    <div class="feature-item">⚡ अचूक काम</div>
                    <div class="feature-item">🚀 जलद सेवा</div>
                    <div class="feature-item">💎 वाजवी दर</div>
                </div>
            </div>
            <div class="adv-footer">
                📍 पत्ता: बालाजी कॉम्प्लेक्स, माणगाव, रायगड, महाराष्ट्र<br>
                📞 संपर्क: 8007365051 | 💬 व्हॉट्सॲप: 8806789013
            </div>
        </div>
    </div>

    <!-- 👑 ३. स्क्रीनशॉट काढण्यासाठी सुंदर व्हॉट्सॲप मेसेज प्रिव्ह्यू बॉक्स -->
    <div class="screenshot-container">
        <div class="wa-header-label">📸 Win + Shift + S दाबून स्क्रीनशॉट काढा</div>
        <div class="wa-chat-bubble"><b>🧾 BALAJI CYBER POINT 🧾</b>
<i>डिजिटल क्रांती आणि शासकीय सेवा केंद्र, माणगाव</i>
───────────────────────
प्रिय <b>{cust_name}</b>,
आपले डिजिटल बिल यशस्वीरित्या तयार झाले आहे:

📄 <b>बिल नंबर:</b> <code>{bill_no}</code>
📅 <b>तारीख/वेळ:</b> {wa_date}
🛠️ <b>कामाचा तपशील:</b> {all_services_text}
💰 <b>एकूण देय रक्कम:</b> ₹ <b>{total_amount:.2f}/-</b>
───────────────────────
👍 <b>STATUS: PAID</b> (बालाजी कॉम्प्लेक्स, माणगाव)
📞 <b>Call:</b> 8007365051 | <b>WA:</b> 8806789013
🙏 <b>धन्यवाद! पुन्हा भेट द्या!</b></div>
    </div>
</body>
</html>
"""
    
    file_path = os.path.abspath("temp_bill.html")
    with open(file_path, "w", encoding="utf-8") as f:
        f.write(html_bill)
        
    try:
        edge_path = "C:\\Program Files (x86)\\Microsoft\\Edge\\Application\\msedge.exe"
        if not os.path.exists(edge_path): edge_path = "C:\\Program Files\\Microsoft\\Edge\\Application\\msedge.exe"
        if os.path.exists(edge_path):
            subprocess.Popen([edge_path, "--kiosk", "--kiosk-printing", "--no-margin", f"file:///{file_path}"])
        else:
            import webbrowser
            webbrowser.open("file://" + file_path)

        if sheet_success:
            messagebox.showinfo("Success", f"बिल {bill_no} सुरक्षित झाले आणि स्क्रीनवर प्रिव्ह्यू उघडला!")
            entry_cust_name.delete(0, tk.END)
            entry_cust_phone.delete(0, tk.END)
            clear_all_items()
    except Exception as e:
        messagebox.showerror("Printer Error", f"प्रिंटर अडचण: {e}")

# === GUI डिझाईन ===
root = tk.Tk()
root.title("Balaji Cyber Point - Smart Billing System")
root.geometry("500x720")
root.configure(bg="#F4F6F9")

header = tk.Label(root, text="🧾 बालाजी सायबर पॉइंट - स्मार्ट बिल मेकर 🧾", font=("Arial", 14, "bold"), bg="#0056b3", fg="white", pady=10)
header.pack(fill=tk.X)

frame = tk.Frame(root, bg="#F4F6F9", padx=20, pady=5)
frame.pack(fill=tk.BOTH, expand=True)

tk.Label(frame, text="ग्राहक नाव (Customer Name):", font=("Arial", 10, "bold"), bg="#F4F6F9").pack(anchor="w", pady=(5, 0))
entry_cust_name = tk.Entry(frame, font=("Arial", 11), bd=1, relief="solid")
entry_cust_name.pack(fill=tk.X, ipady=3)

tk.Label(frame, text="मोबाईल नंबर (Optional):", font=("Arial", 10, "bold"), bg="#F4F6F9").pack(anchor="w", pady=(5, 0))
entry_cust_phone = tk.Entry(frame, font=("Arial", 11), bd=1, relief="solid")
entry_cust_phone.pack(fill=tk.X, ipady=3)

tk.Label(frame, text="────────── काम आणि कॅल्क्युलेटर ──────────", font=("Arial", 10, "bold"), fg="#0056b3", bg="#F4F6F9", pady=8).pack(fill=tk.X)

tk.Label(frame, text="सेवा निवडा (Select Service):", font=("Arial", 10, "bold"), bg="#F4F6F9").pack(anchor="w")
services = [
    "Xerox / झेरॉक्स", 
    "Color Printout / कलर प्रिंट", 
    "Lamination / लॅमिनेशन", 
    "Passport Photo / पासपोर्ट फोटो",
    "Online Form / ऑनलाईन फॉर्म फी",
    "Other / इतर सेवा (मॅन्युअली रक्कम टाका)"
]
combo_item = ttk.Combobox(frame, values=services, font=("Arial", 11), state="readonly")
combo_item.set("निवडा...")
combo_item.pack(fill=tk.X, ipady=3)
combo_item.bind("<<ComboboxSelected>>", on_service_change)

frame_xerox_calc = tk.Frame(frame, bg="#E6EEF8", padx=5, pady=5, bd=1, relief="groove")
tk.Label(frame_xerox_calc, text="पेजेस (Pages):", font=("Arial", 9, "bold"), bg="#E6EEF8").grid(row=0, column=0, padx=5, pady=5)
entry_pages = tk.Entry(frame_xerox_calc, font=("Arial", 10), width=6, bd=1)
entry_pages.insert(0, "1")
entry_pages.grid(row=0, column=1, padx=5)
entry_pages.bind("<KeyRelease>", calculate_xerox)

tk.Label(frame_xerox_calc, text="कॉपी (Copies):", font=("Arial", 9, "bold"), bg="#E6EEF8").grid(row=0, column=2, padx=5)
entry_copies = tk.Entry(frame_xerox_calc, font=("Arial", 10), width=6, bd=1)
entry_copies.insert(0, "1")
entry_copies.grid(row=0, column=3, padx=5)
entry_copies.bind("<KeyRelease>", calculate_xerox)

tk.Label(frame_xerox_calc, text="दर (Rate ₹):", font=("Arial", 9, "bold"), bg="#E6EEF8").grid(row=0, column=4, padx=5)
entry_rate = tk.Entry(frame_xerox_calc, font=("Arial", 10), width=6, bd=1)
entry_rate.grid(row=0, column=5, padx=5)
entry_rate.bind("<KeyRelease>", calculate_xerox)

frame_photo_calc = tk.Frame(frame, bg="#E6EEF8", padx=5, pady=5, bd=1, relief="groove")
tk.Label(frame_photo_calc, text="फोटो पॅक निवडा:", font=("Arial", 9, "bold"), bg="#E6EEF8").pack(side=tk.LEFT, padx=5)
combo_photo_type = ttk.Combobox(frame_photo_calc, values=["4X6 - 9 Photo (₹ 60)", "A4 - 36 Photo (₹ 150)"], font=("Arial", 10), state="readonly")
combo_photo_type.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=5)
combo_photo_type.bind("<<ComboboxSelected>>", update_photo_price)

frame_custom_service = tk.Frame(frame, bg="#FFEAD2", padx=5, pady=5, bd=1, relief="groove")
tk.Label(frame_custom_service, text="कामाचे नाव लिहा:", font=("Arial", 9, "bold"), bg="#FFEAD2").pack(side=tk.LEFT, padx=5)
entry_custom_name = tk.Entry(frame_custom_service, font=("Arial", 10), bd=1)
entry_custom_name.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=5)

tk.Label(frame, text="एकूण रक्कम (₹) [येथे रक्कम बदलू शकता]:", font=("Arial", 10, "bold"), fg="#cc0000", bg="#F4F6F9").pack(anchor="w", pady=(8, 0))
entry_amount = tk.Entry(frame, font=("Arial", 12, "bold"), bd=1, relief="solid", fg="#cc0000")
entry_amount.pack(fill=tk.X, ipady=3)

btn_add = tk.Button(frame, text="➕ Add Item (यादीत काम जोडा)", font=("Arial", 11, "bold"), bg="#FFA500", fg="white", command=add_item_to_list)
btn_add.pack(fill=tk.X, pady=8)

tk.Label(frame, text="सध्या बिलात जोडलेली कामे:", font=("Arial", 10, "bold"), bg="#F4F6F9").pack(anchor="w")
listbox_summary = tk.Listbox(frame, font=("Arial", 10), height=4, bd=1, relief="solid")
listbox_summary.pack(fill=tk.BOTH, expand=True)

btn_clear = tk.Button(frame, text="❌ Clear List", font=("Arial", 9), bg="#d9534f", fg="white", bd=0, command=clear_all_items)
btn_clear.pack(anchor="e", pady=2)

btn_bill = tk.Button(root, text="🖨️ Print & Show WhatsApp Preview", font=("Arial", 12, "bold"), bg="#0056b3", fg="white", bd=1, relief="raised", command=generate_and_print_all)
btn_bill.pack(fill=tk.X, padx=25, pady=(5, 15), ipady=8)

root.mainloop()
