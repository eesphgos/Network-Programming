import socket

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(('localhost', 12345))

while True:
    msg = input("💬 پیام خود را بنویس (یا 'exit' برای خروج): ")
    if msg.lower() == 'exit':
        break
    client.send(msg.encode())
    data = client.recv(1024).decode()
    print("📩 پاسخ:", data)

client.close()
