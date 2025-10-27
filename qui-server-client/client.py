import socket
import threading
import tkinter as tk
from tkinter import scrolledtext, messagebox

# 🧠 تابع برای دریافت پیام‌ها از سرور
def receive_messages():
    while True:
        try:
            msg = client.recv(1024).decode()
            if not msg:
                break
            chat_box.config(state=tk.NORMAL)
            chat_box.insert(tk.END, msg + "\n")
            chat_box.config(state=tk.DISABLED)
            chat_box.see(tk.END)
        except:
            messagebox.showerror("خطا", "ارتباط با سرور قطع شد!")
            client.close()
            break

# 📤 تابع برای ارسال پیام
def send_message():
    msg = msg_entry.get()
    if msg.strip() == "":
        return
    full_msg = f"{nickname}: {msg}"
    client.send(full_msg.encode())
    msg_entry.delete(0, tk.END)

# 🚪 تابع خروج از برنامه
def on_close():
    try:
        client.close()
    except:
        pass
    root.destroy()

# 🌐 اتصال به سرور
def connect_to_server():
    global client, nickname
    nickname = name_entry.get()
    if not nickname:
        messagebox.showwarning("هشدار", "لطفاً نام کاربری وارد کن!")
        return

    try:
        client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client.connect(('localhost', 12345))
    except:
        messagebox.showerror("خطا", "اتصال به سرور ممکن نیست!")
        return

    name_window.destroy()  # بستن پنجره نام کاربری

    # راه‌اندازی رابط چت
    global root, chat_box, msg_entry
    root = tk.Tk()
    root.title(f"💬 چت {nickname}")
    root.geometry("400x450")
    root.protocol("WM_DELETE_WINDOW", on_close)

    chat_box = scrolledtext.ScrolledText(root, wrap=tk.WORD, state=tk.DISABLED)
    chat_box.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)

    msg_entry = tk.Entry(root)
    msg_entry.pack(padx=10, pady=(0,5), fill=tk.X)
    msg_entry.bind("<Return>", lambda event: send_message())

    send_btn = tk.Button(root, text="ارسال", command=send_message)
    send_btn.pack(pady=5)

    # شروع Thread دریافت پیام‌ها
    recv_thread = threading.Thread(target=receive_messages, daemon=True)
    recv_thread.start()

    root.mainloop()

# 🧩 پنجره‌ی اول برای ورود نام کاربری
name_window = tk.Tk()
name_window.title("ورود به چت")
name_window.geometry("250x120")

tk.Label(name_window, text="👤 نام کاربری:").pack(pady=5)
name_entry = tk.Entry(name_window)
name_entry.pack(pady=5)

join_btn = tk.Button(name_window, text="ورود", command=connect_to_server)
join_btn.pack(pady=10)

name_window.mainloop()
