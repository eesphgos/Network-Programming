import socket
import threading

# تابعی که برای هر کلاینت اجرا می‌شود
def handle_client(conn, addr):
    print(f"🔹 اتصال جدید از {addr}")
    while True:
        try:
            data = conn.recv(1024).decode()
            if not data:
                break  # یعنی کلاینت قطع شده
            print(f"📨 از {addr}: {data}")
            conn.send(f"پیام '{data}' دریافت شد ✅".encode())
        except:
            break
    print(f"❌ اتصال با {addr} بسته شد.")
    conn.close()

# ساخت سوکت TCP
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(('localhost', 12345))
server.listen(5)
print("📡 سرور چندکاربره در حال گوش دادن است...")

# حلقه‌ی بی‌نهایت برای پذیرش اتصالات جدید
while True:
    conn, addr = server.accept()
    # ساخت Thread جدید برای هر اتصال
    client_thread = threading.Thread(target=handle_client, args=(conn, addr))
    client_thread.start()
