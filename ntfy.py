import os
import hashlib
import time
import requests
from cryptography.fernet import Fernet, InvalidToken

def calculate_md5(file_path):
    hash_md5 = hashlib.md5()
    with open(file_path, "rb") as f:
        for chunk in iter(lambda: f.read(4096), b""):
            hash_md5.update(chunk)
    return hash_md5.hexdigest()

def send_alert(message):
    print(message)
    requests.post("https://ntfy.sh/Alert", data=message.encode('utf-8'))

def on_file_created(file_path):
    send_alert(f"File created: {file_path}")

def on_file_renamed(old_file_path, new_file_path):
    send_alert(f"File renamed: {old_file_path} to {new_file_path}")

def on_file_modified(file_path):
    send_alert(f"File modified: {file_path}")

def on_file_deleted(file_path):
    send_alert(f"File deleted: {file_path}")

def encrypt_file(file_path, key):
    fernet = Fernet(key)
    with open(file_path, "rb") as file:
        file_data = file.read()
    encrypted_data = fernet.encrypt(file_data)
    with open(file_path, "wb") as file:
        file.write(encrypted_data)

def decrypt_file(file_path, key):
    fernet = Fernet(key)
    try:
        with open(file_path, "rb") as file:
            encrypted_data = file.read()
        decrypted_data = fernet.decrypt(encrypted_data)
        with open(file_path, "wb") as file:
            file.write(decrypted_data)
    except InvalidToken:
        send_alert(f"Invalid decryption key for file: {file_path}")

def process_folder(folder_path, key, operation):
    exclude_extensions = {'.exe', '.py'}
    files = [f for f in os.listdir(folder_path) if os.path.isfile(os.path.join(folder_path, f)) and not os.path.splitext(f)[1].lower() in exclude_extensions]
    total_files = len(files)
    
    for i, file_name in enumerate(files, 1):
        file_path = os.path.join(folder_path, file_name)
        if operation == "encrypt":
            encrypt_file(file_path, key)
        elif operation == "decrypt":
            decrypt_file(file_path, key)
        percentage = (i / total_files) * 100
        send_alert(f"{operation.capitalize()}ion progress: {percentage:.2f}%")

def monitor_folder(folder_path, duration):
    file_hashes = {}
    file_hashes_new = {}

    # Populate the initial file_hashes with the current state of the folder
    for file_name in os.listdir(folder_path):
        file_path = os.path.join(folder_path, file_name)
        if os.path.isfile(file_path):
            file_hashes[file_path] = calculate_md5(file_path)

    start_time = time.time()
    while time.time() - start_time < duration:
        # Update file_hashes_new to get the current state of the folder
        file_hashes_new.clear()
        for file_name in os.listdir(folder_path):
            file_path = os.path.join(folder_path, file_name)
            if os.path.isfile(file_path):
                file_hashes_new[file_path] = calculate_md5(file_path)

        # Detect deleted files and modifications
        for file_path in list(file_hashes.keys()):
            if file_path not in file_hashes_new:
                # Potential deletion or rename
                deleted = True
                for new_file_path in file_hashes_new.keys():
                    if file_hashes[file_path] == file_hashes_new[new_file_path]:
                        send_alert(f"Unauthorized rename detected: {file_path} to {new_file_path}")
                        file_hashes[new_file_path] = file_hashes.pop(file_path)
                        deleted = False
                        break
                if deleted:
                    send_alert(f"Unauthorized deletion detected: {file_path}")
                    del file_hashes[file_path]

            elif file_hashes[file_path] != file_hashes_new[file_path]:
                send_alert(f"Unauthorized modification detected: {file_path}")
                file_hashes[file_path] = file_hashes_new[file_path]

        # Detect new files
        for file_path in file_hashes_new.keys():
            if file_path not in file_hashes:
                on_file_created(file_path)
                file_hashes[file_path] = file_hashes_new[file_path]

        # Sleep for some time before the next iteration
        time.sleep(2)

def main():
    folder_path = "C:\\Users\\user\\Desktop\\Hashing"

    # Generate a key for encryption and save it to the desktop
    key = Fernet.generate_key()
    key_path = "C:\\Users\\user\\Desktop\\encryptionkey.key"
    with open(key_path, "wb") as file:
        file.write(key)
    send_alert("Encryption key saved to encryptionkey.key on desktop!")

    # Initial encryption of all files in the folder
    process_folder(folder_path, key, "encrypt")

    # Prompt the user to enter the monitoring duration
    monitoring_duration = int(input("Enter the time to monitor the folder (in seconds): ").strip())

    # Monitor the folder for the specified duration after encryption
    send_alert(f"Monitoring folder for {monitoring_duration} seconds for unauthorized changes...")
    monitor_folder(folder_path, monitoring_duration)

    # Ask the user if they want to decrypt the files
    decrypt = input("Do you want to decrypt the files? (yes/no): ").strip().lower()
    if decrypt == 'yes':
        input_key = input("Please enter the encryption key: ").strip().encode()
        with open(key_path, "rb") as file:
            saved_key = file.read()
        if input_key == saved_key:
            process_folder(folder_path, input_key, "decrypt")
            send_alert("Files decrypted successfully.")
        else:
            send_alert("The provided key does not match the saved encryption key.")

if __name__ == "__main__":
    main()
