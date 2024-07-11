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
def wait_until_target_time(hour):
    while True:
        now_utc = datetime.utcnow()
        now_wib = now_utc + timedelta(hours=7)  # Mengubah waktu UTC menjadi WIB
        target_time = now_wib.replace(hour=hour, minute=0, second=0, microsecond=0)
        if now_wib > target_time:
            target_time += timedelta(days=1)  # Jika sudah melewati jam target, tunggu besoknya
        time_to_wait = (target_time - now_wib).total_seconds()
        
        if time_to_wait > 3600:  # Jika waktu tunggu lebih dari 1 jam, tidur selama 1 jam
            time.sleep(3600)
        elif time_to_wait > 60:  # Jika waktu tunggu lebih dari 1 menit, tidur selama 1 menit
            time.sleep(60)
        else:  # Jika waktu tunggu kurang dari 1 menit, tidur selama 1 detik
            time.sleep(1)
        
        # Hitungan mundur ditampilkan setiap detik
        now_utc = datetime.utcnow()
        now_wib = now_utc + timedelta(hours=7)  # Mengubah waktu UTC menjadi WIB
        time_to_wait = (target_time - now_wib).total_seconds()
        hours, remainder = divmod(time_to_wait, 3600)
        minutes, seconds = divmod(remainder, 60)
        print(f"Menunggu hingga jam {hour}:00 WIB... {int(hours)} jam {int(minutes)} menit {int(seconds)} detik lagi.", end='\r')
        
        if time_to_wait <= 0:
            break

# Fungsi untuk menjalankan tugas sesuai dengan jadwal
def run_task(min_value, max_value):
    while True:
        wait_until_target_time(2)  # Menunggu hingga jam 2 pagi WIB
        print("\nMenunggu tambahan 3 menit...\n")
        time.sleep(180)  # Menunggu tambahan 3 menit
        send_random_messages_for_all_accounts(min_value, max_value)
        
        wait_until_target_time(14)  # Menunggu hingga jam 2 sore WIB
        print("\nMenunggu tambahan 3 menit...\n")
        time.sleep(180)  # Menunggu tambahan 3 menit
        send_random_messages_for_all_accounts(min_value, max_value)

# Menjalankan tugas dengan input dari pengguna
min_value = int(input("Masukkan nilai minimum untuk pesan acak: "))
max_value = int(input("Masukkan nilai maksimum untuk pesan acak: "))
run_task(min_value, max_value)
