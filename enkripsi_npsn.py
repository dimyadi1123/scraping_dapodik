import requests
import json
import csv
import concurrent.futures

# Membaca daftar kode sekolah dari CSV
list_kode_sekolah = []
jenjang = input(str("Masukkan jenjang: "))
with open(f'npsn_{jenjang}.csv', 'r') as csvfile:
    csvreader = csv.reader(csvfile)
    for row in csvreader:  # Perulangan untuk membaca setiap baris
        list_kode_sekolah.append(row[0])

# URL template
url_template = "https://dapo.kemdikbud.go.id/api/getHasilPencarian?keyword={}"

# Fungsi untuk mengambil data sekolah dari URL
def get_sekolah_data(kode_sekolah):
    url = url_template.format(kode_sekolah)
    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        if data:
            return data[0]  # Mengambil data pertama dari respons JSON
    except requests.RequestException as e:
        print(f"Error requesting data for {kode_sekolah}: {e}")
    return None

# Menggunakan multi-threading untuk mempercepat proses
with concurrent.futures.ThreadPoolExecutor() as executor:
    sekolah_data_list = list(executor.map(get_sekolah_data, list_kode_sekolah))

# Menyimpan data sekolah dalam file txt
txt_filename = f"kode_enkripsi_{jenjang}.txt"
with open(txt_filename, 'w', encoding='utf-8') as txtfile:
    # Menulis header
    header = "nama_sekolah,npsn,sekolah_id_enkrip\n"
    txtfile.write(header)
    
    # Menulis setiap baris data
    for data in sekolah_data_list:
        if data:
            nama_sekolah = data.get("nama_sekolah", "")
            npsn = data.get("npsn", "")
            sekolah_id_enkrip = data.get("sekolah_id_enkrip", "")
            values = f"{nama_sekolah},{npsn},{sekolah_id_enkrip}\n"
            txtfile.write(values)

print(f"Data sekolah telah disimpan dalam file {txt_filename}")