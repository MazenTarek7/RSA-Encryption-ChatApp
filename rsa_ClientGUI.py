import random
import re
import socket
import tkinter as tk
from tkinter import ttk

def is_prime(num):
    if num <= 1:
        return False
    for i in range(2, int(num ** 0.5) + 1):
        if num % i == 0:
            return False
    return True

def generate_prime():
    while True:
        prime = random.randint(2 ** 10, 2 ** 11)
        if is_prime(prime):
            return prime

def gcd(a, b):
    if b == 0:
        return a
    return gcd(b, a % b)

def mod_inverse(e, phi):
    for d in range(3, phi):
        if (d * e) % phi == 1:
            return d

def generate_keys():
    p = generate_prime()
    q = generate_prime()
    n = p * q
    phi = (p - 1) * (q - 1)
    while True:
        e = random.randint(2, phi)
        if gcd(e, phi) == 1:
            break
    d = mod_inverse(e, phi)
    p_label.config(text=f"p: {p}")
    q_label.config(text=f"q: {q}")
    public_key_label.config(text=f"Public Key: ({e}, {n})")
    private_key_label.config(text=f"Private Key: ({d}, {n})")
    return (e, n), (d, n), p, q

def encrypt(message, public_key):
    e, n = public_key
    encrypted = [pow(ord(char), e, n) for char in message]
    return encrypted

def decrypt(encrypted, private_key):
    d, n = private_key
    decrypted = [chr(pow(char, d, n)) for char in encrypted]
    return "".join(decrypted)

def connect_to_server():
    global server_socket, public_key, private_key, server_public_key, chat_text, message_entry

    public_key, private_key, _, _ = generate_keys()

    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.connect(('localhost', 12345))

    server_public_key = eval(server_socket.recv(1024).decode())
    server_socket.send(str(public_key).encode())

    chat_text.insert(tk.END, "Connected to the server\n")

def send_message():
    global server_socket, private_key, server_public_key, chat_text, message_entry

    message = message_entry.get()
    print("User's Public Key: " ,server_public_key)
    encrypted_message = encrypt(message, server_public_key)
    server_socket.send(str(encrypted_message).encode())

    encrypted_message = server_socket.recv(1024).decode()
    if not encrypted_message:
        server_socket.close()
        chat_text.insert(tk.END, "Server disconnected\n")
        return

    encrypted_message = re.findall(r'\d+', encrypted_message)
    encrypted_message = [int(char) for char in encrypted_message]
    decrypted_message = decrypt(encrypted_message, private_key)

    chat_text.insert(tk.END, f"Received encrypted message from server: {encrypted_message}\n")
    chat_text.insert(tk.END, f"Decrypted message: {decrypted_message}\n")

def create_client_gui():
    global chat_text, message_entry, q_label, p_label, public_key_label, private_key_label

    window = tk.Tk()
    window.title("User 2")
    window.iconbitmap("encryptionIcon.ico")

    style = ttk.Style(window)
    window.tk.call("source", "azure.tcl")
    window.tk.call("set_theme", "dark")

    main_frame = ttk.Frame(window)
    main_frame.pack(fill=tk.BOTH, expand=True)

    chat_frame = ttk.Frame(main_frame)
    chat_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

    chat_text = tk.Text(chat_frame, width=70, height=20, font=("Segoe UI", 11))
    chat_text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

    scroll_bar = ttk.Scrollbar(chat_frame, command=chat_text.yview)
    scroll_bar.pack(side=tk.RIGHT, fill=tk.Y)
    chat_text.config(yscrollcommand=scroll_bar.set)

    right_frame = ttk.Frame(main_frame)
    right_frame.pack(side=tk.RIGHT, fill=tk.Y)

    keys_frame = ttk.LabelFrame(right_frame, text="Keys", padding=10)
    keys_frame.grid(row=0, column=0, sticky=tk.N, padx=10, pady=10)

    p_label = ttk.Label(keys_frame, text=f"p: ", font=("Segoe UI", 8))
    p_label.grid(row=0, column=0, sticky=tk.W, padx=10, pady=5)

    q_label = ttk.Label(keys_frame, text=f"q: ", font=("Segoe UI", 8))
    q_label.grid(row=1, column=0, sticky=tk.W, padx=10, pady=5)

    public_key_label = ttk.Label(keys_frame, text="Public Key: ", font=("Segoe UI", 8))
    public_key_label.grid(row=2, column=0, sticky=tk.W, padx=10, pady=5)

    private_key_label = ttk.Label(keys_frame, text="Private Key: ", font=("Segoe UI", 8))
    private_key_label.grid(row=3, column=0, sticky=tk.W, padx=10, pady=5)

    message_frame = ttk.Frame(window, padding=10)
    message_frame.pack()

    message_label = ttk.Label(message_frame, text="Enter your message:", font=("Segoe UI", 10 , "bold"))
    message_label.pack(side=tk.LEFT , padx=(5,5))

    message_entry = ttk.Entry(message_frame, width=50, font=("Segoe UI", 10))
    message_entry.pack(side=tk.LEFT, padx=(0, 10))

    send_button = ttk.Button(message_frame, text="Send and Encrypt", command=send_message)
    send_button.pack(side=tk.LEFT)


    connect_to_server()

    window.mainloop()

create_client_gui()
