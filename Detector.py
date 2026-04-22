import cv2
import numpy as np

def chi_square_attack(video_path):
    print(f"[+] Đang phân tích vật chứa: {video_path}")
    cap = cv2.VideoCapture(video_path)
    
    frame_idx = 0
    while cap.isOpened():
        ret, frame = cap.read()
        if not ret or frame_idx > 10: # Phân tích 10 khung hình đầu để kiểm tra
            break
            
        # Chỉ phân tích kênh màu Red (hoặc có thể lặp qua cả 3 kênh)
        data = frame[:, :, 2].flatten()
        
        # 1. Tính toán Histogram cho các cặp (2n, 2n+1)
        # Tần suất thực tế (Observed)
        counts = np.bincount(data, minlength=256)
        
        # 2. Tính toán tần suất kỳ vọng (Expected) 
        # Theo lý thuyết LSB, sau khi nhúng, số lượng 2n và 2n+1 sẽ xấp xỉ nhau
        chi_stat = 0
        for i in range(0, 256, 2):
            observed_chẵn = counts[i]
            observed_lẻ = counts[i+1]
            expected = (observed_chẵn + observed_lẻ) / 2
            
            if expected > 0:
                chi_stat += ((observed_chẵn - expected)**2) / expected
        
        # 3. Tính xác suất (P-value) - Đơn giản hóa cho bài luận
        # Nếu chi_stat càng nhỏ, khả năng có dữ liệu ẩn càng cao
        result_threshold = 100 # Ngưỡng tùy chỉnh tùy loại video
        
        print(f"--- Khung hình {frame_idx} ---")
        print(f"Chi-square Statistic: {chi_stat:.2f}")
        
        if chi_stat < result_threshold:
            print("[DANGER] Cảnh báo: Phát hiện dấu hiệu Malware/Dữ liệu ẩn!")
        else:
            print("[SAFE] Trạng thái: Bình thường.")
            
        frame_idx += 1

    cap.release()

if __name__ == "__main__":
    chi_square_attack('Video_Malware.avi')