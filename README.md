# RSA-Encryption-ChatApp

RSA Encryption Chat is a simple client-server chat application that uses the RSA encryption algorithm to secure the communication between the client and the server. The server generates a pair of public and private keys, and the client encrypts the messages using the server's public key before sending them the server then decrypts this message using his private key and vice versa.

## Theme

Theme used for the project is the azure.tcl theme made by @rdbende\
you can check it out on his github: https://github.com/rdbende/Azure-ttk-theme \
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
- In function generate_prime() that generates random p,q values the range is set between 1024 and 2048 to have faster computation however this is not secure for message transmissions you have to increase the range depending on your use case this was only for educational purposes

## Screenshots
![image](https://github.com/MazenTarek7/RSA-Encryption-ChatApp/assets/56880548/203395cf-9c54-4602-b928-359f0cc2a3a9)
![image](https://github.com/MazenTarek7/RSA-Encryption-ChatApp/assets/56880548/2e3355d7-c804-4125-ab92-0b36397d260e)






