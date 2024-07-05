# Codealpha_SecureFileTransferApplication

Secure File Transfer Application

This Python script demonstrates a secure file transfer application with a graphical user interface (GUI) built using Tkinter. The application utilizes AES encryption and HMAC (Hash-based Message Authentication Code) for ensuring confidentiality, integrity, and authenticity of transferred files.

Features:

AES Encryption: Encrypts file contents using the AES (Advanced Encryption Standard) algorithm in CFB (Cipher Feedback) mode for secure data transmission.
HMAC Verification: Computes and verifies HMAC (Hash-based Message Authentication Code) to ensure data integrity against tampering.
Logging: Implements logging to file_transfer.log for recording transfer events and errors.
GUI Interface: Provides a user-friendly interface with a "Browse File" button to select files for secure transfer.
Usage:

Run the script and select a file using the GUI.
The file is securely encrypted, transferred (simulated), and decrypted at the receiving end.
Success or error messages are displayed via message boxes for user feedback.
This project showcases fundamental concepts of cryptography and GUI development in Python, suitable for learning and practical application in secure file handling scenarios.
