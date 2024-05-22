# C2C-File-Monitoring-while-encrypting-Decrypting-the-data
Features
File Encryption: Encrypts all files in a specified folder on the client side.
Progress Monitoring: Displays the encryption and decryption progress in percentage on the server side.
Folder Monitoring: Allows monitoring of the folder for a user-defined duration post encryption.
File Decryption: Prompts for decryption with key verification after monitoring.
Requirements
Python 3.x
socket library (standard in Python)
os, time, threading libraries (standard in Python)
cryptography library (can be installed via pip)
#Install the required Python packages:
pip install cryptography
Usage:
1. Running the Server
Start the server to listen for client connections: python server.py
1.1 Running the Client
Start the client to connect to the server and initiate encryption:python client.py
2. Follow the prompts in the client terminal:
Enter the folder path: Provide the absolute or relative path to the folder you wish to encrypt.
Monitor Duration: Specify the number of seconds to monitor the folder after encryption.
Decryption Key: If prompted for decryption, enter the correct key that was used during encryption.

Project Structure:
folder-encryption-monitoring/
├── client.py        # Client-side script for folder encryption and decryption
├── server.py        # Server-side script for monitoring and displaying progress
├── README.md        # Project documentation
└── requirements.txt # Python package requirements (if any)


Example Workflow
1. Encryption:

i)User runs client.py.
ii)User specifies the folder to encrypt.
ii)Encryption progress is displayed on the server terminal.

2. Monitoring:
i)After encryption, the client prompts for the monitoring duration.
ii)The folder is monitored for the specified time.

3. Decryption:

i)After monitoring, the client prompts whether to decrypt the folder.
ii)If the user opts to decrypt, they must provide the decryption key.
iii)Decryption progress is displayed on the server terminal if the key matches.

Notes:
Ensure the server is running before starting the client.
Use the exact encryption key for decryption to succeed.

