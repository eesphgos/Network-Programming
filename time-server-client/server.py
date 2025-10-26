import socket
import threading
from datetime import datetime  # 👈 برای گرفتن زمان

clients = []

def broadcast(message, sender_conn):
    for client in clients:
        if client != sender_conn:
            try:
                client.send(message)
            except:
                client.close()
                clients.remove(client)

def handle_client(conn, addr):
    print(f"🔹 اتصال از {addr}")
    clients.append(conn)
    conn.send("به چت سرور خوش آمدی! 👋".encode())

    while True:
        try:
            message = conn.recv(1024)
            if not message:
                break

            # 📅 اضافه کردن ساعت به پیام
            time_now = datetime.now().strftime("%H:%M:%S")
            final_message = f"[{time_now}] {message.decode()}"

            print(f"📨 از {addr}: {final_message}")
            broadcast(final_message.encode(), conn)

        except:
            break

    print(f"❌ {addr} قطع شد.")
    clients.remove(conn)
    conn.close()

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(('localhost', 12345))
server.listen(5)
print("📡 سرور چت آماده است...")

while True:
    conn, addr = server.accept()
    thread = threading.Thread(target=handle_client, args=(conn, addr))
    thread.start()
