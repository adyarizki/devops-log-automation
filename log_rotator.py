import os
import time

log_dir = '/var/log/app/'
tujuh_hari = 7 * 24 * 60 * 60  # dalam detik

# Pastikan direktori ada
if os.path.exists(log_dir):
    waktu_sekarang = time.time()
    
    for nama_file in os.listdir(log_dir):
        filepath = os.path.join(log_dir, nama_file)
        
        # Pastikan hanya memproses file (bukan folder)
        if os.path.isfile(filepath):
            waktu_modifikasi = os.path.getmtime(filepath)
            umur_file = waktu_sekarang - waktu_modifikasi
            
            if umur_file > tujuh_hari:
                print(f"File arsip: {nama_file}")
else:
    print(f"Direktori {log_dir} tidak ditemukan.")

