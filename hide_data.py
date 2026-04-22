import cv2
import numpy as np
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad
import os

# --- CẤU HÌNH CỦA TRƯỜNG GIANG ---
KEY = b'TruongGiang_2026' 
STEGO_KEY = 0x5A           
VIDEO_INPUT = 'Video_demo_goc.mp4'
PAYLOAD_INPUT = 'payload.exe'
VIDEO_OUTPUT = 'Video_Malware.avi'

def prepare_data(payload_path):
    print("[+] Đang chuẩn bị và mã hóa Payload...")
    with open(payload_path, 'rb') as f:
        data = f.read()
    
    iv = b'0123456789101112' 
    cipher = AES.new(KEY, AES.MODE_CBC, iv=iv)
    encrypted_data = cipher.encrypt(pad(data, AES.block_size))
    
    xor_data = bytearray([b ^ STEGO_KEY for b in encrypted_data])
    
    # Chuyển thành list các bit (kiểu int) để tránh xử lý chuỗi chậm
    bits = []
    for byte in xor_data:
        for i in range(7, -1, -1):
            bits.append((byte >> i) & 1)
    
    # Kết thúc bằng chuỗi đánh dấu (EOF)
    eof = [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,0]
    bits.extend(eof)
    return bits

def embed_data():
    bits = prepare_data(PAYLOAD_INPUT)
    cap = cv2.VideoCapture(VIDEO_INPUT)
    
    fps = cap.get(cv2.CAP_PROP_FPS)
    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    
    # Sử dụng nén lossless (FFV1) để đảm bảo bit LSB không bị thay đổi
    fourcc = cv2.VideoWriter_fourcc(*'FFV1') 
    out = cv2.VideoWriter(VIDEO_OUTPUT, fourcc, fps, (width, height))
    
    bit_idx = 0
    total_bits = len(bits)
    print(f"[+] Tổng số bit cần nhúng: {total_bits}")

    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break
        
        if bit_idx < total_bits:
            # Chuyển frame sang kiểu int32 để tính toán không bị tràn, sau đó chuyển lại uint8
            frame = frame.astype(np.int32)
            
            for i in range(height):
                for j in range(width):
                    for k in range(3):
                        if bit_idx < total_bits:
                            # Thực hiện phép toán LSB an toàn
                            frame[i, j, k] = (frame[i, j, k] & ~1) | bits[bit_idx]
                            bit_idx += 1
                        else: break
                    if bit_idx >= total_bits: break
                if bit_idx >= total_bits: break
            
            # Chuyển ngược về uint8 sau khi đã tính toán xong
            frame = np.clip(frame, 0, 255).astype(np.uint8)
        
        out.write(frame)
    
    cap.release()
    out.release()
    
    if bit_idx >= total_bits:
        print(f"[OK] Thành công! File '{VIDEO_OUTPUT}' đã tạo xong.")
    else:
        print(f"[!] LỖI: Video chỉ chứa được {bit_idx} bit, thiếu {total_bits - bit_idx} bit.")
        print("Hãy dùng video dài hơn hoặc payload nhỏ hơn.")

if __name__ == "__main__":
    embed_data()