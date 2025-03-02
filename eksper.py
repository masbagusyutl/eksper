import requests
import random
import time
from datetime import datetime, timedelta

# Fungsi untuk membaca token dari file data.txt
def read_token():
    with open('data.txt', 'r') as file:
        tokens = file.readlines()
        return [token.strip() for token in tokens]

# Fungsi untuk melakukan permintaan POST
def send_message(token, message):
    url = 'https://server-20.experty.io/api/v2/chat-messages'
    payload = {
        "token": token,
        "message": str(message)
    }
    try:
        response = requests.post(url, json=payload)
        return response.status_code
    except requests.exceptions.RequestException as e:
        print(f"Error sending message: {e}")
        return None

# Fungsi untuk mengirimkan pesan dengan nilai acak antara min_value dan max_value untuk setiap akun
def send_random_messages_for_all_accounts(min_value, max_value):
    tokens = read_token()
    token_count = len(tokens)
    sent_messages = set()

    for index, token in enumerate(tokens):
        while True:
            random_message = random.randint(min_value, max_value)
            if random_message not in sent_messages:
                sent_messages.add(random_message)
                break
        
        status_code = send_message(token, random_message)
        if status_code == 200:
            print(f"Pesan berhasil dikirim dengan token ke-{index + 1} dari total {token_count} akun. Pesan: {random_message}. Status Code: {status_code}")
        else:
            print(f"Gagal mengirim pesan dengan token ke-{index + 1} dari total {token_count} akun. Pesan: {random_message}. Status Code: {status_code}")

# Fungsi untuk menunggu hingga waktu tertentu (jam 2 pagi atau jam 2 sore) dengan hitungan mundur
def wait_until_target_time(hour_1, hour_2):
    now_utc = datetime.utcnow()
    now_wib = now_utc + timedelta(hours=7)  # Mengubah waktu UTC menjadi WIB
    
    target_time_1 = now_wib.replace(hour=hour_1, minute=0, second=0, microsecond=0)
    target_time_2 = now_wib.replace(hour=hour_2, minute=0, second=0, microsecond=0)
    
    if now_wib > target_time_1:
        target_time_1 += timedelta(days=1)  # Jika sudah melewati jam target, tunggu besoknya
    if now_wib > target_time_2:
        target_time_2 += timedelta(days=1)  # Jika sudah melewati jam target, tunggu besoknya

    target_time = min(target_time_1, target_time_2)
    
    time_to_wait = (target_time - now_wib).total_seconds()
    
    while time_to_wait > 0:
        # Hitungan mundur ditampilkan setiap detik
        hours, remainder = divmod(time_to_wait, 3600)
        minutes, seconds = divmod(remainder, 60)
        print(f"Menunggu hingga jam {target_time.hour}:00 WIB... {int(hours)} jam {int(minutes)} menit {int(seconds)} detik lagi.", end='\r')
        time.sleep(1)
        
        now_utc = datetime.utcnow()
        now_wib = now_utc + timedelta(hours=7)  # Mengubah waktu UTC menjadi WIB
        time_to_wait = (target_time - now_wib).total_seconds()

    print(f"Menunggu hingga jam {target_time.hour}:00 WIB... 0 jam 0 menit 0 detik lagi.                    ")

# Fungsi untuk menjalankan tugas sesuai dengan jadwal
def run_task(min_value, max_value):
    while True:
        wait_until_target_time(2, 14)  # Menunggu hingga jam 2 pagi atau 2 sore WIB yang terdekat
        print("\nMenunggu tambahan 3 menit...\n")
        time.sleep(180)  # Menunggu tambahan 3 menit
        send_random_messages_for_all_accounts(min_value, max_value)

# Menjalankan tugas dengan input dari pengguna
min_value = int(input("Masukkan nilai minimum untuk pesan acak: "))
max_value = int(input("Masukkan nilai maksimum untuk pesan acak: "))
run_task(min_value, max_value)
