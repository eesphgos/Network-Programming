import socket
import threading
from datetime import datetime
import os

clients = []

def broadcast(message, sender_conn):
    """ارسال پیام به تمام کلاینت‌ها"""
    for client in clients:
        try:
            client.send(message)
        except:
            client.close()
            clients.remove(client)

def log_message(message):
    """ذخیره پیام در فایل"""
    with open("chat_log.txt", "a", encoding="utf-8") as file:
        file.write(message + "\n")

def read_last_lines(n=50):
    """خواندن آخرین n خط از فایل چت"""
    if not os.path.exists("chat_log.txt"):
        return []
    with open("chat_log.txt", "r", encoding="utf-8") as file:
        lines = file.readlines()
    return lines[-n:]

def send_history(conn):
    """ارسال تاریخچه پیام‌ها به کاربر جدید"""
    history = read_last_lines(500)#line of read the log
    if history:
        try:
            # conn.send("[--- تاریخچه پیام‌ها ---]".encode())
            for line in history:
                conn.send(line.encode())#.strip() if line be line.strip().encode() the log send without \n
            # conn.send("[--- پایان تاریخچه ---]".encode())
        except:
            pass

def handle_client(conn, addr):
    """مدیریت هر کلاینت"""
    print(f"🔹 اتصال از {addr}")
    clients.append(conn)

    # ارسال تاریخچه قبل از پیام خوش‌آمد
    send_history(conn)
    conn.send("به چت سرور خوش آمدی! 👋".encode())

    while True:
        try:
            message = conn.recv(1024)
            if not message:
                break

            # گرفتن ساعت فعلی
            time_now = datetime.now().strftime("%H:%M:%S")
            final_message = f"[{time_now}] {message.decode()}"

            print(f"📨 از {addr}: {final_message}")

            # 📝 ذخیره در فایل
            log_message(final_message)

            # پخش بین بقیه
            broadcast(final_message.encode(), conn)

        except:
            break

    print(f"❌ {addr} قطع شد.")
    if conn in clients:
        clients.remove(conn)
    conn.close()

# راه‌اندازی سرور
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(('localhost', 12345))
server.listen(5)
print("📡 سرور چت آماده است... (برای خروج Ctrl+C بزن)")

try:
    while True:
        conn, addr = server.accept()
        thread = threading.Thread(target=handle_client, args=(conn, addr))
        thread.start()

except KeyboardInterrupt:
    print("\n🛑 سرور با دستور Ctrl+C بسته شد.")
    for c in clients:
        c.close()
    server.close()
    print("✅ همه‌ی ارتباط‌ها بسته شدند.")
