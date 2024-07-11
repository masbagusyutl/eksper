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
    response = requests.post(url, json=payload)
    return response.status_code

# Fungsi untuk mengirimkan pesan dengan nilai acak antara min_value dan max_value
def send_random_message(min_value, max_value):
    tokens = read_token()
    token_count = len(tokens)
    selected_token_index = random.randint(0, token_count - 1)
    selected_token = tokens[selected_token_index]
    random_message = random.randint(min_value, max_value)
    
    status_code = send_message(selected_token, random_message)
    
    return selected_token_index, token_count, status_code

# Fungsi untuk menunggu hingga waktu tertentu (jam 2 pagi atau jam 2 sore)
def wait_until_target_time(hour):
    now = datetime.now()
    target_time = now.replace(hour=hour, minute=0, second=0, microsecond=0)
    if now > target_time:
        target_time += timedelta(days=1)  # Jika sudah melewati jam target, tunggu besoknya
    time_to_wait = (target_time - now).total_seconds()
    print(f"Menunggu hingga jam {hour}:00 WIB...")
    time.sleep(time_to_wait)

# Fungsi untuk menjalankan tugas sesuai dengan jadwal
def run_task():
    while True:
        wait_until_target_time(2)  # Menunggu hingga jam 2 pagi
        index, total_tokens, status = send_random_message(3000, 4000)
        print(f"Pesan berhasil dikirim dengan token ke-{index + 1} dari total {total_tokens} akun. Status Code: {status}")
        
        wait_until_target_time(14)  # Menunggu hingga jam 2 sore
        index, total_tokens, status = send_random_message(3000, 4000)
        print(f"Pesan berhasil dikirim dengan token ke-{index + 1} dari total {total_tokens} akun. Status Code: {status}")

# Menjalankan tugas
run_task()
