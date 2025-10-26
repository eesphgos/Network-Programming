import socket
import threading

nickname = input("👤 نام کاربری خود را وارد کن: ")

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(('localhost', 12345))

# دریافت پیام‌ها از سرور
def receive_messages():
    while True:
        try:
            message = client.recv(1024).decode()
            if not message:
                break
            print("\n" + message)
        except:
            print("⚠️ ارتباط با سرور قطع شد.")
            client.close()
            break

# ارسال پیام‌ها به سرور
def send_messages():
    while True:
        msg = input()
        if msg.lower() == "exit":
            client.close()
            break
        full_msg = f"{nickname}: {msg}"
        client.send(full_msg.encode())

# اجرای دو Thread برای ارسال و دریافت همزمان
recv_thread = threading.Thread(target=receive_messages)
recv_thread.start()

send_thread = threading.Thread(target=send_messages)
send_thread.start()
