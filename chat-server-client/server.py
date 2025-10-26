import socket
import threading

# لیست همه‌ی کلاینت‌های وصل‌شده
clients = []

# ارسال پیام به همه‌ی کلاینت‌ها
def broadcast(message, sender_conn):
    for client in clients:
        if client != sender_conn:
            try:
                client.send(message)
            except:
                client.close()
                clients.remove(client)

# تابع مخصوص رسیدگی به هر کلاینت
def handle_client(conn, addr):
    print(f"🔹 اتصال از {addr}")
    clients.append(conn)
    conn.send("به چت سرور خوش آمدی! 👋".encode())

    while True:
        try:
            message = conn.recv(1024)
            if not message:
                break
            print(f"📨 از {addr}: {message.decode()}")
            broadcast(message, conn)
        except:
            break

    # وقتی کلاینت قطع شد
    print(f"❌ {addr} قطع شد.")
    clients.remove(conn)
    conn.close()

# راه‌اندازی سرور
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(('localhost', 12345))
server.listen(5)
print("📡 سرور چت آماده است...")

# پذیرش بی‌نهایت کلاینت
while True:
    conn, addr = server.accept()
    thread = threading.Thread(target=handle_client, args=(conn, addr))
    thread.start()
