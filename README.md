# RSA-Encryption-ChatApp

RSA Encryption Chat is a simple client-server chat application that uses the RSA encryption algorithm to secure the communication between the client and the server. The server generates a pair of public and private keys, and the client encrypts the messages using the server's public key before sending them the server then decrypts this message using his private key and vice versa.

## Theme

Theme used for the project is the azure.tcl theme made by @rdbende
you can check it out on his github: https://github.com/rdbende/Azure-ttk-theme
you have to download the theme from his github and add the azure.tcl file and theme folder to your project's directory for it to work

## Features

- Secure communication between client and server using RSA encryption
- Automatic key generation for both users.
- Message encryption and decryption
- Real-time chat functionality

## How does the RSA algorithm work?

1- First two random prime numbers are generated (p,q)\
2- Compute the value of n = p*q\
3- Compute euler = (p-1)(q-1)\
4- Choose a value for e that satisfies this condition: 1 < e < euler

Message Encryption:\
Cipher Message = m^e mod n

Message Decryption:\
Message = c^d mod n\
where d = e^-1 mod euler

## Getting Started

1. Clone the repository:

   ```bash
   git clone https://github.com/MazenTarek7/rsa-encryption-chat.git
   
2. Navigate to the project directory:
    ```
    cd "pathHere"
3. Install the dependencies:
    ```
    pip install -r requirements.txt
4. Start the server:
    ```
    python rsa_ServerGUI.py
5. Start the client:
    ```
    python rsa_ClientGUI.py
    
## Configuration
- You can modify the server's host and port by changing the values in the server.py file.
- The default host is localhost and the default port is 12345.





