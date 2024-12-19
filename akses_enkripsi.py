import requests
import json
import csv
import concurrent.futures

# Membaca daftar kode sekolah dari CSV
list_kode_sekolah = []
jenjang = input(str("Masukkan jenjang: "))
with open(f'npsn_{jenjang}.csv', 'r') as csvfile:
    csvreader = csv.reader(csvfile)
    list_kode_sekolah = [row[0] for row in csvreader]

# URL template
url_template = "https://dapo.kemdikbud.go.id/api/getHasilPencarian?keyword={}"

# Fungsi untuk mengambil sekolah_id_enkrip dari URL
def get_sekolah_id_enkrip(kode_sekolah):
    url = url_template.format(kode_sekolah)
    try:
        response = requests.get(url)
        data = response.json()
        if data:
            sekolah_id_enkrip = data[0].get("sekolah_id_enkrip")
            if sekolah_id_enkrip:
                return sekolah_id_enkrip
    except requests.RequestException as e:
        print(f"Error requesting data for {kode_sekolah}: {e}")
    return None

# Menggunakan multi-threading untuk mempercepat proses
with concurrent.futures.ThreadPoolExecutor() as executor:
    sekolah_id_enkrip_list = list(executor.map(get_sekolah_id_enkrip, list_kode_sekolah))

# Menyimpan list sekolah_id_enkrip ke dalam file txt
output_file = f"sekolah_id_enkrip_{jenjang}.txt"
with open(output_file, "w") as txtfile:
    txtfile.write('\n'.join(filter(None, sekolah_id_enkrip_list)))

print(f"Data telah disimpan dalam file {output_file}")
