import os
import random
from datetime import datetime

FOLDER_INVOICE = "invoices"
FILE_RIWAYAT = "trx_history.txt"     
LEBAR_INVOICE = 56                 

def ambil_inisial(nama_kasir):
    inisial = ""
    for kata in nama_kasir.split():
        inisial += kata[0].upper()
    return inisial

def buat_id_transaksi(nama_kasir, waktu):

    while True:
        inisial = ambil_inisial(nama_kasir)
        tanggal = waktu.strftime("%y%m%d")      
        jam_menit = waktu.strftime("%H%M")      
        acak = random.randint(100, 999)         
        id_transaksi = f"{inisial}{tanggal}{jam_menit}{acak}"

        if not os.path.exists(os.path.join(FOLDER_INVOICE, id_transaksi + ".txt")):
            return id_transaksi

def input_angka(pesan, tipe=int):
    
    while True:
        try:
            nilai = tipe(input(pesan))
            if nilai <= 0:
                print("  Nilai harus lebih besar dari 0.")
                continue
            return nilai
        except ValueError:
            print("  Input tidak valid, masukkan angka.")


def input_produk():

    daftar_produk = []
    while True:
        print(f"\n--- Produk ke-{len(daftar_produk) + 1} ---")

        nama = input("Nama produk      : ").strip()
        while nama == "":
            print("  Nama produk tidak boleh kosong.")
            nama = input("Nama produk      : ").strip()

        harga = input_angka("Harga produk     : ")
        jumlah = input_angka("Jumlah dibeli    : ")

        daftar_produk.append({
            "nama": nama,
            "harga": harga,
            "jumlah": jumlah,
            "subtotal": harga * jumlah,
        })

        lagi = input("Tambah produk lagi? (y/n): ").strip().lower()
        if lagi != "y":
            break
    return daftar_produk


def simpan_invoice(id_transaksi, nama_kasir, waktu, daftar_produk, total):

    os.makedirs(FOLDER_INVOICE, exist_ok=True)  
    path_file = os.path.join(FOLDER_INVOICE, id_transaksi + ".txt")

    garis_ganda = "=" * LEBAR_INVOICE
    garis_putus = "-" * LEBAR_INVOICE

    with open(path_file, "w") as f:
        f.write(garis_ganda + "\n")
        f.write("INVOICE / STRUK BELANJA".center(LEBAR_INVOICE) + "\n")
        f.write(garis_ganda + "\n")
        f.write(f"ID Transaksi : {id_transaksi}\n")
        f.write(f"Waktu        : {waktu.strftime('%Y-%m-%d %H:%M:%S')}\n")
        f.write(f"Kasir        : {nama_kasir}\n")
        f.write(garis_putus + "\n")
        f.write(f"{'Produk':20}{'Harga':>12}{'Jml':>6}{'Subtotal':>14}\n")
        f.write(garis_putus + "\n")
        for p in daftar_produk:
            f.write(f"{p['nama']:<20}{p['harga']:>12}{p['jumlah']:>6}{p['subtotal']:>14}\n")
        f.write(garis_putus + "\n")
        f.write(f"{'TOTAL':<38}{'Rp. ' + str(total):>18}\n")
        f.write(garis_ganda + "\n")
        f.write("Terima kasih telah berbelanja!".center(LEBAR_INVOICE) + "\n")

    return path_file


def transaksi_baru():
    
    print("\n===== TRANSAKSI BARU =====")

    nama_kasir = input("Nama kasir       : ").strip()
    while nama_kasir == "":
        print("  Nama kasir tidak boleh kosong.")
        nama_kasir = input("Nama kasir       : ").strip()

    daftar_produk = input_produk()

    waktu = datetime.now()
    total = sum(p["subtotal"] for p in daftar_produk)
    id_transaksi = buat_id_transaksi(nama_kasir, waktu)
    simpan_invoice(id_transaksi, nama_kasir, waktu, daftar_produk, total)

    catat_riwayat(waktu, id_transaksi, total)

    print("\nTransaksi berhasil!")
    print(f"ID Transaksi : {id_transaksi}")
    print(f"Invoice      : {os.path.join(FOLDER_INVOICE, id_transaksi + '.txt')}")

def cari_invoice():
    
    print("\n===== CARI INVOICE =====")
    id_transaksi = input("Masukkan ID transaksi: ").strip().upper()

    path_file = os.path.join(FOLDER_INVOICE, id_transaksi + ".txt")

    if id_transaksi != "" and os.path.isfile(path_file):
        with open(path_file, "r") as f:
            isi = f.read()
        print()
        print(isi)
    else:
        print(f"Invoice dengan ID '{id_transaksi}' tidak ditemukan.")


LEBAR_WAKTU = 21
LEBAR_ID = 20
LEBAR_NOMINAL = 19


def buat_baris(waktu, id_transaksi, nominal):
    
    return (f"| {waktu:<{LEBAR_WAKTU - 2}} "
            f"| {id_transaksi:<{LEBAR_ID - 2}} "
            f"| {nominal:<{LEBAR_NOMINAL - 2}} |")


def catat_riwayat(waktu, id_transaksi, total):
    
    baris_header = buat_baris("Waktu", "ID Transaksi", "Nominal Transaksi")
    garis = "=" * len(baris_header)

    file_baru = not os.path.exists(FILE_RIWAYAT)

    with open(FILE_RIWAYAT, "a") as f:
        if file_baru:
            f.write(garis + "\n")
            f.write(baris_header + "\n")
            f.write(garis + "\n")
        baris_data = buat_baris(waktu.strftime("%Y-%m-%d %H:%M:%S"),
                                id_transaksi,
                                f"Rp. {total}")
        f.write(baris_data + "\n")
        f.write(garis + "\n")


def main():
    while True:
        print("\n===== APLIKASI KASIR SEDERHANA =====")
        print("1. Transaksi baru")
        print("2. Cari invoice")
        print("3. Keluar")
        pilihan = input("Pilih menu (1/2/3): ").strip()

        if pilihan == "1":
            transaksi_baru()
        elif pilihan == "2":
            cari_invoice()
        elif pilihan == "3":
            print("Terima kasih, program selesai.")
            break
        else:
            print("Pilihan tidak valid, coba lagi.")


if __name__ == "__main__":
    main()