import socket

# ایجاد یک سوکت (مثل تلفن)
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# اتصال به IP و پورت
server_socket.bind(('localhost', 12345))

# گوش دادن برای اتصال
server_socket.listen(1)
print("📡 سرور در حال گوش دادن است...")

# پذیرش اتصال
conn, addr = server_socket.accept()
print("✅ اتصال از:", addr)
for i in range(0,5):
    # دریافت پیام از کلاینت
    data = conn.recv(1024).decode()
    print("📨 پیام دریافت‌شده:", data)

    # ارسال پاسخ
    conn.send("سلام از سرور!".encode())

# بستن اتصال
conn.close()
