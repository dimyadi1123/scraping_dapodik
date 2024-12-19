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
jenjang = input(str("Masukkan jenjang: "))
with open(f'sekolah_id_enkrip_{jenjang}.txt', 'r') as txtfile:
    sekolah_id_enkrip_list = [line.strip() for line in txtfile]

# URL template
url_template = "https://dapo.kemdikbud.go.id/rekap/sekolahDetail?semester_id=20221&sekolah_id={}"

# Menggunakan multi-threading untuk mempercepat proses
with concurrent.futures.ThreadPoolExecutor() as executor:
    urls = [url_template.format(enkripsi_sekolah) for enkripsi_sekolah in sekolah_id_enkrip_list]
    data_json_list = list(executor.map(get_json_data, urls))

# Menyimpan data JSON dalam file CSV
csv_filename = f"data_peserta_didik {jenjang}.csv"

# Menulis data ke dalam file CSV
with open(csv_filename, 'w', newline='', encoding='utf-8') as csvfile:
    csvwriter = csv.writer(csvfile)
    
    # Menulis header berdasarkan keys dari objek pertama (jika ada data)
    if data_json_list and data_json_list[0]:
        header = list(data_json_list[0][0].keys()) + ["nama_sekolah", "npsn"]
        csvwriter.writerow(header)
    
    for data in data_json_list:
        if data:  # Pastikan data tidak kosong sebelum mengakses indeks [0]
            sekolah_data = data[0]
            nama_sekolah = sekolah_data.get("nama_sekolah", "")
            npsn = sekolah_data.get("npsn", "")
            values = list(sekolah_data.values()) + [nama_sekolah, npsn]
            csvwriter.writerow(values)

print(f"Data telah disimpan dalam file {csv_filename}")
