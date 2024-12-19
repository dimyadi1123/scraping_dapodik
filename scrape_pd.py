import requests
import json
import csv
import concurrent.futures

# Fungsi untuk mengambil data JSON dari URL
def get_json_data(url):
    try:
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            return data
        else:
            print(f"Failed to retrieve data from {url}. Status code: {response.status_code}")
    except requests.RequestException as e:
        print(f"Error requesting data from {url}: {e}")
    return None

# Membaca daftar enkripsi sekolah dari file txt
sekolah_id_enkrip_list = []
nama_sekolah_list = []
npsn_list = []

jenjang = input("Masukkan jenjang: ")
with open(f'kode_enkripsi_{jenjang}.txt', 'r') as txtfile:
    lines = txtfile.readlines()
    for line in lines[1:]:  # Melewati baris header
        data = line.strip().split(',')
        sekolah_id_enkrip = data[2]
        nama_sekolah = data[0]
        npsn = data[1]
        
        sekolah_id_enkrip_list.append(sekolah_id_enkrip)
        nama_sekolah_list.append(nama_sekolah)
        npsn_list.append(npsn)

# URL template
url_template = "https://dapo.kemdikbud.go.id/rekap/sekolahDetail?semester_id=20231&sekolah_id={}"

# Menggunakan multi-threading untuk mempercepat proses
with concurrent.futures.ThreadPoolExecutor() as executor:
    urls = [url_template.format(enkripsi_sekolah) for enkripsi_sekolah in sekolah_id_enkrip_list]
    data_json_list = list(executor.map(get_json_data, urls))

# Menggabungkan data dari txt (nama sekolah, npsn) dan JSON
merged_data = []
for nama_sekolah, npsn, json_data in zip(nama_sekolah_list, npsn_list, data_json_list):
    if json_data:  # Pastikan data JSON tidak kosong
        sekolah_data = json_data[0]
        sekolah_data.update({"nama_sekolah": nama_sekolah, "npsn": npsn})
        # Membuat urutan field yang diinginkan
        reordered_sekolah_data = {"nama_sekolah": nama_sekolah, "npsn": npsn, **sekolah_data}
        merged_data.append(reordered_sekolah_data)


# Menyimpan data gabungan dalam file CSV
csv_filename = f"data_peserta_didik_{jenjang}.csv"
field_names = list(merged_data[0].keys())

with open(csv_filename, 'w', newline='', encoding='utf-8') as csvfile:
    csvwriter = csv.DictWriter(csvfile, fieldnames=field_names)
    csvwriter.writeheader()
    csvwriter.writerows(merged_data)

print(f"Data telah disimpan dalam file {csv_filename}")
