import tkinter as tk
from tkinter import filedialog, messagebox
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes, hmac
import os
import logging

# Setup logging
logging.basicConfig(filename='file_transfer.log', level=logging.INFO, format='%(asctime)s - %(message)s')

# Encryption function using AES
def encrypt_data(key, data):
    iv = os.urandom(16)  # Generate Initialization Vector (IV)
    cipher = Cipher(algorithms.AES(key), modes.CFB(iv), backend=default_backend())
    encryptor = cipher.encryptor()
    encrypted_data = encryptor.update(data) + encryptor.finalize()
    return iv + encrypted_data

# Decryption function using AES
def decrypt_data(key, encrypted_data):
    iv = encrypted_data[:16]  # Extract IV from encrypted data
    cipher = Cipher(algorithms.AES(key), modes.CFB(iv), backend=default_backend())
    decryptor = cipher.decryptor()
    decrypted_data = decryptor.update(encrypted_data[16:]) + decryptor.finalize()
    return decrypted_data

# Function to compute HMAC for integrity verification
def compute_hmac(key, data):
    h = hmac.HMAC(key, hashes.SHA256(), backend=default_backend())
    h.update(data)
    return h.finalize()

# Function to verify HMAC
def verify_hmac(key, data, received_hmac):
    h = hmac.HMAC(key, hashes.SHA256(), backend=default_backend())
    h.update(data)
    try:
        h.verify(received_hmac)
        return True
    except:
        return False

# Function to transfer file securely
def transfer_file(filename, key):
    try:
        with open(filename, 'rb') as f:
            data = f.read()

        encrypted_data = encrypt_data(key, data)
        hmac_digest = compute_hmac(key, encrypted_data)

        # Simulate transfer over network (normally done via sockets or HTTPS)
        transferred_data = encrypted_data + hmac_digest

        # Simulate receiving end
        received_encrypted_data = transferred_data[:-32]  # Assuming last 32 bytes are HMAC
        received_hmac = transferred_data[-32:]

        if verify_hmac(key, received_encrypted_data, received_hmac):
            decrypted_data = decrypt_data(key, received_encrypted_data)
            # Store or process decrypted_data (e.g., write to a file)
            with open('received_file.txt', 'wb') as f:
                f.write(decrypted_data)
                logging.info(f"Received and saved file: {filename}")
                messagebox.showinfo("Success", f"File transfer successful. Received and saved file: {filename}")
        else:
            logging.warning(f"HMAC verification failed for file: {filename}")
            messagebox.showerror("Error", f"HMAC verification failed. File transfer may have been tampered with.")
    except Exception as e:
        logging.error(f"Error transferring file {filename}: {str(e)}")
        messagebox.showerror("Error", f"Error transferring file {filename}: {str(e)}")

# GUI Initialization
def browse_file():
    filename = filedialog.askopenfilename(initialdir="/", title="Select a File",
                                          filetypes=(("Text files", "*.txt*"), ("all files", "*.*")))
    if filename:
        key = os.urandom(32)  # Generate a random 32-byte key (256 bits) for AES
        transfer_file(filename, key)

# Create the main window
root = tk.Tk()
root.title("Secure File Transfer Application")

# Create and pack widgets
label = tk.Label(root, text="Secure File Transfer Application", font=("Helvetica", 16))
label.pack(pady=20)

button = tk.Button(root, text="Browse File", command=browse_file)
button.pack(pady=10)

# Start the main loop
root.mainloop()
