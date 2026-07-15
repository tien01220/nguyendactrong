import socket
import threading
import tkinter as tk
from tkinter import scrolledtext

# --- Hàm lắng nghe tin nhắn từ server ---
def listen_server():
    while True:
        try:
            data = client.recv(1024).decode()
            if not data:
                break
            chat_log.insert(tk.END, f"Server: {data}\n")
            chat_log.yview(tk.END)
        except:
            break
    client.close()
    chat_log.insert(tk.END, "Mất kết nối với server.\n")

# --- Hàm gửi tin ---
def send_message(event=None):   # event=None để Enter gọi được
    msg = entry.get()
    if msg:
        client.sendall(msg.encode())
        chat_log.insert(tk.END, f"Client: {msg}\n")
        chat_log.yview(tk.END)
        entry.delete(0, tk.END)

# --- Kết nối tới server ---
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_ip = "10.0.0.3"   # sửa lại IP server trong mạng LAN của bạn
client.connect((server_ip, 8888))

# --- Giao diện Tkinter ---
root = tk.Tk()
root.title("Chat Client")
root.geometry("400x500")      # kích thước cửa sổ
root.resizable(False, False)  # không cho thay đổi kích thước

chat_log = scrolledtext.ScrolledText(root, wrap=tk.WORD, height=20)
chat_log.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)
chat_log.insert(tk.END, f"Đã kết nối đến server {server_ip}:8888\n")

entry_frame = tk.Frame(root)
entry_frame.pack(padx=10, pady=5, fill=tk.X)

entry = tk.Entry(entry_frame, font=("Arial", 12))
entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 5))
entry.bind("<Return>", send_message)   # ⬅ Enter để gửi tin nhắn

send_btn = tk.Button(entry_frame, text="Gửi", width=8, command=send_message)
send_btn.pack(side=tk.RIGHT, padx=(5, 0), pady=2)

threading.Thread(target=listen_server, daemon=True).start()

root.mainloop()