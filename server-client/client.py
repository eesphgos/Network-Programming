import socket

# ایجاد سوکت
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# اتصال به سرور
client_socket.connect(('localhost', 12345))
for i in range(0,5):
    # ارسال پیام
    print("متن مورد نظر را وارد کنید")
    text=input()
    client_socket.send(text.encode())

    # دریافت پاسخ
    data = client_socket.recv(1024).decode()
    print("📩 پاسخ سرور:", data)

client_socket.close()
