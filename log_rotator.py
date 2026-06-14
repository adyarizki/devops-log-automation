# 1. Paling atas: Import dan Variabel Utama
import os
import time
import datetime
import tarfile
import subprocess

log_dir = '/var/log/app/'
tujuh_hari = 7 * 24 * 60 * 60

tanggal_sekarang = datetime.datetime.now().strftime('%Y%m%d')
nama_tar = f"backup_log_{tanggal_sekarang}.tar.gz"
path_tar = os.path.join(log_dir, nama_tar)

# 2. Cek Direktori
if os.path.exists(log_dir):
    waktu_sekarang = time.time()
    log_yang_akan_diarsip = []

    # 3. PERULANGAN UNTUK SCAN FILE (Masuk ke dalam)
    for nama_file in os.listdir(log_dir):
        if nama_file.endswith('.log'):
            filepath = os.path.join(log_dir, nama_file)
            if os.path.isfile(filepath):
                waktu_modifikasi = os.path.getmtime(filepath)
                umur_file = waktu_sekarang - waktu_modifikasi

                if umur_file > tujuh_hari:
                    print(f"File arsip: {nama_file}")
                    log_yang_akan_diarsip.append(filepath)

    # 4. PROSES KOMPRESI (Keluarkan dari loop 'for', sejajarkan dengan 'for')
    if log_yang_akan_diarsip:
        with tarfile.open(path_tar, "w:gz") as tar:
            for file in log_yang_akan_diarsip:
                tar.add(file, arcname=os.path.basename(file))
        print(f"Berhasil mengompresi file ke {nama_tar}")
        
        # Langkah B: Hitung & Cetak Ukuran File Arsip
        ukuran_bytes = os.path.getsize(path_tar)
        ukuran_kb = ukuran_bytes / 1024
        print(f"Ukuran file arsip: {ukuran_kb:.2f} KB")
        
        # Langkah C: Hapus File Log Lama yang Asli
        for file_lama in log_yang_akan_diarsip:
            os.remove(file_lama)
        print("File log lama yang asli berhasil dihapus.")
            
        # Langkah D: Restart Service
        # (Catatan: ubah 'app-transaction' ke service lain jika ingin testing di VM tanpa error)
        subprocess.run(["systemctl", "restart", "app-transaction"], check=True)
        print("Service app-transaction berhasil di-restart secara bersih.")
else:
    print(f"Direktori {log_dir} tidak ditemukan.")
