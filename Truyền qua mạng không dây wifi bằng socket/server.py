import socket
import threading
import tkinter as tk
from tkinter import scrolledtext

# --- Hàm lắng nghe tin nhắn từ client ---
def listen_client(conn):
    while True:
        try:
            data = conn.recv(1024).decode()
            if not data:
                break
            chat_log.insert(tk.END, f"Client: {data}\n")
            chat_log.yview(tk.END)
        except:
            break
    conn.close()
    chat_log.insert(tk.END, "Client đã ngắt kết nối.\n")

# --- Hàm khởi động server ---
def start_server():
    global server, conn
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server.bind(("0.0.0.0", 8888))
    server.listen(1)
    chat_log.insert(tk.END, "Server đang chờ client...\n")

    conn, addr = server.accept()
    chat_log.insert(tk.END, f"Đã kết nối với {addr}\n")
    threading.Thread(target=listen_client, args=(conn,), daemon=True).start()

# --- Hàm gửi tin từ server ---
def send_message(event=None):   # event=None để Enter cũng gọi được
    msg = entry.get()
    if msg and conn:
        conn.sendall(msg.encode())
        chat_log.insert(tk.END, f"Server: {msg}\n")
        chat_log.yview(tk.END)
        entry.delete(0, tk.END)

# --- Giao diện Tkinter ---
root = tk.Tk()
root.title("Chat Server")
root.geometry("400x500")      # kích thước cố định
root.resizable(False, False)  # không cho thay đổi kích thước

chat_log = scrolledtext.ScrolledText(root, wrap=tk.WORD, height=20)
chat_log.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)

entry_frame = tk.Frame(root)
entry_frame.pack(padx=10, pady=5, fill=tk.X)

entry = tk.Entry(entry_frame, font=("Arial", 12))
entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 5))
entry.bind("<Return>", send_message)  # Nhấn Enter để gửi

send_btn = tk.Button(entry_frame, text="Gửi", width=8, command=send_message)
send_btn.pack(side=tk.RIGHT, padx=(5, 0), pady=2)

# Chạy server trong thread riêng để không block GUI
threading.Thread(target=start_server, daemon=True).start()

root.mainloop()
