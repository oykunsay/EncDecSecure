import os
import requests
import shutil
import tkinter as tk
from tkinter import filedialog, simpledialog
from Cryptodome.Cipher import DES, AES, Blowfish
from Cryptodome.Util.Padding import pad, unpad


class DosyaYoneticisi:
    def __init__(self, root):
        self.double_click_event = None
        self.root = root
        self.root.title("Dosya Yöneticisi")

        self.listbox = tk.Listbox(root, selectmode=tk.SINGLE)
        self.listbox.pack(expand=tk.YES, fill=tk.BOTH)
        self.listbox.bind("<Double-Button-1>", self.double_click_event)

        btn_frame = tk.Frame(root)
        btn_frame.pack(side=tk.TOP, pady=10)

        btn_yeni_dosya = tk.Button(btn_frame, text="Yeni Dosya Oluştur", command=self.yeni_dosya_olustur)
        btn_yeni_dosya.pack(side=tk.LEFT, padx=5)

        btn_ac = tk.Button(btn_frame, text="Dosya Aç", command=self.dosya_ac)
        btn_ac.pack(side=tk.LEFT, padx=5)

        btn_indir = tk.Button(btn_frame, text="Dosyayı İndir", command=self.dosyayi_indir)
        btn_indir.pack(side=tk.LEFT, padx=5)

        btn_sil = tk.Button(btn_frame, text="Dosya Sil", command=self.dosya_sil)
        btn_sil.pack(side=tk.LEFT, padx=5)

        btn_klasor_olustur = tk.Button(btn_frame, text="Klasör Oluştur", command=self.klasor_olustur)
        btn_klasor_olustur.pack(side=tk.LEFT, padx=5)

        btn_klasore_tasi = tk.Button(btn_frame, text="Dosyayı Klasöre Taşı", command=self.dosyayi_klasore_tasi)
        btn_klasore_tasi.pack(side=tk.LEFT, padx=5)

        btn_klasor_sil = tk.Button(btn_frame, text="Klasörü Sil", command=self.klasor_sil)
        btn_klasor_sil.pack(side=tk.LEFT, padx=5)

    def dosya_listele(self, klasor_yolu):
        self.listbox.delete(0, tk.END)
        dosya_listesi = os.listdir(klasor_yolu)
        for dosya in dosya_listesi:
            self.listbox.insert(tk.END, dosya)

    def yeni_dosya_olustur(self):
        dosya_adi = simpledialog.askstring("Dosya Adı", "Yeni Dosya Adını Girin:")
        if dosya_adi:
            yeni_dosya_yolu = os.path.join(os.path.expanduser('~'), 'Desktop', dosya_adi)
            with open(yeni_dosya_yolu, 'w') as yeni_dosya:
                yeni_dosya.write("")

            self.dosya_listele(os.path.dirname(yeni_dosya_yolu))

    def dosya_ac(self):
        secilen_dosya = self.listbox.get(tk.ACTIVE)
        if secilen_dosya:
            dosya_path = os.path.join(os.path.expanduser('~'), 'Desktop', secilen_dosya)
            sifreleme_alg = simpledialog.askstring("Şifreleme Algoritması",
                                                   "Şifreleme Algoritması Seçin (Des, Aes, Blowfish):")
            if sifreleme_alg and sifreleme_alg.lower() in ['des', 'aes', 'blowfish']:
                anahtar = simpledialog.askstring("Anahtar Değeri", "Anahtar Değerini Girin:")
                if anahtar:
                    self.sifrele_ve_kopyala(dosya_path, sifreleme_alg.lower(), anahtar)
                    self.dosya_listele(os.path.join(os.path.expanduser('~'), 'Desktop'))

    def dosyayi_indir(self):
        secilen_dosya = self.listbox.get(tk.ACTIVE)
        if secilen_dosya:
            dosya_yolu = os.path.join(os.path.expanduser('~'), 'Desktop', secilen_dosya)
            if os.path.isfile(dosya_yolu):
                sifreleme_alg = self.get_sifreleme_algoritma(secilen_dosya)
                anahtar = simpledialog.askstring("Anahtar Değeri", "Anahtar Değerini Girin:")
                if sifreleme_alg and anahtar:
                    self.deşifre_ve_indir(dosya_yolu, sifreleme_alg.lower(), anahtar)
                    self.dosya_listele(os.path.join(os.path.expanduser('~'), 'Desktop'))

    def deşifre_ve_indir(self, dosya_path, sifreleme_alg, anahtar):
        with open(dosya_path, 'rb') as dosya:
            icerik_sifreli = dosya.read()

        if sifreleme_alg == 'des':
            cipher = DES.new(anahtar.encode(), DES.MODE_ECB)
        elif sifreleme_alg == 'aes':
            cipher = AES.new(anahtar.encode(), AES.MODE_ECB)
        elif sifreleme_alg == 'blowfish':
            cipher = Blowfish.new(anahtar.encode(), Blowfish.MODE_ECB)

        icerik = cipher.decrypt(icerik_sifreli)
        icerik = unpad(icerik, DES.block_size) if sifreleme_alg == 'des' else unpad(icerik, AES.block_size)

        # orijinal_format = self.get_orijinal_format(dosya_path)
        orijinal_dosya_adi = self.get_dosya_adi(dosya_path)
        hedef_dosya_yolu = os.path.join(os.path.expanduser('~'), 'Desktop',
                                        orijinal_dosya_adi + f'_{sifreleme_alg}_desifrelenmis.txt')
        with open(hedef_dosya_yolu, 'wb') as hedef_dosya:
            hedef_dosya.write(icerik)

    def get_sifreleme_algoritma(self, dosya_adi):
        # Dosya adından şifreleme algoritmasını tespit et
        algoritmalar = ['des', 'aes', 'blowfish']
        for alg in algoritmalar:
            if f'_{alg}_sifreli' in dosya_adi:
                return alg
        return None

    def get_dosya_adi(self, dosya_adi):
        return os.path.splitext(os.path.basename(dosya_adi))[0]

    def dosya_sil(self):
        secilen_dosya = self.listbox.get(tk.ACTIVE)
        if secilen_dosya:
            dosya_yolu = os.path.join(os.path.expanduser('~'), 'Desktop', secilen_dosya)
            if os.path.isfile(dosya_yolu):
                os.remove(dosya_yolu)
            self.dosya_listele(os.path.dirname(dosya_yolu))

    def klasor_olustur(self):
        yeni_klasor_adı = simpledialog.askstring("Klasör Oluştur", "Yeni Klasör Adı:")
        if yeni_klasor_adı:
            os.makedirs(os.path.join(os.path.expanduser('~'), 'Desktop', yeni_klasor_adı))
            self.dosya_listele(os.path.join(os.path.expanduser('~'), 'Desktop'))

    def dosyayi_klasore_tasi(self):
        secilen_dosya = self.listbox.get(tk.ACTIVE)
        if secilen_dosya:
            hedef_klasor = filedialog.askdirectory()
            if hedef_klasor:
                shutil.move(os.path.join(os.path.expanduser('~'), 'Desktop', secilen_dosya),
                            os.path.join(hedef_klasor, os.path.basename(secilen_dosya)))
                self.dosya_listele(os.path.dirname(os.path.join(hedef_klasor, secilen_dosya)))

    def klasor_sil(self):
        secilen_klasor = self.listbox.get(tk.ACTIVE)
        if secilen_klasor and os.path.isdir(os.path.join(os.path.expanduser('~'), 'Desktop', secilen_klasor)):
            shutil.rmtree(os.path.join(os.path.expanduser('~'), 'Desktop', secilen_klasor))
            self.dosya_listele(os.path.dirname(os.path.join(os.path.expanduser('~'), 'Desktop', secilen_klasor)))

    def sifrele_ve_kopyala(self, dosya_path, sifreleme_alg, anahtar):
        with open(dosya_path, 'rb') as dosya:
            icerik = dosya.read()
            orijinal_dosya_adi = self.get_dosya_adi(dosya_path)

        if sifreleme_alg == 'des':
            # Blok sınırlarına hizala
            icerik = pad(icerik, DES.block_size)

            cipher = DES.new(anahtar.encode(), DES.MODE_ECB)
            icerik_sifreli = cipher.encrypt(icerik)

            hedef_dosya_yolu = os.path.join(os.path.expanduser('~'), 'Desktop',
                                            orijinal_dosya_adi + f'_{sifreleme_alg}_sifreli.txt')
            with open(hedef_dosya_yolu, 'wb') as hedef_dosya:
                hedef_dosya.write(icerik_sifreli)

        elif sifreleme_alg == 'aes':
            # Blok sınırlarına hizala
            icerik = pad(icerik, AES.block_size)

            cipher = AES.new(anahtar.encode(), AES.MODE_ECB)
            icerik_sifreli = cipher.encrypt(icerik)

            hedef_dosya_yolu = os.path.join(os.path.expanduser('~'), 'Desktop',
                                            orijinal_dosya_adi + f'_{sifreleme_alg}_sifreli.txt')

            with open(hedef_dosya_yolu, 'wb') as hedef_dosya:
                hedef_dosya.write(icerik_sifreli)
        elif sifreleme_alg == 'blowfish':
            # Blok sınırlarına hizala
            icerik = pad(icerik, Blowfish.block_size)

            cipher = Blowfish.new(anahtar.encode(), Blowfish.MODE_ECB)
            icerik_sifreli = cipher.encrypt(icerik)

            hedef_dosya_yolu = os.path.join(os.path.expanduser('~'), 'Desktop',
                                            orijinal_dosya_adi + f'_{sifreleme_alg}_sifreli.txt')

            with open(hedef_dosya_yolu, 'wb') as hedef_dosya:
                hedef_dosya.write(icerik_sifreli)


if __name__ == "__main__":
    root = tk.Tk()
    dosya_yoneticisi = DosyaYoneticisi(root)
    dosya_yoneticisi.dosya_listele(os.path.join(os.path.expanduser('~'), 'Desktop'))
    root.mainloop()