import random
import re
import socket
import threading
import tkinter as tk
from tkinter import ttk

class ServerApp:
    def __init__(self):
        self.client_public_key = None
        self.client_socket = None
        self.p = None
        self.q = None

    def is_prime(self, num):
        if num <= 1:
            return False
        for i in range(2, int(num ** 0.5) + 1):
            if num % i == 0:
                return False
        return True

    def generate_prime(self):
        while True:
            prime = random.randint(2 ** 10, 2 ** 11)
            if self.is_prime(prime):
                return prime

    def gcd(self, a, b):
        if b == 0:
            return a
        return self.gcd(b, a % b)

    def mod_inverse(self, e, phi):
        for d in range(3, phi):
            if (d * e) % phi == 1:
                return d

    def generate_keys(self):
        self.p = self.generate_prime()
        self.q = self.generate_prime()
        n = self.p * self.q
        phi = (self.p - 1) * (self.q - 1)
        while True:
            e = random.randint(2, phi)
            if self.gcd(e, phi) == 1:
                break
        d = self.mod_inverse(e, phi)
        p_label.config(text=f"p: {self.p}")
        q_label.config(text=f"q: {self.q}")
        public_key_label.config(text=f"Public Key: ({e}, {n})")
        private_key_label.config(text=f"Private Key: ({d}, {n})")
        return (e, n), (d, n), self.p, self.q

    def encrypt(self, message, public_key):
        e, n = public_key
        encrypted = [pow(ord(char), e, n) for char in message]
        return encrypted

    def decrypt(self, encrypted, private_key):
        d, n = private_key
        decrypted = [chr(pow(char, d, n)) for char in encrypted]
        return "".join(decrypted)

    def send_message(self):
        message = message_entry.get()
        encrypted_message = self.encrypt(message, self.client_public_key)
        print("Client's Public Key: ",self.client_public_key)
        encrypted_message_str = " ".join(str(char) for char in encrypted_message)
        self.client_socket.send(encrypted_message_str.encode())

    def handle_client_connection(self, client_socket, client_address):
        public_key, private_key, _, _ = self.generate_keys()

        client_socket.send(str(public_key).encode())

        self.client_public_key = eval(client_socket.recv(1024).decode())

        while True:
            # Receive message from client
            encrypted_message = client_socket.recv(1024).decode()
            if not encrypted_message:
                client_socket.close()
                chat_text.insert(tk.END, f"Client {client_address} disconnected\n")
                return

            encrypted_message = re.findall(r'\d+', encrypted_message)
            encrypted_message = [int(char) for char in encrypted_message]
            decrypted_message = self.decrypt(encrypted_message, private_key)

            chat_text.insert(tk.END, f"Received encrypted message from {client_address}: {encrypted_message}\n")
            chat_text.insert(tk.END, f"Decrypted message: {decrypted_message}\n")

    def start_server(self):
        global server_socket, chat_text

        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_socket.bind(('localhost', 12345))
        server_socket.listen(1)

        chat_text.insert(tk.END, "Server is running and waiting for a connection...\n")

        self.client_socket, client_address = server_socket.accept()
        chat_text.insert(tk.END, f"Connected to {client_address}\n")

        threading.Thread(target=self.handle_client_connection, args=(self.client_socket, client_address)).start()

    def create_server_gui(self):
        global chat_text, message_entry, q_label, p_label, public_key_label, private_key_label

        window = tk.Tk()
        window.title("User 1")
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

        p_label = ttk.Label(keys_frame, text=f"p: {self.p}", font=("Segoe UI", 8))
        p_label.grid(row=0, column=0, sticky=tk.W, padx=10, pady=5)

        q_label = ttk.Label(keys_frame, text=f"q: {self.q}", font=("Segoe UI", 8))
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

        send_button = ttk.Button(message_frame, text="Send and Encrypt", command=self.send_message)
        send_button.pack(side=tk.LEFT)


        self.start_server()

        window.mainloop()


server_app = ServerApp()
server_app.create_server_gui()
